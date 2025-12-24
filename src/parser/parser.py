"""
Parser for building Abstract syntax trees.
The parser consumes tokens from the lexer and builds an AST.
"""
from src.lexer.token import (INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, EOF)
from src.parser.ast_nodes import (BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp)

class Parser:
    """
    Parser thats builds an Abstract syntax tree.
    Grammar:
        program : BEGIN statement_list END DOT
        statement_list : statement
                       | statement SEMI statement_list
        statement : compound_statement
                  | assignment_statement
                  | empty
        compound_statement : BEGIN statement_list END
        assignment_statement : variable ASSIGN expr
        variable : ID
        expr : term ((PLUS | MINUS) term)*
        term : factor ((MUL | DIV) factor)*
        factor : PLUS factor
               | MINUS factor
               | INTEGER
               | LPAREN expr RPAREN
               | variable
        empty :
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

    def program(self):
        self.eat(BEGIN)
        node = self.statement_list()
        self.eat(END)
        self.eat(DOT)
        return node
    
    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type==ID:
            self.error()
        root = Compound()
        for statement in results:
            root.children.append(statement)
        return root
    
    def statement(self):
        if self.current_token.type==BEGIN:
            node = self.compound_statement()
        elif self.current_token.type==ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node
    
    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        return nodes
    
    def assignment_statement(self):
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node
    
    def variable(self):
        node = Var(self.current_token)
        self.eat(ID)
        return node
    
    def empty(self):
        return NoOp()

    def factor(self):
        """
        factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN | variable
        """
        token = self.current_token
        if token.type==PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type==MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type==INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type==LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            node = self.variable()
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
        node = self.program()
        if self.current_token.type!=EOF:
            self.error()
        return node
    
    