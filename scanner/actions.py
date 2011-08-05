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
symbol_table = {}

# Defines node methods & accept, each node inherits node 
# and does not have to define any methods of its own
class node(object):
	def __init__(self,t):
		global symbol_table
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.t[index]
	def __setitem__(self,key,value):
		self.t[key] = value
	def __len__(self):
		return len(self.tokens)
	
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
class IfStatement(node):
	pass
class ForStatement(node):
	pass
class WhileStatement(node):
	pass
class FunctionDeclaration(node):
	pass
class ClassDeclaration(node):
	pass
class DecoratedDeclaration(node):
	pass

####
#Small Statement --> 5th level: expr_stmt|print_stmt|del_stmt|pass_stmt|flow_stmt|import_stmt
####
class ExpressionStatement(node):
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

####
#Atom --> [NAME | NUMBER | STRING]
####
class Atom(node):
	pass
class Name(node):
	pass
class String(node):
	pass
class Number(node):
	pass

