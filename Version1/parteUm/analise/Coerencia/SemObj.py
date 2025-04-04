class Analisador:
    tokens = []
    posicao = 0
    posicaoInstrucao = -1
    posicaoMetodo = -1
    escopos = [{}]
    instrucoes = []
    infoMetodo = ['', -1]

    def addInstrucao(self,instrucao, valor = ''):
        self.instrucoes.append([instrucao,valor])
        self.posicaoInstrucao += 1
        if instrucao == 'PARA':
            self.posicaoMetodo = self.posicaoInstrucao+1

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

    def getType(self):
        return self.tokens[analisador.posicao].type

    def getValue(self):
        return self.tokens[analisador.posicao].value

analisador = Analisador()


def getInstrucoes(lex, infoMeotodo):
    analisador.tokens = lex
    if infoMeotodo is not None:
        analisador.infoMetodo = infoMeotodo

    if prog():
        if infoMeotodo is not None:
            for instrucao in analisador.instrucoes:
                if instrucao[1] == infoMeotodo[0]:
                    instrucao[1] = analisador.posicaoMetodo

        return analisador.instrucoes
    return None

def prog():

        analisador.addInstrucao('INPP')
        
        analisador.posicao += 2
        analisador.declare(analisador.getValue())

        analisador.posicao += 13
        analisador.addEscopo()
        
        ans = cmds()

        analisador.posicao += 1
        
        return ans and metodo()


def cmds():
    tipo = analisador.getType()

    if tipo == "SOUT" or tipo == "ID":
        
        return cmd() and mais_cmds()
    
    elif tipo == 'IF' or tipo == 'WHILE':

        return cmd_cond() and cmds()
    
    elif tipo == "DOUBLE":
        analisador.posicao += 1
        ans = vars() and mais_cmds()

        return ans
    return True

def cmd_cond():
    tipo = analisador.getType()

    if tipo == 'WHILE':
        analisador.addEscopo()

        savePoint = analisador.posicaoInstrucao + 1

        analisador.posicao += 1

        ans = condicao()

        analisador.posicao += 2
        analisador.addInstrucao('DSVF')
        savePointDSVF = analisador.posicaoInstrucao
        ans = ans and cmds()

        analisador.addInstrucao('DSVI', savePoint)
        analisador.instrucoes[savePointDSVF][1] = analisador.posicaoInstrucao + 1

        analisador.posicao += 1

        analisador.exitEscopo()

        return ans
    else:
        analisador.addEscopo()
        
        savePoint = analisador.posicaoInstrucao + 1
        
        analisador.posicao += 1

        ans = condicao()

        analisador.addInstrucao('DSVF')
        savePointDSVF = analisador.posicaoInstrucao

        analisador.posicao += 2

        ans = ans and cmds()

        analisador.posicao += 1

        analisador.exitEscopo()

        tipo = analisador.getType()
        if(tipo != "ELSE"):
            analisador.instrucoes[savePointDSVF][1] = analisador.posicaoInstrucao + 1
            return ans
        
        analisador.addInstrucao('DSVI')
        savePointDSVI = analisador.posicaoInstrucao

        analisador.instrucoes[savePointDSVF][1] = analisador.posicaoInstrucao + 1

        ans = ans and pfalse()

        analisador.instrucoes[savePointDSVI][1] = analisador.posicaoInstrucao + 1

        return ans

def pfalse():
    tipo = analisador.getType()


    analisador.addEscopo()

    analisador.posicao += 2

    ans = cmds()

    analisador.posicao += 1

    analisador.exitEscopo()

    return ans


def condicao():
    ans = expressao()

    value = analisador.getValue()

    ans = ans and expressao()

    if value == "!=":
        analisador.addInstrucao('CDES')
    elif value == "==":
        analisador.addInstrucao('CPIG')
    elif value == ">":
        analisador.addInstrucao('CPMA')
    elif value == "<":
        analisador.addInstrucao('CPME')
    elif value == "<=":
        analisador.addInstrucao('CPMI')
    elif value == ">=":
        analisador.addInstrucao('CMAI')   

    return ans

def cmd():

    value = analisador.getValue()

    if value == "System.out.println":
        analisador.posicao += 1

        ans = expressao()
        analisador.posicao += 1

        analisador.addInstrucao('IMPR')
        return ans
    else:
        value = analisador.getValue()
        analisador.posicao += 1
        return resto_ident(value)

