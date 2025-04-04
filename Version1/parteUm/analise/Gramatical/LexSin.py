import ply.yacc as yacc
import ply.lex as lex

erro = False

reservadas = {
    'public': 'PUBLIC',
    'main': 'MAIN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'static': 'STATIC',
    'class': 'CLASS',
    'double': 'DOUBLE',
    'void': 'VOID',
    'String': 'STRING',
    'lerDouble': 'LERDOUBLE',
    'args' : 'ARGS'
}

simbolos = {
    ')': 'FECHA_PARENTESE',
    ']': 'FECHA_COLCHETE',
    '}': 'FECHA_CHAVE',
    '(': 'ABRE_PARENTESE',
    '[': 'ABRE_COLCHETE',
    '{': 'ABRE_CHAVE',
    ';': 'PONTO_VIRGULA',
    '=': 'ATRIBUICAO',
    ',': 'VIRGULA'
}

op_ad = {
    '+': 'ADICAO',
    '-': 'SUBTRACAO'
}


tokens = [
    'ID',
    'NUMERO',
    'RELACIONAL',
    'OP_MULT',
    'OP_AD',
    'SOUT'
] + list(op_ad.values()) + list(simbolos.values()) + list(reservadas.values())


t_NUMERO = r'[0-9]+(\.[0-9]+)?'


t_OP_MULT = r'(\*|/)'


t_ignore = ' \t\r\f'


def t_RELACIONAL(t):
    r'==|!=|<=|>=|<|>'
    return t


def t_OP_AD(t):
    r'[\+-]'
    t.type = op_ad.get(t.value)
    return t


def t_SOUT(t):
    r'System\.out\.println'
    return t


def t_simbolos(t):
    r'[=\;\,\{\}\(\)\[\]]'
    t.type = simbolos.get(t.value) 
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"[Erro Léxico na linha {t.lexer.lineno}: {t.value[0]}]")
    t.lexer.skip(1)


lexer = lex.lex()


lexer.linha = 1



def gerarTokens(codigo):
    lexer.input(codigo)
    tokens_gerados = []
    for tok in lexer:
        tokens_gerados.append(tok)
    return tokens_gerados



def p_prog(p):
    '''prog : PUBLIC CLASS ID ABRE_CHAVE PUBLIC STATIC VOID MAIN ABRE_PARENTESE STRING ABRE_COLCHETE FECHA_COLCHETE ARGS FECHA_PARENTESE ABRE_CHAVE cmds FECHA_CHAVE metodo FECHA_CHAVE'''
    p[0] = p[18]
    pass

def p_metodo(p):
    '''metodo : PUBLIC STATIC tipo ID ABRE_PARENTESE params FECHA_PARENTESE ABRE_CHAVE cmds RETURN expressao PONTO_VIRGULA FECHA_CHAVE
              | vazio'''
    if len(p) > 2:
        p[0] = [p[4], p[6]]
    pass

def p_params(p):
    '''params : tipo ID mais_params
              | vazio'''
    if len(p) > 2:
        p[0] = int(p[3])+1
    else:
        p[0] = 0
    pass

def p_mais_params(p):
    '''mais_params : VIRGULA params
                   | vazio'''
    if len(p) > 2:
        p[0] = int(p[2])
    else:
        p[0] = 0
    pass

def p_dc(p):
    '''dc : var mais_cmds'''
    pass

def p_var(p):
    '''var : tipo vars'''
    pass

def p_vars(p):
    '''vars : ID mais_var'''
    pass

def p_mais_var(p):
    '''mais_var : VIRGULA vars
                | vazio'''
    pass

def p_tipo(p):
    '''tipo : DOUBLE'''
    pass

def p_cmds(p):
    '''cmds : cmd mais_cmds
            | cmd_cond cmds
            | dc
            | vazio'''
    pass

def p_mais_cmds(p):
    '''mais_cmds : PONTO_VIRGULA cmds'''
    pass

def p_cmd_cond(p):
    '''cmd_cond : IF ABRE_PARENTESE condicao FECHA_PARENTESE ABRE_CHAVE cmds FECHA_CHAVE pfalsa
                | WHILE ABRE_PARENTESE condicao FECHA_PARENTESE ABRE_CHAVE cmds FECHA_CHAVE'''
    pass

def p_cmd(p):
    '''cmd : SOUT ABRE_PARENTESE expressao FECHA_PARENTESE
           | ID resto_ident'''
    pass

def p_pfalsa(p):
    '''pfalsa : ELSE ABRE_CHAVE cmds FECHA_CHAVE
              | vazio'''
    pass

def p_resto_ident(p):
    '''resto_ident : ATRIBUICAO exp_ident
                   | ABRE_PARENTESE lista_arg FECHA_PARENTESE''' 
    pass

def p_lista_arg(p):
    '''lista_arg : argumentos
                 | vazio'''
    pass

def p_argumentos(p):
    '''argumentos : ID mais_ident'''
    pass

def p_mais_ident(p):
    '''mais_ident : VIRGULA argumentos
                  | vazio'''
    pass

def p_exp_ident(p):
    '''exp_ident : expressao
                 | LERDOUBLE ABRE_PARENTESE FECHA_PARENTESE'''
    pass

def p_condicao(p):
    '''condicao : expressao RELACIONAL expressao'''
    pass


def p_expressao(p):
    '''expressao : termo outros_termos'''
    pass

def p_termo(p):
    '''termo : op_un fator mais_fatores'''
    pass

def p_op_un(p):
    '''op_un : SUBTRACAO
             | vazio'''
    pass

def p_fator(p):
    '''fator : ID
             | NUMERO
             | ABRE_PARENTESE expressao FECHA_PARENTESE'''
    pass

def p_outros_termos(p):
    '''outros_termos : ADICAO termo outros_termos
                     | SUBTRACAO termo outros_termos
                     | vazio'''
    pass



def p_mais_fatores(p):
    '''mais_fatores : OP_MULT fator mais_fatores
                    | vazio'''
    pass

def p_vazio(p):
    '''vazio : '''
    pass



def p_error(p):
    global erro
    if p:
        print(f"Erro de sintaxe na linha {int(p.lineno)-18}, token: {p.value}")
    else:
        print("Erro de sintaxe no final do arquivo")
    erro = True


parser = yacc.yacc()



def analiseSintatica(codigo):
    global erro  
    erro = False  
    resultado = parser.parse(codigo)
    return [erro, resultado]
