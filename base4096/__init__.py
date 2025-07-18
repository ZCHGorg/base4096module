# base4096/__init__.py
from .core import encode, decode
from .frozen_base4096_alphabet import BASE4096_ALPHABET, CHAR_TO_INDEX

__version__ = '2.0'
__all__ = ['encode', 'decode', 'BASE4096_ALPHABET', 'CHAR_TO_INDEX']
