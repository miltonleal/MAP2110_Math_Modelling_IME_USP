import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def gera_grafo(k):
    lista_caciques = []

    cont = 0
    for j in range (1,k+1):
        lista_caciques.append(j+cont) # Cria lista com o número dos nodes dos caciques.
        cont = cont + j

    lista = [] # Cria uma nova lista para os caciques.
    for i in lista_caciques:
        lista.append(i)

    aux_lista = lista_caciques
    aux2_lista = lista_caciques

    print ("O número dos nodes de cada cacique é", lista_caciques)

    G = nx.DiGraph() # Cria um digrafo vazio.

    G.add_nodes_from(lista_caciques) # Adiciona os nodes dos caciques.

    # Cria link entre os caciques.
    count = 0
    for i in aux2_lista:
        count = count + 1
        for p in aux2_lista[count:]:
                G.add_edge(i,p)
                G.add_edge(p,i)

    # Cria link entre os caciques e os índios respectivos.
    cont = 1
    while len(aux_lista) != 0:
        for t in aux_lista:
                G.add_edge(t,t+cont)
                G.add_edge(t+cont,t)
        del aux_lista[0]
        cont = cont + 1

    nova_lista = [] # Vai conter os pares ordenados rearranjados.
    for i in G.edges(): # Percorre a lista com todas as conexões do grafo.
        x = list(i) # x vai receber uma conexão do grafo como uma lista.
        if (x[0] and x[1]) in lista: # Se os dois valores do par ordenado forem caciques, então não é feito nada.
            continue
        # Se o primeiro valor do par ordenado for cacique e o segundo valor do par ordenado não estiver na lista de rearranjo
        # Então a lista de rearranjo é appendada com o cacique na segunda posição do par ordenado (aqui há uma troca no par ordenado).
        if x[0] in lista and x[1] not in nova_lista:
            nova_lista.append([x[1], x[0]])
        # Se o segundo valor do par ordenado for cacique e o primeiro valor do par ordenado não estiver na lista de rearranjo
        # Então a lista de rearranjo é appendada com o cacique na segunda posição do par ordenado (aqui a ordem do par ordenado é mantida).
        if x[1] in lista and x[0] not in nova_lista:
            nova_lista.append([x[0], x[1]])

    # Percerre a lista de caciques.
    for i in lista:
        list2 = [] # Cria uma nova lista para separar todos as conexões de um só cacique.
        # Percorre a lista que contém os pares ordenados rearranjados
        # E verifica se o segundo valor do par ordenado é realmente o cacique procurado.
        # Se for, então o primeiro valor do par ordenado é appendado na lista de conexões do cacique.
        for x in nova_lista:
            if x[1] == i:
                list2.append(x[0])
        # Percorre a lista de conexões do cacique inteiramente e faz todas as "pontes" entre todas as conexões do cacique.
        for x in range(len(list2)-1):
            for k in range(x, len(list2)):
                if list2[x] != list2[k]: # Só irá criar as pontes se os elementos forem diferentes um do outro.
                    # Aqui não é precisa fazer duas pontes, fiz mas depois explico o por quê.
                    G.add_edge(list2[x],list2[k])
                    G.add_edge(list2[k],list2[x])

    return G

def gera_visualizacao(G):
    # Posições de cada nó do grafo no espaço.
    pos = nx.spring_layout(G, dim=3)

    # Número total de nós.
    numero_nodes = G.number_of_nodes()

    # Nó/cacique que contém maior número de índios conectados.
    maior_aresta = max([G.degree(i) for i in range(1,numero_nodes+1)])

    # Cria a cor dos nós cm base na fórmula: (número de arestas)/maior número de aresta de um nó.
    cores_nos = [plt.cm.plasma(G.degree(i)/maior_aresta) for i in range(1, numero_nodes+1)]

    with plt.style.context(('ggplot')):
        # Cria um quadro para o gráfico e inicia o Axes3D nesse quadro.
        fig = plt.figure()
        ax = Axes3D(fig)

        # Percorre o dicionário pos e extrai as coordenadas xyz de cada nó.
        for key, value in pos.items():
            xi = value[0]
            yi = value[1]
            zi = value[2]

            # Cria os nós.
            ax.scatter(xi, yi, zi, c=cores_nos[key-1], s=10+10*G.degree(key), edgecolors='k', alpha=0.7)

        # É feito um loop na lista de arestas para obter as coordenadas x, y, z, dos nós conectados
        # Esses dois pontos são os extremos da linha a ser plotada.
        for i,j in enumerate(G.edges()):
            x = np.array((pos[j[0]][0], pos[j[1]][0]))
            y = np.array((pos[j[0]][1], pos[j[1]][1]))
            z = np.array((pos[j[0]][2], pos[j[1]][2]))

            # Conectando os nós
            ax.plot(x, y, z, c='black', alpha=0.5)

    # Esconde os eixos.
    ax.set_axis_off()

    # Mostra o gráfico.
    plt.show()

    return

def main():
    k = int(input("Digite o número de caciques: "))
    grafo = gera_grafo(k)
    gera_visualizacao(grafo)

if __name__ == "__main__":
    main()

