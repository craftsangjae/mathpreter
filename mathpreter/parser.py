from enum import IntEnum
from typing import List, Dict, Callable, Optional

from mathpreter.ast import (
    Expression, Program, Statement,
    LetStatement, Identifier, ExpressionStatement,
    PrefixExpression, NumberLiteral, InfixExpression, MathReducerExpression
)
from mathpreter.errors import ParserException
from mathpreter.lexer import Lexer
from mathpreter.token import Token, TokenType

# 전위함수 파싱 로직
prefix_parse_ftype = Callable[[], Expression]

# 중위함수 파싱 로직
infix_parse_ftype = Callable[[Expression], Expression]


class OperatorPriority(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    EXPONENTIONAL = 7


PRECEDENCE_RELATION = {
    TokenType.PLUS: OperatorPriority.SUM,
    TokenType.MINUS: OperatorPriority.SUM,
    TokenType.DIVIDE: OperatorPriority.PRODUCT,
    TokenType.MULTIPLY: OperatorPriority.PRODUCT,
    TokenType.HAT: OperatorPriority.EXPONENTIONAL
}


class Parser:
    lexer: Lexer

    curr_token: Token
    next_token: Token

    errors: List[str]

    prefix_parse_fns: Dict[TokenType, prefix_parse_ftype]
    infix_parse_fns: Dict[TokenType, infix_parse_ftype]

    def __init__(self, lexer: Lexer):
        self.lexer = lexer

        # initialize current token & next token
        self.curr_token = self.lexer.next_token()
        self.next_token = self.lexer.next_token()

        self.errors = []
        self.register_prefix_parse_fns()
        self.register_infix_parse_fns()

    def register_prefix_parse_fns(self):
        self.prefix_parse_fns = {}

        self.prefix_parse_fns[TokenType.IDENT] = self.parse_identifier
        self.prefix_parse_fns[TokenType.NUMBER] = self.parse_number
        self.prefix_parse_fns[TokenType.MINUS] = self.parse_prefix_single_expression
        self.prefix_parse_fns[TokenType.LPAREN] = self.parse_grouped_expression
        self.prefix_parse_fns[TokenType.TEX_REDUCE_OP] = self.parse_prefix_reducer_expression

    def register_infix_parse_fns(self):
        self.infix_parse_fns = {}
        self.infix_parse_fns[TokenType.PLUS] = self.parse_infix_arithmetic_expression
        self.infix_parse_fns[TokenType.MINUS] = self.parse_infix_arithmetic_expression
        self.infix_parse_fns[TokenType.MULTIPLY] = self.parse_infix_arithmetic_expression
        self.infix_parse_fns[TokenType.DIVIDE] = self.parse_infix_arithmetic_expression
        self.infix_parse_fns[TokenType.MODULO] = self.parse_infix_arithmetic_expression
        self.infix_parse_fns[TokenType.HAT] = self.parse_infix_arithmetic_expression

    def peek_priority(self) -> OperatorPriority:
        global PRECEDENCE_RELATION
        return PRECEDENCE_RELATION.get(self.next_token.type, OperatorPriority.LOWEST)

    def shift_token(self):
        self.curr_token = self.next_token
        self.next_token = self.lexer.next_token()

    def shift_token_if_type_is(self, type: TokenType):
        if not self.next_token_type_is(type):
            raise ParserException(f"Parsing is failed. the type of {self.next_token} is not {type.value}")
        self.shift_token()

    def skip_if_semicolon_exists(self):
        if self.next_token_type_is(TokenType.SEMICOLON):
            self.shift_token()

    def next_token_type_is(self, token_type: TokenType):
        return self.next_token.type == token_type

    def parse_program(self):
        program = Program()

        while self.curr_token.type != TokenType.EOF:
            # `curr_token` should be located at the `end token` of statement
            stmt = self.parse_statement()
            if stmt:
                program.append(stmt)
            self.shift_token()

        return program

    def parse_statement(self) -> Statement:
        curr_token = self.curr_token

        if curr_token.type == TokenType.LET:
            return self.parse_let_statement()

        return self.parse_expression_statement()

    def parse_let_statement(self) -> LetStatement:
        """ 할당 구문을 파싱하기
        :return:
        """
        token = self.curr_token

        self.shift_token_if_type_is(TokenType.IDENT)
        name = Identifier(self.curr_token)

        self.shift_token_if_type_is(TokenType.ASSIGN)

        self.shift_token()
        value = self.parse_expression(OperatorPriority.LOWEST)

        self.skip_if_semicolon_exists()
        return LetStatement(token, name, value)

    def parse_expression_statement(self):
        token = self.curr_token
        expression = self.parse_expression(OperatorPriority.LOWEST)

        self.skip_if_semicolon_exists()
        return ExpressionStatement(token, expression=expression)

    def parse_expression(self, priority: OperatorPriority) -> Expression:
        left = None
        if prefix_func := self.prefix_parse_fns.get(self.curr_token.type):
            left = prefix_func()

        while (
                not self.next_token_type_is(TokenType.EOF)
                and priority < self.peek_priority()
        ):
            infix_func = self.infix_parse_fns.get(self.next_token.type)

            if not infix_func:
                raise ParserException("infix func is not found")
            self.shift_token()
            left = infix_func(left)
            break

        return left

    def parse_grouped_expression(self) -> Optional[Expression]:
        self.shift_token()

        expr = self.parse_expression(OperatorPriority.LOWEST)

        if not self.next_token_type_is(TokenType.RPAREN):
            raise ParserException("Parsing Failed. `)` is missing.")
        self.shift_token()
        return expr

    def parse_identifier(self) -> Identifier:
        return Identifier(self.curr_token)

    def parse_number(self) -> NumberLiteral:
        return NumberLiteral(self.curr_token)

    def parse_prefix_single_expression(self) -> PrefixExpression:
        token = self.curr_token

        self.shift_token()
        right = self.parse_expression(OperatorPriority.PREFIX)
        return PrefixExpression(token, right)

    def parse_prefix_reducer_expression(self) -> MathReducerExpression:
        token = self.curr_token

        if self.next_token_type_is(TokenType.UNDERSCORE):
            self.shift_token()
            identifier, start_cond = self.parse_start_condition_in_math_reducer()

            self.shift_token_if_type_is(TokenType.HAT)

            end_cond = self.parse_stmt_in_math_reducer()
        elif self.next_token_type_is(TokenType.HAT):
            self.shift_token()
            end_cond = self.parse_stmt_in_math_reducer()

            self.shift_token_if_type_is(TokenType.UNDERSCORE)

            identifier, start_cond = self.parse_start_condition_in_math_reducer()
        else:
            raise ParserException("parsing failed. `^` and `_` is missing")
        body = self.parse_stmt_in_math_reducer()
        return MathReducerExpression(token, identifier, start_cond, end_cond, body)

    def parse_start_condition_in_math_reducer(self):
        self.shift_token_if_type_is(TokenType.LBRACE)
        self.shift_token_if_type_is(TokenType.IDENT)
        identifier = self.parse_identifier()
        self.shift_token_if_type_is(TokenType.ASSIGN)

        self.shift_token()
        start_condition = self.parse_expression(OperatorPriority.LOWEST)

        self.shift_token_if_type_is(TokenType.RBRACE)
        return identifier, start_condition

    def parse_stmt_in_math_reducer(self):
        self.shift_token_if_type_is(TokenType.LBRACE)
        return self.parse_bracket()

    def parse_bracket(self) -> Expression:
        self.shift_token()
        expr = self.parse_expression(OperatorPriority.LOWEST)

        self.shift_token_if_type_is(TokenType.RBRACE)
        return expr

    def parse_infix_arithmetic_expression(self, left: Expression) -> InfixExpression:
        global PRECEDENCE_RELATION
        token = self.curr_token

        self.shift_token()
        priority = PRECEDENCE_RELATION.get(token.type)
        right = self.parse_expression(priority)

        return InfixExpression(token, left, right)
