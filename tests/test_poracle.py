from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
import os

from .context import ctflib


key = os.urandom(16)


def decrypt(data):
    iv = data[:16]
    ct = data[16:]
    dec = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend()).decryptor()
    data = dec.update(ct) + dec.finalize()
    unpadder = PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def unpadded_encrypt(data):
    iv = os.urandom(16)
    enc = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend()).encryptor()
    return iv, enc.update(data) + enc.finalize()


def decrypt_oracle(data):
    try:
        decrypt(data)
        return True
    except ValueError:
        return False


def test_padding_oracle_forging():
    target = b'Ala ma kota i to jest test padding oracle attack'
    data = ctflib.crypto.poracle.plaintext_forger(target, decrypt_oracle).forge()
    assert decrypt(data) == target


def test_padding_oracle_attack():
    plaintext = b'testing, testing'
    iv, ct = unpadded_encrypt(plaintext)
    pt = ctflib.crypto.poracle.block_decryptor(ct, decrypt_oracle).decrypt()
    assert ctflib.util.xor(pt, iv) == plaintext
