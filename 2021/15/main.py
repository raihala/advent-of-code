import networkx


def neighbors(x, y, grid_size):
    res = []
    if x > 0:
        res.append((x-1, y))
    if x < grid_size - 1:
        res.append((x+1, y))
    if y > 0:
        res.append((x, y-1))
    if y < grid_size - 1:
        res.append((x, y+1))
    return res


with open('input') as f:
    part_1_data = [[int(c) for c in line.strip()] for line in f]

size = len(part_1_data)
part_2_data = {}
part_1_graph = networkx.DiGraph()
part_2_graph = networkx.DiGraph()

for y in range(size):
    for x in range(size):
        for other_x, other_y in neighbors(x, y, size):
            part_1_graph.add_edge((x, y), (other_x, other_y), weight=part_1_data[other_y][other_x])
        for y_mult in range(5):
            for x_mult in range(5):
                point = (x + size * x_mult, y + size * y_mult)
                weight = ((part_1_data[y][x] + x_mult + y_mult - 1) % 9) + 1
                part_2_data[point] = weight

for point in part_2_data:
    for other_point in neighbors(*point, 5*size):
        part_2_graph.add_edge(point, other_point, weight=part_2_data[other_point])

part_1_res = networkx.shortest_path_length(part_1_graph, (0, 0), (size - 1, size - 1), weight='weight')
part_2_res = networkx.shortest_path_length(part_2_graph, (0, 0), (5*size - 1, 5*size - 1), weight='weight')

print(part_1_res)
print(part_2_res)
