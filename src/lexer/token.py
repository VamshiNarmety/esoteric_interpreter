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
EQUAL = 'EQUAL'
NOT_EQUAL = 'NOT_EQUAL'
LESS_THAN = 'LESS_THAN'
GREATER_THAN = 'GREATER_THAN'
LESS_EQUAL = 'LESS_EQUAL'
GREATER_EQUAL = 'GREATER_EQUAL'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
IF = 'IF'
THEN = 'THEN'
ELSE = 'ELSE'
WHILE = 'WHILE'
DO = 'DO'
FOR = 'FOR'
TO = 'TO'
DOWNTO = 'DOWNTO'
PRINT = 'PRINT'
WRITELN = 'WRITELN'
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
    'IF': Token(IF, 'IF'),
    'THEN': Token(THEN, 'THEN'),
    'ELSE': Token(ELSE, 'ELSE'),
    'AND': Token(AND, 'AND'),
    'OR': Token(OR, 'OR'),
    'NOT': Token(NOT, 'NOT'),
    'WHILE': Token(WHILE, 'WHILE'),
    'DO': Token(DO, 'DO'),
    'FOR': Token(FOR, 'FOR'), 
    'TO': Token(TO, 'TO'),
    'DOWNTO': Token(DOWNTO, 'DOWNTO'),
    'PRINT': Token(PRINT, 'PRINT'),
    'WRITELN': Token(WRITELN, 'WRITELN')
}