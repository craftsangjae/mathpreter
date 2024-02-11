from enum import Enum
from typing import Iterable, Union

from mathpreter.utils import is_numeric


class TokenType(Enum):
    """ Token 유형
    """
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    IDENT = "IDENT"
    NUMBER = "NUMBER"

    LET = "let"

    ####
    # Arithmetic Operators
    ####
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    EXPONENTIATION = "^"

    ####
    # Latex Operators
    ###
    ASSIGN = "="
    UNDERSCORE = "_"
    SEMICOLON = ";"

    ####
    # Specific Latex Syntax
    ####
    SUM = "\sum"
    PROD = "\prod"
    MATH_RM = "\mathrm"
    CPI = "\Pi"
    PI = "\pi"
    E = "\exp"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    @classmethod
    def symbols(cls) -> Iterable["TokenType"]:
        return (
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MODULO,
            TokenType.MULTIPLY,
            TokenType.DIVIDE,
            TokenType.EXPONENTIATION,

            TokenType.ASSIGN,
            TokenType.UNDERSCORE,
            TokenType.SEMICOLON,

            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.RBRACE,

        )

    @classmethod
    def latex_words(cls) -> Iterable["TokenType"]:
        """ latex words

        :return:
        """
        return (
            TokenType.SUM,
            TokenType.PROD,
            TokenType.MATH_RM,
            TokenType.CPI,
            TokenType.PI,
            TokenType.E,
        )

    @classmethod
    def reserved_words(cls) -> Iterable["TokenType"]:
        return (
            TokenType.LET,
        )

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other: Union["TokenType", str]):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)


class Token:
    """Lexical Analysis를 통해, 수식 텍스트를 토큰 열로 변환"""
    type: TokenType
    literal: str

    @staticmethod
    def illegal():
        token = Token('')
        token.type = TokenType.ILLEGAL
        return token

    def __init__(self, word: str):
        word = word.strip()

        if not word:
            self.type = TokenType.EOF
            self.literal = ""
            return

        for symbol in TokenType.symbols():
            if word == symbol:
                self.type = symbol
                self.literal = word
                return

        for token in TokenType.latex_words():
            if word == token:
                self.type = token
                self.literal = word
                return

        for token in TokenType.reserved_words():
            if word == token:
                self.type = token
                self.literal = word
                return

        if is_numeric(word):
            self.type = TokenType.NUMBER
            self.literal = word
        elif word[0].isalpha() and word.isalnum():
            self.type = TokenType.IDENT
            self.literal = word
        else:
            self.type = TokenType.ILLEGAL
            self.literal = word
