# list of tokens in slang
from typing import List
from enum import Enum, auto

class Token(Enum):
    # special
    ILLEGAL = auto()
    EOF = auto()

    # literals
    IDENT = auto() # main
    STRING = auto() # "abc"

    # operators
    LBRACKET = auto()
    RBRACKET = auto()

    # keywords
    F = auto() # f - function
    P = auto() # p - print


class File:
    def __init__(self, name: str, base: int, size: int, lines: List[int]):
        self.name = name  # file name
        self.base = base  # pos value range for this file is [base, base + size]
        self.size = size
        
        self.lines = lines  # first offset for each line
