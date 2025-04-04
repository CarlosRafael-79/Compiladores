import ply.yacc as yacc
import ply.lex as lex

class Analyzer:
    tokens = []
    position = 0
    position_instruction = -1
    posicaoMetodo = -1
    escopos = [{}]
    instructions = []
    infoMetodo = ['', -1]
    
    def get_type(self):
        return self.tokens[Analyzer.position].type

    def get_value(self):
        return self.tokens[Analyzer.position].value
    
    def get_for_value_type(self,value_type):
        if value_type == 0:
            return Analyzer.get_type
        else:
            return Analyzer.get_value
    
    def addInstrucao(self,instrucao, valor = ''):
        self.instrucoes.append([instrucao,valor])
        self.posicaoInstrucao += 1
        if instrucao == 'PARA':
            self.posicaoMetodo = self.posicaoInstrucao+1

    def add_instruction(self,instruction, value = ''):       
        if instruction == value or value == '':
            self.instructions.append([instruction,value])
            self.position_instruction += 1
            return True
        return False
        #if instrucao == 'PARA':
        #    self.posicaoMetodo = self.posicaoInstrucao+1
        
    def get_comparisons(self,instructions = [], value_type = []):
        for i, instruction in enumerate(instructions):
            if instruction != Analyzer.get_for_value_type(value_type[i]):
                self.position_instruction += 1
                return False
            self.position_instruction += 1
        return True
'''
    def isDeclared(self, variavel):
        for escopo in self.escopos:
            for chave in escopo.keys():
                if chave == variavel:
                    return True
        return False
    
    def declare(self, variavel):
        self.escopos[-1][variavel] = ''

    def exitEscopo(self):
        self.escopos.pop()

    def addEscopo(self):
        self.escopos.append({})
'''

    




var_map = {}
# Mapeamento de palavras reservadas, símbolos e operadores para tokens
token_map = {
    
    'public': 'Public', 'main': 'Main', 'static': 'Static', 'class': 'Class', 'void': 'Void',
    'if': 'If', 'else': 'Else', 'while': 'While', 'return': 'Return',  'double': 'Double',
    'String': 'String', 'lerDouble': 'LerDouble', 'args': 'Args'  
}

tokens = [
    'Id', 'Number', 'Print', 'Mult', 'Relational',
    'LeftParenthesis', 'RightParenthesis', 'LeftBracket', 'RightBracket',
    'LeftKey', 'RightKey', 'Comma', 'Semicolon', 'Assignment', 'Sub', 'Add'
] + list(token_map.values())


# Definição de tokens para símbolos individuais
t_LeftParenthesis = r'\('
t_RightParenthesis = r'\)'
t_LeftBracket = r'\['
t_RightBracket = r'\]'
t_LeftKey = r'\{'
t_RightKey = r'\}'
t_Comma = r','
t_Semicolon = r';'
t_Assignment = r'='
t_Sub = r'-'
t_Add = r'\+'

# Expressões regulares para tokens simples
t_Mult = r'[\*/]'
t_ignore = ' \t\r\f'

