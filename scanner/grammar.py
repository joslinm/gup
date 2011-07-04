from pyparsing import *

'''
-----
GUP.grammar
This module will be imported into scanner.py
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
- Organize into categories / sections 		[ ]
- Name them into groups 					[ ]
- Hook up parse actions 					[ ]
'''

#Basics
NAME = Word(alphas + "_")
NUM = Word(nums)
STRING = Or( dblQuotedString, sglQuotedString )
NEWLINE = StringEnd()
#TODO: INDENT + DEDENT need parse actions to validate indentation
INDENT = StringStart() + OneOrMore('\t')
DEDENT = StringStart() + ZeroOrMore('\t')

#Comparisons
greater = Literal('>')
lesser = Literal('<')
greaterOrEqual = Literal('>=')
lesserOrEqual = Literal('<=')
equal = Literal('==')
notequal = Literal('!=')

_in = Keyword('in')
_not = Keyword('not')
_is = Keyword('is')
_and = Keyword('and')
_or = Keyword('or')

#Flow Control
_while = Keyword('while')
_if = Keyword('if')
_else = Keyword('else')
_elif = Keyword('elif')
_for = Keyword('for')
_continue = Keyword('continue')
_pass = Keyword('pass')
_break = Keyword('break')

#Utility Keywords
_def = Keyword('def')
_class = Keyword('class')
_lambda = Keyword('lambda')
_delete = Keyword('del')
_print = Keyword('print')
_global = Keyword('global')
_import = Keyword('import')
_as = Keyword('as')
_assert = Keyword('assert')
_return = Keyword('return')

#Assignments
assign = Literal('=')
plusAssign = Literal("+=")
minusAssign = Literal("-=")
multAssign = Literal("*=")
divAssign = Literal("/=")
modAssign = Literal("%=")
bitwiseAndAssign = Literal("&=")
bitwiseOrAssign = Literal("|=")
bitwiseComplementAssign = Literal("^=")
shiftLeftAssign = Literal("<<=")
shiftRightAssign = Literal(">>=")
powerAssign = Literal("**=")
floorDivAssign = Literal("//=")

#Math Operations
mult = Literal('*')
power = Literal('**')
div = Literal('/')
divFloor = Literal('//')
mod = Literal('%')
plus = Literal('+')
minus = Literal('-')

#Bitwise Operations
shiftLeft = Literal('<<')
shiftRight = Literal('>>')
bitwiseAnd = Literal('&')
bitwiseOr = Literal('|')
bitwiseXor = Literal('^')
complement = Literal('~')

#Literals (Suppress showing up in results table)
#XXX Using suppress on comma results in not being able to tell single-element tuple ( e.g. `('a',)` )
COMMA = Suppress(',')
#YYY Implement unsuppressed ENDCOMMA
ENDCOMMA = Optional(',')
LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACK = Suppress("[")
RBRACK = Suppress("]")
COLON = Suppress(":")
SEMICOLON = Suppress(';')
DOT = Suppress('.')
COMMENT = Suppress(pythonStyleComment)
KERNELDEC = Suppress('@kernel')

#------------------------------------------------#
# Elements
#------------------------------------------------#
#The simplest elements that don't need forwarding
comp_op = greater|lesser|greaterOrEqual|lesserOrEqual|equal|notequal|_is|_in|_not \
          | _not + _in | _is + _not
augassign = plusAssign | minusAssign | multAssign | divAssign | modAssign \
		| bitwiseAndAssign | bitwiseOrAssign | bitwiseComplementAssign \
		| shiftLeftAssign | shiftRightAssign | powerAssign | floorDivAssign
pass_stmt = _pass
break_stmt = _break
continue_stmt = _continue
decorator_kernel = KERNELDEC + Optional(LPAREN + arglist + RPAREN) + NEWLINE

#Test node is a building block for many elements
test = Forward()
testlist_comp = Forward()
atom = testlist_comp | testlist1 | NAME | NUMBER | OneOrMore(STRING)
testlist = delimitedList(test) + ENDCOMMA
testlist1 = delimitedList(test)
subscript = (test | test + COLON + test)
subscriptlist = subscript + ZeroOrMore(COMMA + subscript) + ENDCOMMA
		   
