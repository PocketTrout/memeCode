from parser1 import parse
from parser1 import makeTree
import AST
from AST import addToClass
from lex1 import mapStuffzJava as map

endLineSemiColon = ';\n'
endLine = '\n'
noSemiColon = "struct"
@addToClass(AST.ProgramNode)
def compile(self, file):
    for node in self.children:
        node.compile(file)
        if node.type not in noSemiColon:
            file.write(endLineSemiColon)
        else:
            file.write(endLine)
    return file

@addToClass(AST.TokenNode)
def compile(self, file):
    file.write(str(self.tok))
    return file

@addToClass(AST.OpNode)
def compile(self, file):
    if self.nbargs == 1:
        file.write(map.get(self.op))
        self.children[0].compile(file)
    else:
        self.children[0].compile(file)
        file.write(map.get(self.op))
        self.children[1].compile(file)
    return file

@addToClass(AST.AssignNode)
def compile(self, file):
    self.children[0].compile(file)
    file.write(map.get("AFFECTATION"))
    self.children[1].compile(file)
    return file

def compilePrint(node, file):
    if 'text' in node.type:
        file.write("\"")
    node.children[0].compile(file)
    if 'text' in node.type:
        file.write("\"")
    file.write(")")
    return file

@addToClass(AST.PrintNode)
def compile(self, file):
    file.write("System.out.println(")
    compilePrint(self,file)
    return file

@addToClass(AST.PrintErrNode)
def compile(self, file):
    file.write("System.err.println(")
    compilePrint(self, file)
    return file

@addToClass(AST.WhileNode)
def compile(self, file):
    file.write(map.get('WHILE')+'(')
    self.children[0].compile(file)
    file.write(')')
    return file

@addToClass(AST.EntryNode)
def compile(self, file):
    pass

@addToClass(AST.StructNode)
def compile(self, file):
    self.children[0].compile(file)
    file.write(endLine + '{'+endLine)
    self.children[1].compile(file)
    file.write(endLine + '}'+ endLine)
    if len(self.children) == 3:
        file.write(map.get("ELSE")+endLine + '{' + endLine)
        self.children[2].compile(file)
        file.write(endLine + '}'+ endLine)
    return file


@addToClass(AST.ForNode)
def compile(self, file):
    file.write(map.get('FOR')+'(')
    if self.type == 'for':
        pass
    self.children[0].compile(file)
    file.write(';')
    self.children[1].compile(file)
    file.write(';')
    self.children[2].compile(file)

    file.write(')')
    return file

@addToClass(AST.IfNode)
def compile(self, file):
    file.write(map.get('IF')+'(')
    self.children[0].compile(file)
    file.write(')')
    return file


@addToClass(AST.ComparisonNode)
def compile(self, file):
    self.children[0].compile(file)
    self.children[1].compile(file)
    self.children[2].compile(file)
    return file

@addToClass(AST.ComparisonTokenNode)
def compile(self, file):
    file.write(map.get(str(self.tok)))
    return file

@addToClass(AST.TypeNode)
def compile(self, file):
    file.write(map.get(self.tok))
    return file

@addToClass(AST.InitNode)
def compile(self, file):
    self.children[0].compile(file)
    file.write(" ")
    self.children[1].compile(file)
    file.write(" " + map.get("AFFECTATION") + " ")
    self.children[2].compile(file)
    return file

@addToClass(AST.IncrNode)
def compile(self, file):
    op = map.get(self.children[0].tok)
    self.children[1].compile(file)
    file.write(op)
    return file

@addToClass(AST.BreakNode)
def compile(self, file):
    file.write(map.get('BREAK'))
    return file

def runCommand(strCommand):
    from subprocess import Popen, PIPE
    pipe = Popen(strCommand, shell=True, stdout=PIPE, stderr=PIPE)
    while True:
        line = pipe.stdout.readline()
        if line:
            sys.stdout.buffer.write(line)
        else:
            break

def compile(argv, result):
    name = argv[1][:argv[1].rfind('.')]
    nameCamelCase = name[0].upper() + name[1:].lower()
    with open(nameCamelCase+".java", 'w+') as file:
        file.write("public class "+ nameCamelCase + '{\n')
        file.write("public static void main(String[] args){\n")
        result.compile(file)
        file.write("}}")
    if "--compile" in argv or "--run" in argv:
        runCommand("javac " + nameCamelCase + ".java")
        if "--run" in argv:
            runCommand("java " + nameCamelCase)

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = parse(prog)
    print(result)
    makeTree(sys.argv[1],result)
    compile(sys.argv, result)