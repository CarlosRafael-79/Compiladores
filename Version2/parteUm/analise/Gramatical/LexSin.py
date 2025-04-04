import ply.yacc as yacc
import ply.lex as lex

class Analyzer:
    tokens = []
    position = 0
    scopes = [{}]
    methods = {}

    infoMetodo = ['', -1]
    
    position_instruction = -1
    posicaoMetodo = -1
    instructions = []
    
    
    def get_type(self):
        return self.tokens[self.position].type

    def get_value(self):
        return self.tokens[self.position].value    
     
    def get_comparisons_type(self,types = []):
        for  type in types:
            print(f'{type} : {self.get_type()}')
            if type != self.get_type():
                self.position += 1
                return False
            self.position += 1
        return True
    
    def is_declared(self, variable):
        for scope in self.scopes:
            for key in scope.keys():
                if key == variable:
                    return True
        return False
    
    def set_declaration(self, variable):
        self.scopes[-1][variable] = 0
        
    def add_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def is_declared_methods(self, variable):
            for key in self.methods.keys():
                if key == variable:
                    return True
            return False
    
    def add_instruction(self,instruction, value = ''):
        self.instructions.append([instruction,value])
        self.position_instruction += 1
        #if instrucao == 'PARA':
        #    self.posicaoMetodo = self.posicaoInstrucao+1

    
'''    
    def addInstrucao(self,instrucao, valor = ''):
        self.instrucoes.append([instrucao,valor])
        self.posicaoInstrucao += 1
        if instrucao == 'PARA':
            self.posicaoMetodo = self.posicaoInstrucao+1
'''
    


    

analyzer = Analyzer()


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






def PROG():


    analyzer.add_instruction('INPP')
    print(analyzer.instructions)
    result = True

    result = result and analyzer.get_comparisons_type(['Public', 'Class'])

    analyzer.set_declaration(analyzer.get_value())
    
    result = result and analyzer.get_comparisons_type(['Id', 'LeftKey', 'Public', 'Static', 'Void', 'Main', 'LeftParenthesis', 'String', 'LeftBracket', 'RightBracket', 'Args', 'RightParenthesis', 'LeftKey'])
    
    analyzer.add_scope()

    result = result and CMDS()
    
    result = result and analyzer.get_comparisons_type(['RightKey'])
    
    result = result and METODO()
    
    result = result and analyzer.get_comparisons_type(['RightKey'])
    
    return result


def CMDS():

    value_type = analyzer.get_type()
    if value_type == "Double":
        #analyzer.position += 1
        result = analyzer.get_comparisons_type(['Double']) and VARS() and MAIS_CMDS()

        return result
    elif  value_type == "Id" or value_type == "Print":
        
        return  CMD() and MAIS_CMDS()  
    elif value_type == 'If' or value_type == 'While':

        return CMD_COND() and CMDS()
    
    
    return True


def CMD():
    value_type = analyzer.get_type()
    
    if value_type == "Print":
        result = analyzer.get_comparisons_type(['Print', 'LeftParenthesis']) and EXPRESSAO() and analyzer.get_comparisons_type(['RightParenthesis'])
        analyzer.add_instruction('IMPR')
        return result
    else:
        
        value_id = analyzer.get_value()
        analyzer.get_comparisons_type(['Id'])
        return RESTO_IDENT(value_id)

def RESTO_IDENT(value_id):
    
    value_type = analyzer.get_type()

    if value_type == "Assignment":
        if not analyzer.is_declared(value_id):
            print(f"Semantic error: variable '{value_id}' is not declared.")
            return False
        result = analyzer.get_comparisons_type(['Assignment']) and EXP_IDENT()

        analyzer.add_instruction('ARMZ', value_id)

        return result
    
    #if analyzer.is_declared_methods(analyzer.get_value()):
    #    print(f"Semantic error: method has more than one name.")
    #    return False

    analyzer.add_instruction('PSHR') 
    savePoint = analyzer.position_instruction

    qtde_args = ARGUMENTOS()

    #if qtde_args != analisador.infoMetodo[1]:
        #print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: {qtde_args} não é número de argumentos esperado pelo método.")
        #return False
    
    analyzer.add_instruction('PSHR','?') 

    #analisador.addInstrucao('CHPR', analisador.infoMetodo[0])

    analyzer.instructions[savePoint][1] = analyzer.position_instruction + 1
    
    return analyzer.get_comparisons_type(['LeftParenthesis']) and ARGUMENTOS() and analyzer.get_comparisons_type(['RightParenthesis'])

    
    if id != analisador.infoMetodo[0]:
        print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: '{id}' não é o nome de uma chamada de método válido.")
        return False
    analisador.posicao += 1

    analisador.addInstrucao('PSHR') 
    savePoint = analisador.posicaoInstrucao

    qtde_args = argumentos(0)
    if qtde_args != analisador.infoMetodo[1]:
        print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: {qtde_args} não é número de argumentos esperado pelo método.")
        return False
    analisador.addInstrucao('CHPR', analisador.infoMetodo[0])

    analisador.instrucoes[savePoint][1] = analisador.posicaoInstrucao + 1
    analisador.posicao += 1
    ''''''

    return True

