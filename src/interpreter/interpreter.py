"""Simple Interpreter for basic arthimetic expressions"""

from src.lexer.token import Token, INTEGER, PLUS, MINUS, EOF, MUL, DIV

class Interpreter:
    """
    A simple Interpreter for arthimetic expressions.
    Grammar:
        expr: term ((PLUS|MINUS) term)*
        term: INTEGER ((MUL|DIV) INTEGER)*
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        """Raise an exception for invalid syntax."""
        raise Exception('Error parsing input')
    
    def advance(self):
        """Move the 'pos' pointer and set the 'current_char' variable."""
        self.pos+=1
        if self.pos>len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
        
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        """
        Lexical analyzer(scanner or tokenizer).
        returns the next token from the input
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char=='+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char=='-':
                self.advance()
                return Token(MINUS, '-')
            
            if self.current_char=='*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char=='/':
                self.advance()
                return Token(DIV, '/')
            
            self.error()

        return Token(EOF, None)
    
    def eat(self, token_type):
        """
        Compare the current token type with the passed token type.
        if they match, assign the next token to self.current_token. Otherwise, raise an exception.
        """
        if self.current_token.type==token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """
        term: INTEGER ((MUL|DIV) INTEGER)*
        Handles mul and div (higher precedence)
        """
        result = self.current_token.value
        self.eat(INTEGER)
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type==MUL:
                self.eat(MUL)
                result = result * self.current_token.value
                self.eat(INTEGER)
            elif token.type==DIV:
                self.eat(DIV)
                result = result // self.current_token.value
                self.eat(INTEGER)

        return result

    def expr(self):
        """
        expr: term ((PLUS|MINUS) term)*
        Handles add and sub(lower precedence). calls term() for MUL/DIV.
        """
        self.current_token = self.get_next_token()
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type==PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type==MINUS:
                self.eat(MINUS)
                result = result - self.term()
        
        if self.current_token.type!=EOF:
            self.error()
            
        return result
    

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__=='__main__':
    main()