from mathpreter.errors import LexerException
from mathpreter.token import Token, TokenType

WHITESPACE_CHARS = {" ", "\n", "\t", "\r"}


class Lexer:
    """
    read math equation and return the array of tokens
    """

    equation_text: str
    c_pos: int  # current position of equation
    n_pos: int  # next position of equation
    char: str  # current character

    def __init__(self, equation_text: str):
        self.equation_text = equation_text
        self.c_pos = 0
        self.n_pos = 0
        self.char = ""
        self.next_char()

    def next_char(self):
        char = self.peek_char()
        self.char = char
        self.c_pos = self.n_pos
        self.n_pos += 1
        return char

    def peek_char(self):
        if self.n_pos >= len(self.equation_text):
            return ""
        else:
            return self.equation_text[self.n_pos]

    def next_token(self) -> Token:
        self.skip_whitespace()

        if self.char.isalpha() or self.char == '\\':
            return self.read_identifier()
        elif self.char.isnumeric():
            return self.read_number()
        elif self.char in TokenType.symbols():
            token = Token(self.char)
            self.next_char()
            return token
        elif self.char == '':
            self.next_char()
            return Token("")

        # lexing is failed...
        raise LexerException(f"lexing is failed. position: {self.c_pos}")

    def read_identifier(self) -> Token:
        start = self.c_pos
        while True:
            if not self.next_char().isalnum():
                break
        end = self.c_pos
        text = self.equation_text[start: end]
        return Token(text)

    def read_number(self) -> Token:
        start = self.c_pos

        exist_stop = False
        while True:
            char = self.next_char()
            if char.isnumeric():
                pass
            elif char == ".":
                if exist_stop:
                    raise LexerException(f"lexing is failed. '.' appears twice in number. position: {self.c_pos}")
                exist_stop = True
            else:
                break
        end = self.c_pos
        text = self.equation_text[start: end]
        return Token(text)

    def skip_whitespace(self):
        global WHITESPACE_CHARS
        while self.char in WHITESPACE_CHARS:
            self.next_char()
