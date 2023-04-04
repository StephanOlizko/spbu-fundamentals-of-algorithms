from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import heapq

from src.plotting import plot_graph


def prim_mst(G: nx.Graph, start_node="0") -> set[tuple[Any, Any]]:
    mst_set = set()  # set of nodes included into MST
    rest_set = set(G.nodes())  # set of nodes not yet included into MST
    mst_edges = set()  # set of edges constituting MST

    #Словарь соседей для каждой вершины: ключи - вершины, значения - списки кортежей (node_neighbour, weight)
    graph = {}
    for graph_node in G.nodes():
        graph[graph_node] = list()
        for node_neighbour in G.neighbors(graph_node):
            graph[graph_node].append((node_neighbour, G.get_edge_data(graph_node, node_neighbour)['weight']))

    #Куча из модуля heapq для нахождения минимального ребра
    #Значения представлены в таком виде (значение приоритета, начальный узел ребра, конечный узел ребра)
    heap = []
    heapq.heapify(heap)
    heap = [(0, start_node, start_node)]

    while heap:
        #Извлекаем минимальное ребро из кучи
        min_edge = heapq.heappop(heap)
        if min_edge[2] in mst_set:
            continue

        #Добавляем минимальное ребро в MST и помечаем соответствующие вершины как добавленные
        mst_edges.add((min_edge[1], min_edge[2]))
        mst_set.add(min_edge[2])

        #Добавляем смежные ребра из новой вершины
        for graph_node_next, weight in graph[min_edge[2]]:
            if graph_node_next not in mst_set:
                heapq.heappush(heap, (weight, min_edge[2], graph_node_next))

    return mst_edges


if __name__ == "__main__":
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    mst_edges = prim_mst(G, start_node="0")
    plot_graph(G, highlighted_edges=list(mst_edges))
