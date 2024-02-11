import pytest

from mathpreter.ast import LetStatement
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
