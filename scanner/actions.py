from pyparsing import *
import pprint

#INDENTATION
indentStack = [1]
indentLevel = 0

def checkIndent(s,l,t):
	#Grab current column
	currentCol = col(l,s)
	print currentCol
	
	#The indent stack.. 
	global indentStack, indentLevel
	while(currentCol < indentStack[-1]):
		indentLevel -= 1
		indentStack.pop()
	#..revives itself after death
	if(not indentStack):
		indentStack = []
		indentLevel = 0
		
	#If the column is greater than the previous line's column
	if(currentCol > indentStack[-1]):
		indentStack.append(currentCol)
		indentLevel += 1
	else:
		raise ParseException(s,l,"Not an indent")


#SYMBOL TABLE
symbol_table = []

#CLASS OBJECTS
class IfStatement(object):
	def __init__(self,t):
		self.arg = t
		pprint.pprint(t.asList())
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
