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
REAL = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST = 'REAL_CONST'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
INTEGER_DIV = 'INTEGER_DIV'
FLOAT_DIV = 'FLOAT_DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
ID = 'ID'
ASSIGN ='ASSIGN'
BEGIN = 'BEGIN'
END = 'END'
SEMI = 'SEMI'
DOT = 'DOT'
PROGRAM = 'PROGRAM'
VAR = 'VAR'
COLON = 'COLON'
COMMA = 'COMMA'
FUNCTION = 'FUNCTION'
EOF = 'EOF'

RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'VAR': Token(VAR, 'VAR'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
    'FUNCTION': Token(FUNCTION, 'FUNCTION'),
}