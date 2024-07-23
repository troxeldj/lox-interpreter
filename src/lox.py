import sys
from Scanner import Scanner


class Lox:

    hadError = False

    def run(self, fileContents: str):
        scanner = Scanner(fileContents)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)

    def runFile(self, path: str):
        try:
            fileContents = open(path,  'w').read()
        except Exception as e:
            raise Exception(f"Unable to open file at {path}")

        self.run(fileContents)

        if Lox.hadError: exit(65)

    def runPrompt(self):
        while True:
            line = input("> ")
            if line is None or line == "exit":
                self.run(line)
                Lox.hadError = False
    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def report(line: int, where: str, message: str):
        sys.stderr.write(f"[{line}] Error {where}: {message}\n")
        Lox.hadError = True


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
