from tokens import TokenType
from ast_nodes import (
    Program, Block, VarDecl, Assignment, PrintStmt,
    IfStmt, WhileStmt, BinaryOp, UnaryOp, Literal, Variable
)


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise ParserError(
                f"Asteptat {token_type.name}, dar am gasit {self.current_token.type.name} "
                f"la linia {self.current_token.line}, coloana {self.current_token.column}"
            )

    def parse(self):
        statements = []

        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())

        return Program(statements)

    def statement(self):
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.BOOL):
            node = self.var_decl()
            self.eat(TokenType.SEMICOLON)
            return node

        elif self.current_token.type == TokenType.IDENTIFIER:
            node = self.assignment()
            self.eat(TokenType.SEMICOLON)
            return node

        elif self.current_token.type == TokenType.PRINT:
            node = self.print_stmt()
            self.eat(TokenType.SEMICOLON)
            return node

        elif self.current_token.type == TokenType.IF:
            return self.if_stmt()

        elif self.current_token.type == TokenType.WHILE:
            return self.while_stmt()

        elif self.current_token.type == TokenType.LBRACE:
            return self.block()

        else:
            raise ParserError(
                f"Instructiune invalida la linia {self.current_token.line}, "
                f"coloana {self.current_token.column}: {self.current_token.type.name}"
            )

    def var_decl(self):
        if self.current_token.type == TokenType.INT:
            var_type = "int"
        elif self.current_token.type == TokenType.FLOAT:
            var_type = "float"
        elif self.current_token.type == TokenType.BOOL:
            var_type = "bool"
        else:
            raise ParserError(
                f"Tip invalid la linia {self.current_token.line}, coloana {self.current_token.column}"
            )

        self.advance()

        if self.current_token.type != TokenType.IDENTIFIER:
            raise ParserError(
                f"Nume de variabila asteptat la linia {self.current_token.line}, "
                f"coloana {self.current_token.column}"
            )

        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)

        return VarDecl(var_type, name)

    def assignment(self):
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.ASSIGN)
        expr = self.expression()
        return Assignment(name, expr)

    def print_stmt(self):
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.expression()
        self.eat(TokenType.RPAREN)
        return PrintStmt(expr)

    def if_stmt(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        then_block = self.block()
        return IfStmt(condition, then_block)

    def while_stmt(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        body = self.block()
        return WhileStmt(condition, body)

    def block(self):
        self.eat(TokenType.LBRACE)
        statements = []

        while self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.EOF:
                raise ParserError("Bloc neterminat: lipseste '}'")
            statements.append(self.statement())

        self.eat(TokenType.RBRACE)
        return Block(statements)

    def expression(self):
        return self.logical_or()

    def logical_or(self):
        node = self.logical_and()

        while self.current_token.type == TokenType.OR:
            op = self.current_token.value
            self.eat(TokenType.OR)
            right = self.logical_and()
            node = BinaryOp(node, op, right)

        return node

    def logical_and(self):
        node = self.equality()

        while self.current_token.type == TokenType.AND:
            op = self.current_token.value
            self.eat(TokenType.AND)
            right = self.equality()
            node = BinaryOp(node, op, right)

        return node

    def equality(self):
        node = self.comparison()

        while self.current_token.type in (TokenType.EQ, TokenType.NEQ):
            op = self.current_token.value
            if self.current_token.type == TokenType.EQ:
                self.eat(TokenType.EQ)
            else:
                self.eat(TokenType.NEQ)
            right = self.comparison()
            node = BinaryOp(node, op, right)

        return node

    def comparison(self):
        node = self.term()

        while self.current_token.type in (TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op = self.current_token.value
            if self.current_token.type == TokenType.LT:
                self.eat(TokenType.LT)
            elif self.current_token.type == TokenType.GT:
                self.eat(TokenType.GT)
            elif self.current_token.type == TokenType.LE:
                self.eat(TokenType.LE)
            elif self.current_token.type == TokenType.GE:
                self.eat(TokenType.GE)

            right = self.term()
            node = BinaryOp(node, op, right)

        return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)

            right = self.factor()
            node = BinaryOp(node, op, right)

        return node

    def factor(self):
        node = self.unary()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV, TokenType.MOD):
            op = self.current_token.value
            if self.current_token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif self.current_token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            else:
                self.eat(TokenType.MOD)

            right = self.unary()
            node = BinaryOp(node, op, right)

        return node

    def unary(self):
        if self.current_token.type == TokenType.NOT:
            op = self.current_token.value
            self.eat(TokenType.NOT)
            operand = self.unary()
            return UnaryOp(op, operand)

        elif self.current_token.type == TokenType.MINUS:
            op = self.current_token.value
            self.eat(TokenType.MINUS)
            operand = self.unary()
            return UnaryOp(op, operand)

        return self.primary()

    def primary(self):
        token = self.current_token

        if token.type == TokenType.INT_LITERAL:
            self.eat(TokenType.INT_LITERAL)
            return Literal(token.value, "int")

        elif token.type == TokenType.FLOAT_LITERAL:
            self.eat(TokenType.FLOAT_LITERAL)
            return Literal(token.value, "float")

        elif token.type == TokenType.BOOL_LITERAL:
            self.eat(TokenType.BOOL_LITERAL)
            return Literal(token.value, "bool")

        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expression()
            self.eat(TokenType.RPAREN)
            return node

        else:
            raise ParserError(
                f"Expresie invalida la linia {token.line}, coloana {token.column}: {token.type.name}"
            )