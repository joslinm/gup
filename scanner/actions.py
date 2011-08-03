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
					[root]
					[stmt]*
		[smpl_stmt]  --|--	[cmpd_stmt]
	{expr,print,del..}	| {if,while,for,..}
		...				|	[suite]
						-------|
'''

class Root(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class Statement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class SimpleStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class CompoundStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class SmallStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class Suite(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class IfStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class ForStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class WhileStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class FunctionDeclaration(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class Expression(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class Comparison(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
	def __len__(self):
		return len(self.tokens)
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
		
class Name(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class String(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class Number(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)

class Atom(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			if type(t) == type(''):
				visitor.visit(t)
			else:
				t.accept(visitor)
		visitor.visit(type(self).__name__)
