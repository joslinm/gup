from pyparsing import *

indentStack = [1]

def checkIndent(s,l,t):
	global indentStack
	currentCol = col(l,s)
	print currentCol
	
	#If the column is greater than the previous line's column
	if(currentCol > indentStack[-1]):
		indentStack.append(currentCol)
	else:
		raise ParseException(s,l,"Not an indent")
		
	#TEST#
	#

def checkUndent(s,l,t):
	global indentStack
	currentCol = col(l,s)
	
	#If the column is less than the previous line's column
	if( not (indentStack and currentCol < indentStack[-1] and currentCol <= indentStack[-2]) ):
		raise ParseException(s,l,"not an undent")
	else:
		indentStack.pop()

INDENT = lineEnd.suppress() + empty + empty.copy().setParseAction(checkIndent).setDebug().setName('indent')
UNDENT = FollowedBy(empty).setParseAction(checkUndent).setDebug().setName("UNDENT")

