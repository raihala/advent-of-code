def neighbors(x, y):
    x_range = range(max(x-1, 0), min(x+2, 10))
    y_range = range(max(y-1, 0), min(y+2, 10))
    return ((a, b) for a in x_range for b in y_range if (a, b) != (x, y))


with open('input') as f:
    data = []
    for line in f:
        data.append([int(c) for c in line.strip()])

flashes = 0
steps = 0
part_1_complete = False
part_2_complete = False

while True:
    # iterate through steps indefinitely
    data = [[x + 1 for x in y] for y in data]
    step_flashes = 0

    while True:
        # scan the grid repeatedly for new flashes. once everything
        # has settled down and there are no new flashes, we can stop checking
        new_flashes = False
        for y in range(0, 10):
            for x in range(0, 10):
                if data[y][x] == -1:
                    # ignore octopuses that have already flashed
                    continue
                if data[y][x] > 9:
                    new_flashes = True
                    step_flashes += 1
                    data[y][x] = -1
                    for nx, ny in neighbors(x, y):
                        if data[ny][nx] != -1:
                            # ignore octopuses that have already flashed
                            data[ny][nx] += 1
        if not new_flashes:
            break

    data = [[max(x, 0) for x in y] for y in data]  # reset flashes from -1 to 0
    flashes += step_flashes
    steps += 1

    if steps == 100:
        print(f'Part 1: {flashes}')
        part_1_complete = True
        if part_2_complete:
            break

    if step_flashes == 100:
        print(f'Part 2: {steps}')
        part_2_complete = True
        if part_1_complete:
            break
