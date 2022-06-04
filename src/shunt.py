input_str = "1+2^2*3^2"
output = "(1 ((2 2 ^) (3 2 ^) *) +)"

ops = {
    "^": (4, "Right"),
    "*": (3, "Left"),
    "/": (3, "Left"),
    "+": (2, "Left"),
    "-": (2, "Left")
}

prec = lambda op: ops[op][0]
assc = lambda op: ops[op][1]

def parse_str(string):
    out_queue = []
    op_stack = []

    for tok in string:
        if tok.isdigit():
            out_queue.append(tok)

        elif tok == "(":
            op_stack.append(tok)

        elif tok == ")":
            while op_stack[-1] != "(":
                out_queue.append(op_stack.pop())

            assert( op_stack[-1] == "(")
            op_stack.pop()

        elif tok in ops:
            if len(op_stack) == 0:
                op_stack.append(tok)
                continue

            while (op_stack[-1] != "(" ) and (prec(op_stack[-1]) > prec(tok)
                or ( prec(op_stack[-1]) == prec(tok) and assc(tok) == "Left" )):

                out_queue.append(op_stack.pop())

            op_stack.append(tok)

    while len(op_stack) > 0:
        assert(op_stack[-1] != "(")
        out_queue.append(op_stack.pop())


    return out_queue

out = parse_str(input_str)
print(out)

# funcs = {
#     "^": lambda x, y: x**y,
#     "*": lambda x, y: x*y,
#     "/": lambda x, y: x/y,
#     "+": lambda x, y: x+y,
#     "-": lambda x, y: x-y
# }
#
# stack = []
# for tok in out:
#     if tok in funcs:
#         x = stack.pop()
#         y = stack.pop()
#         res = funcs[tok](x, y)
#         stack.append(res)
#
#     else:
#         stack.append(int(tok))
#
#     print(stack)