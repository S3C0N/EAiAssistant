# parser.py

from tokens import TokenType, Token
from lexer import Lexer

class Parser:
    def __init__(self, lexer):
        self.tokens = lexer.tokenize()
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.tokens):
            self.current_token = Token(TokenType.EOF, None, self.current_token.line, self.current_token.column)
        else:
            self.current_token = self.tokens[self.pos]

    def expect(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise ValueError(f"Expected token {token_type}, got {self.current_token.type} at line {self.current_token.line} column {self.current_token.column}")

    def parse(self):
        return self.statements()

    def statements(self):
        statements = {}
        while self.current_token.type != TokenType.EOF and self.current_token.type != TokenType.RIGHT_BRACE:
            key, value = self.statement()
            if key in statements:
                if not isinstance(statements[key], list):
                    statements[key] = [statements[key]]
                statements[key].append(value)
            else:
                statements[key] = value
        return statements

    def statement(self):
        if self.current_token.type == TokenType.IDENTIFIER or self.current_token.type == TokenType.STRING:
            key = self.current_token.value
            self.advance()
            self.expect(TokenType.EQUALS)
            value = self.value()
            return key, value
        else:
            raise ValueError(f"Unexpected token {self.current_token.type} at line {self.current_token.line} column {self.current_token.column}")

    def value(self):
        if self.current_token.type == TokenType.LEFT_BRACE:
            return self.block()
        elif self.current_token.type in (TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return value
        else:
            raise ValueError(f"Unexpected value token {self.current_token.type} at line {self.current_token.line} column {self.current_token.column}")

    def block(self):
        self.expect(TokenType.LEFT_BRACE)
        block_content = self.statements()
        self.expect(TokenType.RIGHT_BRACE)
        return block_content
