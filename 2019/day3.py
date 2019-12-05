from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Segment = namedtuple('Segment', ['point1', 'point2', 'direction', 'index'])
Intersection = namedtuple('Intersection', ['wire1_segment', 'wire2_segment', 'point'])

with open('day-3-input.txt') as f:
    wire_descriptions = [line.strip().split(',') for line in f]

wires = []
for wire_description in wire_descriptions:
    current_point = Point(0, 0)
    segments = []
    for n in range(len(wire_description)):
        segment_description = wire_description[n]
        direction, length = segment_description[0], int(segment_description[1:])
        if direction in ['L', 'D']:
            length *= -1

        if direction in ['R', 'L']:  # horizontal segment
            next_point = Point(current_point.x + length, current_point.y)
            point1, point2 = sorted([current_point, next_point], key=lambda point: point.x)
        else:  # vertical segment
            next_point = Point(current_point.x, current_point.y + length)
            point1, point2 = sorted([current_point, next_point], key=lambda point: point.y)

        segments.append(Segment(point1, point2, direction, n))
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
        for other_segment in wire2_vertical_segments:
            if (segment.point1.x < other_segment.point1.x < segment.point2.x and
                    other_segment.point1.y < segment.point1.y < other_segment.point2.y):
                intersections.append(
                    Intersection(segment, other_segment, Point(other_segment.point1.x, segment.point1.y))
                )
    else:
        for other_segment in wire2_horizontal_segments:
            if (segment.point1.y < other_segment.point1.y < segment.point2.y and
                    other_segment.point1.x < segment.point1.x < other_segment.point2.x):
                intersections.append(
                    Intersection(segment, other_segment, Point(segment.point1.x, other_segment.point1.y))
                )

min_cross_distance = min([abs(i.point.x) + abs(i.point.y) for i in intersections])
print(min_cross_distance)
