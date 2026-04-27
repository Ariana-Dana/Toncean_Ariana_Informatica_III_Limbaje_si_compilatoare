from tokens import TokenType, Token


class LexerError(Exception):
    pass


class Lexer:
    KEYWORDS = {
        "int": TokenType.INT,
        "float": TokenType.FLOAT,
        "bool": TokenType.BOOL,
        "if": TokenType.IF,
        "while": TokenType.WHILE,
        "print": TokenType.PRINT,
        "true": TokenType.BOOL_LITERAL,
        "false": TokenType.BOOL_LITERAL,
    }

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()

        elif self.current_char == '/' and self.peek() == '*':
            self.advance() 
            self.advance()  
            while self.current_char is not None:
                if self.current_char == '*' and self.peek() == '/':
                    self.advance()  
                    self.advance()  
                    return
                self.advance()
            raise LexerError(f"Comentariu neterminat la linia {self.line}, coloana {self.column}")

    def number(self):
        start_line = self.line
        start_col = self.column
        result = ''
        dot_count = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:
                    raise LexerError(
                        f"Numar invalid la linia {start_line}, coloana {start_col}"
                    )
            result += self.current_char
            self.advance()

        if '.' in result:
            return Token(TokenType.FLOAT_LITERAL, float(result), start_line, start_col)
        else:
            return Token(TokenType.INT_LITERAL, int(result), start_line, start_col)

    def identifier_or_keyword(self):
        start_line = self.line
        start_col = self.column
        result = ''

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result in self.KEYWORDS:
            token_type = self.KEYWORDS[result]
            if token_type == TokenType.BOOL_LITERAL:
                return Token(token_type, True if result == "true" else False, start_line, start_col)
            return Token(token_type, result, start_line, start_col)

        return Token(TokenType.IDENTIFIER, result, start_line, start_col)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek() in ['/', '*']:
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier_or_keyword()

            if self.current_char == '=' and self.peek() == '=':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.EQ, '==', line, col)

            if self.current_char == '!' and self.peek() == '=':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.NEQ, '!=', line, col)

            if self.current_char == '<' and self.peek() == '=':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.LE, '<=', line, col)

            if self.current_char == '>' and self.peek() == '=':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.GE, '>=', line, col)

            if self.current_char == '&' and self.peek() == '&':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.AND, '&&', line, col)

            if self.current_char == '|' and self.peek() == '|':
                line, col = self.line, self.column
                self.advance()
                self.advance()
                return Token(TokenType.OR, '||', line, col)

            if self.current_char == '+':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.PLUS, '+', line, col)

            if self.current_char == '-':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.MINUS, '-', line, col)

            if self.current_char == '*':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.MUL, '*', line, col)

            if self.current_char == '/':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.DIV, '/', line, col)

            if self.current_char == '%':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.MOD, '%', line, col)

            if self.current_char == '!':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.NOT, '!', line, col)

            if self.current_char == '=':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.ASSIGN, '=', line, col)

            if self.current_char == '<':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.LT, '<', line, col)

            if self.current_char == '>':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.GT, '>', line, col)

            if self.current_char == '(':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.LPAREN, '(', line, col)

            if self.current_char == ')':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.RPAREN, ')', line, col)

            if self.current_char == '{':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.LBRACE, '{', line, col)

            if self.current_char == '}':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.RBRACE, '}', line, col)

            if self.current_char == ';':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.SEMICOLON, ';', line, col)

            if self.current_char == ',':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.COMMA, ',', line, col)

            raise LexerError(
                f"Caracter necunoscut '{self.current_char}' la linia {self.line}, coloana {self.column}"
            )

        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens