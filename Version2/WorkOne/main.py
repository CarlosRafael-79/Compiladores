from analise.Gramatical.LexSin import generateTokens
from analise.Gramatical.LexSin import parse_tokens_and_generate_object_code
from analise.Coerencia.SemObj import getInstrucoes

if __name__ == '__main__':

    # Mude o arquivo de entrada aqui.
    with open('WorkOne\input\Exemplo.java', 'r') as arquivo:
        conteudo = arquivo.read()

    lex = generateTokens(conteudo)
    print("-----------")
    for token in lex:
        print(token)
    print("-----------")
    
    result = parse_tokens_and_generate_object_code(lex)

    print(result[0])


    if result[0] :
        instrucoes = result[1]
        if instrucoes is not None:
            with open('WorkOne\code.txt', 'w') as arquivo:
                for sublista in instrucoes:
                    linha = ' '.join(map(str, sublista)) + '\n'
                    arquivo.write(linha)
