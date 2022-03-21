
import hashlib
import os

def encryption_sha256(password, salt):
    # Use the exact same setup you used to generate the key, but this time put in the password to check
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), # Convert the password to bytes
        salt, 
        100000
    )
    return new_key


def new_key_sha256(password):
    salt = os.urandom(32) # A new salt for this user
    # Use the exact same setup you used to generate the key, but this time put in the password to check
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), # Convert the password to bytes
        salt, 
        100000
    )
    result = {
        salt: salt,
        new_key: new_key
    }
    return result

