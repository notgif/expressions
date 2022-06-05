from typing import NamedTuple, NewType

import math
import operator as op

from tokenizer import *
from exceptions import *

class Number(NamedTuple):
    value: any
    symbol: str
    token: Token

class Paren(NamedTuple):
    symbol: str
    token: Token

class Operator(NamedTuple):
    symbol: str
    prec: int
    assc: str
    function: callable
    token: Token

class Function(NamedTuple):
    symbol: str
    args: int
    function: callable
    token: Token

class Symbol(NamedTuple):
    symbol: str
    value: any
    token: Token

def pow_op(a: Number, b: Number):
    return Number(a.value ** b.value, f"({a.symbol} ^ {b.symbol})", None)

def mul_op(a: Number, b: Number):
    return Number(a.value * b.value, f"({a.symbol} * {b.symbol})", None)

def div_op(a: Number, b: Number):
    return Number(a.value / float(b.value), f"({a.symbol} / {b.symbol})", None)

def add_op(a: Number, b: Number):
    return Number(a.value + b.value, f"({a.symbol} + {b.symbol})", None)

def sub_op(a: Number, b: Number):
    return Number(a.value - b.value, f"({a.symbol} - {b.symbol})", None)

def log_fn(a: Number):
    return Number( math.log(a.value), f"Log({a.symbol})", None)

# Thunks for creating operator symbols with a token
ops = {
    "^": lambda tok: Operator("^", 4, "Right", pow_op, tok),
    "*": lambda tok: Operator("*", 3, "Left", mul_op, tok),
    "/": lambda tok: Operator("/", 3, "Left", div_op, tok),
    "+": lambda tok: Operator("+", 2, "Left", add_op, tok),
    "-": lambda tok: Operator("-", 2, "Left", sub_op, tok)
}

functions = {
    "Log": lambda tok: Function("Log", 1, log_fn, tok)
}

names = {}

def parse(tokens):

    global names

    output = []
    stack = []

    for tok in tokens:
#         raise(TokenError("errr", tok))

        match tok:
            case Token(kind="NUMBER"):
                output.append(Number(int(tok.value), tok.value, tok))

            case Token(kind="PARENTHESIS", value="("):
                stack.append(Paren(tok.value, tok))

            case Token(kind="PARENTHESIS", value=")"):
                while stack[-1].symbol != "(":
                    output.append(stack.pop())

                if not stack[-1].symbol == "(":
                    raise TokenError("Mismatched Parenthesis", tok)

                stack.pop()

            case Token(kind="OPERATOR"):
                op = ops[tok.value](tok)

                if len(stack) == 0:
                    stack.append(op)

                else:
                    while ( (stack[-1].symbol != "(")
                            and ((stack[-1].prec) > op.prec
                                or (stack[-1].prec == op.prec
                                    and op.assc == "Left" ))):
                        output.append(stack.pop())

                    stack.append(op)

            case Token(kind="TERM"):
                if tok.value in functions:
                    stack.append(functions[tok.value](tok))

                elif tok.value in names:
                    output.append(names[tok.value])

                else:
                    string = f"{tok.value} := "
                    print(string)
                    names[tok.value] = Symbol(tok.value, lambda: (breakpoint(), int(input(string))), tok)
                    output.append(names[tok.value])

    while len(stack) > 0:
        if not stack[-1].symbol != "(":
            raise TokenError("Mismatched Parenthesis", stack[-1].token)

        output.append(stack.pop())

    return output

def evaluate_expr(parsed_expr):

    local_names = {}
    stack = []

    for sym in parsed_expr:
        match sym:
            case Number():
                stack.append(sym)

            case Symbol():
                if sym.symbol in local_names:
                    stack.append(local_names[sym.symbol])

                else:
                    local_names[sym.symbol] = Symbol(sym.symbol, sym.value(), sym.token)
                    stack.append(local_names[sym.symbol])

            case Operator():
                b = stack.pop()
                a = stack.pop()
                res = sym.function(a, b)
                #print(f"OP: {a} {b}, {res.symbol} = {res.value}")
                stack.append(res)

            case Function():
                a = stack.pop()
                res = sym.function(a)
                #print(f"FN: {res.symbol} = {res.value}")
                stack.append(res)

    print(f"Result: {stack[-1].symbol} = {stack[-1].value}")

if __name__ == "__main__":
    input_str = "Log((z^3 + 2*z^2 + 3)/((z - 1)^2))"
    print(f"Expression: {input_str}")
    tokens = tokenize_str(input_str)
    rpn_expr = parse(tokens)

    while True:
        evaluate_expr(rpn_expr)
