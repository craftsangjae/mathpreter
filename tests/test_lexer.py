import pytest

from mathpreter.lexer import Lexer
from mathpreter.token import TokenType


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
        (";", TokenType.SEMICOLON),
        ("\sum", TokenType.TEX_REDUCE_OP),
        ("\prod", TokenType.TEX_REDUCE_OP),
        ("\mathrm", TokenType.TEX_SYMBOL),
        ("\Pi", TokenType.TEX_SYMBOL),
        ("\pi", TokenType.NUMBER),
        ("\exp", TokenType.NUMBER),
        ("let", TokenType.LET),
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
      ["32.5", "+", "25.2", "-", "1"]),
     ("\sum_{x=12}^{19}{3*x}",
      [TokenType.TEX_REDUCE_OP, TokenType.UNDERSCORE, TokenType.LBRACE, TokenType.IDENT, TokenType.ASSIGN,
       TokenType.NUMBER,
       TokenType.RBRACE,
       TokenType.HAT, TokenType.LBRACE, TokenType.NUMBER, TokenType.RBRACE, TokenType.LBRACE,
       TokenType.NUMBER, TokenType.MULTIPLY, TokenType.IDENT, TokenType.RBRACE],
      ["\sum", "_", "{", "x", "=", "12", "}", "^", "{", "19", "}", "{", "3", "*", "x", "}"]),
     ("let x = -5;",
      [TokenType.LET, TokenType.IDENT, TokenType.ASSIGN, TokenType.MINUS, TokenType.NUMBER, TokenType.SEMICOLON],
      ["let", "x", "=", "-", "5", ";"]
      )
     ]
)
def test_middle_size_equation(test_input, expected_types, expected_values):
    lexer = Lexer(test_input)
    for expected_type, expected_value in zip(expected_types, expected_values):
        token = lexer.next_token()
        assert token.type == expected_type
        assert token.literal == expected_value
