# !/usr/bin/python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import decimal
import string
import time


#####################
# Core github
class Rede:
    def __init__(self):
        self.nodes = []
        self.conexao = []

    def adiciona_node(self, node):
        self.nodes.append(node)

    def adiciona_nodes(self, nodes):
        for node in nodes:
            if node not in self.nodes:
                self.nodes.append(node)

    def adiciona_conexao(self, conexao):
        if conexao not in self.conexao:
            if conexao[0] not in self.nodes:
                self.nodes.append(conexao[0])
            if conexao[1] not in self.nodes:
                self.nodes.append(conexao[1])
            self.conexao.append(conexao)

    def adiciona_conexoes(self, conexoes):
        for i in conexoes:
            self.adiciona_conexao(i)

    def numero_total_nodes(self):
        return len(self.nodes)

    def conjunto_arestas(self):
        return self.conexao


class GeraGrafo:  # grafo cacique
    def __init__(self, k):
        self.caciques = []  # Cria uma lista para armazenar os caciques.
        self.caciques2 = []  # Cria outra lista para armazenar os caciques.
        self.numero_caciques = k  # Número de caciques.

    def listaNodeCacique(self):
        cont = 0
        # Percorre de 1 até o número de caciques.
        for j in range(1, int(self.numero_caciques) + 1):
            self.caciques.append(j + cont)  # Adiciona os caciques a lista.
            self.caciques2.append(j + cont)  # Adiciona os caciques a lista.
            cont = cont + j

    def criaGrafo(self):
        self.grafo = nx.DiGraph()  # Inicia o grafo.
        # self.grafo = Rede()
        self.grafo.add_nodes_from(self.caciques)  # Adiciona os nós dos caciques.
        # print(self.caciques)
        # self.grafo.adiciona_nodes(self.caciques)

        count = 0
        for i in self.caciques:  # Percorre a lista dos caciques para fazer a conexão entre os mesmos.
            count = count + 1
            for p in self.caciques[count:]:  # Percorre de count pra frente.
                self.grafo.add_edge(i, p)  # Cria uma conexão (aresta) entre i e p.
                # self.grafo.adiciona_conexao((i, p))
                self.grafo.add_edge(p, i)  # Cria uma conexão (aresta) entre p e i.
                # self.grafo.adiciona_conexao((p, i))
                # Aqui é importante fazer duas conexões, pois as conexões no grafo
                # cacique-tribo são dadas por conexões mútuas.

        cont = 1
        while len(self.caciques) != 0:
            for t in self.caciques:  # Faz a conexão entre os caciques e os respectivos índios.
                self.grafo.add_edge(t, t + cont)
                # self.grafo.adiciona_conexao((t, t+cont))
                self.grafo.add_edge(t + cont, t)
                # self.grafo.adiciona_conexao((t+cont, t))
            del self.caciques[0]
            cont = cont + 1

        nova_lista = []  # Cria uma nova lista que guardará os índios.
        for i in self.grafo.edges():  # Percorre todas as conexões.
            # for i in self.grafo.conjunto_arestas():
            x = list(i)  # É preciso converter para lista, pois as conexões são tuplas.
            if (x[0] and x[1]) in self.caciques2:  # Se os dois valores forem caciques, então o loop é reiniciado.
                continue
            # Verifica se o x[0] é cacique e se x[1] não já foi adicionado a nova_lista
            elif x[0] in self.caciques2 and x[1] not in nova_lista:
                nova_lista.append([x[1], x[0]])  # Coloca o cacique como segundo elemento.
            # Verifica se o x[1] é cacique e se x[0] não já foi adicionado a nova_lista
            elif x[1] in self.caciques2 and x[0] not in nova_lista:
                nova_lista.append([x[0], x[1]])  # Coloca o cacique como segundo elemento.

        for i in self.caciques2:  # Percorre a segunda lista de caciques.
            list2 = []  # Cria outra nova lista para guardar só os índios.
            for x in nova_lista:  # Percorre a nova_lista procurando o cacique igual a i.
                if x[1] == i:
                    list2.append(x[0])  # Appenda a list2 com o índio desse cacique i.
            for z in range(len(list2) - 1):  # Percorre a list2 até o penúltimo valor.
                for k in range(z, len(list2)):  # Percorre list2 de z até o último valor.
                    if list2[z] != list2[k]:  # Para que não seja feita conexões de um índio consigo mesmo.
                        self.grafo.add_edge(list2[z], list2[k])  # Liga um índio ao outro.
                        # self.grafo.adiciona_conexao((list2[z], list2[k]))
                        self.grafo.add_edge(list2[k], list2[z])  # Liga um índio ao outro.
                        # self.grafo.adiciona_conexao((list2[k], list2[z]))

        return self.grafo  # Retorna o grafo.

    def n_nodes(self):  # Gera o número de nodes (nós) existentes no grafo.
        return self.grafo.number_of_nodes()
        # return self.grafo.numero_total_nodes()

    def arestas(self):  # Gera as arestas (conexões) existentes no grafo.
        return self.grafo.edges()
        # return self.grafo.conjunto_arestas()

    def posicao(self):  # Gera a posição do grafo.
        self.posicao = nx.spring_layout(self.grafo, dim=3)
        return self.posicao


#######
class GeraMatriz:
    def __init__(self, grafo, n_nodes, arestas):
        self.n_nodes = n_nodes  # Define o número de nós dentro do escopo da classe.
        self.grafo = grafo  # Define o grafo dentro do escopo da classe.
        self.arestas = arestas  # Define as arestas dentro do escopo da classe.

    def geraMatriz(self):
        grafo_lista = []  # Essa lista guardará a arestas em forma de list e não de tupla.
        for k in self.arestas:
            grafo_lista.append(list(k))

        # Cria a matriz com zeros, do tamanho do grafo.
        matriz = [[0 for k in range(self.n_nodes)] for i in range(self.n_nodes)]

        # cria a matriz com 1 onde tem conexão
        for i in range(1, self.n_nodes + 1):
            for k in range(len(grafo_lista)):
                if grafo_lista[k][0] == i:
                    matriz[grafo_lista[k][1] - 1][i - 1] = 1

        # conta a quantidade de ligações de cada página
        for k in range(len(matriz)):
            cont = 0
            for j in range(len(matriz)):
                if matriz[j][k] == 1:
                    cont += 1
            # cria a matriz com os pesos
            for i in range(len(matriz)):
                if matriz[i][k] == 1:
                    matriz[i][k] = 1 / cont

        return matriz


############################################################
# View github
class MostraVisualizacao:
    def __init__(self, G, n_nodes, posicao, arestas):
        self.grafo = G  # Define o grafo dentro do escopo da classe.
        self.n_nodes = n_nodes  # Define o número de nós dentro do escopo da classe.
        self.posicao = posicao  # Define a posição do grafo dentro do escopo da classe.
        self.arestas = arestas  # Define as arestas dentro do escopo da classe.

    def gera3d(self):
        # Define a maior aresta, a que tem mais conexões.
        maior_aresta = max([self.grafo.degree(i) for i in range(1, self.n_nodes + 1)])
        # Define cores diferentes para os nós (nem sempre isso acontece).
        cores_nos = [plt.cm.plasma(self.grafo.degree(i) / maior_aresta) for i in range(1, self.n_nodes + 1)]

        # Define o estilo do quadro 3D. Esse é um estilo temporário, não é global.
        with plt.style.context(('ggplot')):
            quadro = plt.figure()  # Cria a figura para o quadro.
            # Define o intervalo de 10 segundos para a exibição do quadro.
            timeout = quadro.canvas.new_timer(interval=10000)
            # Decorridos os 10 segundos, a função (anônima) lambda será chamada e fechará o quadro.
            timeout.add_callback(lambda: plt.close())
            # Cria os eixos 3D no quadro.
            eixo3d = Axes3D(quadro)

            # Percorre as posições do grafo.
            for chave, valor in self.posicao.items():
                xi = valor[0]  # A posição x de um determinado nó
                yi = valor[1]  # A posição y de um determinado nó
                zi = valor[2]  # A posição z de um determinado nó

                # Plota cada nó no quadro 3D.
                eixo3d.scatter(xi, yi, zi, c=np.array(cores_nos[chave - 1]).reshape(1, -1),
                               s=10 + 10 * self.grafo.degree(chave), edgecolors='k', alpha=0.7)

            # Percorre as conexões e liga as mesmas.
            for j in self.arestas:
                x = np.array((self.posicao[j[0]][0], self.posicao[j[1]][0]))
                y = np.array((self.posicao[j[0]][1], self.posicao[j[1]][1]))
                z = np.array((self.posicao[j[0]][2], self.posicao[j[1]][2]))

                # Plota a ligação x, y, z.
                eixo3d.plot(x, y, z, c='black', alpha=0.5)

        eixo3d.set_axis_off()  # Desabilita os eixos.
        # timeout.start()  # Começa o contagem de tempo (10 segundos).
        plt.show()  # Exibe o quadro.
        return  # Retorna/sai da função.


