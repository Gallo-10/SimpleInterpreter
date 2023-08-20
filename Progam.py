from lexer.Lexer import BasicLexer, SymbolTable
from parser.Parser import BasicParser

if __name__ == "__main__":
    st = SymbolTable()
    lexer = BasicLexer("C:/Users/gabri/PycharmProjects/SimpleInterpreter/Ex/grammar.md", st)
    basicParser = BasicParser(lexer, st)
    basicParser.prog()