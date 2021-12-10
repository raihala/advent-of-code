def explore_basin(lines, point, basin):
    basin.append(point)
    x, y = point
    for next_x, next_y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if (next_x, next_y) not in basin and lines[next_y][next_x] < 9:
            explore_basin(lines, (next_x, next_y), basin)


data = [[10] * 102]
with open('input') as f:
    for line in f:
        row = [10] + [int(x) for x in line.strip()] + [10]
        data.append(row)
data.append([10] * 102)

low_points = {}
for y in range(1, len(data) - 1):
    for x in range(1, 101):
        height = data[y][x]
        neighbor_heights = [data[y-1][x], data[y+1][x], data[y][x-1], data[y][x+1]]
        if all([height < h for h in neighbor_heights]):
            low_points[(x, y)] = height

print(sum([h + 1 for h in low_points.values()]))

basin_sizes = []
for point in low_points:
    basin = []
    explore_basin(data, point, basin)
    basin_sizes.append(len(basin))

a = sorted(basin_sizes)
print(a[-3] * a[-2] * a[-1])
