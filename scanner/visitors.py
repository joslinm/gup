'''Visitors

The base class Visitor should be inherited by all other Visitor classes. It will handle 
dispatching & is packaged with the necessary utility methods such as merge
'''

#General Visitor (Should be inherited)
class Visitor(object):
	def __init__(self):
		self.tokens = []
		
	#General dispatch method
	def visit(self,*args):
		name = type(args[0]).__name__
		elem = args[0]
		visit_func = self._func(type(elem).__name__)
		visit_func(elem)
		
	#Calls function from its string name
	def _func(self,name):
		f = getattr(self, 'visit_' + name)
		return f
		
	#Going in reverse order coinicides with the stack
	#Fills in any non-str positions from right-left
	def merge(self,element, debug=False):
		l = range(len(element))
		l.reverse()
		for x in l:
			if type(element[x]) != type(''):
				a = self.tokens.pop()
				if debug:
					print "Popping " + a
					raw_input()
				element[x] = a
		r = ' '.join(element)
		self.tokens.append(r)
		print self.tokens
	def append(self, trailer):
		x = self.tokens.pop()
		x += trailer
		self.tokens.append(x)
	def prepend(self, pre):
		x = self.tokens.pop()
		x = pre + x
		self.tokens.append(x)
	
	#[ROOT]
	def visit_Root(self, element): 
		#(stmt | NEWLINE)*
		pass

	##[STMT]
	def visit_Statement(self, element): 
		#(simple_stmt ^ compound_stmt)
		pass

	### [COMPOUND_STATEMENT] ^ [SIMPLE_STATEMENT]
	def visit_SimpleStatement(self, element):
		#(small_stmt)
		pass
	def visit_CompoundStatement(self, element):
		#(if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated)*
		pass

	####
	#Simple Statement --> 4th level: small_stmt
	####		
	def visit_SmallStatement(self, element):
		pass
		
	####
	#Compound Statement --> 4th level: if|while|for|funcdef|classdef|decorated
	####				
	def visit_IfStatement(self, element):
		pass
	def visit_ForStatement(self, element):
		pass
	def visit_WhileStatement(self, element):
		pass
	def visit_FunctionDeclaration(self, element):
		pass
	def visit_ClassDeclaration(self, element):
		pass
	def visit_DecoratedDeclaration(self, element):
		pass

	####
	#Small Statement --> 5th level: expr_stmt|print_stmt|del_stmt|pass_stmt|flow_stmt|import_stmt
	####
	def visit_ExpressionStatement(self, element):
		pass		
	def visit_PrintStatement(self, element):
		pass		
	def visit_DeleteStatement(self, element):
		pass
	def visit_PassStatement(self, element):
		pass
	def visit_ImportStatement(self, element):
		pass

	###
	#Flow Statement --> pass, break, continue
	def visit_FlowStatement(self, element):
		pass
	def visit_ContinueStatement(self, element):
		pass
	def visit_BreakStatement(self, element):
		pass
	def visit_PassStatement(self, element):
		pass
	def visit_ReturnStatement(self, element):
		pass

	#################################################################
	# # # # # # # # # # # # L O W E R   #   L E V E L S # # # # # # # ## # # # # # # # ## # # # # # 
	#################################################################

	####
	#Compound Statements' 4th level --> test,suite,exprlist, parameters
	#NOTE: Consider turning if test: while test: for x in y: def NAME parameters: into their respective branch classes
	####
	def visit_Suite(self, element): #(small_stmt ^ compound_stmt)
		pass
	def visit_Parameters(self, element):
		pass

	####
	#Test --> COMPARISON --> [EXPRESSION] --> smaller expressions
	####
	def visit_Test(self, element):
		pass	
	def visit_Comparison(self, element):
		pass
	def visit_Expression(self, element):
		pass
	def visit_ArithmeticExpression(self, element):
		pass

	####
	#Atom --> [NAME | NUMBER | STRING]
	####
	def visit_Atom(self, element):
		pass
	def visit_Name(self, element):
		pass
	def visit_String(self, element):
		pass
	def visit_Number(self, element):
		pass

class PrintListVisitor(Visitor):
	import actions
	
	#Visit methods
	def visit_Root(self, element):
		print type(element).__name__
		print element
		
	def visit_Statement(self,element):
		print type(element).__name__
		print element
		
	def visit_CompoundStatement(self,element):
		print type(element).__name__
		print element
		
	def visit_SimpleStatement(self,element):
		print type(element).__name__
		print element
		
	def visit_SmallStatement(self,element):
		print type(element).__name__
		print element
		
		self.append(';\n')
		
	def visit_Suite(self, element):
		print type(element).__name__
		print element
		print self.tokens
		
		self.merge(element)
		self.prepend('{\n')
		self.append('\n}')
		
	def visit_IfStatement(self, element):
		print type(element).__name__
		print element
		
		self.merge(element)
		
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
		
		length = len(element)
		if length % 3 == 0:
			self.merge(element)
			
	def visit_PrintStatement(self, element):
		print type(element).__name__
		print element
		print len(element)
		print len(element) % 2
		
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
		
		
	def visit_Expression(self, element):
		print type(element).__name__
		print element
		
		
		
	def visit_ArithmeticExpression(self, element):
		print type(element).__name__
		print element
		
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
		

		if length == 1:
			pass
		elif length % 3 == 0:
			self.merge(element)
	
	def visit_Atom(self, element):
		pass
	def visit_Number(self, element):
		print type(element).__name__
		print element
		
		#print element
		self.tokens.append(element[0])
	def visit_Name(self, element):
		print type(element).__name__
		print element
		
		self.tokens.append(element[0])
	def visit_String(self, element):
		print type(element).__name__
		print element
		
		self.tokens.append(element[0])
	
	


	