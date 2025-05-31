import networkx as nx
import matplotlib.pyplot as plt
from rich.pretty import pprint


# sample response
# data = {
#     'results': [],
#     'relations': [
#         {'source': 'pavan', 'relationship': 'likes', 'target': 'technology_evaluation'},
#         {'source': 'alice', 'relationship': 'likes', 'target': 'pizza'},
#         {'source': 'alice', 'relationship': 'friend', 'target': 'pavan'}
#     ]
# }

def display_graph(data):
    pprint(data)
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges with relationship as labels
    for rel in data['relations']:
        G.add_edge(rel['source'], rel['target'], label=rel['relationship'])

    # Get edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)  # for consistent layout

    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Graph Visualization of Relations")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
