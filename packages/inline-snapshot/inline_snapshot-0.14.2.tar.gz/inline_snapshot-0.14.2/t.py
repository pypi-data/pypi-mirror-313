
import ast
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO

def t(s):
    g = tokenize(BytesIO(s.encode('utf-8')).readline) 

    for e in g:
        print(e)

    #ast.literal_eval(s)


t("''")
print()
t("f'{a}'")
