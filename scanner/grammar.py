from pyparsing import *
import actions

'''
-----
GUP.scanner.grammar
This module will be imported into scanner.py and holds our CFG grammar
(heavily influenced by Python)
-----
NOTES
- Keyword('if') will NOT match ("ifsomething") but WILL match ("[if] something")
- Literal('if') will match ("ifsomething")
- Pyparsing requires that you build your grammar bottom up
- Forward is used to define grammars that are recursive and need to be defined
    temporarily (see pgs. 36 - 37 in `Getting Started With Pyparsing` as well as
    http://packages.python.org/pyparsing --> pyparsing.Forward)
TODO
- Finish grammar with base as file_input 	[x]
- Organize into categories / sections 		[x]
- Name them into groups 					[ ]
- Hook up parse actions 					[ ]

XXX
- Using suppress on comma results in unknown    [x]
    single-element tuple declarations
    ( e.g. `('a',)` )(line no.107)
    
    __Resolution__
    Implement optional unsuppressed ENDCOMMA
    (line no.108)
    
- RunTimeError: maximum recursion depth         [x]
    exceeded when doing simple if
    test (or any I think)

    __Resolution__
    atom wasn't implemented properly
    (line no. 162)

- file_input isn't matching anything            [ ]
'''

### SAFE (and slow)
### Uses ^ instead of | for OR expressions:
'''
One issue to be aware of is that '|' is an eager matcher, not a greedy one;
that is, it will match the first successful match, and not evaluate all options
and choose the longest one. In a construct such as this:
OneOrMore(libraryDef | useDef | architectureDef | entityDef | 
          packageBodyDef | packageDef | configurationDeclarationDef)
you must be careful that an early expression might mask a later one in the list.
To work around this, replace the '|'s with '^'s - you'll take a hit in parsing speed
but this may help you identify some subtle issues in your grammar.
'''

ParserElement.setDefaultWhitespaceChars(" \n")
#------------------------------------------------#
# E L E M E N T S
#------------------------------------------------#
#Literals (Suppress showing up in results table)
COMMA = Suppress(',')
ENDCOMMA = Optional(',')
LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACK = Suppress("[")
RBRACK = Suppress("]")
COLON = Suppress(":")
TICK = Suppress('`')
SEMICOLON = Suppress(';')
DOT = Suppress('.')
COMMENT = Suppress(pythonStyleComment)

#Basics
NAME = Word(alphas)("NAME")
NUM = (Word(nums) + Optional(DOT + Word(nums)))("NUM")
STRING = (dblQuotedString ^ sglQuotedString)("STRING")
NEWLINE = Suppress(StringEnd())
#TODO: INDENT + DEDENT need parse actions to validate indentation
TAB = White('\t', exact=1)
INDENT = ((StringStart() + (OneOrMore(TAB))).parseWithTabs())("INDENT")
#XXX Removing Dedent.. need to set parse action instead. Only here as filler for suite
DEDENT = Forward()

#Comparisons
greater = Literal('>')('greater')
lesser = Literal('<')('lesser')
greaterOrEqual = Literal('>=')('greaterOrEqual')
lesserOrEqual = Literal('<=')('lesserOrEqual')
equal = Literal('==')('equal')
notequal = Literal('!=')('notequal')

_in = Keyword('in')('in')
_not = Keyword('not')('not')
_is = Keyword('is')('is')
_and = Keyword('and')('and')
_or = Keyword('or')('or')

#Flow Control
_while = Keyword('while')('while')
_if = Keyword('if')('if')
_else = Keyword('else')('else')
_elif = Keyword('elif')('elif')
_for = Keyword('for')('for')
_continue = Keyword('continue')('continue')
_pass = Keyword('pass')('pass')
_break = Keyword('break')('break')

#Utility Keywords
KERNELDEC = Keyword('@kernel')("KERNELDEC")
_def = Keyword('def')('def')
_class = Keyword('class')('class')
_lambda = Keyword('lambda')('lambda')
_delete = Keyword('del')('delete')
_print = Keyword('print')('print')
_global = Keyword('global')('global')
_import = Keyword('import')('import')
_as = Keyword('as')('as')
_assert = Keyword('assert')('assert')
_return = Keyword('return')('return')

