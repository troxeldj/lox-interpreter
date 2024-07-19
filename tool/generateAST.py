from io import TextIOWrapper
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
        if not os.path.exists(outputDir):
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
        openFile = open(fullPath, 'w')
        openFile.write('from abc import ABC\n\n')
        openFile.write(f"class {baseName}(ABC):\n")
        openFile.write(f"\tdef __init__(self):\n")
        openFile.write(f"\t\tpass\n\n")

        GenerateAST.defineAcceptMethod(openFile)
        
        GenerateAST.defineVisitor(openFile, baseName, types)        


        for type in types:
            className = type.split(':')[0].strip()
            fields = type.split(':')[1].strip()
            GenerateAST.defineType(openFile, baseName, className, fields)

    @staticmethod
    def defineType(file: TextIOWrapper, baseName: str, className: str, fieldList: str):
        terms = fieldList.split(', ')
        names = [term.split(' ')[1] for term in terms]
        file.write(f'class {className}({baseName}):\n')
        file.write(f'\tdef __init__(self, ')
        for i, name in enumerate(names):
            file.write(f'{name}{", " if i < len(names) -1 else ""}')
        
        file.write('):\n')

        for name in names:
            file.write(f'\t\tself.{name} = {name}\n')
        file.write('\n')

    @staticmethod
    def defineVisitor(file, baseName: str, types: List[str]):
        file.write('class visitor(ABC):\n')
        file.write('\tdef __init__(self):\n')
        file.write('\t\tpass\n\n')

        for typeStr in types:
            typeName = typeStr.split(':')[0].strip()
            GenerateAST.defineVisitMethod(file, typeName)


    @staticmethod 
    def defineVisitMethod(file, typeName):
        file.write(f'\tdef visit{typeName}(self):\n')
        file.write(f'\t\tpass\n')


    @staticmethod
    def defineAcceptMethod(file):
        file.write('\t@abstractmethod\n')
        file.write('\tdef accept(visitor):\n')
        file.write('\t\tpass\n')






if __name__ == "__main__":
    GenerateAST.main()
