from pyparsing import *
'''
-----
GUP.scanner.actions
Definition of parse actions on grammar including classes
-----
'''

#SYMBOL TABLE
symbol_table = {
				'output': {'type':'float', 'declared':True, 'scope':-1},
				'inputA': {'type':'float', 'declared':True, 'scope':-1},
				'inputB': {'type':'float', 'declared':True, 'scope':-1},
				'outputbuffer': {'type':'iter', 'declared':True, 'scope':-1}
				}
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
	
	#Give children variables a unique virus
	def plague_children_vars(self, virus):
		try:
			for t in self.t:
				if type(t).__name__ == 'ExpressionStatement':
					name = t.find_child('Name')
					self.symbols[name[0]]['scope'] = virus
				else:
					try:
						name = t.find_child('Name', 'Suite')
						if name:
							self.symbols[name[0]]['scope'] = virus
					except:
						continue
		except:
			pass

	#Looks linearly
	def find_child(self, obj_name, stop_name=None):
		try:
			if stop_name == type(self).__name__:
				return None
			elif obj_name == type(self).__name__:
				return self
			else:
				return self.t[0].find_child(obj_name)
		except:
			return None
	
	def count_nodes(self, obj_name, count=0):
		try:
			for x in self.t:			
				if type(x).__name__ == obj_name:
					count += 1
				else:
					try:
						count = x.count_nodes(obj_name, count)
					except:
						count += 0
			return count
		except:
			return 0 
	
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
				
		visitor.visit(self)

#[ROOT]
class Root(node): 
	def __init__(self,t):
		node.__init__(self,t)
		self.plague_children_vars(1)

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
	def __init__(self, t):
		node.__init__(self, t)
	
####
#Compound Statement --> 4th level: if|while|for|funcdef|classdef|decorated
####	
class Parameters(node):
	pass
class IfStatement(node):
	pass
class ForStatement(node):
	def __init__(self,t):
		node.__init__(self,t)
		self.symbols[t[1].get_child_str()] = {'type':'int', 'declared':True, 'scope':-1}
		self.t[1].type = {'type':'int', 'declared':True, 'scope':-1}
		print self.t[1].type

class WhileStatement(node):
	pass
class FunctionDeclaration(node):
	def __init__(self,t):
		node.__init__(self,t)
		print self.t
		print self.t[2]
		raw_input()
		
		dict = {}
		dict['branch'] = ''
		dict['num_params'] = len(t[2])
		dict['kernel'] = False
		dict['name'] = t[1].get_child_str()
		self.functions[dict['name']] = dict
		self.dict_entry = self.functions[dict['name']]
	def assign_kernel(self):
		self.dict_entry['kernel'] = True
		self.functions[self.dict_entry['name']] = self.dict_entry
		
class KernelDeclaration(node):
	def __init__(self,t):
		global functions
		self.t = t
		self.tokens = t.asList()
		self.functions = functions
		self.t[1].assign_kernel()

		
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
			wand = self.t[2].find_child
			name_obj = self.t[0].find_child('Name')
			name = name_obj[0]
			
			if wand('Number'):
				self.symbols[name] = {'type':'float', 'declared':False, 'scope':0}
			elif wand('String'):
				self.symbols[name] = {'type':'char*', 'declared':False, 'scope':0, 'value': self.t[2].get_child_str()}
			elif wand('Name')[0] in self.symbols:
				dict = self.symbols[wand('Name')[0]].copy()
				print dict
				print name
				print self.symbols
				if name in self.symbols:
					return
				else:
					dict['declared'] = False
					dict['scope'] = 0
					self.symbols[name] = dict
					name_obj.type = dict
			else:
				raise Exception("Unknown variable right hawre: %s" % name)
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
	def __init__(self, t):
		node.__init__(self, t)
		self.hash = hash(self)
		self.plague_children_vars(self.hash)

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
	def __init__(self,t):
		node.__init__(self,t)
		self.t[0] = self.t[0].replace("'", '"')
class Number(node):
	pass
