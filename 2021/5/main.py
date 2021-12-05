import argparse
from collections import namedtuple, defaultdict

Line = namedtuple('Line', ['x1', 'y1', 'x2', 'y2'])

parser = argparse.ArgumentParser()
parser.add_argument('--include-diagonals', action='store_true')
args = parser.parse_args()

lines = []
with open('input') as f:
    for row in f:
        p1, p2 = row.strip().split(' -> ')
        x1, y1 = p1.split(',')
        x2, y2 = p2.split(',')
        line = map(int, [x1, y1, x2, y2])
        lines.append(Line(*line))

points = defaultdict(int)
for line in lines:
    if line.x1 == line.x2:
        y1, y2 = sorted([line.y1, line.y2])
        for y in range(y1, y2 + 1):
            points[(line.x1, y)] += 1
    elif line.y1 == line.y2:
        x1, x2 = sorted([line.x1, line.x2])
        for x in range(x1, x2 + 1):
            points[(x, line.y1)] += 1
    elif args.include_diagonals:
        if line.x2 > line.x1:
            x_range = range(line.x1, line.x2 + 1)
        else:
            x_range = range(line.x1, line.x2 - 1, -1)

        if line.y2 > line.y1:
            y_range = range(line.y1, line.y2 + 1)
        else:
            y_range = range(line.y1, line.y2 - 1, -1)

        for point in zip(x_range, y_range):
            points[point] += 1

overlap = len([p for p, c in points.items() if c > 1])
print(overlap)
