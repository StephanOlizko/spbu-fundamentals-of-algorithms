from typing import Any

import networkx as nx
import numpy as np
import heapq

from src.plotting import plot_graph


def dijkstra_sp(G: nx.Graph, source_node="0") -> dict[Any, list[Any]]:
    shortest_paths = {node: [] for node in G.nodes()}  # key = destination node, value = list of intermediate nodes

    distances = {node: np.Inf for node in G.nodes()}
    distances[source_node] = 0

    prqueue = [(0, source_node)]
    heapq.heapify(prqueue)

    while prqueue:
        min_dist, min_node = heapq.heappop(prqueue)

        if min_dist > distances[min_node]:
            continue

        shortest_paths[min_node].append(min_node)

        #Обновляем расстояния до соседних вершин
        for neighbor in G.neighbors(min_node):
            new_dist = distances[min_node] + G.edges[min_node, neighbor]['weight']

            #Если новое расстояние меньше текущего, то обновляем текущее и добавляем соседнюю вершину в очередь
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(prqueue, (new_dist, neighbor))
                shortest_paths[neighbor] = shortest_paths[min_node] + [min_node]

    #Добавляем начальную вершину в качестве первого элемента в список кратчайшего пути для каждой вершины
    for node in G.nodes():
        if node == source_node:
            shortest_paths[node] = []
        else:
            shortest_paths[node].append(node)

    return shortest_paths


if __name__ == "__main__":
    G = nx.read_edgelist("graph_1.edgelist", create_using=nx.Graph)
    plot_graph(G)
    shortest_paths = dijkstra_sp(G, source_node="0")
    test_node = "4"
    shortest_path_edges = [
        (shortest_paths[test_node][i], shortest_paths[test_node][i + 1])
        for i in range(len(shortest_paths[test_node]) - 1)
    ]
    plot_graph(G, highlighted_edges=shortest_path_edges)
