import pytest

from mathpreter.lexer import Lexer
from mathpreter.token import TokenType, Token


@pytest.mark.parametrize(
    "test_input,expected_type",
    [
        ("x", TokenType.IDENT),
        ("xy", TokenType.IDENT),
        ("x12y", TokenType.IDENT),
        ("1231", TokenType.NUMBER),
        ("1231.1232", TokenType.NUMBER),
        ("+", TokenType.PLUS),
        ("-", TokenType.MINUS),
        ("*", TokenType.MULTIPLY),
        ("/", TokenType.DIVIDE),
        ("%", TokenType.MODULO),
        ("_", TokenType.UNDERSCORE),
        ("\sum", TokenType.SUM),
        ("\prod", TokenType.PROD),
        ("\mathrm", TokenType.MATH_RM),
        ("\Pi", TokenType.CPI),
        ("\pi", TokenType.PI),
        ("\exp", TokenType.E),
        ("(", TokenType.LPAREN),
        (")", TokenType.RPAREN),
        ("{", TokenType.LBRACE),
        ("}", TokenType.RBRACE)]
)
def test_single_size_equation(test_input, expected_type):
    lexer = Lexer(test_input)
    token = lexer.next_token()

    assert token.type == expected_type


@pytest.mark.parametrize(
    "test_input,expected_types,expected_values",
    [("32.5+25.2-1",
      [TokenType.NUMBER, TokenType.PLUS, TokenType.NUMBER, TokenType.MINUS, TokenType.NUMBER],
      ["32.5", "+", "25", "-", "1"]),
     ("\sum_{x=12}^{19}{3*x}",
      [TokenType.SUM, TokenType.UNDERSCORE, TokenType.LBRACE, TokenType.IDENT, TokenType.ASSIGN, TokenType.NUMBER,
       TokenType.RBRACE,
       TokenType.EXPONENTIATION, TokenType.LBRACE, TokenType.NUMBER, TokenType.RBRACE, TokenType.LBRACE,
       TokenType.NUMBER, TokenType.MULTIPLY, TokenType.IDENT, TokenType.RBRACE],
      ["\sum", "_", "{", "x", "=", "12", "}", "^", "{", "19", "}", "{", "3", "*", "x", "}"]),
     ],
)
def test_middle_size_equation(test_input, expected_types, expected_values):
    assert Token(test_input).type == TokenType.ILLEGAL