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
indentLevel = 0

def grabCol(s,l):
	return col(l,s)
	
def checkIndent(s,l,t):
	#Grab current column
	currentCol = grabCol(s,l)
	#print currentCol
	
	#The indent stack & indent level
	global indentStack, indentLevel
	if(not indentStack):
		indentStack = [1]
		
	if(currentCol <= indentStack[-1]):
		raise ParseException(s,l,"Not an indent")
		
	#If the column is greater than the previous line's column
	indentStack.append(currentCol)
	indentLevel += 1

def checkUndent(s,l,t):
	#Grab current column
	currentCol = grabCol(s,l)
	#print currentCol
	
	global indentStack, indentLevel
	changed = False
	while(currentCol < indentStack[-1] and len(indentStack) > 1):
		indentLevel -= 1
		indentStack.pop()
		changed = True
	
	if(not changed):
		raise ParseException(s,l,"Not an undent")

def checkSamedent(s,l,t):
	currentCol = grabCol(s,l)
	print currentCol
	
	global indentStack
	if(not indentStack):
		pass
	elif(not currentCol == indentStack[-1]):
		raise ParseException(s,l,"Not same dent")

def checkReservedWords(s,l,t):
	reserves = ['else','if','elif','else if']
	print "ATOM CHECKING.." + t[0]
	if t[0] in reserves:
		raise ParseException(s,l,"Part of reserved words")
def getCol(s,l,t):
		print l
		print col(l,s)
		print s	
#SYMBOL TABLE
symbol_table = []
INDENT = lineStart.setParseAction(checkIndent).setDebug().setName('indent')
UNDENT = lineEnd.suppress() + empty + empty.copy().setParseAction(checkUndent).setDebug().setName('undent')
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
		return pprint.pformat(self.t.asList())
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
				pass #Do a literal translate here?
		
