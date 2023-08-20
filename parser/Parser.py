from lexer.Lexer import BasicLexer, ETokenType
from lexer.Lexer import Token
from lexer.Lexer import SymbolTable


class BasicParser:
    def __init__(self, lexer, st):
        self._lexer = lexer
        self._lookAhead = self._lexer.get_next_token()
        self._symbolTable = SymbolTable()

    def match(self, token_type):
        if self._lookAhead.token_type == ETokenType.INPUT:
            self._lookAhead = self._lexer.get_next_token()
        else:
            self.error(f"Expected {token_type} - Found {self._lookAhead.token_type}")

    def error(self, msg):
        print(f"#Error on _____ {self._lookAhead.token_type} {self._lookAhead.value}")
        print(f"Line {self._lexer.line}")
        print(f"Column {self._lexer.column}")
        print("________________")
        print(msg)
        print("________________")
        self._lookAhead = self._lexer.get_next_token()  # Avança para o próximo token após o erro

    def prog(self):  # prog   : line X
        self.line()
        self.x()

    def x(self):  # X : EOF | prog
        if self._lookAhead.token_type == ETokenType.EOF:
            self.match(ETokenType.EOF)
        else:
            self.prog()

    def line(self):  # line   : stmt EOL
        self.stmt()
        self.match(ETokenType.EOL)

    def stmt(self):  # stmt   : in | out | atrib
        if self._lookAhead.token_type == ETokenType.INPUT:
            self.input()
        elif self._lookAhead.token_type == ETokenType.OUTPUT:
            self.output()
        elif self._lookAhead.token_type == ETokenType.VAR:
            self.atrib()
        else:
            self.error("Expected INPUT, OUTPUT or VAR")

    def input(self):  # in     : INPUT VAR
        self.match(ETokenType.INPUT)
        self.match(ETokenType.VAR)

    def output(self):  # out    : OUTPUT VAR
        self.match(ETokenType.OUTPUT)
        self.match(ETokenType.VAR)

    def atrib(self):  # atrib  : VAR AT expr
        refx = self._lookAhead.value
        self.match(ETokenType.VAR)
        self.match(ETokenType.AT)
        e = self.expr()
        self._symbolTable.put(refx, e)  # Armazena ou atualiza o valor da variável
        if refx is not None:
            entry = self._symbolTable.get_entry(refx,e)
            if entry is not None:
                entry.value = e

    def expr(self):  # expr   : term Y
        t = self.term()
        return self.y(t)

    def y(self, left):  # Y      : vazio | + expr | - expr
        if self._lookAhead.token_type == ETokenType.SUM:
            self.match(ETokenType.SUM)
            right = self.expr()
            return left + right
        elif self._lookAhead.token_type == ETokenType.SUB:
            self.match(ETokenType.SUB)
            right = self.expr()
            return left - right
        elif not self.test_follow(ETokenType.CE, ETokenType.EOL):
            self.error(f"Found {self._lookAhead.token_type} Expected CE or EOL")
        return left

    def term(self):  # term   : fact Z
        f = self.fact()
        return self.z(f)

    def z(self, left):  # Z      : vazio | * term | / term
        if self._lookAhead.token_type == ETokenType.MULT:
            self.match(ETokenType.MULT)
            right = self.term()
            return left * right
        elif self._lookAhead.token_type == ETokenType.DIV:
            self.match(ETokenType.DIV)
            right = self.term()
            return left / right
        elif not self.test_follow(ETokenType.CE, ETokenType.EOL):
            self.error(f"Found {self._lookAhead.token_type} Expected CE or EOL")
        return left

    def fact(self):  # fact   : NUM | VAR | OE expr CE
        if self._lookAhead.token_type == ETokenType.NUM:
            num = float(self._lookAhead.value)
            self.match(ETokenType.NUM)
            return num
        elif self._lookAhead.token_type == ETokenType.VAR:
            key = self._lookAhead.value
            val = 0.0
            if key is None:
                self.error("Expected VAR")
            else:
                val = SymbolTable.get(key)  # Obter o valor da variável da tabela de símbolos
                self.match(ETokenType.VAR)
            return val
        elif self._lookAhead.type == ETokenType.OE:
            self.match(ETokenType.OE)
            e = self.expr()
            self.match(ETokenType.CE)
            return e
        else:
            self.error("Expected NUM, VAR or OE")
            return 0.0

    def test_follow(self, *args):
        return self._lookAhead.token_type in args or self._lookAhead.token_type == ETokenType.EOL


# Aqui você pode importar as classes SymbolTable, Token e ETokenType, que já foram traduzidas
st = SymbolTable()
lexer = BasicLexer("C:/Users/gabri/PycharmProjects/SimpleInterpreter/Ex/teste.lang", st)
parser = BasicParser(lexer, st)
parser.prog()