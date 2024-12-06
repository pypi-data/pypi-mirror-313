import ctypes
import os
import pathlib

import numpy as np
import sys

# Determine the correct library path based on the operating system
arch=None
if sys.maxsize > 2 ** 32:
  arch = 'x64'
else:
  arch = 'x32'
  raise "Python is 32 bit, please use 64 bit version"

# Determine the correct library path based on the operating system
WINDOWS_OS = 'nt'
if os.name == WINDOWS_OS:  # Windows
  libname = os.path.join(pathlib.Path(__file__).parent.resolve(), "win", arch, "libcrypto.dll")
elif sys.platform == 'darwin':
  libname = os.path.join(pathlib.Path(__file__).parent.resolve(), "darwin", arch, "libcrypto.dylib")
else:  # Unix
  libname = os.path.join(pathlib.Path(__file__).parent.resolve(), "unix", arch, "libcrypto.so")

try:
  crypto_lib = ctypes.CDLL(libname)

except OSError as e:
  print(f"Error during loading library: {e}")


def get_private_key_size():
  """Get the ECDH private key size from crypto C-library

  :return: ECDH private key size [bytes]
  :rtype: int
  """
  return crypto_lib.crypto_privateKeySize()

def get_public_key_size():
  """Get the ECDH public key size from crypto C-library

  :return: ECDH public key size [bytes]
  :rtype: int
  """
  return crypto_lib.crypto_publicKeySize()

def get_aes_chunk_size():
  """Get the AES chunk size used in crypto C-library

  :return: AES chunk size [bytes]
  :rtype: int
  """
  return crypto_lib.crypto_aesChunkSize()

def calculate_pkcs7_padded_size(data_size):
  """Computes output size after PKCS7 padding (RFC2315) in order to respect AES standard
  chunk size (16 bytes).

  :param data_size: Data size for PKCS7 padding
  :type data_size: int
  :return: Length of padded data
  :rtype: int
  """

  arr = np.zeros((1), dtype=np.uint8) # sample array to call the C function
  UIntegerArray3 = ctypes.c_uint8
  arr_c = UIntegerArray3(*arr)
  return crypto_lib.crypto_pkcs7CalculatePaddedSize(arr_c, ctypes.c_size_t(data_size))

def calculate_pkcs7_unpadded_size(data):
  """Computes unpadded size of an array with PKCS7 padding (RFC2315) in order to respect AES standard
  chunk size (16 bytes).

  :param data: Numpy padded array of uint8
  :type data: Numpy array of uint8
  :return: Length of unpadded data
  :rtype: int
  """

  padding = data[-1]
  if padding > crypto_lib.crypto_aesChunkSize() or padding < 1:
    return len(data)

  return len(data) - padding

def pad_pkcs7(data):
  """Performs padding from input data in order to respect AES standard
  chunk size (16 bytes) according to PKCS7 padding from RFC2315.
  Note: this implemention is not allined with C one; mind that C function takes
  a C-like string as input with the last character that is '/0', for this reason
  the padding result is different comparing the two languages.

  :param data: input Numpy array
  :type data: Numpy array of uint8
  :return: padded data as Numpy array
  :rtype: uint8 Numpy array
  """
  padded_size = calculate_pkcs7_padded_size(len(data))
  padding = padded_size - len(data)

  out = np.zeros((padded_size), dtype=np.uint8)

  out[0:len(data)] = data[0:len(data)]
  out[len(data):] = padding

  return out

def unpad_pkcs7(data):
  """Performs unpadding of a PKCS7 (RFC2315) padded input array according to AES standard
  chunk size (16 bytes).

  :param data: _description_
  :type data: _type_
  :param data_size: _description_
  :type data_size: _type_
  :return: _description_
  :rtype: _type_
  """

  unpadded_size = calculate_pkcs7_unpadded_size(data)
  padding = len(data) - unpadded_size
  out = np.empty((unpadded_size), dtype=np.uint8)

  if (data[unpadded_size: len(data)] != padding).any():
    return 0
  out[0:unpadded_size] = data[0:unpadded_size]

  return out

def encrypt_aes(data, key, key_size):
  """Encrypts data using key with certain key size (128, 192 or 256 bits)
  applying AES algorithm.

  :param data: input data (already padded data)
  :type data: Numpy array of uint8
  :param key: AES key
  :type key: Numpy array of uint8
  :param key_size: size of AES key (128, 192 or 256 bits)
  :type key_size: int
  :return: encrypted data
  :rtype: Numpy array of uint8
  """

  # encrypted data size (already padded)
  UIntegerArray = ctypes.c_uint8 * len(data)
  data_c = UIntegerArray(*data)

  # decrypted data size == encrypted data size
  out = np.zeros((len(data)), dtype=np.uint8)
  out_c = UIntegerArray(*out)

  UIntegerArray = ctypes.c_uint8 * len(key)
  key_c = UIntegerArray(*key)

  crypto_lib.crypto_aesEncrypt(data_c, ctypes.c_size_t(len(data)), key_c, key_size, out_c)
  out = np.frombuffer(out_c, dtype=np.uint8)

  return out

