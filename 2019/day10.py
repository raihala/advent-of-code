from itertools import groupby
from math import gcd

with open('day-10-input.txt') as f:
    data = [line.strip() for line in f]

asteroids = set()
for j in range(len(data)):
    row = data[j]
    for i in range(len(row)):
        if row[i] == '#':
            asteroids.add((i, j))


def norm(p1, p2):
    """
    Returns the point (x, y) on the line between points
    p1 and p2 s.t. x, y are relatively prime integers, and x > 0.
    """
    x1, y1 = p1
    x2, y2 = p2

    x, y = x2 - x1, y2 - y1
    x, y = x//gcd(x, y), y//gcd(x, y)
    if x < 0:
        x *= -1
        y *= -1
    elif x == 0:
        y = abs(y)
    return x, y


# will contain sets of points that share a line of sight
lines_of_sight = []

for asteroid in asteroids:
    known_asteroids = set().union(*[line for line in lines_of_sight if asteroid in line])
    unknown_asteroids = asteroids - known_asteroids - {asteroid}

    coordinates = sorted(list(unknown_asteroids), key=lambda x: norm(asteroid, x))
    for _, line_of_sight in groupby(coordinates, key=lambda x: norm(asteroid, x)):
        lines_of_sight.append(set(line_of_sight) | {asteroid})

max_visible = 0
for asteroid in asteroids:
    lines = [line for line in lines_of_sight if asteroid in line]
    long_lines = [line for line in lines if len(line) > 2]
    num_asteroids_visible = len(lines)
    for line in long_lines:
        if (min([p[0] for p in line]) < asteroid[0] < max([p[0] for p in line]) or
                min([p[1] for p in line]) < asteroid[1] < max([p[1] for p in line])):
            num_asteroids_visible += 1
    max_visible = max(max_visible, num_asteroids_visible)

print(max_visible)
