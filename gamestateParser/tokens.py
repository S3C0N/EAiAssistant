import re
from enum import Enum, auto

class TokenType(Enum):
    LEFT_BRACE = auto()    # {
    RIGHT_BRACE = auto()   # }
    EQUALS = auto()        # =
    IDENTIFIER = auto()    # Alphanumeric identifiers
    NUMBER = auto()        # Integers and floats
    STRING = auto()        # Quoted strings
    EOF = auto()           # End of file

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, Line:{self.line}, Col:{self.column})'