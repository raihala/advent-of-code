import numpy as np
from collections import defaultdict

I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
Rx = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
Ry = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
Rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])

# TODO: there's got to be a better way to do this...
ROTATIONS = [
    I,
    Rz,
    Rz @ Rz,
    Rz @ Rz @ Rz,
    Rx,
    Rx @ Rz,
    Rx @ Rz @ Rz,
    Rx @ Rz @ Rz @ Rz,
    Rx @ Rx,
    Rx @ Rx @ Rz,
    Rx @ Rx @ Rz @ Rz,
    Rx @ Rx @ Rz @ Rz @ Rz,
    Rx @ Rx @ Rx,
    Rx @ Rx @ Rx @ Rz,
    Rx @ Rx @ Rx @ Rz @ Rz,
    Rx @ Rx @ Rx @ Rz @ Rz @ Rz,
    Ry,
    Ry @ Rz,
    Ry @ Rz @ Rz,
    Ry @ Rz @ Rz @ Rz,
    Ry @ Ry @ Ry,
    Ry @ Ry @ Ry @ Rz,
    Ry @ Ry @ Ry @ Rz @ Rz,
    Ry @ Ry @ Ry @ Rz @ Rz @ Rz
]


def find_rotation_and_translation(source_points, dest_points):
    """
    Returns a (rotation matrix, translation vector) pair
    specifying how to transform the source points into the dest points.
    """
    source_points = np.array(source_points)
    dest_points = np.array(dest_points)
    for rotation in ROTATIONS:
        source_points_rotated = rotation.dot(source_points.T).T
        translations = dest_points - source_points_rotated
        if np.all(translations == translations[0]):
            return rotation, translations[0]


def distance(a, b):
    """
    Returns a custom "distance" between two points
    """
    return tuple(sorted([
        abs(b[0] - a[0]),
        abs(b[1] - a[1]),
        abs(b[2] - a[2])
    ]))


with open('input') as f:
    data = f.read()

scanner_data = data.split('\n\n')
scanners = []
for scanner in scanner_data:
    beacons = scanner.strip().split('\n')[1:]
    beacons = [tuple(int(x) for x in b.split(',')) for b in beacons]
    scanners.append(beacons)

# NOTE: at least in my input data, none of the scanners contain
# any two pairs of points with the same "distance" between them as
# defined above in my distance function. I'm not sure if this is
# intentional or a coincidence, so your data might be different, but
# I'm going to rely on this fact and assume that a "distance"
# uniquely identifies a pair of points.

# each entry in dist_maps will correspond to a scanner, and
# will map (x, y, z) beacon location tuples to sets of the "distances"
# between that beacon and all the other beacons visible by the scanner.
dist_maps = []
for scanner in scanners:
    dist_map = defaultdict(set)
    for i in range(len(scanner) - 1):
        point = scanner[i]
        for j in range(i+1, len(scanner)):
            other_point = scanner[j]
            dist = distance(point, other_point)
            dist_map[point].add(dist)
            dist_map[other_point].add(dist)
    dist_maps.append(dist_map)

# dict mapping (source, dest) pairs to (rotation matrix, translation vector)
# pairs, specifying how to transform the source scanner's frame to
# get to the dest scanner's frame.
relative_transformations = {}

for i in range(len(dist_maps)):
    for j in range(len(dist_maps)):
        if i == j:
            continue
        source_points = []
        dest_points = []
        for point, dists in dist_maps[i].items():
            for other_point, other_dists in dist_maps[j].items():
                if len(dists & other_dists) >= 11:
                    source_points.append(point)
                    dest_points.append(other_point)
        if source_points:
            rotation_matrix, translation_vector = find_rotation_and_translation(source_points, dest_points)
            relative_transformations[(i, j)] = rotation_matrix, translation_vector

# dict mapping scanner IDs to a (rotation matrix, translation vector) pair
# specifying how to transform the specified scanner's frame to get
# to the frame of scanner 0 (which is considered the 'absolute' frame).
absolute_transformations = {0: (I, np.array([0, 0, 0]))}

# finish filling out absolute_transformations
while len(absolute_transformations) < len(scanners):
    for (source, dest), (source_to_dest_r, source_to_dest_t) in relative_transformations.items():
        if dest in absolute_transformations and source not in absolute_transformations:
            # if we know the rotation matrix and translation vector required
            # to transform the source scanner's frame into the dest scanner's
            # frame, and we know the ones needed to get from the dest scanner
            # to scanner 0 (which is treated as the absolute reference frame),
            # calculate the transformations from source to 0.
            dest_to_0_r, dest_to_0_t = absolute_transformations[dest]
            source_to_0_r = dest_to_0_r.dot(source_to_dest_r)
            source_to_0_t = dest_to_0_r.dot(source_to_dest_t) + dest_to_0_t
            absolute_transformations[source] = source_to_0_r, source_to_0_t

beacon_locations = set()
for i in range(len(scanners)):
    r, t = absolute_transformations[i]
    relative_beacon_locations = np.array(scanners[i])
    absolute_beacon_locations = r.dot(relative_beacon_locations.T).T + t
    for point in absolute_beacon_locations:
        beacon_locations.add(tuple(point))

part_1_res = len(beacon_locations)
print(part_1_res)

scanner_locations = [t for r, t in absolute_transformations.values()]
max_dist = 0
for i in range(len(scanner_locations) - 1):
    for j in range(i+1, len(scanner_locations)):
        dist = sum(distance(scanner_locations[i], scanner_locations[j]))
        max_dist = max(max_dist, dist)

part_2_res = max_dist
print(part_2_res)
