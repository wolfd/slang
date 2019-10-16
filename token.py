# list of tokens in slang
from typing import List
from enum import Enum, auto

class Token(Enum):
    # special
    ILLEGAL = auto()
    EOF = auto()
    EOL = auto()  # \n

    # literals
    IDENT = auto()  # main
    STRING = auto()  # "abc"
    FLOAT = auto()  # 0.1
    INTEGER = auto()  # 5

    # operators
    LBRACKET = auto()
    RBRACKET = auto()

    # keywords
    F = auto()  # f - function
    P = auto()  # p - print

KEYWORDS = {
    "f": Token.F,
    "p": Token.P,
}

def lookup(ident: str) -> Token:
    if (tok := KEYWORDS.get(ident)):
        return tok
    
    return Token.IDENT

STARTS_EXPRESSION = {
    Token.STRING,
}

def starts_expression(tok: Token) -> bool:
    return tok in STARTS_EXPRESSION

class File:
    def __init__(self, name: str, base: int, size: int, lines: List[int]):
        self.name = name  # file name
        self.base = base  # pos value range for this file is [base, base + size]
        self.size = size
        
        self.lines = lines  # first offset for each line
