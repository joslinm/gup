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
- Organize into categories / sections 		[x]
- Name them into groups 			[ ]
- Hook up parse actions 			[ ]

XXX
- Using suppress on comma results in unknown    [x]
    single-element tuple declarations
    ( e.g. `('a',)` )(line no.107)
    
    __Resolution__
    Implement optional unsuppressed ENDCOMMA
    (line no.108)
'''
#------------------------------------------------#
# E L E M E N T S
#------------------------------------------------#
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
COMMA = Suppress(',')
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
# C O R E | G R A M M A R
#------------------------------------------------#
#Imports
dotted_name = delimitedList(NAME, delim='.')
dotted_as_name = dotted_name + Optional(_as + NAME)
import_name = _import + (dotted_as_name | dotted_name)
import_stmt = import_name

#Test & atom node are two building blocks of many grammars
#[depends on #Comparison nodes] => *Forwards test
test = Forward()
testlist_comp = Forward()
testlist = delimitedList(test) + ENDCOMMA
testlist1 = delimitedList(test)
atom = testlist_comp | testlist1 | NAME | NUM | OneOrMore(STRING)
		   
#Expr node is a building block of many grammars
#[depends on #Argument Lists] => *Forwards trailer
factor = Forward()
trailer = Forward()
power = atom + ZeroOrMore(trailer) + Optional('**' + factor)
factor << (plus | minus | complement) + (factor | power)
term = factor + ZeroOrMore((mult | div | mod | divFloor) + factor)
arith_expr = term + ZeroOrMore((plus | minus) + term)
shift_expr = arith_expr + ZeroOrMore((shiftLeft | shiftRight) + arith_expr)
and_expr = shift_expr + ZeroOrMore(bitwiseAnd + shift_expr)
xor_expr = and_expr + ZeroOrMore(complement + and_expr)
expr = xor_expr + ZeroOrMore(bitwiseOr + xor_expr)
exprlist = delimitedList(expr) + ENDCOMMA

#Comparison nodes
comp_op = greater|lesser|greaterOrEqual|lesserOrEqual|equal|notequal|_is|_in|_not \
          | _not + _in | _is + _not
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

#List declarations [depends on #Test Node & #Expr Node]
list_iter = Forward()
list_if = _if + test + Optional(list_iter)
list_for = _for + exprlist + _in + testlist + Optional(list_iter)
list_iter << (list_for | list_if)
subscript = (test | test + COLON + test)
subscriptlist = subscript + ZeroOrMore(COMMA + subscript) + ENDCOMMA

#Argument Lists [depends on #List declarations]
fpdef = Forward()
fplist = delimitedList(fpdef) + ENDCOMMA
fpdef << (NAME | (LPAREN + fplist + RPAREN))
varargslist = ZeroOrMore(fpdef + Optional(assign + test) + COMMA) \
		+ (mult + NAME + ( Optional(COMMA + power + NAME)) 
		| fpdef + Optional(assign + test)
		+ ZeroOrMore(COMMA + fpdef + Optional(assign + test) + ENDCOMMA))

argument = test + Optional(comp_for) | test + assign + test
arglist = ZeroOrMore(argument + COMMA) \
          + (argument + Optional(COMMA)| mult + test + ZeroOrMore(COMMA + argument)
           + Optional(COMMA + power + test)
           | power + test)

trailer << ( LPAREN + Optional(arglist) + RPAREN
          | LBRACK + subscriptlist + RBRACK
          | DOT + NAME)
lambdef = _lambda + Optional(varargslist) + COLON + test
parameters = LPAREN + varargslist + RPAREN


#Block statements [depends on #Top Level Statements] => *Forwards simple_stmt & stmt
simple_stmt = Forward()
stmt = Forward()
suite = simple_stmt | (NEWLINE + INDENT + OneOrMore(stmt) + DEDENT)
if_stmt = _if + test + COLON + suite + ZeroOrMore(_elif + test + COLON + suite) \
		+ Optional(_else + COLON + suite)
for_stmt = _for + exprlist + _in + testlist + COLON + suite \
		+ Optional(_else + COLON + suite)
while_stmt = _while + test + COLON + suite + Optional(_else + COLON + suite)
funcdef = _def + NAME + parameters + COLON + suite
return_stmt = _return + Optional(testlist)

#Block flow control statments
pass_stmt = _pass
break_stmt = _break
continue_stmt = _continue
flow_stmt = break_stmt | continue_stmt | return_stmt

#Class Declarations [depends on #Block Statements]
classdef = _class + NAME + Optional(LPAREN + testlist + RPAREN) + COLON + suite
decorator_kernel = KERNELDEC + Optional(LPAREN + arglist + RPAREN) + NEWLINE
decorated = decorator_kernel + (classdef | funcdef)

#Other Statements
augassign = plusAssign | minusAssign | multAssign | divAssign | modAssign \
		| bitwiseAndAssign | bitwiseOrAssign | bitwiseComplementAssign \
		| shiftLeftAssign | shiftRightAssign | powerAssign | floorDivAssign
global_stmt = _global + delimitedList(NAME)
assert_stmt = _assert + delimitedList(test)
del_stmt = _delete + exprlist
print_stmt = _print + Optional(delimitedList(test) + ENDCOMMA)

#Top level statements
expr_stmt = testlist + ZeroOrMore((augassign + testlist) | (assign + testlist))
small_stmt = (expr_stmt | print_stmt | del_stmt | pass_stmt | flow_stmt \
		| import_stmt | global_stmt | assert_stmt)
simple_stmt << (delimitedList(small_stmt, delim=';') + Optional(SEMICOLON) + NEWLINE)
compound_stmt = if_stmt | while_stmt | for_stmt | funcdef | classdef | decorated
stmt << (simple_stmt | compound_stmt)

#Top of our parser
file_input = ZeroOrMore(NEWLINE | stmt) #ENDMARKER.. not sure if it's needed

print file_input
