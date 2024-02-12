import pytest

from mathpreter.ast import LetStatement, ExpressionStatement, MathReducerExpression
from mathpreter.lexer import Lexer
from mathpreter.parser import Parser


@pytest.mark.parametrize(
    "test_input,expected_name,expected_value",
    [("let x = 3;", "x", "3"),
     ("let a = 5.12;", "a", "5.12"),
     ("let b = -5", "b", "-5")],
)
def test_single_let_statement(test_input, expected_name, expected_value):
    lexer = Lexer(test_input)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 1

    stmt: LetStatement = program.statements[0]

    assert str(stmt.name) == expected_name
    assert str(stmt.value) == expected_value


@pytest.mark.parametrize(
    "test_input,expected_name,expected_value",
    [
        ("let x = 1 + 2;", "x", "(1+2)"),
        ("let x = 3 + 2 / 3;", "x", "(3+(2/3))"),
        ("let x = - (5 - 2) ^ 5;", "x", "-((5-2)^5)"),
    ],
)
def test_single_let_statement_with_expression(test_input, expected_name, expected_value):
    lexer = Lexer(test_input)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 1

    stmt: LetStatement = program.statements[0]

    assert str(stmt.name) == expected_name
    assert str(stmt.value) == expected_value


@pytest.mark.parametrize(
    "test_input,expected_token,expected_identifier,expected_start,expected_end,expected_body",
    [
        ("\sum_{x=1}^{15}{x + 15}", "\sum", "x", "1", "15", "(x+15)"),
        ("\sum^{15}_{x=1}{x + 15}", "\sum", "x", "1", "15", "(x+15)"),
        ("\sum^{15*2}_{x=1+2}{x+15 }", "\sum", "x", "(1+2)", "(15*2)", "(x+15)"),
    ],
)
def test_single_expression_statement_with_tex_reduce_op(
        test_input, expected_token, expected_identifier, expected_start, expected_end, expected_body
):
    lexer = Lexer(test_input)
    parser = Parser(lexer)
    program = parser.parse_program()
    assert len(program.statements) == 1

    stmt: ExpressionStatement = program.statements[0]
    expr: MathReducerExpression = stmt.expression

    assert expr.token.literal == expected_token
    assert expr.identifier.literal() == expected_identifier
    assert str(expr.start) == expected_start
    assert str(expr.end) == expected_end
    assert str(expr.body) == expected_body
