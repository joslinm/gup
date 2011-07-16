from pyparsing import *

#indentLen * currentIndent = starting column
#e.g. 4 * 2 = 8
indentLen = 0
currentIndent = 0

def checkIndent(s,l,t):
	global currentIndent, indentLen
	currentCol = col(l,s)
	
	#If the column is greater than the previous line's column
	if(currentCol > (currentIndent * indentLen)):
	
		#If there's no indentLen, this is the first indent
		if(indentLen == 0):
			indentLen = currentCol
			currentIndent = 1
			
		#This will run through the chain of VALID indents
		#The elses indicate failed logic
		else: 
			#If it's a valid length indent..
			if (currentCol % indentLen == 0):
				#If it is one more indent..
				if(currentCol / indentLen == (currentIndent + 1)):
					#Then it's a valid indentation
					currentIndent += 1
				else:
					raise ParseFatalException("Too many additional indents")
			else:
				raise ParseFatalException("Alteration of initial indent length")
	else:
		raise ParseException("Not an indent")

def checkUndent(s,l,t):
	global currentIndent, indentLen
	currentCol = col(l,s)
	print currentCol
	
	#If the column is less than the previous line's column
	if(currentCol < (currentIndent * indentLen)):
		if (currentCol == 0): #Check for 0 now to avoid divide by 0 below
			#We can drop current indent to 0, because of the following scenario:
			'''
			if x == y:
				for x in y:
					if x > y:
						print 'hello world'
			else:
				print 'hello'
			'''
			#But this also means that it requires additional checking elsewhere
			currentIndent = 0
		else:
			if(currentCol % indentLen == 0): #Valid length indent..
				currentIndent = currentCol / indentLen
			else:
				raise ParseException("Alteration of initial indent length in undent")
	else:
		raise ParseException("Not an undent")

INDENT = empty.setParseAction(checkIndent).setDebug().setName('indent')
UNDENT = FollowedBy(empty).setParseAction(checkUndent).setDebug().setName("UNDENT")

