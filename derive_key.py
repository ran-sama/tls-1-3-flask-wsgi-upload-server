from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from base64 import b64encode
from base64 import b64decode

password = b'usernameANDpassword'

salt = get_random_bytes(16)
print("Your salt (use in the login html):")
print(b64encode(salt).decode('utf-8'))

keys = PBKDF2(password, salt, 32, count=456789, hmac_hash_module=SHA512)
print("Your PBKDF2 key (use in the WSGI code):")
print(''.join('{:02x}'.format(x) for x in keys))