#Assignments
assign = Literal('=')('assign')
plusAssign = Literal("+=")('plusAssign')
minusAssign = Literal("-=")('minusAssign')
multAssign = Literal("*=")('multAssign')
divAssign = Literal("/=")('divAssign')
modAssign = Literal("%=")('modAssign')
bitwiseAndAssign = Literal("&=")('bitwiseAndAssign')
bitwiseOrAssign = Literal("|=")('bitwiseOrAssign')
bitwiseComplementAssign = Literal("^=")('bitwiseComplementAssign')
shiftLeftAssign = Literal("<<=")('shiftLeftAssign')
shiftRightAssign = Literal(">>=")('shiftRightAssign')
powerAssign = Literal("**=")('powerAssign')
floorDivAssign = Literal("//=")('floorDivAssign')

#Math Operations
mult = Literal('*')('mult')
power = Literal('**')('power')
div = Literal('/')('div')
divFloor = Literal('//')('divFloor')
mod = Literal('%')('mod')
plus = Literal('+')('plus')
minus = Literal('-')('minus')

#Bitwise Operations
shiftLeft = Literal('<<')('shiftLeft')
shiftRight = Literal('>>')('shiftRight')
bitwiseAnd = Literal('&')('bitwiseAnd')
bitwiseOr = Literal('|')('bitwiseOr')
bitwiseXor = Literal('^')('bitwiseXor')
complement = Literal('~')('complement')


#------------------------------------------------#
# C O R E | G R A M M A R
#------------------------------------------------#
#Imports
dotted_name = delimitedList(NAME, delim='.')('dotted_name')
dotted_as_name = dotted_name + Optional(_as + NAME)('dotted_as_name')
import_name = _import + (dotted_as_name ^ dotted_name)('import_name')
import_stmt = import_name('import_stmt')

#Test & atom node are two building blocks of many grammars
#[depends on #Comparison nodes] => *Forwards test
test = Forward()('test')
testlist_comp = Forward()('testlist_comp')
testlist1 = Forward()('testlist1')
atom = ((LPAREN + testlist_comp + RPAREN) \
       ^ (TICK + testlist1 + TICK) \
       ^ (NAME | NUM | OneOrMore(STRING)))('atom')
	   
#Expr node is a building block of many grammars
#[depends on #Argument Lists] => *Forwards trailer
factor = Forward()('factor')
trailer = Forward()('trailer')
power = (atom + ZeroOrMore(trailer) + Optional('**' + factor))("power")
factor << (((plus ^ minus ^ complement) + factor) ^ power)
term = (factor + ZeroOrMore((mult ^ div ^ mod ^ divFloor) + factor))('term')
arith_expr = (term + ZeroOrMore((plus ^ minus) + term))('arith_expr')
shift_expr = (arith_expr + ZeroOrMore((shiftLeft ^ shiftRight) + arith_expr)) \
	('shift_expr')
and_expr = (shift_expr + ZeroOrMore(bitwiseAnd + shift_expr))('and_expr')
xor_expr = (and_expr + ZeroOrMore(complement + and_expr))('xor_expr')
expr = (xor_expr + ZeroOrMore(bitwiseOr + xor_expr))('expr')
exprlist = (delimitedList(expr) + ENDCOMMA)('exprlist')

#Comparison nodes
comp_op = (greater^lesser^greaterOrEqual^lesserOrEqual^equal^notequal^_is^_in^_not \
          ^ _not + _in ^ _is + _not)('comp_op')
comparison = (expr + ZeroOrMore(comp_op + expr))('comparison')
not_test = Forward()('not_test')
not_test << ((_not +  not_test) ^ comparison)
and_test = (not_test + ZeroOrMore(_and + not_test))('and_test')
or_test = (and_test + ZeroOrMore(_or + and_test))('or_test')
test << (or_test + Optional(_if + or_test + _else + test))
comp_iter = Forward()('comp_iter')
comp_for = (_for + exprlist + _in + or_test + Optional(comp_iter))('comp_for')
comp_if = (_if + test + Optional(comp_iter))('comp_if')
comp_iter << (comp_for ^ comp_if)
testlist_comp << (test + (comp_for ^ ZeroOrMore(COMMA + test) + ENDCOMMA))
testlist = (delimitedList(test) + ENDCOMMA)('testlist')
testlist1 << (delimitedList(test)('testlist1'))

#List declarations [depends on #Test Node & #Expr Node]
list_iter = Forward()('list_iter')
list_if = (_if + test + Optional(list_iter))('list_if')
list_for = (_for + exprlist + _in + testlist + Optional(list_iter))('list_for')
list_iter << (list_for ^ list_if)
subscript = (test ^ (test + COLON + test))('subscript')
subscriptlist = (delimitedList(subscript) + ENDCOMMA)('subscriptlist')