class MostraMatriz:
    def __init__(self, matriz):
        self.matriz = matriz  # Recebe a matriz e a define dentro do escopo da classe.

    def mostraMatriz(self):  # Exibe a matriz nxn.
        print("\n")
        for i in range(len(self.matriz)):
            for k in range(len(self.matriz)):
                print("%4.2f" % self.matriz[i][k], " ", end='')
            print("")
        return


#######################################################
# Matriz Modificada com o parâmetro Alpha
def Matriz_Modificada(N, Matriz, alfa):  # N=numero de nodes
    alfa_Sn = alfa * 1 / N  # elementos da Matriz Sn
    M_M = []  # Matriz Modificada
    M_M[:] = Matriz[:]

    for k in range(N):
        for i in range(N):  # MM = (1 - alfa)M + alfa*Sn
            M_M[k][i] = (1 - alfa) * M_M[k][i] + alfa_Sn

    return M_M


###CRIANDO MATRIZ A = M-I
# recebe N (tamanho da matriz) e M_M, que é a matriz modificada com o parâmetro alpha
def Matriz_A(N, M_M):
    matriz_A = []
    matriz_A[:] = M_M[:]

    for k in range(N):
        matriz_A[k][k] = matriz_A[k][k] - 1  # subtrai 1 da diagona principal

    return matriz_A


# recebe N (tamanho da matriz) e a matriz_A, que é a matriz subtraída da identidade
def Escalonamento(N, matriz_A):
    # realiza o pivotamento
    for k in range(N):  # varre as colunas
        # define variavel que recebe o elemento de maior valor absoluto da coluna. começa com o 1º
        maximo_absoluto = abs(matriz_A[0][k])
        # define variavel que recebe o indice do maior valor absoluto da coluna. começa com o 1º
        indice_absoluto = 0

        for l in range(N):  # varre as linhas
            # verifica se o valor do elemento da linha l, coluna k é maior que o maximo absoluto
            # melhorar essa linha de codigo. talvez não precise da primeira parte do != l
            if indice_absoluto != l and abs(matriz_A[l][k]) >= maximo_absoluto:
                # troca o maximo e o indice se for verdade
                maximo_absoluto = abs(matriz_A[l][k])
                indice_absoluto = l
        # troca as linhas para levar o maior elemento de valor absoluto ao pivô
        if abs(matriz_A[indice_absoluto][k]) >= abs(matriz_A[k][k]):
            matriz_A[indice_absoluto], matriz_A[k] = matriz_A[k], matriz_A[indice_absoluto]
    # realiza o escalonamento
    for k in range(N):  # varre as colunas
        for i in range(k + 1, N):  # varre as linhas
            alpha_i = matriz_A[i][k] / matriz_A[k][k]  # divide o elemento da linha i pelo pivô
            for j in range(k, N):  # varre as colunas
                # altera os elementos das linhas à direita da coluna que está sendo zerada
                matriz_A[i][j] = matriz_A[i][j] - (alpha_i * matriz_A[k][j])

    return matriz_A


