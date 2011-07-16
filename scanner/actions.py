from pyparsing import *
import pprint

symbol_table = []

#Indentation Handling
indent = 0
def checkIndent(t):
	global indent
	if len(t) > 0:
		tabs = t[0]
		tabs_l = tabs.split('\t')		
		new_indent = len(tabs_l) - 1
		
		if(new_indent - indent > 1):
			raise ParseException("Excess indentation")
		else:
			indent = new_indent

def checkUndent(t):
	global indent
	
	if indent > 0:
		tabs = t[0]
		tabs_l = tabs.split('\t')
		new_indent = len(tabs_l) - 1
		
		if(new_indent + 1 != indent):
			raise ParseException("Invalid dedentation")
		else:
			indent = new_indent

#Classes that grammar will break into its respective objects
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
