#Visitors


class PrintVisitor(object):
	#Calls function from its string name
	def _func(self,name):
		return getattr(self, 'visit_' + name)
	def visit(self,*args):
		name = type(args[0]).__name__
		elem = args[0]
		visit_func = self._func(name)
		visit_func(elem)
	
	#Visit methods
	def visit_Root(self, element):
		print str(self, element)
	def visit_Statement(self,element):
		print str(self, element)
	def visit_CompoundStatement(self,element):
		print str(self, element)
	def visit_SimpleStatement(self,element):
		print str(self, element)
	def visit_SmallStatement(self,element):
		print str(self, element)
	def visit_Suite(self, element):
		print str(self, element)
	def visit_IfStatement(self, element):
		print str(self, element)
	def visit_ForStatement(self, element):
		print str(self, element)
	def visit_WhileStatement(self, element):
		print str(self, element)
	def visit_FunctionDeclaration(self, element):
		print str(self, element)
	def visit_Expression(self, element):
		print str(self, element)
	def visit_Comparison(self, element):
		print str(self, element)
	def visit_Name(self, element):
		print str(self, element)
	def visit_str(self,element):
		print element