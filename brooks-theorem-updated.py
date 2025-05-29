import networkx as nx
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

import numpy as np
import os

# ---------- Brook's Theorem Helpers ----------

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

# ---------- Visualization Function ----------

def save_graph_image(G, coloring, filename, show_plot=False, window_title="Graph"):
    fig = plt.figure(figsize=(8, 6))
    color_map = [coloring[node] for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=color_map, cmap=plt.cm.tab20, node_size=300, font_size=8)
    plt.title("Graph Coloring Visualization")

    if show_plot:
        try:
            fig.canvas.manager.set_window_title(window_title)
        except Exception as e:
            print("Window title could not be set:", e)

    plt.savefig(filename)

    if show_plot:
        plt.show()

    plt.close()



# ---------- Multiple Realization Test ----------

def run_multiple_realizations(model='watts', N=50, realizations=50):
    violations = 0
    chromatic_numbers = []
    max_degrees = []

    output_dir = f"output_graphs/{model}"
    os.makedirs(output_dir, exist_ok=True)

    for i in range(realizations):
        if model == 'watts':
            G = nx.watts_strogatz_graph(N, k=4, p=0.3)
        elif model == 'barabasi':
            G = nx.barabasi_albert_graph(N, m=2)
        else:
            raise ValueError("Model should be 'watts' or 'barabasi'")

        max_deg = max(dict(G.degree()).values())
        coloring = nx.coloring.greedy_color(G, strategy='largest_first')
        chromatic = len(set(coloring.values()))

        chromatic_numbers.append(chromatic)
        max_degrees.append(max_deg)

        if nx.is_connected(G) and not is_complete_graph(G) and not is_odd_cycle(G):
            if chromatic > max_deg:
                violations += 1

        if i % 10 == 0:
            filename = os.path.join(output_dir, f"{model}_{i}.png")
            title = f"{model.title().replace('-', ' ')} Realization #{i}"
            save_graph_image(G, coloring, filename, show_plot=True, window_title=title)

    print(f"\nModel: {model.upper()}")
    print(f"Average Chromatic Number (χ̄): {np.mean(chromatic_numbers):.2f} ± {np.std(chromatic_numbers):.2f}")
    print(f"Average Max Degree (Δ̄): {np.mean(max_degrees):.2f} ± {np.std(max_degrees):.2f}")
    print(f"Number of Violations of Brooks' Theorem: {violations}/{realizations}")
    print("-" * 50)

# ---------- Run Final Project Tests ----------

run_multiple_realizations(model='watts', N=50)
run_multiple_realizations(model='barabasi', N=50)