""" Token types and Token class for the lexer."""

class Token:
    """
    Represents a token with a type and value
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String representation of the token
        """
        return f'Token({self.type}, {repr(self.value)})'
    
    def __repr__(self):
        return self.__str__()
    


INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
EOF = 'EOF'