def decrypt_aes(encrypted_data, key, key_size):
  """Decrypts data using key with certain key size (128, 192 or 256 bits)
  applying AES algorithm.

  :param encrypted_data: cipher data array (padded data size)
  :type encrypted_data: Numpy array of uint8
  :param key: AES key
  :type key: Numpy array of uint8
  :param key_size: size of AES key (128, 192 or 256 bits)
  :type key_size: int
  :return: decrypted data (same length of input encrypted data)
  :rtype: Numpy array of uint8
  """

  UIntegerArray = ctypes.c_uint8 * len(encrypted_data)
  encrypted_data_c = UIntegerArray(*encrypted_data)

  UIntegerArray = ctypes.c_uint8 * len(key)
  key_c = UIntegerArray(*key)

  # output size with padding
  output_size = calculate_pkcs7_unpadded_size(encrypted_data)
  out = np.zeros((output_size), dtype=np.uint8)
  UIntegerArray = ctypes.c_uint8 * len(encrypted_data)
  out_c = UIntegerArray(*out)

  crypto_lib.crypto_aesDecrypt(encrypted_data_c, ctypes.c_size_t(len(encrypted_data)), key_c, key_size, out_c)
  out = np.frombuffer(out_c, dtype=np.uint8)

  return out

def generate_key_pair(private_key):
  """Generates ECDH public key starting from random private key (local secret).
  The public key can be sent to the remote host to generate the shared secret.
  It uses NIST K-163 elliptic curve.

  :param private_key_8: input private key (call method crypto_privateKeySize for getting the length, i.e. 24 bytes)
  :type private_key_8: Numpy array of uint8
  :return: ECDH public key (call method crypto_publicKeySize for getting the length, i.e. 48 bytes)
  :rtype: Numpy array of uint8
  """
  # private key (input data)
  UIntegerArray = ctypes.c_uint8 * len(private_key)
  private_key_c = UIntegerArray(*private_key)

  # public key (output data)
  public_key = np.zeros((len(private_key)*2), dtype=np.uint8)
  UIntegerArray = ctypes.c_uint8 * len(public_key)
  public_key_c = UIntegerArray(*public_key)

  ret = crypto_lib.crypto_generateKeyPair(public_key_c, private_key_c)
  public_key = np.frombuffer(public_key_c, dtype=np.uint8)

  return public_key

#size_t crypto_sign(uint8_t* my_private_key, uint8_t* cloud_public_key, uint8_t* data, size_t data_size, uint8_t* out);
def sign(local_private_key, remote_public_key, data):
  """Computes the digital signature of input data using ECDH algorithm.
  The private key is integer value chosen by the local user to multiply the generator point of ECC.
  The public key is the point generate by the remote user multipling the generator point of ECC by
  its secret integer value.
  The signature is computed applying AES encryption to the input data with the ashared key computed
  multiplying the private and public key in ECC domain using ECDH Diffie - Hellman algoritm.

  :param local_private_key: local private key as Numpy array of 24 unsigned integer values
  :type local_private_key: Numpy array of uint8
  :param remote_public_key: remote public key as Numpy array of 48 unsigned integer values
  :type remote_public_key: Numpy array of uint8
  :param data: input data to be signed
  :type data: Numpy array of uint8
  :return: digital signature (padded input data size)
  :rtype: Numpy array of uint8
  """

  # local private key (input data)
  UIntegerArray = ctypes.c_uint8 * len(local_private_key)
  local_private_key_c = UIntegerArray(*local_private_key)

  # remote public key (input data)
  UIntegerArray = ctypes.c_uint8 * len(remote_public_key)
  remote_public_key_c = UIntegerArray(*remote_public_key)

  # input data to be signed (encrypted with computed shared key)
  UIntegerArray = ctypes.c_uint8 * len(data)
  data_c = UIntegerArray(*data)

  # output encrypted data (signature)
  output_size = calculate_pkcs7_padded_size(len(data))
  signature = np.zeros((output_size), dtype=np.uint8)
  UIntegerArray = ctypes.c_uint8 * output_size
  signature_c = UIntegerArray(*signature)

  # call C library function
  ret = crypto_lib.crypto_sign(local_private_key_c, remote_public_key_c, data_c, ctypes.c_size_t(len(data)), signature_c)

  signature = np.frombuffer(signature_c, dtype=np.uint8)

  return signature

def unsign(local_private_key, remote_public_key, signature):
  """Verifies the digital signature of input data using ECDH algorithm.
  The private key is integer value chosen by the local user to multiply the generator point of ECC.
  The public key is the point generate by the remote user multipling the generator point of ECC by
  its secret integer value.
  The signature is computed applying AES encryption to the input data with the ashared key computed
  multiplying the private and public key in ECC domain using ECDH Diffie - Hellman algoritm.

  :param local_private_key: local private key as Numpy array of 24 unsigned integer values
  :type local_private_key: Numpy array of uint8
  :param remote_public_key: remote public key as Numpy array of 48 unsigned integer values
  :type remote_public_key: Numpy array of uint8
  :param signature: signature to be verified (padded size)
  :type signature: Numpy array of uint8
  :return: decrypted data to be verified
  :rtype: Numpy array of uint8
  """

  # local private key (input data)
  UIntegerArray = ctypes.c_uint8 * len(local_private_key)
  local_private_key_c = UIntegerArray(*local_private_key)

  # remote public key (input data)
  UIntegerArray = ctypes.c_uint8 * len(remote_public_key)
  remote_public_key_c = UIntegerArray(*remote_public_key)

  # input signature (previously encrypted with computed shared key)
  UIntegerArray = ctypes.c_uint8 * len(signature)
  signature_c = UIntegerArray(*signature)

  # output decrypted signature
  decrypted_data = np.zeros((len(signature)), dtype=np.uint8)
  UIntegerArray = ctypes.c_uint8 * len(signature)
  decrypted_data_c = UIntegerArray(*decrypted_data)

  # call C library function
  unpadded_size = crypto_lib.crypto_unsign(local_private_key_c, remote_public_key_c, signature_c, ctypes.c_size_t(len(signature)), decrypted_data_c)
  decrypted_data = np.frombuffer(decrypted_data_c, dtype=np.uint8)
  decrypted_data = decrypted_data[0:unpadded_size]

  return decrypted_data
