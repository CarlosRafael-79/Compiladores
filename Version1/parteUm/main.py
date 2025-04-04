from analise.Gramatical.LexSin import gerarTokens
from analise.Gramatical.LexSin import analiseSintatica
from analise.Coerencia.SemObj import getInstrucoes

if __name__ == '__main__':

    # Mude o arquivo de entrada aqui.
    with open('parteUm\entradas\Exemplo.java', 'r') as arquivo:
        conteudo = arquivo.read()

    lex = gerarTokens(conteudo)

    for token in lex:
        print(token)

    resultado = analiseSintatica(conteudo)
    print("\n\n")
'''
    if not resultado[0] :
        instrucoes = getInstrucoes(lex, resultado[1])
        if instrucoes is not None:
            with open('parteUm\codigo.txt', 'w') as arquivo:
                for sublista in instrucoes:
                    linha = ' '.join(map(str, sublista)) + '\n'
                    arquivo.write(linha)
'''
    