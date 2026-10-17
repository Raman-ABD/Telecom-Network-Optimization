import os
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
st.title("🌐 Telecom Network Design & Routing Optimizer")
st.write("This website calculates the Minimum Spanning Tree (MST) and finds the shortest path between cities.")

# 1. Load Data
G = nx.Graph()
# data_path set kar rahe hain jo main folder ke data/network_data.csv ko point karega
data_path = os.path.join('data', 'network_data.csv')

if os.path.exists(data_path):
    with open(data_path, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            origin, destination, distance = line.strip().split(',')
            G.add_edge(origin, destination, weight=int(distance))
else:
    st.error("Data file not found! Please check your 'data/network_data.csv'.")

cities = sorted(list(G.nodes()))

# 2. Frontend Sidebar Controls
st.sidebar.header("🎯 Routing Configurations")
start_city = st.sidebar.selectbox("Select Start City (Origin):", cities, index=0)
dest_city = st.sidebar.selectbox("Select Destination City:", cities, index=1)

# 3. Algorithms Processing
mst_graph = nx.minimum_spanning_tree(G, algorithm='kruskal')
total_mst_cost = sum(d['weight'] for u, v, d in mst_graph.edges(data=True))

# Find shortest path using Dijkstra
try:
    shortest_path = nx.shortest_path(G, source=start_city, target=dest_city, weight='weight')
    shortest_path_distance = nx.shortest_path_length(G, source=start_city, target=dest_city, weight='weight')
    path_edges = list(zip(shortest_path[:-1], shortest_path[1:]))
except Exception as e:
    shortest_path = []
    shortest_path_distance = 0
    path_edges = []

# 4. Display Metrics
col1, col2 = st.columns(2)
col1.metric("Total Cable Needed for Full Network (MST)", f"{total_mst_cost} KM")
if start_city != dest_city:
    col2.metric(f"Shortest Distance ({start_city} ➡️ {dest_city})", f"{shortest_path_distance} KM")

# 5. Visualizing side by side
pos = nx.spring_layout(G, seed=42)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot A: MST Layout
nx.draw(mst_graph, pos, with_labels=True, node_color='lightgreen', node_size=2000, font_weight='bold', edge_color='green', width=3, ax=ax[0])
mst_labels = nx.get_edge_attributes(mst_graph, 'weight')
nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=mst_labels, ax=ax[0])
ax[0].set_title("Optimized Network Layout (MST)", fontsize=14)

# Plot B: Shortest Path Highlighted
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_weight='bold', edge_color='gray', width=1, ax=ax[1])
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax[1])

# Highlight the user selected path in Red
if path_edges:
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=4, ax=ax[1])
ax[1].set_title(f"Shortest Route: {start_city} to {dest_city}", fontsize=14)

st.pyplot(fig)

if path_edges:
    st.info(f"👉 **Optimal Route to Travel:** {' ➡️ '.join(shortest_path)}")
