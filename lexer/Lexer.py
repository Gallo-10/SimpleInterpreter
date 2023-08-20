from enum import Enum


class ETokenType(Enum):
    SUM = 1
    SUB = 2
    MULT = 3
    DIV = 4
    OE = 5
    CE = 6
    AT = 7
    EOL = 8
    VAR = 9
    INPUT = 10
    OUTPUT = 11
    NUM = 12
    ERR = 13
    EOF = 14


class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value


class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.counter = 0

    def put(self, symbol):
        if symbol not in self.symbols:
            self.counter += 1
            self.symbols[symbol] = self.counter
        return self.symbols[symbol]


class BasicLexer:
    def __init__(self, filename, st=None):
        self.filename = filename
        if st is None:
            st = SymbolTable()
        self.symbol_table = st
        self.reader = open(filename, 'r')
        self.line = 1
        self.column = 1
        self.peek = None

    def get_next_token(self):
        if self.reader.closed:
            return Token(ETokenType.EOF)

        while True:
            if self.peek is None:
                self.peek = self.next_char()

            while self.peek in [' ', '\t', '\r']:
                self.peek = self.next_char()

            if self.peek == '+':
                self.peek = None
                return Token(ETokenType.SUM)
            elif self.peek == '-':
                self.peek = None
                return Token(ETokenType.SUB)
            elif self.peek == '=':
                self.peek = None
                return Token(ETokenType.AT)
            # Add more token checks here...
            elif self.peek.isdigit():  # Check for NUM
                num = ""
                while self.peek.isdigit():
                    num += self.peek
                    self.peek = self.next_char()
                return Token(ETokenType.NUM, value=num)
            elif self.peek == '$':  # Check for VAR
                var = ""
                while self.peek.isalpha():
                    var += self.peek
                    self.peek = self.next_char()
                return Token(ETokenType.VAR, value=var)
            elif self.peek == '(':
                self.peek = None
                return Token(ETokenType.OE)
            elif self.peek == ')':
                self.peek = None
                return Token(ETokenType.CE)
            elif self.peek == '\0':
                return Token(ETokenType.EOF)
            else:
                error_msg = f"Unrecognized token: {self.peek}"
                self.peek = None
                return Token(ETokenType.ERR, value=error_msg)

    def next_char(self):
        self.column += 1
        if not self.reader.closed:
            return self.reader.read(1)
        return '\0'

    def test_suffix(self, suffix):
        for c in suffix:
            self.peek = self.next_char()
            if self.peek != c:
                return False
        self.peek = None
        return True

    def get_value(self, c):
        return int(c)

    def __del__(self):
        if not self.reader.closed:
            self.reader.close()

    # Usage


if __name__ == "__main__":
    lexer = BasicLexer("C:/Users/gabri/PycharmProjects/SimpleInterpreter/Ex/teste.lang")
    token = lexer.get_next_token()
    while token.token_type != ETokenType.EOF:
        if token.token_type != ETokenType.ERR:
            print(token.token_type, token.value)
        else:
            print("Unrecognized token")
        token = lexer.get_next_token()
