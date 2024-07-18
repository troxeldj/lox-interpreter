import sys
import os
from typing import List
class GenerateAST:
    def __init__(self):
        pass
    
    @staticmethod
    def main():
        if len(sys.argv) != 2:
            sys.stderr.write("Usage: generateAST <output dir>")
            return(64)
        outputDir = sys.argv[1]
        if not os._exists(outputDir):
            sys.stderr.write("Invalid directory provided.")
        GenerateAST.defineAst(outputDir, "Expr", [
            "Binary : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal : Object value",
            "Unary : Token operator, Expr right"
        ])

    @staticmethod
    def defineAst(outputDir: str, baseName: str, types: List[str]):
        fullPath = f"{outputDir}/{baseName}.py"
        with open(fullPath, 'w') as file:
            file.write('from abc import ABC')
            file.write(f"class {baseName}(ABC):")
            file.write(f"\tdef __init__(self):")
            file.write(f"\t\tpass")

            
        


        




if __name__ == "__main__":
    GenerateAST.main()
