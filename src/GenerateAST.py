import io
import sys
import os
from typing import List, Any, IO

class GenerateAST:
    def __init__(self): ...

    def main(self):
        if len(sys.argv) != 2:
            sys.stderr.write("usage python3 GenerateAST.py <output directory>\n")
            exit(65)

        outputDir = sys.argv[1]

        if(not os.path.exists(outputDir)):
            sys.stderr.write("Invalid Path\n")
            exit(65)

        self.defineAST(outputDir, "Expr", [
            "Binary : left, operator, right",
            "Grouping : expression",
            "Literal : value",
            "Unary : operator, right"
        ])

    def defineAST(self, outputDir: str, baseClass: str, types: List[str]):
        fullPath: str = f"{outputDir}/{baseClass}.py"
        file = open(fullPath, 'w')

        file.write('from abc import ABC, abstractmethod\n\n')

        self.defineVisitor(file, baseClass, types)

        file.write(f'class {baseClass}(ABC): \n\n')
        file.write('    @abstractmethod\n')
        file.write(f'    def accept(self, visitor: ExprVisitor): ...\n\n')


        
        for typee in types:
            className = typee.split(":")[0].strip()
            fields = typee.split(":")[1].strip()
            self.defineType(file, baseClass, className, fields)

        file.close()
    
    def defineType(self, file: IO[Any], baseClass: str, className: str, fields: str):
        fieldList = fields.split(', ')
        file.write(f'class {className}({baseClass}):\n')

        file.write(f'    def __init__(self, {", ".join(field for field in fieldList)}):\n')
        for name in fieldList:
            file.write(f'        self.{name} = {name}\n')
        file.write(f'\n    def accept(self, visitor: {baseClass}Visitor):\n        return visitor.visit_{className.lower()}_expr(self)\n')
        file.write('\n')

    def defineVisitor(self, file: IO[Any], baseClass: str, types: List[str]):
        file.write(f'class {baseClass}Visitor(ABC):\n')
        types = [typee.split(':')[0].lower().strip() for typee in types]
        for typee in types:
            file.write('    @abstractmethod\n')
            file.write(f'    def visit_{typee}_expr(self, expr): ...\n\n')


if __name__ == "__main__":
    ast = GenerateAST()
    ast.main()
