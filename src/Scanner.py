from sys import _current_frames
from typing import Any, List

from TT import TokenType
from Tok import Token



class Scanner:
    
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }

    def __init__(self, source: str):
        self.source = source 
        self.start = 0
        self.current = 0
        self.line = 1
        self.tokens = list()

    def scanTokens(self) -> List[Token]:
        while(not self.isAtEnd()):
            self.start = self.current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    # adds token to self.tokens (list)
    def scanToken(self):
        from lox import Lox
        current_char = self.advance()
        match(current_char):
            # 1 char tokens
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
            
            # 1 or 2 character tokens
            case '!': self.addToken(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=': self.addToken(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<': self.addToken(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>': self.addToken(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and (not self.isAtEnd()): self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            # whitespace
            case ' ': pass
            case '\r': pass 
            case '\t': pass 
            
            # newline
            case '\n':
                self.line += 1

            #strings
            case '"': self.string()
            case _:
                if self.isDigit(current_char):
                    self.number()
                elif self.isAlpha(current_char):
                    self.identifier()
                else:
                    Lox.error(self.line, f"Unexpected character {current_char}.")

    def match(self, expected: str):
        if self.isAtEnd(): return False
        if(self.source[self.current] != expected): return False
        self.current += 1
        return True

    def peek(self) -> str:
        if self.isAtEnd(): return '\0'
        return self.source[self.current]


    def addToken(self, type: TokenType, literal: Any=None):
        self._addToken(type, literal)
    
    def _addToken(self, type: TokenType, literal: Any):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def isAtEnd(self) -> bool:
        return self.current >= len(self.source)
    

    def isDigit(self, charac: str):
        return charac >= '0' and charac <= '9'
    
    def isAlpha(self, charac: str):
        return ((charac >= 'a' and charac <= 'z') or
            (charac >= 'A' and charac <= 'Z') or
            charac == '_')

    def isAlphaNumeric(self, charac: str):
        return self.isDigit(charac) or self.isAlpha(charac)

    def string(self):
        from .lox import Lox
        while(self.peek != '"' and not self.isAtEnd()):
            if(self.peek()) == '\n': self.line += 1
            self.advance()

        if self.isAtEnd():
            Lox.error(self.line, "Unterminated string.")
        # last quote
        self.advance()
        
        value = self.source[self.start+1:self.current-1].strip()
        self.addToken(TokenType.STRING, value)

    def number(self):
        while(self.isDigit(self.peek())): self.advance()
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()): self.advance()

        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
    def identifier(self):
        while(self.isAlphaNumeric(self.peek())): self.advance()

        text = self.source[self.start:self.current]
        tokType = Scanner.keywords.get(text)
        if tokType is None:
           tokType = TokenType.IDENTIFIER
        self.addToken(tokType)

    def peekNext(self):
        if (self.current + 1) >= len(self.source): return '\0'
        return self.source[self.current + 1]
