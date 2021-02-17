import networkx as nx
import random
import matplotlib.pyplot as plt



def Gera_Grafo_2():

    X = int(input("digite x: "))

    G = nx.DiGraph()

    for i in range(1, X+1): #cria x bolinhas, do 1 até o x
        G.add_node(i)

    for k in range (1, X+1): #varre os nodes para fazer as ligações
        lista_numero_ligacoes = random.sample(range(1, X+1), random.randrange(1,X-1))
        for j in lista_numero_ligacoes: # determina com quem o node será ligado
            if k == j: #se a ligação for com ele mesmo, passa
                pass
            else:
                G.add_edge(k,j)

    for k in range (1,X+1):
        ligacao_obrigatoria = random.choice([i for i in range (1,X+1) if i not in [k]])
        G.add_edge(ligacao_obrigatoria, k)


    nx.draw (G, with_labels=1)
    plt.show()

    Grafo2 = []
    for k in G.edges():
        Grafo2.append(list(k))

    return Grafo2

print (Gera_Grafo_2())










