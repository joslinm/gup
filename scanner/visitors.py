#Visitors

translate_dict = {'print':'printf({0})'}

class PrintVisitor(object):
	#Calls function from its string name
	def _func(self,name):
		f = getattr(PrintVisitor(), 'visit_' + name)
		return f
	#General dispatcher
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
		#This buffer is limited to derivations of ATOM
		self.str_buf = []
		self.poststr_buf = []
		self.node_buf = []
		
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
		print type(element).__name__
		print element
		raw_input()
	def visit_Statement(self,element):
		print type(element).__name__
		print element
		raw_input()
	def visit_CompoundStatement(self,element):
		print type(element).__name__
		print element
		raw_input()
	def visit_SimpleStatement(self,element):
		print type(element).__name__
		print element
		raw_input()
	def visit_SmallStatement(self,element):
		print type(element).__name__
		print element
		raw_input()
	def visit_Suite(self, element):
		print type(element).__name__
		print element
		raw_input()
	def visit_IfStatement(self, element):
		print type(element).__name__
		print element
		raw_input()
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
		raw_input()
		length = len(element)
		if length % 3 == 0:
			self.merge(element)
			
	def visit_PrintStatement(self, element):
		print type(element).__name__
		print element
		print len(element)
		print len(element) % 2
		raw_input()
		length = len(element)
		if length == 1:
			pass
		elif length % 2 == 0:
			self.merge(element)
		
	def visit_FunctionDeclaration(self, element):
		print type(element).__name__
		pass
	
	def visit_Test(self, element):
		print type(element).__name__
		print element
		raw_input()
		
	def visit_Expression(self, element):
		print type(element).__name__
		print element
		raw_input()
		
		
	def visit_ArithmeticExpression(self, element):
		print type(element).__name__
		print element
		raw_input()
		length = len(element)
		if length == 1:
			pass
		elif length % 3 == 0:
			self.merge(element)
		
	def visit_Comparison(self, element):
		print type(element).__name__
		print element
		print len(element)
		length = len(element)
		raw_input()

		if length == 1:
			pass
		elif length % 3 == 0:
			self.merge(element)
	
	def visit_Atom(self, element):
		pass
	def visit_Number(self, element):
		print type(element).__name__
		print element
		raw_input()
		#print element
		self.tokens.append(element[0])
	def visit_Name(self, element):
		print type(element).__name__
		print element
		raw_input()
		self.tokens.append(element[0])
	def visit_String(self, element):
		print type(element).__name__
		print element
		raw_input()
		self.tokens.append(element[0])
	
	def merge(self,element):
		#Going in reverse order coinicides with the stack
		l = range(len(element))
		l.reverse()
		print l
		print element
		for x in l:
			if type(element[x]) != type(''):
				element[x] = self.tokens.pop()
		r = ' '.join(element)
		self.tokens.append(r)
		print self.tokens