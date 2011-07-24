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
- Hook up parse actions 					[ ]
- Match names with _						[ ]

XXX
- `suite` is unable to match consecutive		[ ]
	lines in a row
'''


#ParserElement.setDefaultWhitespaceChars(" \t")
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
STRING = (dblQuotedString | sglQuotedString)("STRING")
NEWLINE = lineEnd.suppress()

#Indentation
#INDENT = lineEnd.suppress() + empty + empty.copy().setParseAction(actions.checkIndent).setDebug().setName('indent')
#INDENT = lineStart.setParseAction(actions.checkIndent).setDebug().setName('indent')
#UNDENT = empty.copy().setParseAction(actions.checkUndent).setDebug().setName('undent')
#SAME_DENT = lineEnd.suppress() + empty + empty.copy().setParseAction(actions.checkSamedent).setDebug().setName('samedent')

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
_while = Keyword('while')
_if = Keyword('if')
_else = Keyword('else')
_elif = Keyword('elif') | Keyword('else if')
_for = Keyword('for')
_continue = Keyword('continue')
_pass = Keyword('pass')
_break = Keyword('break')

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

#Reserves
reserves = _while | _if | _elif | _else | _for | _continue | _pass | _def | _class

ParserElement.setDefaultWhitespaceChars(" \t")
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
test = Forward()('test')#.setParseAction(actions.Test)
testlist_comp = Forward()('testlist_comp')
testlist1 = Forward()('testlist1')
atom = NotAny(reserves) + ((LPAREN + testlist_comp + RPAREN) \
       ^ (TICK + testlist1 + TICK) \
       ^ (NAME | NUM | OneOrMore(STRING)))('atom').setParseAction(actions.checkReservedWords)
	   
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
expr = (xor_expr + ZeroOrMore(bitwiseOr + xor_expr))('expr')#.setDebug().setName('EXPR')
exprlist = (delimitedList(expr) + ENDCOMMA)('exprlist')

#Comparison nodes
comp_op = (greater^lesser^greaterOrEqual^lesserOrEqual^equal^notequal^_is^_in^_not \
          ^ _not + _in ^ _is + _not)('comp_op')
comparison = (expr + ZeroOrMore(comp_op + expr))('comparison').setDebug().setName('COMPARISON')
not_test = Forward()('not_test')
not_test << ((_not +  not_test) ^ comparison).setDebug().setName("teasdfst")
and_test = (not_test + ZeroOrMore(_and + not_test))('and_test')
or_test = (and_test + ZeroOrMore(_or + and_test))('or_test').setDebug().setName('ORtest')
test << Group(or_test + Optional(_if + or_test + _else + test))('test').setDebug().setName('test')
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

argument = ( (test + Optional(comp_for)) ^ test + assign + test)('argument')
arglist = (ZeroOrMore(argument + COMMA) \
          + (argument + Optional(COMMA)^ mult + test + ZeroOrMore(COMMA + argument)
           + Optional(COMMA + power + test)
           ^ power + test))('arglist')

trailer << ( (LPAREN + Optional(arglist) + RPAREN) \
          ^ (LBRACK + subscriptlist + RBRACK) \
          ^ (DOT + NAME))('trailer')
lambdef = (_lambda + Optional(varargslist) + COLON + test)('lambdef')
parameters = (LPAREN + Optional(varargslist) + RPAREN)('parameters')


#Block statements [depends on #Top Level Statements] => *Forwards simple_stmt & stmt
simple_stmt = Forward()('simple_stmt')
stmt = Forward()('stmt')
suite_stmt = Forward()('suite_stmt')
indentst = [1]
suite = indentedBlock(suite_stmt, indentst)#.setParseAction(actions.Suite)
suite.setDebug().setName('indent blocked')
#suite = ((INDENT + OneOrMore(suite_stmt)) ^ simple_stmt )('suite').setDebug().setName('suite')
#suite = ((NEWLINE + INDENT + OneOrMore(stmt) + UNDENT) | simple_stmt)('suite')#.setDebug().setName("suite")
if_stmt = ((Group(Group(_if + test + COLON) + suite + ZeroOrMore(Group(_elif + test + COLON) + suite) \
		+ Optional(Group(_else + COLON) + suite)))('if_stmt')).setParseAction(actions.IfStatement) \
		.setDebug().setName("if statement")
for_stmt = (Group(_for + exprlist + _in + testlist + COLON) + suite \
		+ Optional(_else + COLON + suite))('for_stmt').setParseAction(actions.ForStatement)
while_stmt = (Group(_while + test + COLON) + suite + Optional(_else + COLON + suite))('while').setParseAction(actions.WhileStatement)
funcdef = (Group(_def + NAME + parameters + COLON)('DefiningLine') + suite)('funcdef').setParseAction(actions.FunctionDeclaration)
return_stmt = (_return + Optional(testlist))('return_stmt')

#Block flow control statments
pass_stmt = _pass('pass_stmt')
break_stmt = _break('break_stmt')
continue_stmt = _continue('continue_stmt')
flow_stmt = (break_stmt ^ continue_stmt ^ return_stmt) ('flow_stmt')

#Class Declarations [depends on #Block Statements]
classdef = (_class + NAME + Optional(LPAREN + testlist + RPAREN) + COLON + suite)('classdef')
decorator_kernel = (KERNELDEC + Optional(LPAREN + arglist + RPAREN) + NEWLINE)('decorator_kernel')
decorated = (decorator_kernel + (classdef ^ funcdef))('decorated').setParseAction(actions.FunctionDeclaration)#.setDebug().setName("dec kernel")

#Other Statements
augassign = (plusAssign ^ minusAssign ^ multAssign ^ divAssign ^ modAssign \
		^ bitwiseAndAssign ^ bitwiseOrAssign ^ bitwiseComplementAssign \
		^ shiftLeftAssign ^ shiftRightAssign ^ powerAssign ^ floorDivAssign) \
		.setResultsName('augassign')
global_stmt = (_global + delimitedList(NAME))('global_stmt')
assert_stmt = (_assert + delimitedList(test))('assert_stmt')
del_stmt = (_delete + exprlist)('del_stmt')
print_stmt = (_print + (delimitedList(test) + ENDCOMMA))('print_stmt')

#Top level statements
expr_stmt = (testlist + ZeroOrMore((augassign + testlist) ^ (assign + testlist)))('expr_stmt').setParseAction(actions.Expression)#.setDebug().setName('expression')
small_stmt = (expr_stmt ^ print_stmt.setDebug().setName('PRINT') ^ del_stmt ^ pass_stmt ^ flow_stmt \
		^ import_stmt ^ global_stmt ^ assert_stmt)('small_stmt').setDebug().setName("small_stmt").setParseAction(actions.SmallStatement)
simple_stmt << (small_stmt + ZeroOrMore(';' + small_stmt) \
		+ Optional(SEMICOLON) + NEWLINE)#.setDebug().setName("simple statement")
compound_stmt = (if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated) \
	('compound_stmt').setName("compound statement").setDebug()

suite_stmt << (small_stmt ^ compound_stmt)#.setParseAction(actions.checkSamedent)
stmt << (simple_stmt ^ compound_stmt)#.setParseAction(actions.checkSamedent).setName("stmt").setDebug()

#Top of our parser
file_input = ZeroOrMore(stmt | NEWLINE)#.setDebug().setName("file_input")
