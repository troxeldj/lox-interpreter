import Expr
from Tok import Token
from TT import TokenType

class AstPrinter(Expr.ExprVisitor):
    def print(self, expr):
        return expr.accept(self)

    def parenthesize(self, name, *exprs) -> str:
        content = ' '.join(expr.accept(self) for expr in exprs)
        return f'({name} {content})'

    def visit_binary_expr(self, expr: Expr.Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_unary_expr(self, expr: Expr.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visit_grouping_expr(self, expr: Expr.Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Expr.Literal):
        if expr.value is None: return "nil"
        return str(expr.value)

if __name__ == '__main__':
    expression = (Expr.Binary(
        Expr.Unary(
    Token(TokenType.MINUS, "-", None, 1),
        Expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(
        Expr.Literal(45.67))));

    print(AstPrinter().print(expression))
