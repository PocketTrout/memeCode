import ply.lex as lex

mapStuffzToken = {
    'umadbro': 'IF',
    'tellme': 'OPEN_BRACE',
    'coolstorybro': 'CLOSE_BRACE',
    'notmad': 'ELSE',
    'is': 'AFFECTATION',
    'pwnz': 'GREATER_OP',
    'pwndby': 'LESSER_OP',
    'pwnzOE':'GREATER_OR_EQUALS_OP',
    'pwndbyOE':'LESSER_OR_EQUALS_OP',
    'notlikey':'NOT_EQUALS',
    'likey': 'EQUALS',
    'robz': 'SUB_OP',
    'rekts': 'DIV_OP',
    'rabbits': 'MUL_OP',
    'moar': 'ADD_OP',
    'poncedilate': 'INCR_OP',
    'eroderamazzotti': 'DECR_OP',
    'kthxbye': 'BREAK',
    'gif': 'FOR',
    'gifpos': 'FORPOS',
    'gifneg': 'FORNEG',
    'rammus': 'WHILE',
    'omgbbq': 'PRINT',
    'shithappens': 'PRINTERR',
    'roundedstuff': 'INT',
    'stuff': 'FLOAT',
    'binarystuff': 'BOOLEAN',
    'writtenstuff': 'STRING',
    'yeah': 'TRUE',
    'nope': 'FALSE',
}
mapStuffzJava = {
    'IF': 'if',
    'OPEN_BRACE': '{',
    'CLOSE_BRACE': '}',
    'ELSE': 'else',
    'AFFECTATION': '=',
    'GREATER_OP': '>',
    'LESSER_OP': '>',
    'EQUALS': '==',
    'SUB_OP': '-',
    'DIV_OP': '/',
    'MUL_OP': '*',
    'ADD_OP': '+',
    'INCR_OP': '++',
    'DECR_OP': '--',
    'BREAK': 'break',
    'FOR': 'for',
    'FORPOS': 'forpos',
    'FORNEG': 'forneg',
    'WHILE': 'while',
    'PRINT': 'print',
    'PRINTERR': 'err',
    'INT': 'int',
    'FLOAT': 'float',
    'BOOLEAN': 'boolean',
    'STRING': 'String',
}

tokens = (
             'NUMBER',
             'IDENTIFIER',
             'TEXT',
         ) + tuple(mapStuffzToken.values())

literals = '()-'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in mapStuffzToken:
        t.type = mapStuffzToken[t.value]
    return t

def t_TEXT(t):
    r'[+][^+]+[+]'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))