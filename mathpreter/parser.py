from typing import List, Dict, Callable

from mathpreter.ast import Expression, Program, Statement, LetStatement, Identifier, ExpressionStatement, \
    PrefixExpression, NumberLiteral
from mathpreter.errors import ParserException
from mathpreter.lexer import Lexer
from mathpreter.token import Token, TokenType

# 전위함수 파싱 로직
prefix_parse_ftype = Callable[[], Expression]

# 중위함수 파싱 로직
infix_parse_ftype = Callable[[Expression], Expression]


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

    def register_prefix_parse_fns(self):
        self.prefix_parse_fns = {}

        self.prefix_parse_fns[TokenType.IDENT] = self.parse_identifier
        self.prefix_parse_fns[TokenType.NUMBER] = self.parse_number
        self.prefix_parse_fns[TokenType.MINUS] = self.parse_prefix_single_expression

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
        value = self.parse_expression()

        self.skip_if_semicolon_exists()
        return LetStatement(token, name, value)

    def parse_expression_statement(self):
        token = self.curr_token
        expression = self.parse_expression()

        self.skip_if_semicolon_exists()
        return ExpressionStatement(token, expression=expression)

    def parse_expression(self) -> Expression:
        left = None
        if prefix_func := self.prefix_parse_fns.get(self.curr_token.type):
            left = prefix_func()

        return left

    def parse_identifier(self) -> Identifier:
        identifier = Identifier(self.curr_token)

        self.shift_token()
        return identifier

    def parse_number(self) -> NumberLiteral:
        number = NumberLiteral(self.curr_token)

        self.shift_token()
        return number

    def parse_prefix_single_expression(self) -> PrefixExpression:
        token = self.curr_token

        self.shift_token()
        right = self.parse_expression()
        return PrefixExpression(token, right)