# Token para números (inteiros e decimais)
def t_Number(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Operadores relacionais
def t_Relational(t):
    r'==|!=|<=|>=|<|>'
    return t

# System.out.println
def t_Print(t):
    r'System\.out\.println'
    return t

# Identificadores e palavras reservadas
def t_Id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = token_map.get(t.value, 'Id')
    return t


# Captura de novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar comentários de linha (// ...) e de bloco (/* ... */)
def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass  # Ignora o token

def t_error(t):
    print(f"Lexical error in {t.lineno}: '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()


lexer.linha = 1



def generateTokens(code):
    lexer.input(code)
    tokens_gerados = []
    for token in lexer:
        tokens_gerados.append(token)
    return tokens_gerados






def p_PROG(p):
    '''PROG : Public Class Id LeftKey Public Static Void Main LeftParenthesis String LeftBracket RightBracket Args RightParenthesis LeftKey CMDS RightKey METODO RightKey'''
    print("Entrando em PROG")
    
    p[0] = ("PROG", p[3], p[16], p[18])
    pass

def PROG():
    result = True
    result = result and Analyzer.get_comparisons(['Public', 'Class'],[1,1])
    
    result = result and Analyzer.get_comparisons(['Id', 'LeftKey ', 'Public', 'Static', 'Void', 'Main', 'LeftParenthesis', 'String', 'LeftBracket', 'RightBracket', 'Args', 'RightParenthesis', 'LeftKey'],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    return result

def p_METODO(p):
    '''METODO : Public Static Double Id LeftParenthesis PARAMS RightParenthesis LeftKey CMDS Return EXPRESSAO Semicolon RightKey
              | VOID'''
    print("Entrando em METODO")
    
    if len(p) > 2:
        p[0] = ("METODO", p[3], p[4], p[6], p[9], p[11])
    else:
        p[0] = ("METODO", None)
    pass

def p_PARAMS(p):
    '''PARAMS : Double Id MAIS_PARAMS
              | VOID'''
    print("Entrando em PARAMS")
    
    if len(p) > 2:
        p[0] = ("PARAMS", p[1], p[2], p[3])
    else:
        p[0] = ("PARAMS", None)
    pass

def p_MAIS_PARAMS(p):
    '''MAIS_PARAMS : Comma PARAMS
                   | VOID'''
    print("Entrando em MAIS_PARAMS")
    
    if len(p) > 2:
        p[0] = ("MAIS_PARAMS", p[2])
    else:
        p[0] = ("MAIS_PARAMS", None)
    pass

def p_DC(p):
    '''DC : VAR MAIS_CMDS'''
    print("Entrando em DC")
    
    p[0] = ("DC", p[1], p[2])
    pass

def p_VAR(p):
    '''VAR : Double VARS'''
    print(f"Entrando em VAR")
    
    p[0] = ("VAR", p[1], p[2])
    pass

def p_VARS(p):
    '''VARS : Id MAIS_VAR'''
    print(f"Entrando em VARS: {p[1]}")
    
    p[0] = ("VARS", p[1], p[2])
    pass

def p_MAIS_VAR(p):
    '''MAIS_VAR : Comma VARS
                | VOID'''
    print("Entrando em MAIS_VAR")
    
    if len(p) > 2:
        p[0] = ("MAIS_VAR", p[2])
    else:
        p[0] = ("MAIS_VAR", None)
    pass

def p_CMDS(p):
    '''CMDS : CMD MAIS_CMDS
            | CMD_COND CMDS
            | DC
            | VOID'''
    print("Entrando em CMDS")
    
    if len(p) == 3:
        p[0] = ("CMDS", p[1], p[2])
    elif len(p) == 2:
        p[0] = ("CMDS", p[1])
    else:
        p[0] = ("CMDS", None)
    pass

def p_MAIS_CMDS(p):
    '''MAIS_CMDS : Semicolon CMDS'''
    print("Entrando em MAIS_CMDS")
    
    p[0] = ("MAIS_CMDS", p[2])
    pass

def p_CMD_COND(p):
    '''CMD_COND : If LeftParenthesis CONDICAO RightParenthesis LeftKey CMDS RightKey PFALSA
                | While LeftParenthesis CONDICAO RightParenthesis LeftKey CMDS RightKey'''
    print("Entrando em CMD_COND")
    
    if p[1] == 'if':
        p[0] = ("CMD_COND_IF", p[3], p[6], p[8])
    else:
        p[0] = ("CMD_COND_WHILE", p[3], p[6])

    pass

def p_CMD(p):
    '''CMD : Print LeftParenthesis EXPRESSAO RightParenthesis
           | Id RESTO_IDENT'''
    print("Entrando em CMD")
    
    if len(p) == 8:
        p[0] = ("CMD_PRINTLN_EXPR", p[7])
    else:
        p[0] = ("CMD_ASSIGN", p[1], p[2])
    pass

def p_PFALSA(p):
    '''PFALSA : Else LeftKey CMDS RightKey
              | VOID'''
    print("Entrando em PFALSA")
    
    if len(p) > 2:
        p[0] = ("PFALSA", p[3])
    else:
        p[0] = ("PFALSA", None)
    pass

def p_RESTO_IDENT(p):
    '''RESTO_IDENT : Assignment EXP_IDENT
                   | LeftParenthesis LISTA_ARG RightParenthesis''' 
    print("Entrando em RESTO_IDENT")
    
    if p[1] == '=':
        p[0] = ("ASSIGN_EXPR", p[2])
    else:
        p[0] = ("FUNC_CALL", p[2])
    pass

def p_LISTA_ARG(p):
    '''LISTA_ARG : ARGUMENTOS
                 | VOID'''
    print("Entrando em LISTA_ARG")
    
    p[0] = p[1]
    pass

def p_ARGUMENTOS(p):
    '''ARGUMENTOS : Id MAIS_IDENT'''
    print("Entrando em ARGUMENTOS")
    
    p[0] = ("ARGUMENTOS", p[1], p[2])
    pass

def p_MAIS_IDENT(p):
    '''MAIS_IDENT : Comma ARGUMENTOS
                  | VOID'''
    print("Entrando em MAIS_IDENT")
    
    if len(p) > 2:
        p[0] = ("MAIS_IDENT", p[2])
    else:
        p[0] = None
    pass

def p_EXP_IDENT(p):
    '''EXP_IDENT : EXPRESSAO
                 | LerDouble LeftParenthesis RightParenthesis'''
    print("Entrando em EXP_IDENT")
    
    if len(p) == 2:
        p[0] = ("EXP_IDENT", p[1])
    else:
        p[0] = ("EXP_IDENT_FUNC", "lerDouble")
    pass

def p_CONDICAO(p):
    '''CONDICAO : EXPRESSAO Relational EXPRESSAO'''
    print("Entrando em CONDICAO")
    
    p[0] = ("CONDICAO", p[1], p[2], p[3])
    pass

def p_EXPRESSAO(p):
    '''EXPRESSAO : TERMO OUTROS_TERMOS'''
    print("Entrando em EXPRESSAO")
    
    p[0] = ("EXPRESSAO", p[1], p[2])
    pass

def p_TERMO(p):
    '''TERMO : OP_UN FATOR MAIS_FATORES'''
    print("Entrando em TERMO")
    
    p[0] = ("TERMO", p[1], p[2], p[3])
    pass

def p_OP_UN(p):
    '''OP_UN : Sub
             | VOID'''
    print("Entrando em OP_UN")
    
    p[0] = p[1] if p[1] == '-' else None
    pass

def p_FATOR(p):
    '''FATOR : Id
             | Number
             | LeftParenthesis EXPRESSAO RightParenthesis'''
    print("Entrando em FATOR")
    
    if len(p) == 2:
        p[0] = ("FATOR",p[1])
    else:
        p[0] = ("NEW_EXPRESSAO",p[2])
    pass

def p_OUTROS_TERMOS(p):
    '''OUTROS_TERMOS : Add TERMO OUTROS_TERMOS
                     | Sub TERMO OUTROS_TERMOS
                     | VOID'''
    print("Entrando em OUTROS_TERMOS")
    
    if len(p) > 2:
        p[0] = ("OUTROS_TERMOS", p[1], p[2], p[3])
    else:
        p[0] = None
    pass

def p_MAIS_FATORES(p):
    '''MAIS_FATORES : Mult FATOR MAIS_FATORES
                    | VOID'''
    print("Entrando em MAIS_FATORES")
    
    if len(p) > 2:
        p[0] = ("MAIS_FATORES", p[1], p[2], p[3])
    else:
        p[0] = None
    pass

def p_VOID(p):
    '''VOID : '''
    print("Entrando em VOID")
    pass



parser = yacc.yacc()

def parse_tokens_and_generate_object_code(tokens):
    Analyzer.tokens = tokens
    print("ola")
    return PROG()


def analiseSintatica(codigo):
    
    return parser.parse(codigo)
