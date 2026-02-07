"""Custom exception classes for the interpreter."""
class InterpreterError(Exception):
    """Base class for all interpreter errors."""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_error())
        
    def format_error(self):
        if self.line is not None and self.column is not None:
            return f"{self.__class__.__name__} at line {self.line}, column {self.column}: {self.message}"
        elif self.line is not None:
            return f"{self.__class__.__name__} at line {self.line}: {self.message}"
        else:
            return f"{self.__class__.__name__} : {self.message}"
            

class LexerError(InterpreterError):
    pass

class ParserError(InterpreterError):
    pass

class SemanticError(InterpreterError):
    pass

class RuntimeError(InterpreterError):
    pass