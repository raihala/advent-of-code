points = set()
folds = []

with open('input') as f:
    for line in f:
        if ',' in line:
            x, y = line.strip().split(',')
            points.add((int(x), int(y)))
        elif 'fold' in line:
            axis, value = line.strip().split()[-1].split('=')
            folds.append((axis, int(value)))

part_1_res = None
for axis, value in folds:
    new_points = set()
    if axis == 'x':
        for p in points:
            if p[0] < value:
                new_points.add(p)
            else:
                new_points.add((2*value - p[0], p[1]))
    else:
        for p in points:
            if p[1] < value:
                new_points.add(p)
            else:
                new_points.add((p[0], 2*value - p[1]))
    points = new_points
    if part_1_res is None:
        part_1_res = len(points)

print(part_1_res)

min_x = min([p[0] for p in points])
max_x = max([p[0] for p in points])
min_y = min([p[1] for p in points])
max_y = max([p[1] for p in points])

for y in range(min_y, max_y + 1):
    line = []
    for x in range(min_x, max_x + 1):
        if (x, y) in points:
            line.append('#')
        else:
            line.append('.')
    print(''.join(line))