def ARGUMENTOS():
    
    value_type = analyzer.get_type()
    
    if value_type == "Id":
        value = analyzer.get_value()
        
        if not analyzer.is_declared(value):
            print(f"Semantic error: variable '{value}' not is declared.")
            return False
        
        result = analyzer.get_comparisons_type(['Id'])
        
        analyzer.add_instruction('CRVL', value)

        
        return result and MAIS_IDENT()
     
    return True #qtde


def MAIS_IDENT():
    '''
    value = analisador.getValue()

    if value == ',':
        analisador.posicao += 1
        return argumentos(qtde)
    return qtde 
    ''' 
    value_type = analyzer.get_type()
    
    if value_type == 'Comma':
        return analyzer.get_comparisons_type(['Comma']) and ARGUMENTOS()
    
    return True

def EXP_IDENT():
    value_type = analyzer.get_type()

    if value_type == "LerDouble":
        analyzer.add_instruction('LEIT')

        return analyzer.get_comparisons_type(['LerDouble', 'LeftParenthesis', 'RightParenthesis']) 
    #analisador.posicao -= 1
    return EXPRESSAO()

def MAIS_CMDS():
    result = analyzer.get_comparisons_type(['Semicolon'])
    
    value_type = analyzer.get_type()
    
    if   value_type == 'If' or value_type == 'While' or value_type == "Print" or value_type == "Id" or value_type == "Double":
        return CMDS()
    
    return result

def CMD_COND():
    value_type = analyzer.get_type()

    if value_type == 'While':
        analyzer.add_scope()

        savePoint = analyzer.position_instruction + 1

        result = analyzer.get_comparisons_type(['While','LeftParenthesis']) and CONDICAO() and analyzer.get_comparisons_type(['RightParenthesis','LeftKey'])
        
        analyzer.add_instruction('DSVF')
        savePointDSVF = analyzer.position_instruction
        
        result = result and CMDS()

        analyzer.add_instruction('DSVI', savePoint)
        analyzer.instructions[savePointDSVF][1] = analyzer.position_instruction + 1


        result = result and analyzer.get_comparisons_type(['RightKey'])

        analyzer.exit_scope()


        return result

    analyzer.add_scope()

    savePoint = analyzer.position_instruction + 1

    result = analyzer.get_comparisons_type(['If','LeftParenthesis']) and CONDICAO()

    analyzer.add_instruction('DSVF')
    savePointDSVF = analyzer.position_instruction

    result = result and analyzer.get_comparisons_type(['RightParenthesis','LeftKey']) and CMDS() and analyzer.get_comparisons_type(['RightKey'])

    analyzer.exit_scope()

    
    value_type = analyzer.get_type()
    
    
    if(value_type != "Else"):
            analyzer.instructions[savePointDSVF][1] = analyzer.position_instruction + 1
            return result
    
    analyzer.add_instruction('DSVI')
    savePointDSVI = analyzer.position_instruction

    analyzer.instructions[savePointDSVF][1] = analyzer.position_instruction + 1

    
    result = result and PFALSE()

    analyzer.instructions[savePointDSVI][1] = analyzer.position_instruction + 1
    
    return result


def PFALSE():

    analyzer.add_scope()

    result = analyzer.get_comparisons_type(['Else','LeftKey']) and CMDS() and analyzer.get_comparisons_type(['RightKey'])

    analyzer.exit_scope()

    return result 

def CONDICAO():
    result = EXPRESSAO()
    value = analyzer.get_value()
    result = result and analyzer.get_comparisons_type(['Relational'])
    
    
    if value == "!=":       
        analyzer.add_instruction('CDES')
    elif value == "==":
        analyzer.add_instruction('CPIG')
    elif value == ">":
        analyzer.add_instruction('CPMA')
    elif value == "<=":
        analyzer.add_instruction('CPMI')
    elif value == ">=":
        analyzer.add_instruction('CMAI') 
    elif value == "<":
        analyzer.add_instruction('CPME')
     
    
    
    return result and EXPRESSAO()

