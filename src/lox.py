import sys
from Scanner import Scanner
from Tok import Token
from TT import TokenType
from error import LRuntimeError
from Parser import Parser
from Interpreter import Interpreter
class Lox:
    interpreter = Interpreter()
    hadError = False
    hadRuntimeError = False

    def run(self, fileContents: str):
        from ast_printer import AstPrinter
        
        scanner = Scanner(fileContents)
        tokens = scanner.scanTokens()

        parser = Parser(tokens)
        
        # this is returning none for some reason
        expr = parser.parse()

        if(Lox.hadError):
            return
        
        Lox.interpreter.interpret(expr)
        

    def runFile(self, path: str):
        try:
            fileContents = open(path,  'w').read()
        except Exception as e:
            raise Exception(f"Unable to open file at {path}")

        self.run(fileContents)

        if Lox.hadError: exit(65)
        if Lox.hadRuntimeError: exit(70)

    def runPrompt(self):
        while True:
            line = input("> ")
            if line is not None or line != "exit":
                self.run(line)
                Lox.hadError = False
    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        sys.stderr.write(f"[{line}] Error {where}: {message}\n")
        Lox.hadError = True

    @staticmethod
    def error_tok(tok: Token, message: str):
        if (tok.type == TokenType.EOF):
            Lox.report(tok.line, " at end", message)
        else:
            Lox.report(tok.line, f"at '{tok.lexeme}", message)

    @staticmethod
    def runtimeError(err: LRuntimeError):
        sys.stderr.write(f"err.message\n[line{err.token.line}]")
        Lox.hadRuntimeError = True

    def main(self):
        if len(sys.argv) > 2:
            print("usage: main.py <script_name>")
            exit(64)
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
        else:
            self.runPrompt()

if __name__ == "__main__":
    lox = Lox()
    lox.main()
