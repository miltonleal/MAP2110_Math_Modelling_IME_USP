import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
##############################################
# Models github
# from .core import GeraMatriz

import networkx as nx


class GeraGrafo:
    def __init__(self, k):
        self.caciques = []
        self.caciques2 = []
        self.tamanho = k

    def listaNodeCacique(self):
        cont = 0
        for j in range(1, int(self.tamanho) + 1):
            self.caciques.append(j + cont)
            self.caciques2.append(j + cont)
            cont = cont + j

        print("O número dos nodes de cada cacique é", self.caciques)

    def criaGrafo(self):
        self.grafo = nx.DiGraph()
        self.grafo.add_nodes_from(self.caciques)

        count = 0
        for i in self.caciques:
            count = count + 1
            for p in self.caciques[count:]:
                self.grafo.add_edge(i, p)
                self.grafo.add_edge(p, i)

        cont = 1
        while len(self.caciques) != 0:
            for t in self.caciques:
                self.grafo.add_edge(t, t + cont)
                self.grafo.add_edge(t + cont, t)
            del self.caciques[0]
            cont = cont + 1

        nova_lista = []
        for i in self.grafo.edges():
            x = list(i)
            if (x[0] and x[1]) in self.caciques2:
                continue
            elif x[0] in self.caciques2 and x[1] not in nova_lista:
                nova_lista.append([x[1], x[0]])
            elif x[1] in self.caciques2 and x[0] not in nova_lista:
                nova_lista.append([x[1], x[0]])

        for i in self.caciques2:
            list2 = []
            for x in nova_lista:
                if x[1] == i:
                    list2.append(x[0])
            for x in range(len(list2) - 1):
                for k in range(x, len(list2)):
                    if list2[x] != list2[k]:
                        self.grafo.add_edge(list2[x], list2[k])
                        self.grafo.add_edge(list2[k], list2[x])

        return self.grafo

    def n_nodes(self):
        return self.grafo.number_of_nodes()

    def arestas(self):
        return self.grafo.edges()


#####################################################
# Core github

class GeraMatriz:
    def __init__(self, grafo, n_nodes, arestas):
        self.n_nodes = n_nodes
        self.grafo = grafo
        self.arestas = arestas

    def geraMatriz(self):
        grafo_lista = []
        for k in self.arestas:
            grafo_lista.append(list(k))

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
# Vier github
"""    
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
"""


class GeraVisualizacao:
    def __init__(self, G, n_nodes):
        self.grafo = G
        self.posicao = nx.spring_layout(self.grafo, dim=3)
        self.n_nodes = n_nodes

    def gera3d(self):
        maior_aresta = max([self.grafo.degree(i) for i in range(1, self.n_nodes + 1)])
        cores_nos = [plt.cm.plasma(self.grafo.degree(i) / maior_aresta) for i in range(1, self.n_nodes + 1)]

        with plt.style.context(('ggplot')):
            quadro = plt.figure()
            eixo3d = Axes3D(quadro)

            for chave, valor in pos.items():
                xi = value[0]
                yi = value[1]
                zi = value[2]

                eixo3d(xi, yi, zi, c=np.array(cores_nos[key - 1]).reshape(1, -1), s=10 + 10 * self.grafo.degree(key),
                       edgecolors='k', alpha=0.7)

            for i, j in enumerate(self.grafo.edges()):
                x = np.array((self.posicao[j[0]][0], self.posicao[j[1]][0]))
                y = np.array((self.posicao[j[0]][1], self.posicao[j[1]][1]))
                z = np.array((self.posicao[j[0]][2], self.posicao[j[1]][2]))

                eixo3d.plot(x, y, z, c='black', alpha=0.5)

        eixo3d.set_axis_off()
        plt.show()
        return


class MostraMatriz:
    def __init__(self, matriz):
        self.matriz = matriz

    def mostraMatriz(self):
        print("\n")
        for i in range(len(self.matriz)):
            for k in range(len(self.matriz)):
                print("%4.2f" % self.matriz[i][k], " ", end='')
            print("")


#######################################################
# Matriz Modificada


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


###CRIANDO MATRIZ A

def Matriz_A(N,M_M):

    matriz_A = []
    matriz_A[:] = M_M[:]

    for k in range (N):
        matriz_A[k][k] = matriz_A[k][k] - 1

    return matriz_A

def Escalonamento(N, matriz_A):

    for k in range (N):

        maximo_absoluto = abs(matriz_A[0][k])
        indice_absoluto = 0
        for l in range (1, N):
            if indice_absoluto != l and abs(matriz_A[l][k]) >= maximo_absoluto:
                maximo_absoluto = abs(matriz_A[l][k])
                indice_absoluto = l
        #print ("maximo absoluto",maximo_absoluto)
        #print("indice absoluto", indice_absoluto)
        # a = matriz_A.index(max(matriz_A, key=lambda x: abs(x[k])))
        # maximo = max(matriz_A[k])

        print("valor do indice:", indice_absoluto)
        if abs(matriz_A[indice_absoluto][k]) >= abs(matriz_A[k][k]):
            print("matriz indice absoluto", matriz_A[indice_absoluto])

            matriz_A[indice_absoluto], matriz_A[k] = matriz_A[k], matriz_A[indice_absoluto]

            print("matriz indice absoluto depois", matriz_A[indice_absoluto])
        for i in range(k + 1, N):
            alpha_i = matriz_A[i][k] / matriz_A[k][k]
            for j in range(k, N):
                matriz_A[i][j] = matriz_A[i][j] - (alpha_i * matriz_A[k][j])
    return matriz_A


#def Encontrando_X(N,matriz_escalonada):"

    #for k in range (N,0,-1):
        #x_k =






###########################################################
# App github
"""
from models import GeraGrafo
from core import GeraMatriz
from views import MostraMatriz
"""


def main():
    k = input("Digite o k: ")
    grafo = GeraGrafo(k)
    grafo.listaNodeCacique()
    grafo.criaGrafo()
    n_nodes = grafo.n_nodes()
    arestas = grafo.arestas()

    gera = GeraMatriz(grafo, n_nodes, arestas)
    matriz = gera.geraMatriz()

    print(MostraMatriz(matriz).mostraMatriz())

    #################
    M_M = Matriz_Modificada(n_nodes, matriz)
    # printa linha por linha com duas casas decimais
    print(MostraMatriz(M_M).mostraMatriz())

    #### Matriz A
    Matriz_A_subtraida_identidade = Matriz_A(n_nodes,M_M)
    # printa linha por linha com duas casas decimais
    print(MostraMatriz(Matriz_A_subtraida_identidade).mostraMatriz())

    ### Escalonando
    Matriz_Escalonada = Escalonamento(n_nodes, Matriz_A_subtraida_identidade)
    #print("O valor de a",Escalonamento(n_nodes, Matriz_A_subtraida_identidade))
    print(MostraMatriz(Matriz_Escalonada).mostraMatriz())

    print(n_nodes)

if __name__ == "__main__":
    main()
    #########