import pytest

from mathpreter.token import TokenType, Token


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("x", TokenType.IDENT),
        ("x1", TokenType.IDENT),
        ("variable", TokenType.IDENT),

        ("123", TokenType.NUMBER),
        ("123.456", TokenType.NUMBER),

        ("+", TokenType.PLUS),
        ("-", TokenType.MINUS),
        ("*", TokenType.MULTIPLY),
        ("/", TokenType.DIVIDE),
        ("%", TokenType.MODULO),
        ("^", TokenType.EXPONENTIATION),
        ("_", TokenType.UNDERSCORE),
        (";", TokenType.SEMICOLON),
        ('let', TokenType.LET),

        ("\sum", TokenType.SUM),
        ("\prod", TokenType.PROD),
        ("\mathrm", TokenType.MATH_RM),
        ("\Pi", TokenType.CPI),
        ("\pi", TokenType.PI),
        ("\exp", TokenType.E),

        ("(", TokenType.LPAREN),
        (")", TokenType.RPAREN),
        ("{", TokenType.LBRACE),
        ("}", TokenType.RBRACE),
    ],
)
def test_initialize_token(test_input, expected):
    assert Token(test_input).type == expected


@pytest.mark.parametrize(
    "test_input",
    ["1a", "\su", "1231.abc"],
)
def test_illegal_token(test_input):
    assert Token(test_input).type == TokenType.ILLEGAL


def test_token_type_equal():
    assert TokenType.CPI == "\Pi"
    assert "\Pi" in {TokenType.CPI}
    assert "\Pi" not in {TokenType.PI}
