import ply.lex as lex

class Analyzer:
    tokens = []
    position = 0
    scopes = [{}]
    methods = {}   
    position_instruction = -1
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
    
    def add_instruction(self,instruction, value = ''):
        self.instructions.append([instruction,value])
        self.position_instruction += 1

    


    

analyzer = Analyzer()


var_map = {}

token_map = {
    
    'public': 'Public', 'main': 'Main', 'static': 'Static', 'class': 'Class', 'void': 'Void',
    'if': 'If', 'else': 'Else', 'while': 'While', 'double': 'Double','String': 'String', 
    'lerDouble': 'LerDouble', 'args': 'Args'  
}

tokens = [
    'Id', 'Number', 'Print', 'Mult', 'Relational',
    'LeftParenthesis', 'RightParenthesis', 'LeftBracket', 'RightBracket',
    'LeftKey', 'RightKey', 'Comma', 'Semicolon', 'Assignment', 'Sub', 'Add'
] + list(token_map.values())


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


t_Mult = r'[\*/]'
t_ignore = ' \t\r\f'


def t_Number(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


def t_Relational(t):
    r'==|!=|<=|>=|<|>'
    return t


def t_Print(t):
    r'System\.out\.println'
    return t


def t_Id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = token_map.get(t.value, 'Id')
    return t



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass  

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

    result = True

    result = result and analyzer.get_comparisons_type(['Public', 'Class'])

    analyzer.set_declaration(analyzer.get_value())
    
    result = result and analyzer.get_comparisons_type(['Id', 'LeftKey', 'Public', 'Static', 'Void', 'Main', 'LeftParenthesis', 'String', 'LeftBracket', 'RightBracket', 'Args', 'RightParenthesis', 'LeftKey'])
    
    analyzer.add_scope()

    result = result and CMDS()   

    analyzer.add_instruction('PARA')

    return result and analyzer.get_comparisons_type(['RightKey', 'RightKey'])


def CMDS():

    value_type = analyzer.get_type()
    if value_type == "Double":

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

    return analyzer.get_comparisons_type(['LeftParenthesis']) and ARGUMENTOS() and analyzer.get_comparisons_type(['RightParenthesis'])

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
     
    return True 


def MAIS_IDENT():
    value_type = analyzer.get_type()
    
    if value_type == 'Comma':
        return analyzer.get_comparisons_type(['Comma']) and ARGUMENTOS()
    
    return True

def EXP_IDENT():
    value_type = analyzer.get_type()

    if value_type == "LerDouble":
        analyzer.add_instruction('LEIT')

        return analyzer.get_comparisons_type(['LerDouble', 'LeftParenthesis', 'RightParenthesis']) 
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
    
    result = result and EXPRESSAO()
    
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
     
    
    
    return result

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
            print(f"Semantic error: variable '{value}'is not declared.")
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



def parse_tokens_and_generate_object_code(tokens):
    analyzer.tokens = tokens

    result =  PROG()

    for instruction in analyzer.instructions:
        print(instruction)

    return [result, analyzer.instructions]

