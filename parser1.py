import ply.yacc as yacc
from lex1 import tokens
import AST
from lex1 import mapStuffzToken as mapStuffzToken
import re

TODO = 'lol'

def p_program(p):
    """ program : statement
        | statement program """
    try:
        p[0] = AST.ProgramNode([p[1]]+p[2].children)
    except:
        p[0] = AST.ProgramNode(p[1])

def p_expression(p):
    """ expression : expression_num
        | expression_sign
        | expression_op
        | expression_incr """
    p[0] = p[1]

textPattern = re.compile(r'[+][^+]+[+]')

def p_statement(p):
    """ statement : expression '-'
        | assignation '-'
        | structure
        | initialization '-'
        | PRINT TEXT '-'
        | PRINT IDENTIFIER '-'
        | PRINTERR TEXT '-'
        | PRINTERR IDENTIFIER '-'
        | BREAK '-'
        """
    if mapStuffzToken.get(p[1]) == 'PRINT':
        if textPattern.match(p[2]) is not None:
            p[2] = str(p[2])[1:-1]
            p[0] = AST.PrintNode([AST.TokenNode(p[2])])
            p[0].type = 'print-text'
        else:
            p[0] = AST.PrintNode([AST.TokenNode(p[2])])
            p[0].type = 'print-identifier'
    elif mapStuffzToken.get(p[1]) == 'PRINTERR':
        if textPattern.match(p[2]) is not None:
            p[2] = str(p[2])[1:-1]
            p[0] = AST.PrintErrNode([AST.TokenNode(p[2])])
            p[0].type = 'printerr-text'
        else:
            p[0] = AST.PrintErrNode([AST.TokenNode(p[2])])
            p[0].type = 'printerr-identifier'
    elif mapStuffzToken.get(p[1]) == 'BREAK':
        p[0] = AST.BreakNode()
    else:
        p[0] = p[1]

def p_bloc(p):
    """ bloc : OPEN_BRACE program CLOSE_BRACE """
    p[0] = p[2]

def p_structure(p):
    """ structure : whileloop bloc
        | forloop bloc
        | if bloc
        | if bloc ELSE bloc"""
    try:
        # if - else
        p[0] = AST.StructNode([p[1], p[2], p[4]])
    except:
        # if, for or while
        p[0] = AST.StructNode([p[1], p[2]])

def p_for(p):
    """ forloop : FOR '(' initialization '-' comparison '-' expression ')'
        | FORNEG '(' initialization '-' NUMBER ')'
        | FORNEG '(' initialization '-' IDENTIFIER ')'
        | FORPOS '(' initialization '-' NUMBER ')'
        | FORPOS '(' initialization '-' IDENTIFIER ')' """
    try:
        p[0] = AST.ForNode([p[3], p[5],p[7]])
    except:
        #untested
        p[0] = AST.ForNode([p[3],AST.TokenNode(p[5])])
        if mapStuffzToken.get(p[1]) == 'FORNEG':
            p[0].type = 'forneg'
        else:
            p[0].type = 'forpos'

def p_while(p):
    """ whileloop : WHILE '(' comparison ')' """
    p[0] = AST.WhileNode([p[3]])

def p_if(p):
    """ if : IF '(' comparison ')' """
    p[0] = AST.IfNode([p[3]])

def p_comparison_operator(p):
    """ comparison_operator : GREATER_OP
        | LESSER_OP
        | EQUALS
        | GREATER_OR_EQUALS_OP
        | LESSER_OR_EQUALS_OP
        | NOT_EQUALS"""
    p[0] = mapStuffzToken.get(p[1])

def p_comparison(p):
    """ comparison : expression comparison_operator expression """
    p[0] = AST.ComparisonNode([p[1], AST.ComparisonTokenNode(p[2]), p[3]])

def p_initialization(p):
    """ initialization : initialization_num
        | initialization_string
        | initialization_bool
    """
    p[0] = p[1]

def p_initialization_num(p):
    """ initialization_num : FLOAT IDENTIFIER AFFECTATION NUMBER
        | FLOAT IDENTIFIER AFFECTATION IDENTIFIER
        | INT IDENTIFIER AFFECTATION NUMBER
        | INT IDENTIFIER AFFECTATION IDENTIFIER """
    p[0] = AST.InitNode([AST.TypeNode(mapStuffzToken.get(p[1])), AST.TokenNode(p[2]), AST.TokenNode(p[4])])

def p_initialization_string(p):
    """ initialization_string : STRING IDENTIFIER AFFECTATION TEXT """
    p[4] = str(p[4])[1:-1]
    p[0] = AST.InitNode([AST.TypeNode(mapStuffzToken.get(p[1])), AST.TokenNode(p[2]), AST.TokenNode(p[4])])

def p_initialization_bool(p):
    """ initialization_bool : BOOLEAN IDENTIFIER AFFECTATION TRUE
        | BOOLEAN IDENTIFIER AFFECTATION FALSE
        | BOOLEAN IDENTIFIER AFFECTATION IDENTIFIER """
    p[0] = AST.InitNode([AST.TypeNode(mapStuffzToken.get(p[1])), AST.TokenNode(p[2]), AST.TokenNode(p[4])])

def p_assignation(p):
    """ assignation : IDENTIFIER AFFECTATION expression """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_expression_num(p):
    """expression_num : NUMBER
        | IDENTIFIER """
    p[0] = AST.TokenNode(p[1])

def p_expression_sign(p):
    """expression_sign : ADD_OP expression %prec UMINUS
        | SUB_OP expression %prec UMINUS"""
    p[0] = AST.OpNode(p[1],[p[2]])

def p_expression_op(p):
    """expression_op : expression ADD_OP expression
        | expression SUB_OP expression
        | expression MUL_OP expression
        | expression DIV_OP expression"""
    p[0] = AST.OpNode(mapStuffzToken.get(p[2]),[p[1],p[3]])

def p_expression_incr(p):
    """ expression_incr : INCR_OP IDENTIFIER
        | DECR_OP IDENTIFIER """
    p[0] = AST.IncrNode([AST.TokenNode(mapStuffzToken.get(p[1])), AST.TokenNode(p[2])])

def p_error(p):
    print("Synthax error in line %d" % p.lineno)
    yacc.errok()

def p_parenthesis(p):
    """ expression : '(' expression ')' """
    p[0] = p[2]

precedence=(
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('left', 'DIV_OP'),
    ('left', 'SUB_OP'),
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