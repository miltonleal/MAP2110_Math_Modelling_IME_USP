import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
# from .core import GeraMatriz
# !/usr/bin/python3
#####################
# Core github
import networkx as nx


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

        print("O número dos nodes de cada cacique é", self.caciques)

    def criaGrafo(self):
        self.grafo = nx.DiGraph()  # Inicia o grafo.
        self.grafo.add_nodes_from(self.caciques)  # Adiciona os nós dos caciques.

        count = 0
        for i in self.caciques:  # Percorre a lista dos caciques para fazer a conexão entre os mesmos.
            count = count + 1
            for p in self.caciques[count:]:  # Percorre de count pra frente.
                self.grafo.add_edge(i, p)  # Cria uma conexão (aresta) entre i e p.
                self.grafo.add_edge(p, i)  # Cria uma conexão (aresta) entre p e i.
                # Aqui é importante fazer duas conexões, pois as conexões no grafo
                # cacique-tribo são dadas por conexões mútuas.

        cont = 1
        while len(self.caciques) != 0:
            for t in self.caciques:  # Faz a conexão entre os caciques e os respectivos índios.
                self.grafo.add_edge(t, t + cont)
                self.grafo.add_edge(t + cont, t)
            del self.caciques[0]
            cont = cont + 1

        nova_lista = []  # Cria uma nova lista que guardará os índios.
        for i in self.grafo.edges():  # Percorre todas as conexões.
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
                        self.grafo.add_edge(list2[k], list2[z])  # Liga um índio ao outro.

        return self.grafo  # Retorna o grafo.

    def n_nodes(self):  # Gera o número de nodes (nós) existentes no grafo.
        return self.grafo.number_of_nodes()

    def arestas(self):  # Gera as arestas (conexões) existentes no grafo.
        return self.grafo.edges()

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

        for i in range(1, self.n_nodes + 1):
            for k in range(len(grafo_lista)):
                if grafo_lista[k][0] == i:
                    matriz[grafo_lista[k][1] - 1][i - 1] = 1

        for k in range(len(matriz)):
            cont = 0
            for j in range(len(matriz)):
                if matriz[j][k] == 1:
                    cont += 1
            for i in range(len(matriz)):
                if matriz[i][k] == 1:
                    matriz[i][k] = 1 / cont

        return matriz


############################################################
# !/usr/bin/python3
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
        timeout.start()  # Começa o contagem de tempo (10 segundos).
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


def Matriz_Modificada(N, Matriz):  # N=numero de nodes
    alfa = 0.15
    alfa_Sn = alfa * 1 / N  # elementos da Matriz Sn
    M_M = []  # Matriz Modificada
    M_M[:] = Matriz[:]

    for k in range(N):
        for i in range(N):  # MM = (1 - alfa)M + alfa*Sn
            M_M[k][i] = (1 - alfa) * M_M[k][i] + alfa_Sn

    """
    #Matriz Modificada  Visualização com mais casas decimais
    print("\n")
    for i in range(len(M_M)):
        for k in range(len(M_M)):
            #altere %4.4 pra imprimir com mais casas decimais
            #printa linha por linha com 4 casas decimais
            print("%4.4f" % M_M[i][k], " ", end ='')
        print("")
    """

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

        for l in range(1, N):  # varre as linhas
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
    x_n = 1  # define o vetor da linha de zeros como 1
    lista_x_k = [x_n]  # cria lista que receberá o peso das páginas (x_k)
    for k in range(N - 2, -1, -1):  # inicia na penúltima coluna e vai até a primeira
        x_k = 0  # inicia a soma do x_k, que é o vetor em questão que está sendo calculado
        for i in range(k + 1, N):  # varre as colunas da linha que está sendo calculada
            # multiplica o pivô pelo elemento à direita e soma na x_k
            x_k += matriz_escalonada[k][i] * matriz_escalonada[k][k]
        # divide a soma total do x_k pelo elemento pivô
        x_k = -(x_k) / matriz_escalonada[k][k]
        # adiciona o valor do peso de x_k à lista de pesos
        lista_x_k.append(x_k)

    # NORMALIZAÇÃO

    soma_lista = sum(lista_x_k)

    # divide os pesos de cada elemento pela soma de todos os pesos
    for k in range(len(lista_x_k)):
        lista_x_k[k] = lista_x_k[k] / soma_lista

    # inverte a ordem da lista para ter o x_1 como primeiro elemento indo até o x_n
    lista_x_k.reverse()

    print("\nSolução Escalonamento", lista_x_k)
    print("\nSoma: ", sum(lista_x_k))


# DEFININDO A CONSTANTE C

def Constante_C(numero_nodes, M_M):
    lista_max = []
    min_coluna = M_M[0][0]
    print("M_M[0][0]", min_coluna)

    for j in range(numero_nodes):
        for i in range(numero_nodes):
            if M_M[i][j] < min_coluna:
                min_coluna = M_M[i][j]
        lista_max.append(abs(1 - (2 * min_coluna)))
    print("lista com os elementos performados de cada coluna", lista_max)
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

    # print("\nV: ",V)
    # print("L", L)
    # print("C", C)

    return V, L, C


