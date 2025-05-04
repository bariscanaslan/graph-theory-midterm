import networkx as nx
import matplotlib.pyplot as plt

def is_complete_graph(G):
    n = len(G.nodes)
    return G.number_of_edges() == n * (n - 1) // 2

def is_odd_cycle(G):
    return nx.is_connected(G) and G.number_of_nodes() % 2 == 1 and all(deg == 2 for _, deg in G.degree())

def brook_theorem_check(G):
    max_degree = max(dict(G.degree()).values())
    chromatic_number = nx.coloring.greedy_color(G, strategy='largest_first')
    used_colors = set(chromatic_number.values())

    print("Max Degree (Δ):", max_degree)
    print("Chromatic Number (χ):", len(used_colors))

    if nx.is_connected(G) and not is_complete_graph(G) and not is_odd_cycle(G):
        if len(used_colors) <= max_degree:
            print("Brook's Theorem is satisfied.")
        else:
            print("Brook's Theorem is violated!")
    else:
        print("This graph may be an exceptional case where Brook's Theorem does not apply.")

    # Optional: plot
    color_map = [chromatic_number[node] for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=color_map, cmap=plt.cm.tab20)
    plt.title("Graph Coloring Visualization")
    plt.show()

# Example 1: Random Graph
G1 = nx.erdos_renyi_graph(n=8, p=0.4)
brook_theorem_check(G1)

# Example 2: Complete Graph
G2 = nx.complete_graph(5)
brook_theorem_check(G2)

# Example 3: Odd Cycle
G3 = nx.cycle_graph(5)
brook_theorem_check(G3)
