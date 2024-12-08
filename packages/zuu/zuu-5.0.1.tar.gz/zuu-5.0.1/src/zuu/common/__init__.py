from .string import rreplace, is_fstring, extract_fstring_keys 
from .clsprop import classProperty


def xor_encrypt(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