def Solução_Iterativo(V, L, C, constante_c):
    Z_k1 = [0 for i in range(max(L) + 1)]  # inicia nulo com tamanho n da matriz nxn
    # Y = 1/(len(Z_k1))
    Y = [1 / len(Z_k1) for i in range(len(Z_k1))]

    Erro = 1

    Z_k = [1 / len(Z_k1) for i in range(len(Z_k1))]

    cont = 0
    while abs(Erro) >= 1e-5:

        cont += 1
        if cont > 50:
            break

        Z_k1 = [0 for i in range(max(L) + 1)]

        # print("Z_K = ", Z_k)
        # print("Y = ", Y)

        for k in range(len(L)):
            # if type(Y) != list:
            #    Z_k1[L[k]] = Z_k1[L[k]] + V[k]*Y
            #    continue
            Z_k1[L[k]] = Z_k1[L[k]] + V[k] * Y[C[k]]
        # print("Z_K1 = ", Z_k1)
        Y = Z_k1[:]

        norma_1_diferenca = 0
        for i in range(len(Z_k1)):
            norma_1_diferenca += (Z_k1[i] - Z_k[i])
        Erro = (constante_c / (1 - constante_c)) * norma_1_diferenca

        print("\nErro =", Erro)

        Z_k[:] = Z_k1[:]

    # print("\nsoma Z_k1 = ",sum(Z_k1))
    return Z_k1


# Grafo aleat´roio
def Gera_Grafo_2(X):  # grafo aleatorio
    G = nx.DiGraph()

    for i in range(1, X):
        G.add_node(i + 1)

    for i in range(X + 1):
        lig = random.randint(0, 1)
        for j in range(X):
            if j == i:
                lig = 0
            if j == X // 2:
                G.add_edge(i, j)
            if j != i and j != X / 2:
                if lig == 1:
                    G.add_edge(i, j)

    nx.draw(G, with_labels=1)
    plt.show()

    Grafo2 = []
    for k in G.edges():
        Grafo2.append(list(k))

    n_nodes2 = nx.Graph.number_of_nodes(G)
    arestas2 = G.edges()
    posicao2 = nx.spring_layout(G, dim=3)

    return Grafo2, n_nodes2, arestas2, posicao2


###########################################################
# App github

def main():
    try:
        print("\nPageRank - Projeto Modelagem\n")
        k = int(input("Digite o número de caciques: "))
    except:
        print("Apenas valores inteiros.")
        exit()

    # Gerando o grafo cacique.
    grafo = GeraGrafo(k)
    grafo.listaNodeCacique()
    grafo.criaGrafo()
    numero_nodes = grafo.n_nodes()
    arestas = grafo.arestas()
    posicao = grafo.posicao()

    # Exibindo o grafo cacique em 3D.
    #print("A visualização será exibida por 10 segundos.")
    #mostra = MostraVisualizacao(vars(grafo)['grafo'], numero_nodes, posicao, arestas)
    #mostra.gera3d()

    # Gerando a matriz com base no grafo.
    gera = GeraMatriz(grafo, numero_nodes, arestas)
    matriz = gera.geraMatriz()
    Matriz_Esparsa = []  # copiando matriz esparsa para fazer VLC
    Matriz_Esparsa = gera.geraMatriz()[:]

    # Exibindo a matriz.
    #MostraMatriz(matriz).mostraMatriz()

    ####################################

    M_M = Matriz_Modificada(numero_nodes, matriz)
    # printa linha por linha com duas casas decimais
    #print(MostraMatriz(M_M).mostraMatriz())

    # Constante C
    constante_c = Constante_C(numero_nodes, M_M)
    print("Esta é a constante C", constante_c)

    #### Matriz A
    Matriz_A_subtraida_identidade = Matriz_A(numero_nodes, M_M)
    # printa linha por linha com duas casas decimais
    print(MostraMatriz(Matriz_A_subtraida_identidade).mostraMatriz())

    ### Escalonando
    Matriz_Escalonada = Escalonamento(numero_nodes, Matriz_A_subtraida_identidade)
    # print("O valor de a",Escalonamento(n_nodes, Matriz_A_subtraida_identidade))
    print(MostraMatriz(Matriz_Escalonada).mostraMatriz())

    ### Encontrando X
    Encontrando_X(numero_nodes, Matriz_Escalonada)

    # Vetores V L C
    V, L, C = Vetor_VLC(Matriz_Esparsa)
    #print("\nV:", V)
    #print("\nL:", L)
    #print("\nC:", C)

    # Solução Iterativa
    Solução = Solução_Iterativo(V, L, C, constante_c)
    print("\nvetor solução do modo iterativo", Solução)
    print("\nSoma solução interativa: ", sum(Solução))

    #########################################################

    # Grafo 2 - Aleatório
    X = int(input("\n\nNúmero de sites grafo aleatório: "))
    grafo2, n_nodes2, arestas2, posicao2 = Gera_Grafo_2(X)

    """
    # Gerando a matriz com base no grafo.
    gera2 = GeraMatriz(grafo2, n_nodes2, arestas2)
    matriz2 = gera2.geraMatriz()

    # Exibindo o grafo em 3D.
    print("A visualização será exibida por 10 segundos.")
    mostra = MostraVisualizacao(vars(grafo2)['grafo2'], n_nodes2, posicao2, arestas2)
    mostra.gera3d()
    """


if __name__ == "__main__":
    main()
    #########