"""
Parser for building Abstract syntax trees.
The parser consumes tokens from the lexer and builds an AST.
"""
from src.lexer.token import (INTEGER_CONST, REAL_CONST, PLUS, MINUS, MUL, INTEGER_DIV, FLOAT_DIV, LPAREN, RPAREN, ID, ASSIGN, BEGIN, END, SEMI, DOT, PROGRAM, VAR, COLON, COMMA, INTEGER, REAL, FUNCTION, EOF)
from src.parser.ast_nodes import (Program, Block, VarDecl, FunctionDecl, Param, FunctionCall, Type, BinOp, Num, UnaryOp, Compound, Assign, Var, NoOp)

class Parser:
    """
    program : PROGRAM variable SEMI block DOT
    block : declarations compound_statement
    declarations : (VAR (variable_declaration SEMI)+)? (FUNCTION ID (LPAREN formal_parameter_list RPAREN)? COLON type_spec SEMI block SEMI)*
                 | empty
    formal_parameter_list : formal_parameters
                          | formal_parameters SEMI formal_parameter_list
    formal_parameters : ID (COMMA ID)* COLON type_spec
    variable_declaration : ID (COMMA ID)* COLON type_spec
    type_spec : INTEGER | REAL
    compound_statement : BEGIN statement_list END
    statement_list : statement
                   | statement SEMI statement_list
    statement : compound_statement
              | assignment_statement
              | empty
    assignment_statement : variable ASSIGN expr
    variable : ID
    expr : term ((PLUS | MINUS) term)*
    term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
    factor : PLUS factor
           | MINUS factor
           | INTEGER_CONST
           | REAL_CONST
           | LPAREN expr RPAREN
           | function_call
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
        self.eat(PROGRAM)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node
    
    def block(self):
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node
    
    def declarations(self):
        declarations = []
        #Variable declaraions
        if self.current_token.type==VAR:
            self.eat(VAR)
            while self.current_token.type==ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)
        #Function declarations
        while self.current_token.type==FUNCTION:
            self.eat(FUNCTION)
            func_name = self.current_token.value
            self.eat(ID)
            params = []
            if self.current_token.type==LPAREN:
                self.eat(LPAREN)
                params = self.formal_parameter_list()
                self.eat(RPAREN)
            self.eat(COLON)
            return_type = self.type_spec()
            self.eat(SEMI)
            block_node = self.block()
            func_decl = FunctionDecl(func_name, params, return_type, block_node)
            declarations.append(func_decl)
            self.eat(SEMI)
        return declarations
    
    def formal_parameter_list(self):
        if self.current_token.type!=ID:
            return []
        params = self.formal_parameters()
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            params.extend(self.formal_parameters())
        return params
    
    def formal_parameters(self):
        param_nodes = []
        param_tokens = [self.current_token]
        self.eat(ID)
        while self.current_token.type==COMMA:
            self.eat(COMMA)
            param_tokens.append(self.current_token)
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        for param_token in param_tokens:
            param_nodes.append(Param(Var(param_token), type_node))
        return param_nodes
    
    def variable_declaration(self):
        var_nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type==COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)
        type_node = self.type_spec()
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]
        return var_declarations
    
    def type_spec(self):
        token = self.current_token
        if self.current_token.type==INTEGER:
            self.eat(INTEGER)
        else:
            self.eat(REAL)
        node = Type(token)
        return node
    
    def compound_statement(self):
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)
        root = Compound()
        for node in nodes:
            root.children.append(node)
        return root
    
    def statement_list(self):
        node = self.statement()
        results = [node]
        while self.current_token.type==SEMI:
            self.eat(SEMI)
            results.append(self.statement())
        if self.current_token.type==ID:
            self.error()
        return results
    
    def statement(self):
        if self.current_token.type==BEGIN:
            node = self.compound_statement()
        elif self.current_token.type==ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node
    
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
        factor : PLUS factor | MINUS factor | INTEGER_CONST | REAL_CONST | LPAREN expr RPAREN | function_call | variable
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
        elif token.type==INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type==REAL_CONST:
            self.eat(REAL_CONST)
            return Num(token)
        elif token.type==LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type==ID:
            if self.lexer.current_char=='(':
                return self.function_call()
            else:
                return self.variable()
        else:
            self.error()

    def function_call(self):
        token = self.current_token
        func_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        actual_params = []
        if self.current_token.type!=RPAREN:
            actual_params.append(self.expr())
            while self.current_token.type==COMMA:
                self.eat(COMMA)
                actual_params.append(self.expr())
        self.eat(RPAREN)
        return FunctionCall(func_name, actual_params, token)
        
    def term(self):
        """
        term: factor((MUL| INTEGER_DIV | FLOAT_DIV)factor)*
        """
        node = self.factor()
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            token = self.current_token
            if token.type==MUL:
                self.eat(MUL)
            elif token.type==INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif token.type==FLOAT_DIV:
                self.eat(FLOAT_DIV)
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
    
    