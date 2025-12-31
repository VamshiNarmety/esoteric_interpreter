"""
Symbol table for semantic analysis.
Tracks variable declarations and their types.
"""
class Symbol:
    """Base class for all symbols"""
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

class BuiltinTypeSymbol(Symbol):
    """Represents built-in types like INTEGER, REAL"""
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"
    
class VarSymbol(Symbol):
    """Represents a variable symbol."""
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return f"<{self.name}:{self.type}>"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', type='{self.type}')>"
    
class SymbolTable:
    """Symbol table to store and lookup symbols."""
    def __init__(self):
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        """Initialize built-in type symbols."""
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        symtab_header = 'Symbol table contents:'
        lines = ['\n', symtab_header, '_'*len(symtab_header)]
        lines.extend(f'{key:7}: {value}' for key, value in self._symbols.items())
        lines.append('\n')
        return '\n'.join(lines)
    
    def __repr__(self):
        return self.__str__()
    
    def define(self, symbol):
        """Define a symbol in the symbol table."""
        # print(f'Define: {symbol}')
        self._symbols[symbol.name] = symbol

    def lookup(self, name):
        """Lookup a symbol by name"""
        # print(f'Lookup: {name}')
        symbol = self._symbols.get(name)
        return symbol