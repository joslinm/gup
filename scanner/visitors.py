#Visitors


class PrintVisitor(object):
	#Calls function from its string name
	def _func(self,name):
		f = getattr(PrintVisitor(), 'visit_' + name)
		return f
	def visit(self,*args):
		name = type(args[0]).__name__
		elem = args[0]
		visit_func = self._func(type(elem).__name__)
		visit_func(elem)
	
	#Visit methods
	def visit_Root(self, element):
		print str(element)
	def visit_Statement(self,element):
		print str(element)
	def visit_CompoundStatement(self,element):
		print str(element)
	def visit_SimpleStatement(self,element):
		print str(element)
	def visit_SmallStatement(self,element):
		print str(element)
	def visit_Suite(self, element):
		print str(element)
	def visit_IfStatement(self, element):
		print str(element)
	def visit_ForStatement(self, element):
		print str(element)
	def visit_WhileStatement(self, element):
		print str(element)
	def visit_FunctionDeclaration(self, element):
		print str(element)
	def visit_Expression(self, element):
		print str(element)
	def visit_Comparison(self, element):
		print str(element)
	def visit_Name(self, element):
		print str(element)
	def visit_String(self, element):
		print str(element)
	def visit_str(self,element):
		print element

class PrintListVisitor(object):
	import actions
	
	def __init__(self):
		self.tokens = []
		
	#Calls function from its string name
	def _func(self,name):
		f = getattr(self, 'visit_' + name)
		return f
	def visit(self,*args):
		name = type(args[0]).__name__
		elem = args[0]
		visit_func = self._func(type(elem).__name__)
		visit_func(elem)
	
	#Visit methods
	def visit_Root(self, element):
		for l in element:
			self.tokens.append(l)
	def visit_Statement(self,element):
		#print type(element).__name__
		pass
	def visit_CompoundStatement(self,element):
		#print type(element).__name__
		pass
	def visit_SimpleStatement(self,element):
		#print type(element).__name__
		pass
	def visit_SmallStatement(self,element):
		#print type(element).__name__
		pass
	def visit_Suite(self, element):
		#print type(element).__name__
		pass
	def visit_IfStatement(self, element):
		#print type(element).__name__
		pass
	def visit_ForStatement(self, element):
		#print type(element).__name__
		pass
	def visit_WhileStatement(self, element):
		#print type(element).__name__
		pass
	def visit_ExpressionStatement(self, element):
		##e.g. COMPARISON '=' COMPARISON 
		print type(element).__name__
		print element
		print element[0][0][0][0][0]
	def visit_PrintStatement(self, element):
		print type(element).__name__
		print element
		
		
		
	def visit_FunctionDeclaration(self, element):
		print type(element).__name__
		pass
	
	def visit_IfBranch(self, element):
		print type(element).__name__
		print element
	
	def visit_Test(self, element):
		print type(element).__name__
		print element
		
	def visit_Expression(self, element):
		print type(element).__name__
		print self.tokens
	def visit_ArithmeticExpression(self, element):
		print type(element).__name__
		print element
		print self.tokens
		
		
	def visit_Comparison(self, element):
		print str(element)
		string = '{0} {1} {2}'
		#b = self.tokens.pop()
		#c = self.tokens.pop()
		#print self.tokens
		#a = string.format(c, element[1], b)
		#a = comp_format.format(self.tokens.pop(), self.tokens.pop(), self.tokens.pop())
		#self.tokens.append(a)
		#a = self.tokens.pop()
		#b = self.tokens.pop()
		#c = string.format(a, self
		print a
		self.tokens.append(a)
		
	
	def visit_Atom(self, element):
		pass
	def visit_Number(self, element):
		#print element
		self.tokens.append(element[0])
	def visit_Name(self, element):
		self.tokens.append(element[0])
	def visit_String(self, element):
		self.tokens.append(element[0])
	