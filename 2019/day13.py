import itertools
import subprocess
import sys
from intcode import IntcodeComputer


def parse_data(data):
    tiles = {}
    score = None
    for n in range(0, len(data), 3):
        x, y, tile_id = data[n:n+3]
        if x == -1 and y == 0:
            score = tile_id
        else:
            tiles[(x, y)] = tile_id
    return tiles, score


def display(tiles):
    left_x = min([x for x, y in tiles])
    right_x = max([x for x, y in tiles])
    top_y = min([y for x, y in tiles])
    bottom_y = max([y for x, y in tiles])

    for y in range(top_y, bottom_y+1):
        for x in range(left_x, right_x+1):
            tile = tiles.get((x, y), 0)  # default to tile_id 0 == empty tile
            display_char = ' X*_O'[tile]
            sys.stdout.write(display_char)
        sys.stdout.write('\n')


# Part 1
def part_one(computer, program):
    data = computer.run(program)
    tiles, _ = parse_data(data)  # don't care about the score
    display(tiles)
    num_bricks = len([t for t in tiles.values() if t == 2])
    print(f'There are {num_bricks} bricks.')


# Part 2
def part_two(computer, program):
    program[0] = 2  # trick cabinet into thinking we've paid
    computer.load(program)
    tiles = {}
    score = 0

    for n in itertools.count(0):  # infinite iterator
        data = computer.kontinue()
        tile_updates, score_update = parse_data(data)
        tiles.update(tile_updates)
        if score_update is not None:
            score = score_update

        # update the screen every 100 frames just for fun
        if n % 100 == 0:
            subprocess.run(['clear'])
            print(f'Your score is: {score}')
            display(tiles)

        ball_pos = [k for k, v in tiles.items() if v == 4][0][0]  # ball x pos
        paddle_pos = [k for k, v in tiles.items() if v == 3][0][0]  # paddle x pos
        if paddle_pos < ball_pos:
            joystick_input = 1  # move to the right
        elif paddle_pos > ball_pos:
            joystick_input = -1  # move to the left
        else:
            joystick_input = 0

        computer.send_inputs([joystick_input])

        if computer.halted:
            subprocess.run(['clear'])
            print(f'Your score is: {score}')
            display(tiles)
            break

    print(f'Game over! Your final score is: {score}')


with open('day-13-input.txt') as f:
    program = [int(x) for x in f.readline().strip().split(',')]

computer = IntcodeComputer()
# part_one(computer, program)
part_two(computer, program)