# encontra o vetor X. Recebe a matriz que já está escalonada
def Encontrando_X(N, matriz_escalonada):
    # print(matriz_escalonada)
    x_n = 1  # define o vetor da linha de zeros como 1
    lista_x_k = [x_n]  # cria lista que receberá o peso das páginas (x_k)
    # lista_x_k = []
    for k in range(N - 2, -1, -1):  # inicia na penúltima coluna e vai até a primeira
        x_k = 0  # inicia a soma do x_k, que é o vetor em questão que está sendo calculado
        p = -1  # variável que vai controlar os x_n's.
        for i in range(k + 1, N):  # varre as colunas da linha que está sendo calculada
            # multiplica os elementos à direita do pivô da linha pelo x_n correspondente e soma em x_k
            x_k += matriz_escalonada[k][i] * lista_x_k[p]
            p += -1
        # print(x_k, p, lista_x_k)
        # x_k += matriz_escalonada[k][i] * x_n
        # divide a soma total do x_k pelo elemento pivô
        x_k = (-x_k) / matriz_escalonada[k][k]
        """
            A linha acima é como:
                5x - 2 = 0 => 5x = 2 => x = 2/5
        """
        # adiciona o valor do peso de x_k à lista de pesos
        lista_x_k.append(x_k)

    # NORMALIZAÇÃO
    soma_lista = sum(lista_x_k)

    # divide os pesos de cada elemento pela soma de todos os pesos
    for k in range(len(lista_x_k)):
        lista_x_k[k] = lista_x_k[k] / soma_lista

    # inverte a ordem da lista para ter o x_1 como primeiro elemento indo até o x_n
    lista_x_k.reverse()

    return lista_x_k


# DEFININDO A CONSTANTE C
def Constante_C(numero_nodes, M_M):
    lista_max = []
    min_coluna = M_M[0][0]

    for j in range(numero_nodes):
        for i in range(numero_nodes):
            if M_M[i][j] < min_coluna:
                min_coluna = M_M[i][j]
        lista_max.append(abs(1 - (2 * min_coluna)))

    return max(lista_max)


# DEFININDO OS VETORES V, L, C
def Vetor_VLC(Matriz):  # Matriz esparsa
    V = []  # Elemento
    L = []  # Linha do elemento
    C = []  # Coluna do elemento

    for k in range(len(Matriz)):
        for j in range(len(Matriz)):
            if Matriz[k][j] != 0:
                V.append(Matriz[k][j])  # adiciona elemento em V
                L.append(k)  # salva a linha
                C.append(j)  # salva a coluna

    return V, L, C


def Solucao_Iterativo(V, L, C, constante_c, alpha):
    Sn = 1 / (max(L) + 1)
    constante_2 = 1 - alpha
    Y = [1 / (max(L) + 1) for i in range(max(L) + 1)]
    Erro = 1
    iteracoes = 0  # numeros iterações

    while abs(Erro) >= 1e-5:
        Z_k1 = [0 for i in range(max(L) + 1)]

        for k in range(len(L)):
            Z_k1[L[k]] += V[k] * Y[C[k]]

        for i in range(len(Z_k1)):
            Z_k1[i] = Z_k1[i] * constante_2
            Z_k1[i] = Z_k1[i] + (alpha*Sn)

        # Z_k1 == x^(k+1)
        # Y[i] == x^k

        norma_1_diferenca = 0
        for i in range(len(Z_k1)):
            norma_1_diferenca += (abs(Z_k1[i] - Y[i]))
        Erro = (constante_c / (1 - constante_c)) * norma_1_diferenca
        # print("Erro: ",Erro)

        Y = Z_k1[:]

        iteracoes += 1
    # print("soma antes ",sum(Z_k1))
    #for k in range(len(Z_k1)):
        #Z_k1[i] = Z_k1[i] + (alpha * Sn)
    # print("soma depois ",sum(Z_k1))
    # print("ZK1", Z_k1)

    soma_lista = sum(Z_k1)
    # divide os pesos de cada elemento pela soma de todos os pesos
    for k in range(len(Z_k1)):
        Z_k1[k] = Z_k1[k] / soma_lista

    return Z_k1, iteracoes


