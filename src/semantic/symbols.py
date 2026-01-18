"""
Symbol table for semantic analysis.
Tracks variable declarations and their types with scope support.
"""
import os

# Control debug output via environment variable
_DEBUG = os.environ.get('PASCAL_DEBUG', '0') == '1'

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
    
class FunctionSymbol(Symbol):
    """Represents a function symbol."""
    def __init__(self, name, params=None, return_type=None):
        super().__init__(name, return_type)
        self.params = params if params is not None else []
        self.return_type = return_type

    def __str__(self):
        params_str = ', '.join(str(p) for p in self.params)
        return f"<{self.name}({params_str}):{self.return_type}>"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}', params={self.params}, return_type={self.return_type})>"
    
class ScopedSymbolTable:
    """
    scoped symbol table with support for nested scopes.
    Each scope has a name, level and optional parent scope.
    """
    def __init__(self, scope_name, scope_level, enclosing_scope=None):
        self._symbols = {}
        self.scope_name = scope_name
        self.scope_level = scope_level
        self.enclosing_scope = enclosing_scope #parent scope

    def _init_builtins(self):
        """Initialize built-in type symbols."""
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self):
        h1 = 'SCOPE (SCOPED SYMBOL TABLE)'
        lines = ['\n', h1, '='*len(h1)]
        lines.append(f'Scope name     : {self.scope_name}')
        lines.append(f'Scope level    : {self.scope_level}')
        lines.append(f'Enclosing scope: {self.enclosing_scope.scope_name if self.enclosing_scope else None}')
        h2 = 'Scope (Scoped symbol table) contents'
        lines.extend([h2, '-'*len(h2)])
        lines.extend(f'{key:7}: {value}' for key, value in self._symbols.items())
        lines.append('\n')
        return '\n'.join(lines)
    
    def __repr__(self):
        return self.__str__()
    
    def define(self, symbol):
        """Define a symbol in the current scope only."""
        if _DEBUG:
            print(f'Define: {symbol}')
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        """
        Lookup a symbol by name.
        If current_scope_only=True, only search this scope.
        Otherwise, search this scope and all enclosing scopes.
        """
        if _DEBUG:
            print(f'Lookup: {name}. (Scope name: {self.scope_name})')
        symbol = self._symbols.get(name)
        if symbol is not None:
            return symbol
        
        if not current_scope_only and self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        return None
    
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