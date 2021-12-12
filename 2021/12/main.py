from collections import defaultdict


def paths(edges, node, path, small_cave_return_allowed=True):
    if node == 'end':
        return [['end']]
    if small_cave_return_allowed:
        next_nodes = [n for n in edges[node] if n != 'start']
    else:
        next_nodes = [n for n in edges[node] if n.isupper() or n not in path]
    path_remainders = []
    for next_node in next_nodes:
        if small_cave_return_allowed and next_node.islower() and next_node in path:
            scra = False
        else:
            scra = small_cave_return_allowed
        path_remainders.extend(paths(edges, next_node, path + [node], small_cave_return_allowed=scra))
    return [[node] + p for p in path_remainders]


edges = defaultdict(list)
with open('input') as f:
    for line in f:
        a, b = line.strip().split('-')
        edges[a].append(b)
        edges[b].append(a)

part_1_paths = paths(edges, 'start', [], small_cave_return_allowed=False)
print(len(part_1_paths))

part_2_paths = paths(edges, 'start', [])
print(len(part_2_paths))
