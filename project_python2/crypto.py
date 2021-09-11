from DES import *
from Crypto.Util.number import *
import binascii
import os
import re


def des():
    Des = DES()
    return Des


def encrypt(des_instance, key, message):
    cipher = des_instance.encrypt(key, message)
    return binascii.b2a_hex(cipher)


def decrypt(des_instance, key, cipher, cipher_iv):
    m = des_instance.decrypt(key, binascii.a2b_hex(cipher))
    m = long_to_bytes(int(m, 16))
    if m.startswith(binascii.a2b_hex(cipher_iv)):
        m = hex(bytes_to_long(m[len(binascii.a2b_hex(cipher_iv)):]))  # hex() return a string start with useless '0x'
        if m.endswith('L'):  # If m is very long, the end of it is a useless 'L'
            return m[2:-1]
        else:
            return m[2:]
    else:
        raise Exception('InValid input')


def formats(string, mode='key'):
    flag = hex_to_bytes(string)  # Determine whether it is a hexadecimal string

    if flag != b'not hex' and string[:2] != b'0x' and string[:2] != b'0X':
        string = flag
        string, iv = form(string, mode)
    elif flag != b'not hex' and string[:2] == b'0x' and string[:2] == b'0X':
        string, iv = form(string[2:], mode)
    else:
        string, iv = form(string, mode)
    return string, iv


def form(string, mode='message'):
    iv = b''
    if mode == 'key':
        string = bytes(string)
        if len(string) < 8 and string != b'':
            iv = os.urandom(8 - len(string))
            string += iv
        elif string == b'':
            string = os.urandom(8)
        else:
            string = string[:8]
        string = binascii.b2a_hex(string)
    else:
        string = bytes(string)
        if len(string) % 8 > 0:
            iv = os.urandom(8 - len(string) % 8)
            string = iv + string
        elif string == b'':
            string = b'I was born king'
        string = binascii.b2a_hex(string)
    return string, binascii.b2a_hex(iv)


def hex_to_bytes(string):
    Formats = r'^\A[0-9a-fA-F]+\Z'
    pattern = re.compile(Formats)
    string = string.replace(' ', '')
    if string[:2] == '0x' or string[:2] == '0X':
        string = string[2:]
    if not pattern.findall(string):
        return b'not hex'
    string = long_to_bytes(int(string, 16))  # binascii.b2a_hex() requires an even-length string
    return string
