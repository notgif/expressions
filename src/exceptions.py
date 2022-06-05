
class ExprCalcException(Exception):
    pass

class TokenError(ExprCalcException):
    def __init__(self, message, token):
        super(TokenError, self).__init__(f"{message}: Line: {token.line}, Col: {token.col}")