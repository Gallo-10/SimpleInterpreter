from enum import Enum

class ETokenType(Enum):
    EOF = 1
    EOL = 2
    INPUT = 3
    OUTPUT = 4
    VAR = 5
    NUM = 6
    AT = 7
    OE = 8
    CE = 9
    SUM = 10
    SUB = 11
    DIV = 12
    MULT = 13
    ERR = 14
