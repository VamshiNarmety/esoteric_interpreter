from src.lexer.token import (Token, INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, EOF, RESERVED_KEYWORDS)

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

    def integer(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)
    
    def _id(self):
        """Handles identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
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

            if self.current_char.isalpha():
                return self._id()
            
            if self.current_char==':' and self.peek()=='=':
                self.advance()
                self.advance()
                return Token(ASSIGN, ':=')
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
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
            
            self.error()
        
        return Token(EOF, None)