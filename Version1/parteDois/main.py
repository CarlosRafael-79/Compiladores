
if __name__ == '__main__':

    with open('parteUm\\codigo.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    lista = [list(map(str, linha.strip().split())) for linha in linhas]

    codigo = lista
    dados = []
    registradores = [{}]
    posicao = 1

    while True:
        
        aux = codigo[int(posicao)]

        if aux[0] == "ALME":
            registradores[-1][aux[1]] = 0
        elif aux[0] == "PSHR":
            n = float(aux[1])
            dados.append(n)
        elif aux[0] == "CHPR":
            posicao = float(aux[1])
            registradores.append({})
            continue
        elif aux[0] == "RTPR":
            dados.pop()
            primeiro = dados.pop()
            posicao = primeiro
            registradores.pop()
            continue
        elif aux[0] == "ARMZ":
            primeiro = dados.pop()
            registradores[-1][aux[1]] = primeiro
        elif aux[0] == "DSVI":
            posicao = int(aux[1])
            continue
        elif aux[0] == "DSVF":
            primeiro = dados.pop()
            if not primeiro:
                posicao = int(aux[1])
                continue
        elif aux[0] == "CRCT":
            n = float(aux[1])
            dados.append(n)
        elif aux[0] == "CRVL":
            n = registradores[-1][aux[1]]
            dados.append(n)
        elif aux[0] == "SOMA":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo+primeiro)
        elif aux[0] == "SUBT":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo-primeiro)
        elif aux[0] == "MULT":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo*primeiro)
        elif aux[0] == "DIVI":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo/primeiro)
        elif aux[0] == "INVE":
            primeiro = dados.pop()
            dados.append(-primeiro)
        elif aux[0] == "CPME":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo<primeiro)
        elif aux[0] == "CPMA":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo>primeiro)
        elif aux[0] == "CPIG":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo==primeiro)
        elif aux[0] == "CDES":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo!=primeiro)
        elif aux[0] == "CPMI":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo<=primeiro)
        elif aux[0] == "CMAI":
            primeiro = dados.pop()
            segundo = dados.pop()
            dados.append(segundo>=primeiro)
        elif aux[0] == "LEIT":
            entrada = float(input())
            dados.append(entrada)
        elif aux[0] == "IMPR":
            primeiro = dados.pop()
            print(primeiro)
        elif aux[0] == "PARA":
            break
        else:
            print(f'{aux[0]} não é aceito!')
            break
        
        posicao += 1
    