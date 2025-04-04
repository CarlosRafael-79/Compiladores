from analise.Gramatical.LexSin import generateTokens
from analise.Gramatical.LexSin import parse_tokens_and_generate_object_code
from analise.Coerencia.SemObj import getInstrucoes

if __name__ == '__main__':

    # Mude o arquivo de entrada aqui.
    with open('parteUm\entradas\Exemplo.java', 'r') as arquivo:
        conteudo = arquivo.read()

    lex = generateTokens(conteudo)
    print("-----------")
    for token in lex:
        print(token)
    print("-----------")
    print(parse_tokens_and_generate_object_code(lex))
    #resultado = analiseSintatica(conteudo)
    #print(resultado)
    #print("\n\n")
'''
    if not resultado[0] :
        instrucoes = getInstrucoes(lex, resultado[1])
        if instrucoes is not None:
            with open('parteUm\codigo.txt', 'w') as arquivo:
                for sublista in instrucoes:
                    linha = ' '.join(map(str, sublista)) + '\n'
                    arquivo.write(linha)

'''