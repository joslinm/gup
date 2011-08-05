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
- Make parse action to catch wrong undents	[ ]
- Create a translation dict	& make it		[ ]
	so that every Keyword() is in there
'''

#INDENTATION
indentStack = [1]

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

class ExpressionStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
	def accept_str(self,list):
		for t in self.tokens:
			if type(t) == type(''):
				list.push(t)
			else:
				list.extend(t.accept_str(list))
		return list
		
class PrintStatement(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
	def accept_str(self,list):
		for t in self.tokens:
			if type(t) == type(''):
				list.push(t)
			else:
				list.extend(t.accept_str(list))
		return list
		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
		
class IfBranch(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
class Test(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		for t in self.tokens:
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)		
####
####COMPARISON -- [EXPRESSION]
####		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)

class ArithmeticExpression(object):
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
			try:
				t.accept(visitor)
			except Exception:
				pass
		visitor.visit(self)
	
	def accept_str(self, lis):
		print "sldkjfs" + self.tokens
		for t in self.tokens:
			print "Token: %s" % str(t)
			if type(t) is type(''):
				print 'pushing'
				lis.push(t)
			else:
				print 'extending list'
				lis.extend(t.accept_str(list))
		return lis

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
			try:
				t.accept(visitor)
			except Exception:
				pass
		visitor.visit(self)
	
	def accept_str(self, lis):
		print "sldkjfs" + self.tokens
		for t in self.tokens:
			print "Token: %s" % str(t)
			if type(t) is type(''):
				print 'pushing'
				lis.push(t)
			else:
				print 'extending list'
				lis.extend(t.accept_str(list))
		return lis

####
####ATOM -- [NAME | NUMBER | STRING]
####
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
	def accept_str(self,list):
		for t in self.tokens:
			if type(t) == type(''):
				list.push(t)
			else:
				list.extend(t.accept_str(list))
		return list
		
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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
	
	def accept_str(self, list):
		for t in self.tokens:
			if type(t) == type(''):
				list.append(t)
			else:
				list.extend(t.accept_str(list))
		return list

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
			try:
				t.accept(visitor)
			except:
				pass
		visitor.visit(self)
	
	def accept_str(self, list):
		for t in self.tokens:
			if type(t) == type(''):
				list.push(t)
			else:
				list.extend(t.accept_str(list))
		return list

class Number(object):
	def __init__(self,t):
		self.t = t
		self.tokens = t.asList()
	def __str__(self):
		return str(self.t)
	def __getitem__(self, index):
		return self.tokens[index]
		
	def accept(self, visitor):
		visitor.visit(self)
	
	def accept_str(self, list):
		for t in self.tokens:
			if type(t) == type(''):
				list.push(t)
			else:
				list.extend(t.accept_str(list))
		return list

