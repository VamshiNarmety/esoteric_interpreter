"""
Parser for building Abstract syntax trees.
The parser consumes tokens from the lexer and builds an AST.
"""
from src.lexer.token import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF
from src.parser.ast_nodes import BinOp, Num

class Parser:
    """
    Parser thats builds an Abstract syntax tree.
    Grammar:
       expr: term((PLUS|MINUS)term)*
       term: factor((MUL|DIV)factor)*
       factor: INTEGER | LPAREN expr RPAREN
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')
    
    def eat(self, token_type):
        """
        Verify current token type and get next token.
        """
        if self.current_token.type==token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """
        factor : INTEGER | LPAREN expr RPAREN
        """
        token = self.current_token
        if token.type==INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type==LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        
    def term(self):
        """
        term: factor((MUL|DIV)factor)*
        """
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type==MUL:
                self.eat(MUL)
            elif token.type==DIV:
                self.eat(DIV)
            node = BinOp(node, token, self.factor())
        return node
    
    def expr(self):
        """
        expr: term((PLUS|MINUS)term)*
        """
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type==PLUS:
                self.eat(PLUS)
            elif token.type==MINUS:
                self.eat(MINUS)
            node = BinOp(node, token, self.term())
        return node
    
    def parse(self):
        """
        Main entry point - build and return AST.
        """
        node = self.expr()
        if self.current_token.type!=EOF:
            self.error()
        return node
    
    