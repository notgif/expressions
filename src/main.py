import re
from typing import NamedTuple

expr = "Log((z^3 + 2*z^2 + 3)/((z-1)^2))"

class Token(NamedTuple):
    kind: str
    value: str
    line: int
    col: int

token_patterns = {
    'NUMBER': r'-?\d+(\.\d*)?',
    'TERM': r'[a-zA-Z]+[a-zA-Z0-9_]*',
    'OPERATOR': r'[\^*/%+\-]',
    'PARENTHESIS': r'[(){}\[\]]',
    'NEWLINE': r'\n',
    'SKIP': r'\s',
    'OTHER': r'.'
}

tokenizer_pat = '|'.join(r"(?P<{}>{})".format(key, token_patterns[key]) for key in token_patterns)

def tokenize_str(string, line=1):

    for tok in re.finditer(tokenizer_pat, string):
        kind = tok.lastgroup
        value = tok.group()
        col = tok.start()

        if kind == "NEWLINE":
            line += 1
            continue

        if kind == "SKIP":
            continue

        yield Token(kind, value, line, col)

if __name__ == "__main__":
    print('\n'.join(map(str, tokenize_str(expr))))