def VARS():
    value = analyzer.get_value()
    
    if analyzer.is_declared(value):
        print(f"Semantic error: variable '{value}' is declared.")
        return False
    analyzer.set_declaration(value)
    analyzer.add_instruction('ALME', value)
                      
    return analyzer.get_comparisons_type(['Id']) and MAIS_VARS()

def MAIS_VARS():
    value_type = analyzer.get_type()

    if value_type == 'Comma':
        return analyzer.get_comparisons_type(['Comma']) and VARS()
    return True

def EXPRESSAO():
    return TERMO() and MAIS_TERMOS()

def TERMO():
    value_type = analyzer.get_type()

    if value_type == 'Sub':

        
        result = analyzer.get_comparisons_type(['Sub']) and FATOR() and MAIS_FATORES()
        analyzer.add_instruction('INVE')


        return result
    
    return FATOR() and MAIS_FATORES()

def MAIS_TERMOS():
    value_type = analyzer.get_type()

    if   value_type == 'Sub' or value_type == 'Add':
        if value_type == 'Sub':
            analyzer.get_comparisons_type(['Sub'])
            operation = 'SUBT'
            
        if value_type == 'Add':
            analyzer.get_comparisons_type(['Add'])
            operation = 'SOMA'
            

        if TERMO():
            value_type = analyzer.get_type()
            analyzer.add_instruction(operation)


            if value_type == 'Add' or value_type == 'Sub':
                return MAIS_TERMOS()
            return True
        return False
    return True

def FATOR():
    value_type = analyzer.get_type()
    value = analyzer.get_value()
    
    if value_type == 'Number':
        result = analyzer.get_comparisons_type(['Number'])
        analyzer.add_instruction('CRCT', value)

    elif value_type == 'Id':

        if not analyzer.is_declared(value):
            print(f"Semantic error: variable '{value}' is declared.")
            return False
        
        result = analyzer.get_comparisons_type(['Id'])

        analyzer.add_instruction('CRVL', value)
        
    else:
        result = analyzer.get_comparisons_type(['LeftParenthesis'])
        return result and EXPRESSAO() and analyzer.get_comparisons_type(['RightParenthesis'])
    return True
    
def MAIS_FATORES():
    value_type = analyzer.get_type()
    value = analyzer.get_value()

    if value_type == 'Mult':
        operation = 'MULT'
        if value == '/':
            operation = 'DIVI'
        
        if analyzer.get_comparisons_type(['Mult']) and FATOR():
            value_type = analyzer.get_type()

            analyzer.add_instruction(operation)
            
            if value_type == 'Mult':
                return MAIS_FATORES()
            return True
        
        return False
    return True

def METODO():
    
    analyzer.exit_scope()
    analyzer.add_scope()

    analyzer.add_instruction('PARA')

    value_type = analyzer.get_type()
    if value_type == 'Public':
    
        result = analyzer.get_comparisons_type(['Public', 'Static', 'Double'])

        analyzer.methods[analyzer.get_value()] = analyzer.position_instruction
        
        result = result and analyzer.get_comparisons_type(['Id', 'LeftParenthesis'])
        
        result = result and  PARAMS() and analyzer.get_comparisons_type(['RightParenthesis', 'LeftKey']) and CMDS() and analyzer.get_comparisons_type(['Return'])
    
        result = result and EXPRESSAO() and analyzer.get_comparisons_type(['Semicolon', 'RightKey'])

        analyzer.add_instruction('RTPR')

        return result
    return True


def PARAMS():
    
    value_type = analyzer.get_type()

    if value_type == "Double":
        result = analyzer.get_comparisons_type(['Double'])
        
        value = analyzer.get_value()
        
        result = analyzer.get_comparisons_type(['Id'])
        
        if analyzer.is_declared(value):
            print(f"Semantic error: variable '{value}' is declared.")
            return False
        
        analyzer.set_declaration(value)
        
        result  = result and MAIS_PARAMS()

        analyzer.add_instruction('ALME', value)
        analyzer.add_instruction('ARMZ', value)


        return result

    return True

def MAIS_PARAMS():
    value_type = analyzer.get_type()

    if value_type == 'Comma':       
        return analyzer.get_comparisons_type(['Comma']) and PARAMS()
    return True


def parse_tokens_and_generate_object_code(tokens):
    analyzer.tokens = tokens

    result =  PROG()

    for instruction in analyzer.instructions:
        print(instruction)

    return result

