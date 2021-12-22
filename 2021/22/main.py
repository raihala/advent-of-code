import re
from collections import namedtuple


Cuboid = namedtuple('Cuboid', ['xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax'])


def volume(c):
    return (
        (c.xmax + 1 - c.xmin) *
        (c.ymax + 1 - c.ymin) *
        (c.zmax + 1 - c.zmin)
    )


def intersect(a, b):
    return (
        b.xmin <= a.xmax and b.xmax >= a.xmin and
        b.ymin <= a.ymax and b.ymax >= a.ymin and
        b.zmin <= a.zmax and b.zmax >= a.zmin
    )


def subtract(a, b):
    """
    Return a list of Cuboids equivalent to the sections
    of a that do not intersect with b
    """
    if not intersect(a, b):
        return [a]

    left = right = back = front = down = up = None

    if b.xmin > a.xmin:
        left = Cuboid(
            a.xmin, b.xmin-1,
            a.ymin, a.ymax,
            a.zmin, a.zmax
        )
    if b.xmax < a.xmax:
        right = Cuboid(
            b.xmax+1, a.xmax,
            a.ymin, a.ymax,
            a.zmin, a.zmax
        )
    if b.ymin > a.ymin:
        back = Cuboid(
            max(a.xmin, b.xmin), min(a.xmax, b.xmax),
            a.ymin, b.ymin-1,
            a.zmin, a.zmax
        )
    if b.ymax < a.ymax:
        front = Cuboid(
            max(a.xmin, b.xmin), min(a.xmax, b.xmax),
            b.ymax+1, a.ymax,
            a.zmin, a.zmax
        )
    if b.zmin > a.zmin:
        down = Cuboid(
            max(a.xmin, b.xmin), min(a.xmax, b.xmax),
            max(a.ymin, b.ymin), min(a.ymax, b.ymax),
            a.zmin, b.zmin-1
        )
    if b.zmax < a.zmax:
        up = Cuboid(
            max(a.xmin, b.xmin), min(a.xmax, b.xmax),
            max(a.ymin, b.ymin), min(a.ymax, b.ymax),
            b.zmax+1, a.zmax
        )

    return [c for c in [left, right, back, front, down, up] if c]


def calculate_on_cuboids(actions, initial_on_cuboids=None):
    on_cuboids = initial_on_cuboids or []

    for action, cuboid in actions:
        if action == 'off':
            updated_on_cuboids = []
            for on_cuboid in on_cuboids:
                updated_on_cuboids.extend(subtract(on_cuboid, cuboid))
            on_cuboids = updated_on_cuboids

        else:
            # need on_cuboids to be non-intersecting so we
            # can't just tack the new one onto the list
            new_on_cuboids = [cuboid]
            for on_cuboid in on_cuboids:
                # for each existing on cuboid C, replace our evolving
                # list of new on cuboids with an updated list that
                # removes any intersections with C
                updated_new_on_cuboids = []
                for new_on_cuboid in new_on_cuboids:
                    updated_new_on_cuboids.extend(subtract(new_on_cuboid, on_cuboid))
                new_on_cuboids = updated_new_on_cuboids
            on_cuboids.extend(new_on_cuboids)

    return on_cuboids


n = '([-0-9]+)'
pattern = f'(on|off) x={n}..{n},y={n}..{n},z={n}..{n}'
part_1_actions = []
part_2_actions = []
initial_cuboid = Cuboid(-50, 50, -50, 50, -50, 50)

with open('input') as f:
    for line in f:
        match = re.match(pattern, line)
        action, xmin, xmax, ymin, ymax, zmin, zmax = match.groups()
        if action == 'off' and not part_1_actions:
            continue

        cuboid = Cuboid(*map(int, [xmin, xmax, ymin, ymax, zmin, zmax]))
        if intersect(cuboid, initial_cuboid):
            part_1_actions.append((action, cuboid))
        else:
            part_2_actions.append((action, cuboid))

part_1_on_cuboids = calculate_on_cuboids(part_1_actions)
part_1_res = sum([volume(c) for c in part_1_on_cuboids])
print(part_1_res)

part_2_on_cuboids = calculate_on_cuboids(part_2_actions, part_1_on_cuboids)
part_2_res = sum([volume(c) for c in part_2_on_cuboids])
print(part_2_res)
