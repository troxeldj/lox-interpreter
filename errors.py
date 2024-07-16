
# Base error Class
class Error(Exception):
    def __init__(self, line: str, message:str):
        self.message = message

    def __str__(self):
        return str(self.message)




class FileNotFoundError(Error):
    def __init__(self, line: str):
        self.line = line
        super().__init__(line, "File not found. Please check the path provided and ensure it's valid.")

    def __str__(self):
        return f"Line: {self.line}\nError:{self.message}"





