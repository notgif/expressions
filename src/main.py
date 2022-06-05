from typing import NamedTuple, NewType

import math
import operator as op

from tokenizer import *

class Number(NamedTuple):
    value: any
    symbol: str

class Paren(NamedTuple):
    symbol: str

class Operator(NamedTuple):
    symbol: str
    prec: int
    assc: str
    function: callable

class Function(NamedTuple):
    symbol: str
    args: int
    function: callable

class Symbol(NamedTuple):
    symbol: str
    value: any

def pow_op(a: Number, b: Number):
    return Number(a.value ** b.value, f"({a.symbol} ^ {b.symbol})")

def mul_op(a: Number, b: Number):
    return Number(a.value * b.value, f"({a.symbol} * {b.symbol})")

def div_op(a: Number, b: Number):
    return Number(a.value / float(b.value), f"({a.symbol} / {b.symbol})")

def add_op(a: Number, b: Number):
    return Number(a.value + b.value, f"({a.symbol} + {b.symbol})")

def sub_op(a: Number, b: Number):
    return Number(a.value - b.value, f"({a.symbol} - {b.symbol})")

def log_fn(a: Number):
    return Number( math.log(a.value), f"Log({a.symbol})" )

ops = {
    "^": Operator("^", 4, "Right", pow_op),
    "*": Operator("*", 3, "Left", mul_op),
    "/": Operator("/", 3, "Left", div_op),
    "+": Operator("+", 2, "Left", add_op),
    "-": Operator("-", 2, "Left", sub_op)
}

functions = {
    "Log": Function("Log", 1, log_fn)
}

names = {}

def parse(tokens):

    global names

    output = []
    stack = []

    for tok in tokens:
        match tok:
            case Token(kind="NUMBER"):
                output.append(Number(int(tok.value), tok.value))

            case Token(kind="PARENTHESIS", value="("):
                stack.append(Paren(tok.value))

            case Token(kind="PARENTHESIS", value=")"):
                while stack[-1].symbol != "(":
                    output.append(stack.pop())

                assert(stack[-1].symbol == "(")
                stack.pop()

            case Token(kind="OPERATOR"):
                op = ops[tok.value]

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
                    stack.append(functions[tok.value])

                elif tok.value in names:
                    output.append(names[tok.value])

                else:
                    string = f"{tok.value} := "
                    names[tok.value] = Symbol(tok.value, lambda: int(input(string)))
                    output.append(names[tok.value])

    while len(stack) > 0:
        assert(stack[-1].symbol != "(")
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
                    local_names[sym.symbol] = Symbol(sym.symbol, sym.value())
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
