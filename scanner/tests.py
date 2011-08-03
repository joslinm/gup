import grammar

'''
-----
GUP.scanner.tests
This module will run test starting from validating the very basic grammars working
its way upward to more complex grammars.
-----
'''

def manual_test(xml, node, message):
	print "MANUAL TEST [%s]: %s" % (node, message)
	print xml + "\n"

#Test NAME | NUMBER | STRING+ | INDENT
def basics():
	print "Running Basic Tests"
	
	#STRING+
	tokens = grammar.atom.parseString("'hello' 'hello2' 'hello3'").asXML()
	manual_test(tokens, "STRING+", "Verify three strings -> hello hello2 hello3")
	
	#NUMBER
	print "TESTING [NUM]"
	tokens = grammar.atom.parseString("42").asDict()
	assert('NUM' in tokens and tokens['NUM'] == '42'), 'NUM failed'
	
	#NAME
	print "TESTING [NAME]"
	tokens = grammar.atom.parseString("imaname").asDict()
	assert('NAME' in tokens and tokens['NAME'] == "imaname"), "NAME failed"
	
	#INDENT
	print "TESTING [INDENT]"
	tokens = grammar.INDENT.parseString("\t\t").asDict()
	assert('INDENT' in tokens), 'INDENT failed'
	print tokens
	
	return True

def trailer():
	print "Running tests on [trailer]"
	'''
	trailer << ( LPAREN + Optional(arglist) + RPAREN
          ^ LBRACK + subscriptlist + RBRACK
          ^ DOT + NAME)
	'''
	print '.name'
	tokens = grammar.trailer.parseString('.name')
	print tokens.dump()
	
	print '(hello,hello,is,anybody,out,there)'
	tokens = grammar.trailer.parseString('(hello,hello,is,anybody,out,there)')
	print tokens.asXML()
	
	print tokens.dump()
	print '[x==5]'
	tokens = grammar.trailer.parseString('[x == 5]')
	print tokens.asXML()
	
def power():
	print "Running tests on [power]"
	#power = (atom + ZeroOrMore(trailer) + Optional('**' + factor)).setResultsName("power")
	tokens = grammar.power.parseString("42.3")
	tokens = grammar.power.parseString("name.trailer")
	
def factor():
	print "Running tests on [factor]"
	#factor << ( ((plus ^ minus ^ complement) + factor) ^ power).setResultsName("factor")
	
	tokens = grammar.factor.parseString("42").dump()
	print tokens

	tokens = grammar.factor.parseString("+ 5").dump()
	print tokens

def expr():
	print "Running tests on [expr]"
	#expr = (xor_expr + ZeroOrMore(bitwiseOr + xor_expr))('expr')
	
	print 'x * 5'
	tokens = grammar.expr.parseString("x * 5")
	print tokens.dump()

def stmt():
	print "Running tests.."
	#expr_stmt = (testlist + ZeroOrMore((augassign + testlist) ^ (assign + testlist)))('expr_stmt')
	
	data = '''x == 5:
	\tx*5'''
	#tokens = grammar.test.parseString(data)
	#print tokens.dump()
	tokens = grammar.file_input.parseFile("code_test.gup")
	#print tokens.dump()

	#tokens = grammar.expr_stmt.parseString("x * 5")
	#print tokens.dump()

def file_input():
	data = '''x == 5:
	\tx*5'''
	tokens = grammar.file_input.parseFile(os.normcase("/code_test.gup"))
	
	print tokens.dump()

def indent():
	tokens = grammar.INDENT.parseString(data)
	print tokens.dump()
	tokens = grammar.UNDENT.parseString("")
	print tokens.dump()
	

def general_test():
	import os
	cdir = os.getcwd()
	os.chdir(os.path.normcase(cdir + '/gup_code'))
	tokens = grammar.file_input.parseFile("general.gup")
	
def test_files(file=None):
	import os
	cdir = os.getcwd()
	os.chdir(os.path.normcase(cdir + '/gup_code'))
	if file:
		tokens = grammar.file_input.parseFile(file)
		print tokens.asList()
		import visitors
		tokens[0].accept(visitors.PrintVisitor())
		#print len(tokens[0][0][0][0][1])
		#print tokens[0][0][0][0][1][2]
	else:
		files = ['if.gup', 'for.gup', 'while.gup', 'functions.gup',
			'kernel_functions.gup']
		
		for file in files:
			tokens = grammar.file_input.parseFile(file)
			
	os.chdir(cdir)

#basics()
#factor()
#power()
#trailer()
#expr()
#stmt()
#indent()


import sys
for arg in sys.argv[1:]:
	if arg == '-f':
		test_files()
	else:
		test_files(arg + '.gup')