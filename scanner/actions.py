from pyparsing import *
import pprint
'''
-----
GUP.scanner.actions
Definition of parse actions on grammar including classes
-----
NOTES
- Indentation is handled here and every stmt is given an indent level

TODO
- Create class hierarchy			 		[ ]
- Create a translation dict	& make it		[ ]
	so that every Keyword() is in there
'''


def getCol(s,l,t):
		print l
		print col(l,s)
		print s	

#SYMBOL TABLE
symbol_table = []

'''Class Structure

					[stmt]
		[smpl_stmt]  --|--	[cmpd_stmt]
	{expr,print,del..}	| {if,while,for,..}
		...				|	[suite]
						-------|
'''

class Statement(object):
	def __init__(self,t):
		global indentLevel
		self.t = t
		self.indentLevel = indentLevel
	def __str__(self):
		return " ".join(self.arg)
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?

class SimpleStatement(Statement):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
		pprint.pprint(self.tokens)
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?
		
class CompoundStatement(Statement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?

class SmallStatement(SimpleStatement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?

class Suite(CompoundStatement):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		for t in self.t.asList():
			return pprint.pformat(t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?

class IfStatement(CompoundStatement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
		self.tokens = t.asList()
	def __str__(self):
		return pprint.pformat(self.t.asList()[0][1].getOperator())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?

class ForStatement(CompoundStatement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
		self.tokens = t.asList()
	def __str__(self):
		for t in self.t.asList():
			return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?
class WhileStatement(CompoundStatement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
		self.tokens = t.asList()
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?
class FunctionDeclaration(CompoundStatement):
	def __init__(self,t):
		self.t = t
		pprint.pprint(t.asList())
		self.tokens = t.asList()
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass #Do a literal translate here?
class Expression(SmallStatement):
	def __init__(self, t):
		self.t = t
		self.tokens = t.asList()
		#pprint.pprint(t.asList())
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass
class Comparison(Expression):
	def __init__(self, t):
		self.t = t
		self.tokens = t.asList()
		#pprint.pprint(t.asList())
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def asList(self):
		return self.tokens
	def getOperator(self):
		return type(self.tokens[1])
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass
class Name(Expression):
	def __init__(self, t):
		self.t = t
		self.tokens = t.asList()
		#pprint.pprint(t.asList())
	def __str__(self):
		return pprint.pformat(self.t.asList())
	def accept(self):
		for t in self.tokens:
			try:
				t.visit()
			except:
				pass

		
