def gera_matriz_inputada (arquivo):

    matriz_inputada = []

    while True:
        try:
            arq = open(arquivo, "r") #abre o arquivo
            lines = arq.readlines() #retorna uma lista que contém cada linha do arquivo como um item da lista
        except:
            print("\nErro na abertura do arquivo. Insira novamente o nome do arquivo.\n")
            continue

        for linha in lines:
            linhas_matriz_inputada = []
            lin = linha[:len(linha)-1] #variável que recebe cada linha do arquivo de texto original como uma string
            v = lin.split('\t') #variável que recebe a linha acima e a transforma em uma lista com n elementos

            for i in range (len(v)):
                    linhas_matriz_inputada.append(int(v[i]))
            matriz_inputada.append(linhas_matriz_inputada)

        break
        #return  matriz_inputada
        arq.close()

        print(matriz_inputada)

    # conta a quantidade de ligações de cada página
    for k in range(len(matriz_inputada)):
        cont = 0
        for j in range(len(matriz_inputada)):
            if matriz_inputada[j][k] == 1:
                cont += 1
        # cria a matriz com os pesos
        for i in range(len(matriz_inputada)):
            if matriz_inputada[i][k] == 1:
                matriz_inputada[i][k] = 1 / cont

    return matriz_inputada

def mostra_matriz_inputada(matriz):
    print("\n")
    for i in range(len(matriz)):
        for k in range(len(matriz)):
            print("%4.2f" % matriz[i][k], " ", end='')
        print("")

print(mostra_matriz_inputada(gera_matriz_inputada("rede_8_paginas.txt")))






