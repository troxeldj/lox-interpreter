from Expr import ExprVisitor, Expr, Grouping, Unary, Binary
from TT import TokenType
from error import LRuntimeError
class Interpreter(ExprVisitor):

  def interpret(self, expr):
    from lox import Lox
    try:
      value = self.evaluate(expr)
      print(self.stringify(value))
    except LRuntimeError as e:
      Lox.runtimeError(e)

  def stringify(self, obj):
    if obj is None:
      return None
    
    if isinstance(obj, float):
      text = str(obj)
      if text.endswith(".0"):
        text = text[0:len(text) - 2]
      return text
    return str(obj)

  def visit_binary_expr(self, expr: Binary):
    left = self.evaluate(expr.left)
    right = self.evaluate(expr.right)
    match(expr.operator.type):
      case TokenType.PLUS:
        if (isinstance(left, float) and isinstance(right, float)):
          return(float)(left) + (float)(right) 
        if (isinstance(left, str)) and isinstance(right, str):
          return(str)(left) + (str)(right) 
        raise LRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
      case TokenType.MINUS:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) - (float)(right)
      case TokenType.SLASH:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) / (float)(right)
      case TokenType.STAR:
        self.checkNumberOperandB(expr.operator, left, right)
        return(float)(left) * (float)(right) 
      case TokenType.GREATER:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) > (float)(right)
      case TokenType.GREATER_EQUAL:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) >= (float)(right)
      case TokenType.LESS:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) < (float)(right)
      case TokenType.LESS_EQUAL:
        self.checkNumberOperandB(expr.operator, left, right)
        return (float)(left) <= (float)(right)
      case TokenType.BANG_EQUAL: return not self.isEqual(left, right)
      case TokenType.EQUAL_EQUAL: return self.isEqual(left, right)
    return None
  

  def isEqual(self, leftEx, rightEx):
    if leftEx is None and rightEx is None:
      return True
    if leftEx is None:
      return False
    return leftEx == rightEx


  def visit_grouping_expr(self, expr: Grouping):
    return self.evaluate(expr.expression)

  def evaluate(self, expr: Expr):
    return expr.accept(self)

  def visit_literal_expr(self, expr: Expr):
    return expr.value

  def visit_unary_expr(self, expr: Unary):
    right = self.evaluate(expr.right)
    match(expr.operator.type):
      case TokenType.MINUS:
        self.checkNumberOperand(expr.operator, right)
        return -((float)(right))
      case TokenType.PLUS:
        return not self.isTruthy(right)
    return None
  
  def isTruthy(self, obj):
    if obj is None:
      return False
    if isinstance(obj, bool):
      return (bool)(obj)
    return True

  def checkNumberOperand(self, operator, operand):
    if isinstance(operand, float): return 
    raise LRuntimeError(operator, "Operand must be a number.")
  
  def checkNumberOperandB(self, operator, left, right):
    if isinstance(left, float) and isinstance(right, float): return
    raise LRuntimeError(operator, "Operands must be numbers.")
