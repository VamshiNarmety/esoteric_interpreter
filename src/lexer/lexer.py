from src.lexer.token import (Token, INTEGER_CONST, REAL_CONST, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, PROGRAM, VAR, COLON, COMMA, EOF, EQUAL, NOT_EQUAL, LESS_THAN, GREATER_THAN, LESS_EQUAL, GREATER_EQUAL, RESERVED_KEYWORDS)

class Lexer:
    """
    Lexical analyzer
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception('Invalid character')
    
    def advance(self):
        """
        Move the 'pos' pointer and set the 'current_char' variable.
        """
        self.pos += 1
        if self.pos>len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """Look ahead one character without consuming it"""
        peek_pos = self.pos+1
        if self.pos>len(self.text)-1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Skip comments enclosed in {}."""
        while self.current_char!='}':
            self.advance()
        self.advance()

    def number(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        if self.current_char=='.':
            result+=self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result+=self.current_char
                self.advance()
            token = Token(REAL_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))

        return token
    
    def _id(self):
        """Handles identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char=='_'):
            result+=self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result.upper(), Token(ID, result))
        return token
    
    def get_next_token(self):
        """
        returns next token from the input
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char=='_':
                return self._id()
            
            if self.current_char==':' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            
            if self.current_char==':':
                self.advance()
                return Token(COLON, ':')
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char=='<':
                self.advance()
                if self.current_char=='=':
                    self.advance()
                    return Token(LESS_EQUAL, '<=')
                elif self.current_char=='>':
                    self.advance()
                    return Token(NOT_EQUAL, '<>')
                else:
                    return Token(LESS_THAN, '<')
                
            if self.current_char=='>':
                self.advance()
                if self.current_char=='=':
                    self.advance()
                    return Token(GREATER_EQUAL, '>=')
                else:
                    return Token(GREATER_THAN, '>')
            
            if self.current_char=='=':
                self.advance()
                return Token(EQUAL, '=')
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char=='/' and self.peek()=='/':
                self.advance()
                self.advance()
                return Token(INTEGER_DIV, '//')
            
            if self.current_char == '/':
                self.advance()
                return Token(FLOAT_DIV, '/')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char==';':
                self.advance()
                return Token(SEMI, ';')
            
            if self.current_char=='.':
                self.advance()
                return Token(DOT, '.')
            
            if self.current_char==',':
                self.advance()
                return Token(COMMA, ',')
            
            self.error()
        
        return Token(EOF, None)