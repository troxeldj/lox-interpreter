import sys
from errors import FileNotFoundError

class Lox:
    hadError = False

    def __init__(self):
        pass

    def main(self):
        if len(sys.argv) > 2:
            print('Usage: jlox <script>')
            exit(64)
        elif len(sys.argv) == 2:
            self.runFile(sys.argv[1])
        else: self.runPrompt()

    # runs lox source code
    def run(self, source: str):
        tokens = source.split(" ")
        
        for token in tokens:
            print(token, end=" ")
        print()


    # runs prompt (if file not given)
    def runPrompt(self):
        while True:
            line = input("> ")
            if line == '' or not line or line == 'exit':
                break
            self.run(line)
    
    # runs file (file specified in command)
    def runFile(self, fileName: str):
        fileContents = ""
        # Get file contents
        try:
            fileContents = open(fileName, "r").read()
        except Exception as e:
            self.error(1, f"Unable to open {fileName}. Please check that this file exists.")
        if fileContents != "":
            self.run(fileContents)

        if(Lox.hadError): sys.exit(65)

    def makeTokens(self, progInput):
        pass
    
    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        sys.stderr.write(f"[Line {line}] Error {where}: {message}" )
        Lox.hadError = True
