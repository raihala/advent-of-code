import math
import matplotlib.pyplot as plt
from collections import defaultdict


def distance(a, b):
    """
    Return the manhattan distance between two Points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def circle(center, radius):
    """
    Return a list of points comprising the manhattan distance
    circle of specified radius, with specified center point.
    """
    points = []
    for i in range(radius):
        points += [
            (i, radius-i),
            (-i, -radius+i),
            (radius-i, -i),
            (-radius+i, i)
        ]
    center_x, center_y = center
    points = [(x + center_x, y + center_y) for x, y in points]
    return points


coordinates = []
with open('day-6-input.txt') as f:
    for line in f:
        x, y = line.strip().split(', ')
        coordinates.append((int(x), int(y)))

min_x = min([p[0] for p in coordinates])
max_x = max([p[0] for p in coordinates])
min_y = min([p[1] for p in coordinates])
max_y = max([p[1] for p in coordinates])
corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]

# Part 1

# once populated, this will be:
# {point: {'coordinate': <coordinate nearest to point>, 'distance': <its distance>}, ... }
closest_coordinate = defaultdict(lambda: {'coordinate': None, 'distance': math.inf})

# we will "splash" each coordinate onto the grid, one at a time
for coordinate in coordinates:
    closest_coordinate[coordinate] = {'coordinate': coordinate, 'distance': 0}

    # beyond this radius, every point tested will be off the grid
    max_radius = max([distance(coordinate, corner) for corner in corners])

    # circle outwards from the coordinate
    for radius in range(1, max_radius+1):
        any_updated = False
        for point in circle(center=coordinate, radius=radius):
            if (point[0] < min_x) or (point[0] > max_x) or (point[1] < min_y) or (point[1] > max_y):
                continue
            elif radius < closest_coordinate[point]['distance']:
                closest_coordinate[point] = {'coordinate': coordinate, 'distance': radius}
                any_updated = True
            elif radius == closest_coordinate[point]['distance']:
                closest_coordinate[point]['coordinate'] = None  # tie, no coordinate is closest
        if not any_updated:
            break

areas = defaultdict(int)
for c in closest_coordinate.values():
    if c['coordinate'] is None:
        continue
    areas[c['coordinate']] += 1

# any area that includes points on the edge is in fact infinite,
# so we will filter them out.
edge_points = {k: v for k, v in closest_coordinate.items() if k[0] in (min_x, max_x) or k[1] in (min_y, max_y)}
coordinates_with_infinite_areas = set([p['coordinate'] for p in edge_points.values() if p['coordinate']])
interior_areas = {k: v for k, v in areas.items() if k not in coordinates_with_infinite_areas}

most_isolated_coordinate = max(interior_areas, key=lambda x: interior_areas[x])
# print(f"Most isolated coordinate is {most_isolated_coordinate}, with area {interior_areas[most_isolated_coordinate]}")

# plt.subplot('211')
# plt.scatter([p[0] for p in coordinates], [p[1] for p in coordinates])
# plt.subplot('212')
# plt.scatter([p[0] for p in coordinates_with_infinite_areas], [p[1] for p in coordinates_with_infinite_areas])
# plt.show()

# Part 2

# This is very similar to Part 1.
# Once populated, this will be a map from point to its distance sum.
distance_sum = defaultdict(int)

# we will "splash" each coordinate onto the grid, one at a time
for coordinate in coordinates:
    # beyond this radius, every point tested will be off the grid
    max_radius = max([distance(coordinate, corner) for corner in corners])

    # circle outwards from the coordinate
    for radius in range(1, max_radius+1):
        for point in circle(center=coordinate, radius=radius):
            if (point[0] < min_x) or (point[0] > max_x) or (point[1] < min_y) or (point[1] > max_y):
                continue
            distance_sum[point] += radius

# for y in range(min_y, max_y+1):
#     for x in range(min_x, max_x+1):
#         s = distance_sum[(x, y)]
#         if s < 10000:
#             output = '*'
#         else:
#             output = '.'
#         print(output, end='')
#     print()

print(len([s for s in distance_sum.values() if s < 10000]))
