import networkx as nx
import matplotlib.pyplot as plt

# WebRTC IP dictionary
data = {
    '157.240.245.58:56442': {'type': 'relay', 'location': 'caller'}, '157.240.245.58:57182': {'type': 'relay', 'location': 'caller'}, '10.239.233.249:62232': {'type': 'host', 'location': 'caller'}, '10.239.233.249:52105': {'type': 'host', 'location': 'caller'}, '128.197.29.249:36960': {'type': 'srflx', 'location': 'caller'}, '128.197.29.249:28071': {'type': 'srflx', 'location': 'caller'}, '157.240.245.58:56180': {'type': 'relay', 'location': 'caller'}, '10.239.233.249:9': {'type': 'host', 'location': 'caller'}, '157.240.245.58:53978': {'type': 'relay',
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              'location': 'caller'}, '157.240.245.58:52465': {'type': 'relay', 'location': 'caller'}, '157.240.245.58:55860': {'type': 'relay', 'location': 'caller'}, '128.197.29.249:50060': {'type': 'srflx', 'location': 'caller'}, '128.197.29.249:38743': {'type': 'srflx', 'location': 'caller'}, '128.197.29.225:28023': {'type': 'srflx', 'location': 'receiver'}, '10.239.25.33:55902': {'type': 'host', 'location': 'receiver'}, '128.197.29.225:15914': {'type': 'srflx', 'location': 'receiver'}, '157.240.245.58:56078': {'type': 'relay', 'location': 'receiver'}, '157.240.245.58:58341': {'type': 'relay', 'location': 'receiver'}, '128.197.29.249:25754': {'type': 'prflx', 'location': 'caller'}, '157.240.245.58:53239': {'type': 'relay', 'location': 'receiver'}, '10.239.25.33:9': {'type': 'host', 'location': 'receiver'}, '128.197.29.225:36307': {'type': 'prflx', 'location': 'receiver'}, '128.197.29.225:46635': {'type': 'prflx', 'location': 'receiver'}}

G = nx.DiGraph()

for ip, data in data.items():
    G.add_node(ip)
    if data['type'] == 'relay':
        G.add_edge(ip, data['location'] + ' RELAY')
    elif data['type'] == 'host':
        G.add_edge(ip, data['location'] + ' HOST')
    elif data['type'] == 'srflx':
        G.add_edge(ip, data['location'] + ' SRFLX')
    elif data['type'] == 'prflx':
        G.add_edge(ip, data['location'] + ' PRFLX')

# Set node positions for better visualization
pos = nx.shell_layout(G)

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)

# Draw edges
nx.draw_networkx_edges(G, pos, edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, font_size=8)

# Set plot title and display the graph
plt.title('WebRTC Network Diagram')
plt.axis('off')
plt.tight_layout()
plt.show()
