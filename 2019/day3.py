from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

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
            segment = sorted([current_point, next_point], key=lambda point: point.x)
        else:  # vertical segment
            next_point = Point(current_point.x, current_point.y + length)
            segment = sorted([current_point, next_point], key=lambda point: point.y)

        segments.append(segment)
        current_point = next_point
    wires.append(segments)

# we can filter and sort a bit to reduce the number of comparisons needed
wire1_vertical_segments = [s for s in wires[0] if s[0].x == s[1].x]
wire1_horizontal_segments = [s for s in wires[0] if s[0].y == s[1].y]

# for each segment in the second wire, look for
# intersecting segments of the first wire
intersections = []
for segment in wires[1]:
    horizontal = segment[0].y == segment[1].y
    if horizontal:
        for test_segment in wire1_vertical_segments:
            if (segment[0].x < test_segment[0].x < segment[1].x and
                    test_segment[0].y < segment[0].y < test_segment[1].y):
                intersections.append(Point(test_segment[0].x, segment[0].y))
    else:
        for test_segment in wire1_horizontal_segments:
            if (segment[0].y < test_segment[0].y < segment[1].y and
                    test_segment[0].x < segment[0].x < test_segment[1].x):
                intersections.append(Point(segment[0].x, test_segment[0].y))

min_cross_distance = min([abs(p.x) + abs(p.y) for p in intersections])
print(min_cross_distance)
