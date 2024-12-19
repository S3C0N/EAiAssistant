# lexer.py

from tokens import TokenType, Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(text)

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 0
        self.pos += 1
        self.column += 1

    @property
    def current_char(self):
        if self.pos >= self.length:
            return None
        return self.text[self.pos]


    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
            elif self.current_char == '{':
                tokens.append(Token(TokenType.LEFT_BRACE, '{', self.line, self.column))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TokenType.RIGHT_BRACE, '}', self.line, self.column))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TokenType.EQUALS, '=', self.line, self.column))
                self.advance()
            elif self.current_char == '"':
                token = self.string()
                tokens.append(token)
            elif self.current_char.isdigit() or self.current_char in '-.':
                token = self.number_or_date()
                tokens.append(token)
            elif self.current_char.isalpha() or self.current_char == '_':
                token = self.identifier()
                tokens.append(token)
            elif self.current_char.isalpha() or self.current_char == '---':
                token = self.identifier()
                tokens.append(token)
            else:
                raise ValueError(f"Unexpected character '{self.current_char}' at line {self.line} column {self.column}")
        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens


    def string(self):
        start_line = self.line
        start_column = self.column
        result = ''
        self.advance()  # Skip opening quote
        while self.current_char != '"' and self.current_char is not None:
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError(f"Unterminated string at line {start_line} column {start_column}")
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, result, start_line, start_column)

    def identifier(self):
        start_line = self.line
        start_column = self.column
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in '_-.'):
            result += self.current_char
            self.advance()
        return Token(TokenType.IDENTIFIER, result, start_line, start_column)

    def number(self):
        start_line = self.line
        start_column = self.column
        result = ''
        has_decimal_point = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char in '-.eE'):
            if self.current_char == '.':
                if has_decimal_point:
                    raise ValueError(f"Invalid number format at line {start_line} column {start_column}")
                has_decimal_point = True
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, result, start_line, start_column)
    def number_or_date(self):
        start_line = self.line
        start_column = self.column
        result = ''
        has_decimal_point = False
        dot_count = 0

        if self.current_char == '-':
            result += self.current_char
            self.advance()

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char in '.-'):
            if self.current_char == '.':
                dot_count += 1
            result += self.current_char
            self.advance()
        # Check if it's a date (contains two dots)
        if dot_count == 2:
            # Treat as a string (date)
            return Token(TokenType.STRING, result, start_line, start_column)
        else:
            # Attempt to convert to a number
            try:
                value = float(result)
                return Token(TokenType.NUMBER, value, start_line, start_column)
            except ValueError:
                raise ValueError(f"Invalid number format '{result}' at line {start_line} column {start_column}")

