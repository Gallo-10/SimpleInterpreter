from enum import Enum
from typing import Optional
from collections import OrderedDict

class ETokenType(Enum):
    EOF = 0
    EOL = 1
    INPUT = 2
    OUTPUT = 3
    VAR = 4
    NUM = 5
    AT = 6
    OE = 7
    CE = 8
    SUM = 9
    SUB = 10
    DIV = 11
    MULT = 12
    ERR = 13

class TableEntry:
    def __init__(self, type: ETokenType, name: str, value: Optional[float] = None):
        self.Type = type
        self.Name = name
        self.Value = value




class SymbolTable:
    def __init__(self):
        self._key = 0
        self._data = OrderedDict()
        self.symbols = {}

    def put(self, symbol, value):
        self.symbols[symbol] = value

    def get(self, symbol):
        return self.symbols.get(symbol, None)

    def put(self, name: str, value: Optional[float] = None) -> int:
        entry, k = self.get_by_name(name)
        self.symbols[symbol] = value
        if entry:
            return k


        self._key += 1
        self._data[self._key] = TableEntry(ETokenType.VAR, name, value)
        return self._key

    def get_by_name(self, name: str):
        for k in self._data:
            if self._data[k].Name == name:
                return self._data[k], k
        return None, 0

    def get(self, key: int) -> Optional[float]:
        entry = self._data.get(key)
        if entry:
            return entry.Value
        return self.symbols.get(symbol, None)

    def get_entry(self, key):
        return self.symbols.get(key, None)

    def __str__(self):
        sb = []
        sb.append("ID".ljust(5, ' '))
        sb.append("Type".ljust(10, ' '))
        sb.append("Name".ljust(15, ' '))
        sb.append("Value".ljust(5, ' '))
        sb.append('\n')

        for k, entry in self._data.items():
            sb.append(str(k).ljust(5, ' '))
            sb.append(str(entry.Type).ljust(10, ' '))
            sb.append(str(entry.Name).ljust(15, ' '))
            if entry.Value is not None:
                sb.append(str(entry.Value).ljust(5, ' '))
            sb.append('\n')
        return ''.join(sb)
