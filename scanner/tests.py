import grammar

def NAME():
    grammar.NAME += grammar.StringEnd()
    return grammar.NAME.parseString("hi")
def atom():
    grammar.atom += grammar.StringEnd()
    return grammar.atom.parseString("hi")

functions = [NAME, atom]
tests = ['''if (x == 5):
        print "hello kitty"
    else:
        print "hello!"
    ''']

print grammar.file_input.parseString(tests[0])

for func in functions:
    print func()
