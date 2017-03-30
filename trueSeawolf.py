#Kenny Chen 109400714


import ply
import inspect
import numbers
from ply import lex
import ply.yacc

import sys


reserved = {
   'and' : 'AND',
   'or' : 'OR',
   'in' : 'IN', 
   'not' : 'NOT',
   'print' : 'PRINT',
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'return' : 'RETURN',

}

tokens = ['LPAR', 'RPAR', 'PLUS', 'MINUS', 'MULT',
          'DIV', "EQUALS", 'INT_CONST', 'NAME', 
          'LESS', 'GREATER', 'NEQUALS',
          'LESSEQ', 'GREATEREQ', 'EQUALITY',
          'EXP', 'FLOOR', 'MOD', 'DECIMAL',
          'STRING' , 'LBRACKET', 'RBRACKET',
          'COMMA', 'SEMICOLON', 'LBRACE', 'RBRACE'] + list(reserved.values())

def t_name_rule(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if(t.value in reserved):
        t.type = reserved.get(t.value,'ID')    # Check for reserved words
    else:
        t.type = 'NAME'
    return t
    

def t_error(t):
    t.lexer.skip(1)
 

#def t_ignore(t) = r'[ \t\n]'

t_ignore = ' \t\r\n'



t_COMMA = r','

t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_EQUALS = r'='

t_LESS = r'<'
t_GREATER = r'>'
t_NEQUALS = r'<>'
t_LESSEQ = r'<='
t_GREATEREQ = r'>='
t_EQUALITY = r'=='

t_EXP = r'\*\*'
t_FLOOR = r'//'
t_MOD = r'%'
t_SEMICOLON = r';'

t_INT_CONST = r'[0-9]+'
t_DECIMAL = r'[0-9]*\.[0-9]+'
t_NAME   = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_STRING = r'"[^"]*"'

lex.lex(debug = 0)

'''
if __name__ == "__main__":
    lex = lex.input("ccc(1);")
    while 1:
        tok = ply.lex.token()
        if not tok: break
        print(tok.type, tok.value, tok.lineno, tok.lexpos)
''' 

variables = [{}]
stack = []
def p_error(p):
    
    print("SYNTAX ERROR")
    
    

precedence = (
    ('left', 'IN'),
    ('left', 'COMMA'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'NEQUALS', 'EQUALITY'),
    ('left', 'LESS', 'GREATER', 'LESSEQ', 'GREATEREQ'),
    ('left','PLUS','MINUS'),
    ('left','MULT','DIV', 'MOD', 'FLOOR'),
    ('right', 'UMINUS'),
    ('left','EXP'),
    )




class Node:
    def __init__(self):

        pass
    def evaluate(self):
        
        return 696969
    def execute(self):
        return ""

class binNode(Node):
    
    def __init__(self, a, op, b):
        self.a = a
        self.value = op        
        self.b = b
        
    def evaluate(self):
        return self.execute()
    def execute(self):
        if(self.a == 'not'): 
            if(not self.value): return 1
            else:       return 0
        x = self.a.evaluate()
        while(isinstance(x, (exprNode, functionCallNode))):
            x = x.execute()
        y = self.b.evaluate()
        while(isinstance(y, (exprNode, functionCallNode))):
            y = y.execute()

        
        
        if(self.value == '+'): return (x + y)
        elif(self.value == '-' ): return (x - y)
        elif(self.value == '*' ): return (x * y)
        elif(self.value == '/' ): return (x / y)
        elif(self.value == '<' ):
            if(x < y):  return 1
            else:       return 0
        elif(self.value == '>' ):
            if(x > y):  return 1
            else:       return 0
        elif(self.value == '<>'):
            if(x != y): return 1
            else:       return 0
        elif(self.value == '<='):
            if(x <= y): return 1
            else:       return 0
        elif(self.value == '>='):
            if(x >= y): return 1
            else:       return 0
        elif(self.value == '=='):
            if(x == y): return 1
            else:       return 0
        elif(self.value == '**'): return (x ** y)
        elif(self.value == '//'): return (x // y)
        elif(self.value == '%'): return (x % y)
        elif(self.value == 'and'): 
            if(x and y): return 1
            else:       return 0
        elif(self.value == 'or'): 
            if(x or y): return 1
            else:       return 0
        elif(self.value == 'in' ):
            if(x in y): return 1
            else: return 0



class PrintNode(Node):
    def __init__(self, v):
        self.value = v
    def getValue():
        return self.value
    def evaluate(self):
        return self.value
    def execute(self):
        if(isinstance(self.value, lookupNode)):
            print(self.evaluate().execute())
        elif(isinstance(self.value, functionCallNode)):
            print(self.value.execute())
        else:
            if(isinstance(self.value, binNode)):
                print(self.evaluate().execute())
            else:
                print(self.evaluate().value)  #expession
            
                
class exprNode(Node):
    def __init__(self, v):
        self.value = v
    def evaluate(self):
        try:
            return variables[-1][self.value].execute()
        except:
            return self.value
    def execute(self):
        pass

class IfNode(Node):
    def __init__(self, c, t, e):
        self.condition = c
        self.thenBlock = t
        self.elseBlock = e
    def evaluate(self):
        return self.execute()
    def execute(self):
        if(self.condition.evaluate()):
            if(isinstance(self.thenBlock, returnNode)):
                return self.thenBlock.execute()
            
            if("return" in inspect.stack()[1][4][0]):
                return self.thenBlock.execute()
            self.thenBlock.execute()
            
        else:
            zzz = inspect.stack()[1][4][0]
            if(isinstance(self.elseBlock, Node)):
                self.elseBlock.execute()
            if(isinstance(self.elseBlock, returnNode)):# or "return statement.execute()" in zzz):
                return self.elseBlock.execute()
            if("return" in inspect.stack()[1][4][0]):
                return self.elseBlock.execute()
            self.elseBlock.execute()

     
class BlockNode(Node):
    def __init__(self, sl):
        self.statementNodes = sl        

    def evaluate(self):
        return self.execute()
            
            
    def execute(self):

        a = self.statementNodes
        while(isinstance(a[-1], list)):
            if(len(a[-1]) > 1):
                b = a.pop()
                a.append(b[0])
                b.pop(0)
                b = b[0]
                a.append(b)
            else:
                b = a.pop()
                a.append(b[0])
        poop = []
        for statement in self.statementNodes:
            if(isinstance(statement, returnNode)):
                return statement.execute()
            if(isinstance(statement, IfNode)):
                if("x = functions[self.name].execute()" in inspect.stack()[1][4][0]):
                    return statement.execute()
                    
            poop.append(statement)
            statement.execute()
            #print(poop)

class assignNode(Node):
    global variables
    def __init__(self, v, n):
        self.name = n
        self.value = v        
    def evaluate(self):
        variables[-1][self.value] = self.name
    def execute(self):
        if(isinstance(self.name, functionCallNode)):
            variables[-1][self.value] = self.name.execute()
        else:
            try:           
                variables[-1][self.value] = self.name.evaluate().evaluate()
            except:            
                variables[-1][self.value] = self.name.value
        

class lookupNode(Node):
    global variables
    def __init__(self, v):
        self.value = v
    def getName(self):
        return self.value
    def evaluate(self):        
        try:
            return (variables[-1][self.value])
        except:
            
            return variables[0][self.value]
    def execute(self):
        try:
            return variables[-1][self.value]
        except:
            return variables[0][self.value]

        
class whileNode(Node):
    def __init__(self, c, t):
        self.condition = c
        self.thenBlock = t
    def evaluate(self):
        return 0
    def execute(self):
        while(self.condition.evaluate()):
            self.thenBlock.execute()

def p_statement_line(p):
    ''' lol : block'''
    p[0] = BlockNode(p[1])

def p_while_statement(p):
    ''' statement : WHILE LPAR expression RPAR statement'''

    p[0] = whileNode(p[3], p[5])
    
    


def p_if_statement(p):
    ''' statement : IF LPAR expression RPAR statement
                  | IF LPAR expression RPAR statement ELSE statement'''
    if(len(p) == 6):
        p[0] = IfNode(p[3], p[5], Node())
    else:
        p[0] = IfNode(p[3], p[5], p[7])



functions = {}
functionsVars = {}


class functionNode(Node):
    def __init__(self, name, block, args):
        self.name = name
        self.node = block
        self.vars = args
    def evaluate(self):
        return 0
    def execute(self):
        a = self.vars
        c = []
        
        while(isinstance(a[-1], list)):                        
            c.append(a[0])
            a = a[-1]
        c.append(a[0])
        
        self.vars = c

        test = [x.getName() for x in self.vars]

        functionsVars[self.name] = test      
        functions[self.name] = self.node

    
def p_func(p):
    ''' statement : NAME LPAR arguments RPAR LBRACE block RBRACE'''
    
    p[0] = functionNode(p[1], BlockNode(p[6]), p[3])
def p_parem(p):
    ''' arguments : expression COMMA arguments
                  | expression'''
    p[0] = []
    for i in p[1:]:
        p[0].append(i)

class returnNode(Node):
    def __init__(self, name):
        self.name = name
    def evaluate(self):
        print("as")
        return self.name.evaluate()
    def execute(self):
        #print(self.name, "asdd")
        return self.name.evaluate()

def p_return(p):
    ''' statement : RETURN expression SEMICOLON
                  | RETURN statement SEMICOLON
                  | RETURN NAME LPAR arguments RPAR SEMICOLON'''

    if len(p) == 7:
        p[0] = returnNode(functionCallNode(p[2], p[4]))
    else:
        p[0] = returnNode(p[2])
    

def p_was(p):
    ''' expression : NAME LPAR arguments RPAR'''
    p[0] = exprNode(functionCallNode(p[1], p[3]))
    

varStack = []

class functionCallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        
    def value(self):
        return "22222"
    def evaluate(self):
        return self.execute()
        pass
    def execute(self):
        
        a = self.args
        expr = []
        
        while(isinstance(a[-1], list)):                        
            expr.append(a[0])
            a = a[-1]
        expr.append(a[0].evaluate())

        for i in range(len(expr)):
            while(isinstance(expr[i], (exprNode, lookupNode))):
                expr[i] = expr[i].evaluate()
        diction = {}
        for i in range(len(expr)):
            diction[functionsVars[self.name][i]] = expr[i]
        
        variables.append(diction)
        #print(variables);
        
        x = functions[self.name].execute()

        variables.pop()
        return x



def p_function_call(p):
    ''' statement : NAME LPAR arguments RPAR SEMICOLON '''
    p[0] = functionCallNode(p[1], p[3])

    

        
def p_statement_block(p):
    ''' statement : LBRACE block RBRACE
                  | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = BlockNode(p[2])
    else:
        p[0] = Node()



def p_block(p):
    ''' block : statement block
              | statement'''
    p[0] = []
    for i in p[1:]:
        p[0].append(i)



def p_statement_assign(p):
    '''statement : NAME EQUALS expression SEMICOLON
                 | NAME EQUALS NAME LPAR arguments RPAR SEMICOLON
                 | NAME indices EQUALS expression SEMICOLON'''
    if(len(p) ==  5):
        p[0] = assignNode(p[1], exprNode(p[3]))
    elif(len(p) ==  8):
        p[0] = assignNode(p[1], functionCallNode(p[3], p[5]))
    else:
        p[0] = listerNode(p[1], p[2], p[4])


def p_indices_list(p):
    '''indices : LBRACKET expression RBRACKET indices
               | LBRACKET expression RBRACKET'''
    p[0] = []
    for i in p[2:]:
        p[0].append(i)
    

def p_print_expr(p):
    '''statement : PRINT LPAR expression RPAR SEMICOLON
                 | PRINT LPAR RPAR SEMICOLON
                 | PRINT LPAR NAME LPAR arguments RPAR RPAR SEMICOLON'''
    if(len(p) == 9):
        p[0] = PrintNode(functionCallNode(p[3], p[5]))
    else:
        p[0] = PrintNode(p[3])

class listerNode(Node):
    def __init__(self, l, x, i):
        self.list = l;
        self.index = x
        self.value = i
    def evaluate(self):
        return 0
    def execute(self):
        a = self.index
        while(isinstance(a[-1], list)):
            if(len(a[-1]) > 1):
                b = a.pop()
                a.append(b[0])
                b.pop(0)
                b = b[0]
                a.append(b)
            else:
                b = a.pop()
                a.append(b[0])
        a = [x for x in a if x != ']']

        
        b = variables[-1][self.list]

        if(len(a) == 1):
            b[int(a[0].evaluate())] = self.value.evaluate()
        if(len(a) == 2):
            b[int(a[0].evaluate())][int(a[1].evaluate())] = self.value.evaluate()
        if(len(a) == 3):
            b[int(a[0].evaluate())][int(a[1].evaluate())][int(a[2].evaluate())] = self.value.evaluate()
        if(len(a) == 4):
            b[int(a[0].evaluate())][int(a[1].evaluate())][int(a[3].evaluate())][int(a[4].evaluate())] = self.value.evaluate()

        pass    


def p_expr_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = exprNode(-p[2].evaluate())



def p_expression_binary_operators(p):
    '''       expression : expression PLUS expression
            | expression MINUS expression
            | expression MULT expression
            | expression DIV expression
            | expression LESS expression
            | expression GREATER expression
            | expression NEQUALS expression
            | expression LESSEQ expression
            | expression GREATEREQ expression
            | expression EQUALITY expression
            | expression EXP expression
            | expression FLOOR expression
            | expression MOD expression
            | expression AND expression
            | expression OR expression
            | expression IN expression
            '''

    p[0] = binNode(p[1], p[2], p[3])


def p_expression_unary_operators(p):
    '''expression : NOT expression'''
    p[0] = binNode(p[1], p[2], Node())


def p_expression_string_sub(p):
    '''expression : STRING LBRACKET INT_CONST RBRACKET '''
    p[0] = p[1][int(p[3])+1]

###### lists might not work poperly in the right order 
def p_expression_list_empty(p):
    '''expression : LBRACKET RBRACKET '''
    p[0] = exprNode([])

def p_expression_list(p):
    '''expression : LBRACKET list RBRACKET '''
    p[0] = exprNode(p[2])


def p_type_list_1(p):
    '''list : expression'''
    p[0] = [p[1].evaluate()]

def p_type_list_2(p):
    '''list : list COMMA expression'''
    p[0] = (p[1] + [p[3].evaluate()])

def p_list_sublist(p):
    '''expression : expression LBRACKET expression RBRACKET'''
    p[0] = listNode(p[1], p[3])

class listNode(Node):
    def __init__(self, c, t):
        self.value = c
        self.index = t
    def evaluate(self):
        return self.value.evaluate()[int(self.index.evaluate())]
    def execute(self):
        return 0
    
def p_expression_integer(p):
    'expression : INT_CONST'
    p[0] = exprNode(int(p[1]))

def p_expression_real(p):
    'expression : DECIMAL'
    p[0] = exprNode(float(p[1]))

def p_expression_string(p):
    'expression : STRING'
    p[0] = exprNode(p[1][1:-1])


def p_expression_group(p):
    'expression : LPAR expression RPAR'
    p[0] = p[2]


def p_expression_name_lookup(p):
    'expression : NAME'
    p[0] = lookupNode(p[1])
    
    
parser = ply.yacc.yacc()


if(len(sys.argv) > 1):
    lines = open(sys.argv[1]).read()
else:
    lines = open("input5.txt").read()

parser.parse(lines).execute()

