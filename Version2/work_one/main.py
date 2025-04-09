from analise.compiler import generateTokens
from analise.compiler import parse_tokens_and_generate_object_code


if __name__ == '__main__':

    # Mude o arquivo de entrada aqui.
    #with open('work_one\input\Exemplo.java', 'r') as arquivo:
    #    conteudo = arquivo.read()
        
    #print(conteudo)

    conteudo = """
    public class Exemplo {
        public static void main ( String [ ] args ){
            double a, b;
            a = lerDouble();
            b = 5+3*(4-3);
            if(a > b){
                System.out.println(a);
            }else{
                System.out.println(b);
            }

            while(a > 0){
                System.out.println(a);
                a = a - 1;
            }
        }
    }
"""
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
            with open('work_one\code.txt', 'w') as arquivo:
                for sublista in instrucoes:
                    linha = ' '.join(map(str, sublista)) + '\n'
                    arquivo.write(linha)
