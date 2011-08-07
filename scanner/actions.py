from pyparsing import *
'''
-----
GUP.scanner.actions
Definition of parse actions on grammar including classes
-----

TODO
- Create a translation dict	& make it		[ ]
	so that every Keyword() is in there
'''

#SYMBOL TABLE
symbol_table = {'inputA': ('float',1), 'inputB':('float',1), 'output':('cl_mem',1)}
functions = {}

#Bare class to define functions with
class function(object):
	def __init__(self, name, num_param, kernel):
		self.name = name
		self.num_param = num_param
		self.kernel = kernel
	
# Defines node methods & accept, each node inherits node 
# and does not have to define any methods of its own
class node(object):
	def __init__(self,t):
		global symbol_table, functions
		self.t = t
		self.tokens = t.asList()
		self.symbols = symbol_table
		self.functions = functions
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.t[index]
	def __setitem__(self,key,value):
		self.t[key] = value
	def __len__(self):
		return len(self.tokens)
	
	def get_child_str(self):
		if type(self.t[0]) is not type(''):
			return self.t[0].get_child_str()
		else:
			return self.t[0]
	
	def traverse_to(self, obj_name):
		try:
			if obj_name == type(self).__name__:
				return self
			else:
				return self.t[0].traverse_to(obj_name)
		except:
			return None
		
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
				
		visitor.visit(self)

#[ROOT]
class Root(node): 
	#(stmt | NEWLINE)*
	pass

##[STMT]
class Statement(node): 
	#(simple_stmt ^ compound_stmt)
	pass

### [COMPOUND_STATEMENT] ^ [SIMPLE_STATEMENT]
class SimpleStatement(node):
	#(small_stmt)
	pass
class CompoundStatement(node):
	#(if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated)*
	pass

####
#Simple Statement --> 4th level: small_stmt
####		
class SmallStatement(node):
	pass
	
####
#Compound Statement --> 4th level: if|while|for|funcdef|classdef|decorated
####	
class Parameters(node):
	pass
class IfStatement(node):
	pass
class ForStatement(node):
	pass
class WhileStatement(node):
	pass
class FunctionDeclaration(node):
	def __init__(self,t):
		global functions
		self.t = t
		self.tokens = t.asList()
		self.functions = functions
		dict = {}
		dict['num_params'] = len(t[2])
		dict['kernel'] = False
		dict['name'] = t[1].get_child_str()
		self.functions[dict['name']] = dict
		self.dict_entry = self.functions[dict['name']]
	def assign_kernel(self):
		self.dict_entry['kernel'] = True
		
class KernelDeclaration(node):
	def __init__(self,t):
		global functions
		self.t = t
		self.tokens = t.asList()
		self.functions = functions
		
		print t 
		print self.t[1].assign_kernel()
		print self.t[1].dict_entry
		
class ClassDeclaration(node):
	pass
class DecoratedDeclaration(node):	
	pass

####
#Small Statement --> 5th level: expr_stmt|print_stmt|del_stmt|pass_stmt|flow_stmt|import_stmt
####

#Expression statement catches assignment statements & operates on the NAME
class ExpressionStatement(node):
	def __init__(self, t):
		global symbol_table
		self.symbols = symbol_table
		self.tokens = t.asList()
		self.t = t
		self.check_assignment()
		
		
	#Check for assignment statement & grab name
	def check_assignment(self):
		if self.t[1] == '=':
			search_obj = self.t[2].traverse_to
			name_obj = self.t[0].traverse_to('Name')
			name = name_obj[0]
			
			if search_obj('Number'):
				self.symbols[name] = ('float ',0)
			elif search_obj('String'):
				self.symbols[name] = ('char[250] ',0)
			elif search_obj('Name')[0] in self.symbols:
				self.symbols[name] = self.symbols[search_obj('Name')[0]]
				raw_input()
			else:
				self.symbols[name] = ('unknown',0)
			
			name_obj.type = self.symbols[name_obj[0]]
			return name_obj.type
		else:
			return None

class FunctionCall(node):	
	pass
class PrintStatement(node):
	pass		
class DeleteStatement(node):
	pass
class PassStatement(node):
	pass
class ImportStatement(node):
	pass

###
#Flow Statement --> pass, break, continue
class FlowStatement(node):
	pass
class ContinueStatement(node):
	pass
class BreakStatement(node):
	pass
class PassStatement(node):
	pass
class ReturnStatement(node):
	pass

#################################################################
# # # # # # # # # # # # L O W E R   #   L E V E L S # # # # # # # ## # # # # # # # ## # # # # # 
#################################################################

####
#Compound Statements' 4th level --> test,suite,exprlist, parameters
#NOTE: Consider turning if test: while test: for x in y: def NAME parameters: into their respective branch classes
####
class Suite(node): #(small_stmt ^ compound_stmt)
	pass
class Parameters(node):
	pass

####
#Test --> COMPARISON --> [EXPRESSION] --> smaller expressions
####
class Test(node):
	pass	
class Comparison(node):
	pass
class Expression(node):
	pass
class ArithmeticExpression(node):
	pass

	
class Power(node):
	pass
####
#Atom --> [NAME | NUMBER | STRING]
####
class Atom(node):
	pass
class Name(node):
	type = None
	def __init__(self,t):
		node.__init__(self,t)
		
		#Catch reserved words
		if self[0] in self.symbols:
			self.type = self.symbols[self[0]]

class String(node):
	pass
class Number(node):
	pass

