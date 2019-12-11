import math
from collections import defaultdict
from itertools import chain, groupby, zip_longest

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
    x, y = x//math.gcd(x, y), y//math.gcd(x, y)
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

result = {'asteroid': None, 'visible': 0}
for asteroid in asteroids:
    lines = [line for line in lines_of_sight if asteroid in line]
    long_lines = [line for line in lines if len(line) > 2]
    num_asteroids_visible = len(lines)
    for line in long_lines:
        if (min([p[0] for p in line]) < asteroid[0] < max([p[0] for p in line]) or
                min([p[1] for p in line]) < asteroid[1] < max([p[1] for p in line])):
            num_asteroids_visible += 1
    if num_asteroids_visible > result['visible']:
        result['asteroid'] = asteroid
        result['visible'] = num_asteroids_visible

print(result)


# Part 2
def angle(p1, p2):
    """
    Return degrees cw between negative y axis and the line p1->p2
    """
    x1, y1 = p1
    x2, y2 = p2
    x, y = x2 - x1, y1 - y2  # NB: negate y values because grid is weird
    radians = math.atan2(x, y)
    degrees = radians * 180 / math.pi
    degrees %= 360
    return degrees


def dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


station = result['asteroid']
asteroids_to_destroy = asteroids - {station}
laser_angles = defaultdict(list)
for asteroid in asteroids_to_destroy:
    laser_angle = angle(station, asteroid)
    laser_angle = int(laser_angle * 100)  # for rough equality testing between floats
    distance = dist(station, asteroid)
    laser_angles[laser_angle].append({'point': asteroid, 'dist': distance})

asteroids_by_angle = [
    sorted(laser_angles[laser_angle], key=lambda p: p['dist'])
    for laser_angle in sorted(laser_angles.keys())
]
asteroids_by_angle = [[p['point'] for p in laser_angle] for laser_angle in asteroids_by_angle]
asteroids_by_angle = [p for p in chain(*zip_longest(*asteroids_by_angle)) if p is not None]

print(asteroids_by_angle[199])
