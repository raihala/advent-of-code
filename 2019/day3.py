from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Segment = namedtuple('Segment', ['point1', 'point2'])
Intersection = namedtuple('Intersection', ['wire1_segment', 'wire2_segment', 'point'])

with open('day-3-input.txt') as f:
    wire_descriptions = [line.strip().split(',') for line in f]

wires = []
for wire_description in wire_descriptions:
    current_point = Point(0, 0)
    segments = []
    for segment_description in wire_description:
        direction, length = segment_description[0], int(segment_description[1:])
        if direction in ['L', 'D']:
            length *= -1

        if direction in ['R', 'L']:  # horizontal segment
            next_point = Point(current_point.x + length, current_point.y)
        else:  # vertical segment
            next_point = Point(current_point.x, current_point.y + length)

        segments.append(Segment(current_point, next_point))
        current_point = next_point
    wires.append(segments)

# we can filter a bit to reduce the number of comparisons needed
wire2_vertical_segments = [s for s in wires[1] if s.point1.x == s.point2.x]
wire2_horizontal_segments = [s for s in wires[1] if s.point1.y == s.point2.y]

# for each segment in the first wire, look for
# intersecting segments of the second wire
intersections = []
for segment in wires[0]:
    if segment.point1.y == segment.point2.y:  # horizontal
        left_x, right_x = sorted([segment.point1.x, segment.point2.x])
        for other_segment in wire2_vertical_segments:
            bottom_y, top_y = sorted([other_segment.point1.y, other_segment.point2.y])
            if (left_x < other_segment.point1.x < right_x and
                    bottom_y < segment.point1.y < top_y):
                intersections.append(
                    Intersection(segment, other_segment, Point(other_segment.point1.x, segment.point1.y))
                )
    else:  # vertical
        bottom_y, top_y = sorted([segment.point1.y, segment.point2.y])
        for other_segment in wire2_horizontal_segments:
            left_x, right_x = sorted([other_segment.point1.x, other_segment.point2.x])
            if (bottom_y < other_segment.point1.y < top_y and
                    left_x < segment.point1.x < right_x):
                intersections.append(
                    Intersection(segment, other_segment, Point(segment.point1.x, other_segment.point1.y))
                )


def dist(point1, point2):
    """
    Calculate the Manhattan distance between two points.
    """
    return abs(point2.x - point1.x) + abs(point2.y - point1.y)


# Part 1
origin = Point(0, 0)
min_cross_distance = min([dist(origin, i.point) for i in intersections])
print(min_cross_distance)

# Part 2
distances_along_wires = []
for intersection in intersections:
    # wire length up to but not including intersecting segment
    index1 = wires[0].index(intersection.wire1_segment)
    index2 = wires[1].index(intersection.wire2_segment)
    wire1_length = sum([dist(s.point1, s.point2) for s in wires[0][:index1]])
    wire2_length = sum([dist(s.point1, s.point2) for s in wires[1][:index2]])

    # plus the partial lengths of intersecting segments
    wire1_length += dist(intersection.wire1_segment.point1, intersection.point)
    wire2_length += dist(intersection.wire2_segment.point1, intersection.point)

    distances_along_wires.append(wire1_length + wire2_length)

min_cross_distance = min(distances_along_wires)
print(min_cross_distance)
