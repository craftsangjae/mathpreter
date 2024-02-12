from abc import ABC, abstractmethod
from typing import List, Optional
from decimal import Decimal

from mathpreter.token import Token


class Node(ABC):
    """AST(Abstract Syntax Tree) 내 Node들"""

    @abstractmethod
    def literal(self) -> str:
        pass


class Expression(Node):
    """표현식"""
    pass


class Statement(Node):
    """명령문"""
    pass


class Program(Node):
    statements: List[Statement]

    def __init__(self, statements: Optional[List[Statement]] = None):
        self.statements = statements if statements else []

    def append(self, statement: Statement):
        self.statements.append(statement)

    def literal(self) -> str:
        if self.statements:
            return self.statements[0].literal()
        return ""

    def __str__(self):
        return "\n".join([str(stmt) for stmt in self.statements])


class ExpressionStatement(Statement):
    """ 표현식
    """
    token: Token
    expression: Expression

    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return str(self.expression)


class Identifier(Expression):
    """ 식별자
    """
    token: Token
    value: str

    def __init__(self, token: Token):
        self.token = token
        self.value = token.literal

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return str(self.token.literal)


class NumberLiteral(Expression):
    """ 숫자 리터럴 """
    token: Token
    value: Decimal

    def __init__(self, token: Token):
        self.token = token
        self.value = Decimal(token.literal)

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return str(self.token.literal)


class LetStatement(Statement):
    """let 명령문
    """
    token: Token
    name: Identifier
    value: Expression

    def __init__(self, token: Token, name: Identifier, value: Expression):
        self.token = token
        self.name = name
        self.value = value

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"let {self.name} = {self.value}"


class AssignStatement(Statement):
    """할당 명령문"""
    pass


class PrefixExpression(Expression):
    """전위연산자 표현식"""
    token: Token
    operator: str
    right: Expression

    def __init__(self, token: Token, right: Expression):
        self.token = token
        self.operator = token.literal
        self.right = right

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"{self.operator}{self.right}"


class InfixExpression(Expression):
    """중위연산자 표현식"""
    token: Token
    left: Expression
    operator: str
    right: Expression

    def __init__(self, token: Token, left: Expression, right: Expression):
        self.token = token
        self.left = left
        self.operator = token.literal
        self.right = right

    def literal(self) -> str:
        return self.token.literal

    def __str__(self):
        return f"({self.left}{self.operator}{self.right})"


class ReducerExpression(Expression):
    """시그마 혹은 곱기호 표현식
    1. 합기호
    \sum_{k=1}^7 k^2

    2. 곱기호
    \prod_{i=1}^5 (i+1)
    """

    pass


class CombinatoricsExpression(Expression):
    """조합론 표현식
    1. permutation(순열)
    : _{n}\mathrm{P}_{k}

    2. combination(조합)
    : _{n}\mathrm{C}_{k}

    3. permutation with repetition(중복 순열)
    : _{n}\mathrm{\Pi}_{k}

    3. combination with repetition(중복 조합)
    : _{n}\mathrm{\Pi}_{k}
    """
    pass
