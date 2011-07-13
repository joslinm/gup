from pyparsing import *
#INDENTATION HANDLING
indentStack = [1]

def checkPeerIndent(s,l,t):
	curCol = col(l,s)
	if curCol != indentStack[-1]:
		if(not indentStack) or curCol > indentStack[-1]:
			raise ParseFatalException(s,l,"illegal nesting")
		raise ParseException(s,l,"Not a peer entry")

def checkSubIndent(s,l,t):
	curCol = col(l,s)
	if curCol > indentStack[-1]:
		indentStack.append(curCol)
	else:
		raise ParseException(s,l,"Not a sub-entry")

def checkUnindent(s,l,t):
	if l >= len(s):
		return
	curCol = col(l,s)
	if not(curCol < indentStack[-1] and curCol <= indentStack[-2]):
		raise ParseException(s,l,"Not an unindent")

def doUnindent():
	indentStack.pop()

class Expression(object):
	def __init__(self, t):
		print t