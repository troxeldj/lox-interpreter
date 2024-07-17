from lox_lang import Lox
from tok import TokenType, Token

# At 4.5.2 

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = list()
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        # append eof token
        self.tokens.append(Token(TokenType.EOF, "", None, self.line ))
        return self.tokens
        
    def isAtEnd(self):
        return self.current >= len(self.source)

    def scanToken(self):
        current_char = self.advance()
        match(current_char):
            # simple single characters
            case '(': self.addToken(TokenType.LEFT_PAREN)
            case ')': self.addToken(TokenType.RIGHT_PAREN)
            case '{': self.addToken(TokenType.LEFT_BRACE)
            case '}': self.addToken(TokenType.RIGHT_BRACE)
            case ',': self.addToken(TokenType.COMMA)
            case '.': self.addToken(TokenType.DOT)
            case '-': self.addToken(TokenType.MINUS)
            case '+': self.addToken(TokenType.PLUS)
            case ';': self.addToken(TokenType.SEMICOLON)
            case '*': self.addToken(TokenType.STAR)

            case '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType. BANG)


            # case: invalid character
            case _:
                Lox.error(self.line, "Unexpected character.")

    def addToken(self, type: TokenType):
        self._addToken(type, None)

    def _addToken(self, type: TokenType, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def advance(self):
        self.current += 1

        return self.source[self.current - 1]
    
    def match(self, expected: str):
        if self.isAtEnd(): return False
        
        # does not match expected character
        if(self.source[self.current] != expected): return False

        self.current += 1
        return True
