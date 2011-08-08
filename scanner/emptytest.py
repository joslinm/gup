from pyparsing import *

_if = Literal('if').setDebug().setName('if')
hi = Literal('hi')
em = OneOrMore(lineEnd + empty + hi | _if + empty + hi + empty.setDebug().setName('empty copy')) 

data = '''
if hi
gekki
jkdf

'''

#print em.parseString(data)
#
#--------------------------

def getCol(s,loc,toks):
	print col(loc,s)
	print loc
	print s


ParserElement.setDefaultWhitespaceChars(" ")
test = Literal('if') + Literal('True') + Literal(':') + LineEnd().setParseAction(getCol).setDebug().setName('linend') \
	+ empty.copy().setParseAction(getCol) + empty.copy().setParseAction(getCol).setDebug().setName('empty2') + Literal('hi').setDebug().setName('hii') + empty.copy().setParseAction(getCol).setDebug().setName('empty3')
data = '''if True:
i
'''
#print test.parseString(data)

import grammar
#print grammar.test.parseString('else').asList()

def Checker(t):
	pass
	#raise ParseException(t)

a = Literal('a')
b = Literal('matchme')

c = a + LineEnd() + empty.setParseAction(getCol) + empty.setParseAction(getCol) + empty.setParseAction(getCol) + b.setParseAction(getCol).setDebug().setName('b') + LineEnd().setParseAction(getCol).setDebug().setName('lineend') + LineEnd().setParseAction(getCol).setDebug().setName('lineend')
d = c.parseString('''a
		matchme
''')
print d.asList()

#a.setParseAction(Checker).setDebug().setName('.')
#a.parseString('a')