def resto_ident(id):

    value = analisador.getValue()

    if value == "=":
        if not analisador.isDeclared(id):
            print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: variável '{id}' não foi declarado.")
            return False
        analisador.posicao += 1
        
        ans = exp_ident()

        analisador.addInstrucao('ARMZ', id) 
        return ans
    
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


    return True

def exp_ident():
    tipo = analisador.getType()

    if tipo == "LERDOUBLE":
        analisador.posicao += 3
        analisador.addInstrucao('LEIT')
        return True
    analisador.posicao -= 1
    return expressao()

def argumentos(qtde):
    tipo = analisador.getType()

    if tipo == "ID":

        value = analisador.getValue()
        if not analisador.isDeclared(value):
            print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: variável '{id}' não foi declarado.")
            return False
        
        analisador.posicao += 1

        analisador.addInstrucao('CRVL', value)

        return mais_ident(qtde+1)

    return qtde
    

def mais_ident(qtde):
    value = analisador.getValue()

    if value == ',':
        analisador.posicao += 1
        return argumentos(qtde)
    return qtde    

def vars():
    
    value = analisador.getValue()

    if analisador.isDeclared(value):
        print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: variável '{value}' já foi declarada.")
        return False
    analisador.declare(value)

    analisador.addInstrucao('ALME', value)
                          
    analisador.posicao += 1
    return mais_vars()

def mais_vars():
    value = analisador.getValue()

    if value == ',':
        analisador.posicao += 1
        return vars()
    return True

def mais_cmds():

    analisador.posicao += 1
    tipo = analisador.getType()
    if tipo == "SOUT" or tipo == "ID" or tipo == 'IF' or tipo == 'WHILE' or tipo == "DOUBLE":
        return cmds()
    return True

def metodo():
    analisador.exitEscopo()
    analisador.addEscopo()
    tipo = analisador.getType()

    analisador.addInstrucao('PARA')

    if tipo == "PUBLIC":

        analisador.posicao += 3
        analisador.declare(analisador.getValue())
        analisador.posicao += 1
        
        ans = params()

        analisador.posicao += 2

        ans = ans and cmds() and expressao()
        
        analisador.addInstrucao('RTPR')

        return ans 



    return True
    
def params():
    analisador.posicao += 1
    value = analisador.getValue()

    if value == "double":
        analisador.posicao += 1
        value = analisador.getValue()

        if analisador.isDeclared(value):
            print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: variável '{value}' já foi declarada.")
            return False
        analisador.declare(value)

        ans = mais_params()

        analisador.addInstrucao('ALME', value)
        analisador.addInstrucao('ARMZ', value)

        return ans

    return True

def mais_params():
    analisador.posicao += 1
    value = analisador.getValue()
    if value == ',':
        return params()
    return True

def expressao():
    analisador.posicao += 1

    return termo() and mais_termos()

def termo():
    
    value = analisador.getValue()

    if value == "-":

        analisador.posicao += 1
        ans = fator() and mais_fatores()

        analisador.addInstrucao('INVE')

        return ans
    
    return fator() and mais_fatores()

def mais_termos():
    tipo = analisador.getType()

    if tipo == 'ADICAO' or tipo == 'SUBTRACAO':
        analisador.posicao += 1

        opAd = 'SOMA'
        if tipo == 'SUBTRACAO':
            opAd = 'SUBT'

        if termo():

            tipo = analisador.getType()

            analisador.addInstrucao(opAd)

            if tipo == 'ADICAO' or tipo == 'SUBTRACAO':
                return mais_termos()
            return True
        return False
    return True

def fator():
    tipo = analisador.getType()
    value = analisador.getValue()

    if tipo == 'NUMERO':
        analisador.posicao += 1
        analisador.addInstrucao('CRCT', value)
    elif tipo == 'ID':
        if not analisador.isDeclared(value):
            print(f"Erro de sintaxe na linha {analisador.tokens[analisador.posicao].lineno - 18}: variável '{id}' não foi declarado.")
            return False
        analisador.posicao += 1
        analisador.addInstrucao('CRVL', value)
    else:
        ans = expressao()
        analisador.posicao += 1
        return ans
    return True

def mais_fatores():
    
    tipo = analisador.getType()
    value = analisador.getValue()

    if tipo == 'OP_MULT':
        opMult = 'MULT'
        if value == '/':
            opMult = 'DIVI'

        analisador.posicao += 1 
        if fator():
            tipo = analisador.getType()

            analisador.addInstrucao(opMult)
            if tipo == 'OP_MULT':
                return mais_fatores()
            return True
        return False
    return True