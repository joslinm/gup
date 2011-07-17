from pyparsing import *
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


INDENT = lineEnd.suppress() + empty + empty.copy().setParseAction(checkIndent).setDebug().setName('indent')

