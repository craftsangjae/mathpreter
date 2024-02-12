class LexerException(Exception):
    """ Lexer 동작에서 발생한 에러
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class ParserException(Exception):
    """ Parser 동작에서 발생한 에러
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message
