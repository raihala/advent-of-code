import networkx as nx


def edge_exists(a, b):
    if a == 'S':
        a = 'a'
    elif a == 'E':
        a = 'z'

    if b == 'S':
        b = 'a'
    elif b == 'E':
        b = 'z'

    return ord(b) <= ord(a) + 1


with open('input') as f:
    data = [line.strip() for line in f]

G = nx.DiGraph()

height = len(data)
width = len(data[0])
start = None
end = None

for row in range(height):
    for col in range(width):
        elevation = data[row][col]
        if elevation == 'S':
            start = (row, col)
        elif elevation == 'E':
            end = (row, col)
        G.add_node((row, col), elevation=elevation)

for row in range(height):
    for col in range(width):
        current = (row, col)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for n in neighbors:
            if n in G.nodes and edge_exists(G.nodes[current]['elevation'], G.nodes[n]['elevation']):
                G.add_edge(current, n)

part_1_res = nx.shortest_path_length(G, start, end)

low_nodes = [n for n in G.nodes if G.nodes[n]['elevation'] == 'a']
part_2_res = part_1_res
for node in low_nodes:
    try:
        length = nx.shortest_path_length(G, node, end)
    except nx.NetworkXNoPath:
        continue
    if length < part_2_res:
        part_2_res = length

print(part_1_res)
print(part_2_res)
