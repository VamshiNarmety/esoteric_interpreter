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
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN ='ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
EOF = 'EOF'

RESERVED_KEYWORDS = {
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
}