from .tok import TokenType, Token, keywords


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
        from .lox import Lox
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

            # more complicated characters (need to look ahead)
            case '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
                
            # special cases 
            case '"': self.string()
            case ' ': pass
            case '\r': pass
            case '\t': pass

            case '\n':
                self.line += 1
            
            # // comments
            case '/':
                if(self.match('/')):
                    while(self.peek() != '\n' and not self.isAtEnd()): 
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            
            # general case: invalid character
            case _:
                if self.isDigit(current_char):
                    self.number()
                elif self.isAlpha(current_char):
                    self.identifier()
                else:
                    Lox.error(self.line, "Unexpected character.")
    
    def isDigit(self, char:str):
        return char.isnumeric()

    def isAlpha(self, char:str):
        return (
                    (char >= 'a' and char <= 'z') or
                    (char >= 'A' and char <= 'Z') or
                    char == '_'
                )

    def isAlphaNumeric(self, char: str):
        return self.isAlpha(char) or self.isDigit(char)

    def addToken(self, type: TokenType):
        self._addToken(type, None)

    def _addToken(self, type: TokenType, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def advance(self):
        self.current += 1

        return self.source[self.current - 1]

    def peek(self):
        if self.isAtEnd(): return '\0';
        return self.source[self.current]

    def match(self, expected: str):
        if self.isAtEnd(): return False
        
        # does not match expected character
        if(self.source[self.current] != expected): return False

        self.current += 1
        return True

    def string(self):
        from .lox import Lox
        while(self.peek() != '"' and not self.isAtEnd()):
            if self.peek() == '\n': self.line += 1
            self.advance()
        # reached end without closing quote 
        if self.isAtEnd():
            Lox.error(self.line, "Unterminated string.")
            return

        # consume last quote "
        self.advance()

        value = self.source[self.start + 1:self.current - 1]
        self._addToken(TokenType.STRING, value)
    
    def number(self):
        while(self.isDigit(self.peek())):
            self.advance()
        
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            
            while(self.isDigit(self.peek())): self.advance()

        self._addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def identifier(self):
        while(self.isAlpha(self.peek())):
            self.advance()

        text = self.source[self.start:self.current]
        tType = keywords.get(text)
        if not tType:
            tType = TokenType.IDENTIFIER

        self.addToken(tType)

    def peekNext(self):
        if ((self.current + 1) >= len(self.source)): return '\0'
        else:
            return self.source[self.current + 1]

