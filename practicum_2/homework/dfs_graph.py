import queue
from typing import Any

import networkx as nx

from src.plotting import plot_graph


def visit(node: Any):
    print(f"Wow, it is {node} right here!")


def dfs_iterative(G: nx.Graph, node: Any):
    visited = {n: False for n in G}

    q = queue.LifoQueue()
    q.put(node)

    while not q.empty():
        t_node = q.get()
        if visited[t_node] != True:
            visit(t_node)
            visited[t_node] = True

        for i in G.neighbors(t_node):
            if visited[i] != True:
                q.put(i)


def topological_sort(G: nx.DiGraph, node: Any):
    visited = {n: False for n in G}

    q = queue.LifoQueue()
    q.put(node)

    while not q.empty():
        t_node = q.get()
        if visited[t_node] != True:
            flg = True
            for i in G.predecessors(t_node):
                if visited[i] != True:
                    flg = False
            if flg:
                visit(t_node)
                visited[t_node] = True

        for i in G.neighbors(t_node):
            if visited[i] != True:
                q.put(i)


if __name__ == "__main__":
    # Load and plot the graph
    G = nx.read_edgelist("graph_2.edgelist", create_using=nx.Graph)
    # plot_graph(G)

    print("Iterative DFS")
    print("-" * 32)
    dfs_iterative(G, node="0")
    print()

    G = nx.read_edgelist(
        "graph_2.edgelist", create_using=nx.DiGraph
    )
    plot_graph(G)
    print("Topological sort")
    print("-" * 32)
    topological_sort(G, node="0")
