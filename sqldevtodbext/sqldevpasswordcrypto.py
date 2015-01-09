#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES, DES
from Crypto.Hash import MD5
from Crypto import Random
import Padding
import logging
import base64

from argh import arg, dispatch_command

def decryptv4(ciphertext, password, salt='\x05\x13\x99\x42\x93\x72\xE8\xAD', iterations=42):
    """
    Decrypts PBEWithMD5AndDES encrypted password.

    The default salt and iteration values are from Oracle SQL Developer v4.
    """
    ciphertext = ciphertext.decode('base64')

    hasher = MD5.new()
    hasher.update(password)
    hasher.update(salt)
    result = hasher.digest()

    for i in range(1, iterations):
        hasher = MD5.new()
        hasher.update(result)
        result = hasher.digest()

    decoder = DES.new(result[:8], DES.MODE_CBC, result[8:16])
    plaintext = decoder.decrypt(ciphertext)
    return Padding.removePadding(plaintext, blocksize=Padding.DES_blocksize)

def encryptv4(plaintext, password, salt='\x05\x13\x99\x42\x93\x72\xE8\xAD', iterations=42):
    """
    Encrypts as password using Java's PBEWithMD5AndDES method.

    The default salt and iteration values are from Oracle SQL Developer v4.
    """
    # http://stackoverflow.com/questions/24168246/replicate-javas-pbewithmd5anddes-in-python-2-7
    plaintext = Padding.appendPadding(plaintext, blocksize=Padding.DES_blocksize)

    hasher = MD5.new()
    hasher.update(password)
    hasher.update(salt)
    result = hasher.digest()

    for i in range(1, iterations):
        hasher = MD5.new()
        hasher.update(result)
        result = hasher.digest()

    encoder = DES.new(result[:8], DES.MODE_CBC, result[8:16])
    encrypted = encoder.encrypt(plaintext)
    return encrypted.encode('base64')

def decrypt(password):
    """
    Decrypts an Oracle SQL Developer v2 or v3 stored password.
    """
    const = bytes(password[0:2])
    key = bytes(password[2:18])
    ciphertext = bytes(password[18:])

    logging.debug("Const = {}".format(const))
    logging.debug("Key = {}".format(key))
    logging.debug("Cipher Text = {}".format(ciphertext))

    iv = b'0000000000000000'.decode("hex")
    key = key.decode("hex")

    desd = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = ciphertext.decode("hex")

    plaintext = desd.decrypt(ciphertext)
    plaintext = Padding.removePadding(plaintext, blocksize=Padding.DES_blocksize)
    return plaintext

def encrypt(plaintext):
    """
    Encrypts a password for Oracle SQL Developer v2 or v3.
    """
    key = Random.get_random_bytes(8)

    iv = b'0000000000000000'.decode("hex")
    dese = DES.new(key, DES.MODE_CBC, iv)

    logging.debug("Key = {}".format(key.encode("hex")))

    plaintext = Padding.appendPadding(plaintext, blocksize=Padding.DES_blocksize)

    ciphertext = dese.encrypt(plaintext)

    return "{}{}{}".format("05", key.encode("hex"), ciphertext.encode("hex")).upper()

@arg('--reverse', action='store_true', default=False,
     help="Decrypts the inputs. The default operation is to encrypt them.")
@arg('passwords', metavar='password', type=str, nargs='+',
     help='The strings to encrypt or decrypt')
@arg('--v4', action='store_true', default=False, 
     help='Uses the SQL Developer v4 method to encrypt and decrypt passwords.')
def cli(reverse, passwords, v4=False, key='password'):
    longest = len(max(passwords, key=len))

    format_str = '%' + str(longest) + 's : %s'

    for password in passwords:
        if v4:
            if reverse:
                output = decryptv4(password, key)
            else:
                output = encryptv4(password, key)
        else:
            if reverse:
                output = decrypt(password)
            else:
                output = encrypt(password)

        print format_str % (password, output)


if __name__ == '__main__':
    dispatch_command(cli)
