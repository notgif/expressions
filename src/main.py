from tokenizer import *

input_str = "Log((z^3 + 2*z^2 + 3)/((z-1)^2))"

tokens = tokenize_str(input_str)

names = {
    "z": 10
}

def parse(tokens):

    for tok in tokens:
        pass
