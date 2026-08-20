import hashlib
import os
import random

def hash_password(password):
    salt = os.urandom(16) #превращаем пароль в байт строку для того чтобы подмешать соли в хэш
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1024)
    return salt.hex() + ':' + key.hex()

def verify_password(password, stored):
    salt_hex, key_hex = stored.split(':')
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1024)
    return key.hex() == key_hex


def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    question = f"{a} + {b}"
    answer = a + b
    return question, answer