# Grafo aleatório
def Gera_Grafo_2(X):  # grafo aleatorio
    G = nx.DiGraph()
    # G = Rede()

    for i in range(1, X + 1):  # cria x bolinhas, do 1 até o x
        G.add_node(i)
        # G.adiciona_node(i)

    for k in range(1, X + 1):  # varre os nodes para fazer as ligações
        if X > 3:  # obriga um minimo e um maximo de ligações(evita 1 ou maximo de ligações)
            lista_numero_ligacoes = random.sample(range(1, X + 1), random.randrange(X // 3, ((X - 1) - (X // 3))))
        else:
            lista_numero_ligacoes = random.sample(range(1, X + 1), random.randrange(1, X - 1))

        for j in lista_numero_ligacoes:  # determina com quem o node será ligado
            if k == j:  # se a ligação for com ele mesmo, passa
                pass
            else:
                G.add_edge(k, j)
                # G.adiciona_conexao((k,j))

    for k in range(1, X + 1):
        ligacao_obrigatoria = random.choice([i for i in range(1, X + 1) if i not in [k]])
        G.add_edge(ligacao_obrigatoria, k)
        # G.adiciona_conexao((ligacao_obrigatoria, k))

    Grafo2 = []
    for k in G.edges():
        # for k in G.conjunto_arestas():
        Grafo2.append(list(k))

    n_nodes2 = nx.Graph.number_of_nodes(G)
    # n_nodes2 = G.numero_total_nodes()
    arestas2 = G.edges()
    # arestas2 = G.conjunto_arestas()
    posicao2 = nx.spring_layout(G, dim=3)

    # return Grafo2, n_nodes2, arestas2, posicao2
    return G, n_nodes2, arestas2, posicao2


def funcao(matrizOriginal, matrizEsparsa, numero_nodes, alfa):
    # começa medir o tempo para o metodo de escalonamento
    tempo_inicio = time.time_ns()
    M_M = Matriz_Modificada(numero_nodes, matrizOriginal, alfa)

    # Constante C
    # constante_c = Constante_C(numero_nodes, M_M)

    #### Matriz A
    Matriz_A_subtraida_identidade = Matriz_A(numero_nodes, M_M)

    ### Escalonando
    Matriz_Escalonada = Escalonamento(numero_nodes, Matriz_A_subtraida_identidade)

    ### Encontrando X
    # tempo_inicio = time.time_ns()
    Solucao_Escalonamento = Encontrando_X(numero_nodes, Matriz_Escalonada)
    # para de contar o tempo do escalonamento
    tempo_fim = time.time_ns()

    numeros1, ordenado1 = Ranking(Solucao_Escalonamento)
    tempo = (tempo_fim - tempo_inicio) / 10e9  # tempo passado
    # print("Tempo de execução do Método de Escalonamento (em segundos):", )

    # comça contar tempo para o método iterativo
    tempo_inicio1 = time.time_ns()

    # Vetores V L C
    V, L, C = Vetor_VLC(matrizEsparsa)

    # Constante C
    constante_c = Constante_C(numero_nodes, M_M)

    # Solução Iterativa
    # tempo_inicio1 = time.time_ns()
    Solucao, iteracoes = Solucao_Iterativo(V, L, C, constante_c, alfa)
    # para de contar o tempo para o iterativo
    tempo_fim1 = time.time_ns()

    numeros2, ordenado2 = Ranking(Solucao)
    tempo1 = (tempo_fim1 - tempo_inicio1) / 10e9  # tempo passado
    # print("Tempo de execução do Método Iterativo (em segundos):", )

    tabela(numeros1, ordenado1, numeros2, ordenado2, tempo, tempo1, iteracoes)


def diferenca(Escalonamento, Iterativo):
    diferenca = []
    for k in range(len(Escalonamento)):
        diferenca.append(abs(Escalonamento[k] - Iterativo[k]))
    print("Diferença:", diferenca)


def gera_matriz_inputada(arquivo):
    matriz_inputada = []
    try:
        arq = open(arquivo, "r")  # abre o arquivo
        lines = arq.readlines()  # retorna uma lista que contém cada linha do arquivo como um item da lista
    except:
        return False

    for linha in lines:
        linhas_matriz_inputada = []
        lin = linha[:len(linha) - 1]  # variável que recebe cada linha do arquivo de texto original como uma string
        v = lin.split('\t')  # variável que recebe a linha acima e a transforma em uma lista com n elementos

        for i in range(len(v)):
            linhas_matriz_inputada.append(int(v[i]))
        matriz_inputada.append(linhas_matriz_inputada)

    arq.close()

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


def Ranking(X):  # recebe vetor solução
    X_ordenado = X[:]
    X_ordenado.sort()
    X_ordenado.reverse()

    lista_aux = []
    numeros = []
    ordenado = []

    for k in range(len(X)):
        ind = int(X.index(X_ordenado[k]))
        while ind in lista_aux:
            ind = int(X.index(X_ordenado[k], ind + 1))
        numero_pagina = X.index(X_ordenado[k], ind)  # encontra o indice da primeira ocorrência do valor
        lista_aux.append(ind)
        numeros.append(numero_pagina + 1)
        ordenado.append(X_ordenado[k])

    # ordena classificação (arruma desempate)
    auxiliar = []  # guarda as ligações pra poder ordenar
    for k in range(len(numeros)):
        auxiliar.append([ordenado[k], numeros[k]])

    auxiliar.sort()
    auxiliar.reverse()
    numeros = []
    ordenado = []
    for k in range(len(auxiliar)):  # refaz lista numero e ordenado
        ordenado.append(auxiliar[k][0])
        numeros.append(auxiliar[k][1])

    return numeros, ordenado


def tabela(numeros1, ordenado1, numeros2, ordenado2, tempo, tempo1, iteracoes):
    print("-----------")
    print("Deseja visualizar quantas páginas?")
    print("[1] - Escolher um determinado número de páginas.")
    print("[2] - Todas as páginas.")
    print("[3] - Gerar um arquivo com todas as páginas.")
    resp = input("> ")

    if resp == "1":
        resp = input("Digite o número de páginas (no máximo %i): " % (len(numeros1)))

        print("\nMétodo Escalonamento\t\t| Método Iterativo")
        print("Pos. \t| Pág. \t| Score \t| Pos. \t| Pág. \t| Score \t| Diferença")
        cont = 1
        for i in range(int(resp)):
            print("%.2iº \t| %.2i \t| %.5f \t| %.2iº \t| %.2i \t| %.5f \t| %.3e" % (
            cont, numeros1[i], ordenado1[i], cont, numeros2[i], ordenado2[i],
            decimal.Decimal(abs(ordenado2[i] - ordenado1[i]))))
            cont += 1
        print("Número de iterações do Método Iterativo:", str(iteracoes))
        print("Tempo de execução do Método de Escalonamento (em segundos):", str(tempo))
        print("Tempo de execução do Método Iterativo (em segundos):", str(tempo1))
    elif resp == "2":
        print("\nMétodo Escalonamento\t\t| Método Iterativo")
        print("Pos. \t| Pág. \t| Score \t| Pos. \t| Pág. \t| Score \t| Diferença")
        cont = 1
        for i in range(len(numeros1)):
            print("%.2iº \t| %.2i \t| %.5f \t| %.2iº \t| %.2i \t| %.5f \t| %.3e" % (
            cont, numeros1[i], ordenado1[i], cont, numeros2[i], ordenado2[i],
            decimal.Decimal(abs(ordenado2[i] - ordenado1[i]))))
            cont += 1
        print("Número de iterações do Método Iterativo:", str(iteracoes))
        print("Tempo de execução do Método de Escalonamento (em segundos):", str(tempo))
        print("Tempo de execução do Método Iterativo (em segundos):", str(tempo1))
    else:
        with open("ranking.txt", "w", encoding="utf-8") as file:
            file.write("Método Escalonamento\t\t| Método Iterativo")
            file.write("\nPos. \t| Pág. \t| Score \t| Pos. \t| Pág. \t| Score \t| Diferença")
            cont = 1
            for i in range(len(numeros1)):
                file.write("\n%.2iº \t| %.2i \t| %.5f \t| %.2iº \t| %.2i \t| %.5f \t| %.3e" % (
                cont, numeros1[i], ordenado1[i], cont, numeros2[i], ordenado2[i],
                decimal.Decimal(abs(ordenado2[i] - ordenado1[i]))))
                cont += 1
            file.write("\nNúmero de iterações do Método Iterativo: %s" % (str(iteracoes)))
            file.write("\nTempo de execução do Método de Escalonamento (em segundos): %s" % str(tempo))
            file.write("\nTempo de execução do Método Iterativo (em segundos): %s" % (str(tempo1) + "\n"))

        print("O arquivo com o ranking foi criado com o nome: ranking.txt")


###########################################################
# App github
def main():
    print("\t" + "-" * 30)
    print("\tProjeto PageRank\n")
    print("\tEscolha uma opção:")
    print("\t[1] - Rede cacique-tribo")
    print("\t[2] - Rede aleatória")
    print("\t[3] - Importar arquivo")
    print("\t[0] - Sair do programa")

    resposta = ""
    while resposta == "":
        try:
            resposta = int(input("> "))
        except:
            print("Valor não númerico ou opção inválida.")
            continue

    if resposta == 0:
        print("Saindo do programa...")
        exit()
    elif resposta == 1:
        print("\nModelo Cacique-Tribo")
        k = ""
        while k == "":
            try:
                # alfa q será passado como parametro para as funções
                alpha = input("\nInsira um valor de alpha entre 0 e 1  (aperte enter para alpha padrão 0.15): ")
                for letra in alpha.lower():
                    if letra in string.ascii_lowercase:
                        assert ()

                if alpha == "":
                    alpha = 0.15
                if float(alpha) < 0 or float(alpha) > 1:
                    print("Valor não númerico ou negativo.")
                    print("Valor do alpha precisa estar entre 0 e 1.")
                    continue
                k = input("Digite o número de caciques: ")
                if int(k) < 1:
                    k = ""
                    print("Valor não númerico ou negativo.")
                    continue
            except:
                k = ""
                print("Valor não númerico ou negativo.")
                continue

        # Gerando o grafo cacique.
        grafo = GeraGrafo(k)
        grafo.listaNodeCacique()
        grafo.criaGrafo()
        numero_nodes = grafo.n_nodes()
        posicao = grafo.posicao()
        arestas = grafo.arestas()

        # Gerando a matriz com base no grafo.
        gera = GeraMatriz(grafo, numero_nodes, arestas)
        matriz = gera.geraMatriz()
        Matriz_Esparsa = []  # copiando matriz esparsa para fazer VLC
        Matriz_Esparsa = gera.geraMatriz()[:]

        funcao(matriz, Matriz_Esparsa, numero_nodes, float(alpha))


    elif resposta == 2:
        print("\nModelo Grafo Aleatório")
        k = ""
        while k == "":
            try:
                alpha = input("\nInsira um valor de alpha entre 0 e 1 (aperte enter para alpha padrão 0.15): ")
                for letra in alpha.lower():
                    if letra in string.ascii_lowercase:
                        assert ()

                if alpha == "":
                    alpha = 0.15
                if float(alpha) < 0 or float(alpha) > 1:
                    print("Valor não númerico, negativo ou opção inválida.")
                    print("Valor do alpha precisa estar entre 0 e 1.")
                    continue

                k = input("Digite o número de páginas: ")
                if int(k) < 1:
                    k = ""
                    print("Valor não númerico ou negativo.")
                    continue
            except:
                k = ""
                print("Valor não númerico ou negativo.")
                continue

        # Gerando o grafo aleatório.
        grafo2, n_nodes2, arestas2, posicao2 = Gera_Grafo_2(int(k))

        # Gerando a matriz com base no grafo.
        gera2 = GeraMatriz(grafo2, n_nodes2, arestas2)
        matriz2 = gera2.geraMatriz()
        matriz_esparsa2 = gera2.geraMatriz()[:]

        funcao(matriz2, matriz_esparsa2, n_nodes2, float(alpha))

    elif resposta == 3:
        print("\nImportação de Arquivo")
        nome_arq = ""
        while nome_arq == "":
            try:
                alpha = input("\nInsira um valor de alpha entre 0 e 1 (aperte enter para alpha padrão 0.15): ")
                for letra in alpha.lower():
                    if letra in string.ascii_lowercase:
                        assert ()
                if alpha == "":
                    alpha = 0.15
                if float(alpha) < 0 or float(alpha) > 1:
                    print("Valor não númerico, negativo ou opção inválida.")
                    print("Valor do alpha precisa estar entre 0 e 1.")
                    continue

                nome_arq = input("Digite o nome do arquivo: ")
            except:
                print("Valor não númerico ou negativo.")
                continue

        # Gera a matriz inputada
        matriz = gera_matriz_inputada(nome_arq)

        # Se for retornado False, ficará em loop até encontrar o arquivo com nome correto.
        while matriz == False:
            print("Arquivo não encontrado.\n")
            nome_arq = input("Digite o nome do arquivo: ")
            matriz = gera_matriz_inputada(nome_arq)

        # Cria a matriz esparsa
        matriz_esparsa = matriz[:]
        numero_nodes = len(matriz[0])  # Número de nós (com base no número de colunas)

        funcao(matriz, matriz_esparsa, numero_nodes, float(alpha))
    print("-" * 10)


if __name__ == "__main__":
    while True:
        main()
        resp = input("Deseja executar novamente? [S/N] ")
        if resp.lower() == "s":
            continue
        else:
            break