from Crypto.Cipher import AES
import base64
import os

# Encrypt data
# Requires AES obj with CRYPTO_KEY, and CRYPTO_IV environment variables
# Encrypt data and return encoded Base64 string, without Base64 padding
def encrypt_data(data):
    obj = AES.new(os.environ.get('CRYPTO_KEY').encode('utf-8'), AES.MODE_CFB, os.environ.get('CRYPTO_IV').encode('utf-8'))
    data = obj.encrypt(data.encode('utf-8'))
    # Calculate base64 padding and remove it from the end
    pad = 3 - (len(data) % 3)
    return base64.b64encode(data)[:-pad].decode('utf-8')


# Decrypt data
# Requires AES obj with CRYPTO_KEY, and CRYPTO_IV environment variables
# Add Base64 padding, decode Base64 encoding and return decrypted string
def decrypt_data(data):
    obj = AES.new(os.environ.get('CRYPTO_KEY').encode('utf-8'), AES.MODE_CFB, os.environ.get('CRYPTO_IV').encode('utf-8'))
    # Calculate needed base64 padding and add it
    pad = len(data) % 3
    data += pad * '='
    data = base64.b64decode(data)
    return obj.decrypt(data).decode('utf-8')
