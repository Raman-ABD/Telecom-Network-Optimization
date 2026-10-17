import os
import networkx as nx
import matplotlib.pyplot as plt

# 1. Read data from our CSV file safely
# We read the lines manually so you don't even need the pandas library!
G = nx.Graph()

data_path = os.path.join('data', 'network_data.csv')

with open(data_path, 'r') as file:
    lines = file.readlines()
    # Skip the first row because it contains column headers (Origin, Destination, Distance)
    for line in lines[1:]:
        origin, destination, distance = line.strip().split(',')
        G.add_edge(origin, destination, weight=int(distance))

# 2. Run the Minimum Spanning Tree (MST) Algorithm
mst_graph = nx.minimum_spanning_tree(G, algorithm='kruskal')

# Calculate total optimized wire length
total_cost = sum(d['weight'] for u, v, d in mst_graph.edges(data=True))

# 3. Print a neat text summary report in the console terminal
print("--- Telecom Network Design Optimization Report ---")
print(f"Total optimal fiber cable required: {total_cost} KM\n")
print("Optimal links to establish:")
for u, v, d in mst_graph.edges(data=True):
    print(f" - Connect {u} to {v} ({d['weight']} KM)")

# 4. Generate Visual Maps Comparison
pos = nx.spring_layout(G, seed=42) # keeps city positions locked in place
plt.figure(figsize=(12, 5))

# Plot Diagram A: Unoptimized Network
plt.subplot(1, 2, 1)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("All Possible Intercity Routes (Expensive & Redundant)")

# Plot Diagram B: Optimized Network Layout
plt.subplot(1, 2, 2)
nx.draw(mst_graph, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_weight='bold', edge_color='green', width=3)
mst_edge_labels = nx.get_edge_attributes(mst_graph, 'weight')
nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=mst_edge_labels)
plt.title(f"Optimized Layout (MST Topology)\nTotal Cable Needed: {total_cost} KM")

plt.tight_layout()

# 5. Automatically save the final diagram image inside the output folder
plt.savefig(os.path.join('output', 'optimized_network_map.png'))
print("\n[Success] Network map image successfully saved inside the 'output' folder!")

plt.show()
