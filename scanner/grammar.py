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

'''

#Basics
NAME = Word(alphas + "_")
NUM = Word(nums)
STRING = Or( dblQuotedString, sglQuotedString )

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

#Functions
_def = Keyword('def')
_return = Keyword('return')

#Augmented Assignments
plusAssign = Literal("+=")
minusAssign = Literal("-=")
multAssign = Literal("*=")
divAssign = Literal("/=")

#Math Operations
mult = Literal('*')
div = Literal('/')
mod = Literal('%')
divFloor = Literal('//')
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
LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACK = Suppress("[")
RBRACK = Suppress("]")
COLON = Suppress(":")
COMMENT = Suppress(pythonStyleComment)

#------------------------------------------------#
# Elements
#------------------------------------------------#
#The simplest elements that don't need forwarding
atom = (STRING | NAME | NUM)
comp_op = greater|lesser|greaterOrEqual|lesserOrEqual|equal|notequal|_is|_in|_not \
          | _not + _in | _is + _not
augassign = plusAssign | minusAssign | multAssign | divAssign


#Test node is a building block for many other elements
test = Forward()
testlist = test + ZeroOrMore(COMMA + test) + Optional(COMMA)
argument = test | (test + '=' + test)
arglist = delimitedList(argument)
subscript = (test | test + ":" + test)
subscriptlist = subscript + ZeroOrMore(COMMA + subscript) + Optional(COMMA)
trailer = (LPAREN + arglist + RPAREN |
           LBRACK + subscriptlist + RBRACK |
           Suppress('.') + NAME)

#Defining factor will allow us to define expr -- another useful building block
factor = Forward()
power = atom + ZeroOrMore(trailer) + Optional('**' + factor)
factor << (plus | minus | tilde) + (factor | power)
term = factor + ZeroOrMore((mult | div | mod | divFloor) + factor)
arith_expr = term + ZeroOrMore((plus | minus) term)
shift_expr = arith_expr + ZeroOrMore((shiftLeft | shiftRight) + arith_expr)
and_expr = shift_expr + ZeroOrMore(bitwiseAnd + shift_expr)
xor_expr = and_expr + ZeroOrMore(complement + and_expr)
expr = xor_expr + ZeroOrMore(bitwiseOr + xor_expr)