#Argument Lists [depends on #List declarations]
fpdef = Forward()('fpdef')
fplist = (delimitedList(fpdef) + ENDCOMMA)('fplist')
fpdef << (NAME ^ (LPAREN + fplist + RPAREN))
varargslist = (ZeroOrMore(fpdef + Optional(assign + test) + COMMA) \
		+ (mult + NAME + ( Optional(COMMA + power + NAME)) 
		^ fpdef + Optional(assign + test)
		+ ZeroOrMore(COMMA + fpdef + Optional(assign + test) + ENDCOMMA))) \
		('varargslist')

argument = (test + Optional(comp_for) ^ test + assign + test)('argument')
arglist = (ZeroOrMore(argument + COMMA) \
          + (argument + Optional(COMMA)^ mult + test + ZeroOrMore(COMMA + argument)
           + Optional(COMMA + power + test)
           ^ power + test))('arglist')

trailer << ( (LPAREN + Optional(arglist) + RPAREN) \
          ^ (LBRACK + subscriptlist + RBRACK) \
          ^ (DOT + NAME))('trailer')
lambdef = (_lambda + Optional(varargslist) + COLON + test)('lambdef')
parameters = (LPAREN + varargslist + RPAREN)('parameters')


#Block statements [depends on #Top Level Statements] => *Forwards simple_stmt & stmt
simple_stmt = Forward()('simple_stmt')
stmt = Forward()('stmt')
#XXX Need to remove DEDENT as it matches INDENT just the same..
#XXX Need to place a action statement to verify the ending DEDENT
suite = (simple_stmt ^ (NEWLINE + INDENT + OneOrMore(stmt) + DEDENT))('suite')
if_stmt = (_if + test + COLON + suite + ZeroOrMore(_elif + test + COLON + suite) \
		+ Optional(_else + COLON + suite))('if_stmt')
for_stmt = (_for + exprlist + _in + testlist + COLON + suite \
		+ Optional(_else + COLON + suite))('for_stmt')
while_stmt = (_while + test + COLON + suite + Optional(_else + COLON + suite))('while')
funcdef = (_def + NAME + parameters + COLON + suite)('funcdef')
return_stmt = (_return + Optional(testlist))('return_stmt')

#Block flow control statments
pass_stmt = _pass('pass_stmt')
break_stmt = _break('break_stmt')
continue_stmt = _continue('continue_stmt')
flow_stmt = (break_stmt ^ continue_stmt ^ return_stmt) ('flow_stmt')

#Class Declarations [depends on #Block Statements]
classdef = (_class + NAME + Optional(LPAREN + testlist + RPAREN) + COLON + suite)('classdef')
decorator_kernel = (KERNELDEC + Optional(LPAREN + arglist + RPAREN) + NEWLINE)('decorator_kernel')
decorated = (decorator_kernel + (classdef ^ funcdef))('decorated')

#Other Statements
augassign = (plusAssign ^ minusAssign ^ multAssign ^ divAssign ^ modAssign \
		^ bitwiseAndAssign ^ bitwiseOrAssign ^ bitwiseComplementAssign \
		^ shiftLeftAssign ^ shiftRightAssign ^ powerAssign ^ floorDivAssign) \
		.setResultsName('augassign')
global_stmt = (_global + delimitedList(NAME))('global_stmt')
assert_stmt = (_assert + delimitedList(test))('assert_stmt')
del_stmt = (_delete + exprlist)('del_stmt')
print_stmt = (_print + Optional(delimitedList(test) + ENDCOMMA))('print_stmt')

#Top level statements
expr_stmt = (testlist + ZeroOrMore((augassign + testlist) ^ (assign + testlist)))('expr_stmt')
small_stmt = (expr_stmt ^ print_stmt ^ del_stmt ^ pass_stmt ^ flow_stmt \
		^ import_stmt ^ global_stmt ^ assert_stmt)('small_stmt')
simple_stmt << (delimitedList(small_stmt, delim=';') + Optional(SEMICOLON) + NEWLINE)
compound_stmt = (if_stmt ^ while_stmt ^ for_stmt ^ funcdef ^ classdef ^ decorated) \
	('compound_stmt')
stmt << (simple_stmt ^ compound_stmt)

#Top of our parser
file_input = (ZeroOrMore(stmt + NEWLINE))('file_input')
