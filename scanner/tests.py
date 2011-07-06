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
	assert('NUM' in tokens and tokens['NUM'] == '42')
	
	#NAME
	print "TESTING [NAME]"
	tokens = grammar.atom.parseString("imaname").asDict()
	assert('NAME' in tokens and tokens['NAME'] == "imaname"), "NAME failed"
	
	#INDENT
	print "TESTING [INDENT]"
	tokens = grammar.INDENT.parseString("\t\t").asDict()
	assert('INDENT' in tokens)
	print tokens
	
	return True
	
	

basics()

