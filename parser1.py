import ply.yacc as yacc
from lex1 import tokens
import AST

def p_program(p):
    ''' program : statement
        | statement ';' program '''
    try:
        p[0] = AST.ProgramNode([p[1]]+p[3].children)
    except:
        p[0] = AST.ProgramNode(p[1])

def p_statement(p):
    ''' statement : expression
        | assignation
        | structure
        | PRINT expression '''
    try:
        p[0] = AST.PrintNode(p[2])
    except:
        p[0] = p[1]

def p_structure(p):
    ''' structure : WHILE expression '{' program '}' '''
    p[0] = AST.WhileNode([p[2],p[4]])

def p_assignation(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])


def p_expression_num(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

operation = {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: x/y,
}

def p_expression_sign(p):
    '''expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1],[p[2]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
        | expression MULT_OP expression'''
    p[0] = AST.OpNode(p[2],[p[1],p[3]])

def p_error(p):
    print("Synthax error in line %d" % p.lineno)
    yacc.errok()

def p_parenthesis(p):
    ''' expression : '(' expression ')' '''
    p[0] = p[2]

precedence=(
    ('left', 'ADD_OP'),
    ('left', 'MULT_OP'),
    ('right', 'UMINUS'),
)
yacc.yacc(outputdir='generated')

def parse(program):
    return yacc.parse(program)

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = parse(prog)
    print(result)
    import os
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print ("wrote ast to %s"%name)