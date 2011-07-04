import grammar

def if_else_test():
    test = '''
    if (x == 5):
        print "hello kitty"
    else:
        print "hello!"
    '''
	
tests = ['''
    if (x == 5):
        print "hello kitty"
    else:
        print "hello!"
    ''']
for test in tests:
    grammar.file_input.parseString(test, parseAll=True)
