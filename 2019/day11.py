import sys
from collections import defaultdict
from intcode import IntcodeComputer


def turn(curr_dir, turn_dir):
    """
    This is kinda obnoxious I guess. Subtracts 1
    from current direction if turn direction is 0,
    otherwise if turn direction is 1, adds 1 to the
    current direction. Then mod 4 to make sure
    direction is still 0, 1, 2, or 3.
    """
    return (curr_dir + (-1)**turn_dir) % 4


def step(position, direction):
    """
    This is definitely obnoxious, sorry about that.
    Basically treats direction as a 2-bit variable
    where one bit encodes which axis to move along
    and the other encodes whether to move in a
    positive or negative direction.
    """
    new_position = list(position)
    plus_or_minus, axis = divmod(direction, 2)
    new_position[axis] += (-1)**plus_or_minus
    return tuple(new_position)


with open('day-11-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()
computer.load(program)

panel_colors = defaultdict(int)
panel_colors[(0, 0)] = 1  # Part 2 only! comment this out for Part 1

robot_position = (0, 0)  # y is listed first, then x
robot_direction = 0  # 0 = up, 1 = left, 2 = down, 3 = right
while not computer.halted:
    computer.send_inputs([panel_colors[robot_position]])
    color, turn_direction = computer.kontinue()

    panel_colors[robot_position] = color
    robot_direction = turn(robot_direction, turn_direction)
    robot_position = step(robot_position, robot_direction)

# Part 1 answer: number of entries in defaultdict is number
# of panels painted at least once during the process
print(len(panel_colors))

# Part 2 answer: gotta print the whole thing out
min_y = min([panel[0] for panel in panel_colors])
max_y = max([panel[0] for panel in panel_colors])
min_x = min([panel[1] for panel in panel_colors])
max_x = max([panel[1] for panel in panel_colors])


# I kinda messed this up, so coordinates are listed as (y, x)
# where positive y direction is up and positive x direction is *left*
for y in range(max_y, min_y-1, -1):
    for x in range(max_x, min_x-1, -1):
        color = panel_colors[(y, x)]
        char = ['.', 'X'][color]
        sys.stdout.write(char)
    sys.stdout.write('\n')