#Defining factor will allow us to define expr -- another useful building block
factor = Forward()
power = atom + ZeroOrMore(trailer) + Optional('**' + factor)
factor << (plus | minus | complement) + (factor | power)
term = factor + ZeroOrMore((mult | div | mod | divFloor) + factor)
arith_expr = term + ZeroOrMore((plus | minus) + term)
shift_expr = arith_expr + ZeroOrMore((shiftLeft | shiftRight) + arith_expr)
and_expr = shift_expr + ZeroOrMore(bitwiseAnd + shift_expr)
xor_expr = and_expr + ZeroOrMore(complement + and_expr)
expr = xor_expr + ZeroOrMore(bitwiseOr + xor_expr)
exprlist = delimitedList(expr) + ENDCOMMA

#Comparison elements
comparison = expr + ZeroOrMore(comp_op + expr)
not_test = Forward()
not_test << ((_not +  not_test) | comparison)
and_test = not_test + ZeroOrMore(_and + not_test)
or_test = and_test + ZeroOrMore(_or + and_test)
test << (or_test + Optional(_if + or_test + _else + test))
comp_iter = Forward()
comp_for = _for + exprlist + _in + or_test + Optional(comp_iter)
comp_if = _if + test + Optional(comp_iter)
comp_iter << (comp_for | comp_if)
testlist_comp << (test + (comp_for | ZeroOrMore(COMMA + test) + ENDCOMMA))

#Statements
stmt = Forward()
flow_stmt = break_stmt | continue_stmt | return_stmt
return_stmt = _return + Optional(testlist)
del_stmt = _delete + exprlist
print_stmt = _print + Optional(delimitedList(test) + ENDCOMMA)
dotted_name = delimitedList(NAME, delim='.')
dotted_as_name = dotted_name + Optional(_as + NAME)
import_name = _import + (dotted_as_name | dotted_name)
import_stmt = import_name
expr_stmt = testlist + ZeroOrMore((augassign + testlist) | (assign + testlist))
global_stmt = _global + delimitedList(NAME)
assert_stmt = _assert + delimitedList(test)
small_stmt = (expr_stmt | print_stmt | del_stmt | pass_stmt | flow_stmt \
		| import_stmt | global_stmt | assert_stmt)
simple_stmt = delimitedList(small_stmt, delim=';') + Optional(SEMICOLON) + NEWLINE

suite = simple_stmt | (NEWLINE + INDENT + OneOrMore(stmt) + DEDENT)
for_stmt = _for + exprlist + _in + testlist + COLON + suite \
		+ Optional(_else + COLON + suite)
while_stmt = _while + test + COLON + suite + Optional(_else + COLON + suite)
if_stmt = _if + test + COLON + suite + ZeroOrMore(_elif + test + COLON + suite) \
		+ Optional(_else + COLON + suite)
return_stmt = _return + Optional(testlist)
flow_stmt = break_stmt | continue_stmt | return_stmt

fpdef = Forward()
fplist = delimitedList(fpdef) + ENDCOMMA
fpdef << (NAME | (LPAREN + fplist + RPAREN))
varargslist = ZeroOrMore(fpdef + Optional(assign + test) + COMMA) \
		+ (mult + NAME + ( Optional(COMMA + power + NAME)) 
		| fpdef + Optional(assign + test)
		+ ZeroOrMore(COMMA + fpdef + Optional(assign + test) + ENDCOMMA))
lambdef = _lambda + Optional(varargslist) + COLON + test
parameters = LPAREN + varargslist + RPAREN
funcdef = _def + NAME + parameters + COLON + suite

#Argument List
argument = test + Optional(comp_for) | test + assign + test
arglist = ZeroOrMore(argument + COMMA) + (argument + Optional(COMMA) \ 
		| mult + test + ZeroOrMore(COMMA + argument) + Optional(COMMA + power + test)
		| power + test
trailer = LPAREN + Optional(arglist) + RPAREN \ 
		| LBRACK + subscriptlist + RBRACK
		| DOT + NAME
list_iter = Forward()
list_if = _if + test + Optional(list_iter)
list_for = _for + exprlist + _in + testlist + Optional(list_iter)
list_iter << (list_for | list_if)

classdef = _class + NAME + Optional(LPAREN + testlist + RPAREN) + COLON + suite
decorated = decorator + (classdef | funcdef)
compound_stmt = if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated
stmt = simple_stmt | compound_stmt
file_input = ZeroOrMore(NEWLINE | stmt) ENDMARKER