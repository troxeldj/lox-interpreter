from abc import ABC

class Expr(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def accept(visitor):
		pass
class visitor(ABC):
	def __init__(self):
		pass

	def visitBinary(self):
		pass
	def visitGrouping(self):
		pass
	def visitLiteral(self):
		pass
	def visitUnary(self):
		pass
class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

class Literal(Expr):
	def __init__(self, value):
		self.value = value

class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

