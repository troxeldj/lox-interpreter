from Tok import Token

class ParseError(RuntimeError): ...


class LRuntimeError(RuntimeError):
  def __init__(self, token: Token, message: str):
    super().__init__(message)
    self.token = token
    self.message = message
