from pyparsing import *
import pprint

symbol_table = []

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
