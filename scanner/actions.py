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

def checkIndent(s,l,t):
	#Grab current column
	currentCol = col(l,s)
	print currentCol
	
	#The indent stack & indent level
	global indentStack, indentLevel
	while(currentCol < indentStack[-1] and len(indentStack) > 1):
		indentLevel -= 1
		indentStack.pop()
		
	#If the column is greater than the previous line's column
	if(currentCol > indentStack[-1]):
		indentStack.append(currentCol)
		indentLevel += 1
	else:
		raise ParseException(s,l,"Not an indent")


#SYMBOL TABLE
symbol_table = []

#CLASS OBJECTS
class Statement(object):
	def __init__(self,t):
		global indentLevel
		self.indentLevel = indentLevel
	def __str__(self):
		return " ".join(t)
		
class SmallStatement(Statement):
	def __init__(self,t):
		pprint.pprint(t.asList())
		print "indent level = %s" % (indentLevel) 

class Suite(Statement):
	def __init__(self,t):
		print pprint.pprint("suite = %s" % t.asList())

class IfStatement(Statement):
	def __init__(self,t):
		self.arg = t
		#pprint.pprint(t.asList())
	def __str__(self):
		return self.arg.asXML()

class ForStatement(object):
	def __init__(self,t):
		self.arg = t
		pprint.pprint(t.asList())
	def __str__(self):
		return self.arg.asXML()
class WhileStatement(object):
	def __init__(self,t):
		self.arg = t
		pprint.pprint(t.asList())
	def __str__(self):
		return self.arg.asXML()
class FunctionDeclaration(object):
	def __init__(self,t):
		self.arg = t
		pprint.pprint(t.asList())
	def __str__(self):
		return self.arg.asXML()
class Expression(object):
	def __init__(self, t):
		self.arg = t
		#pprint.pprint(t.asList())
class Test(object):
	def __init__(self,t):
		self.arg = t
