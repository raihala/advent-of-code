with open('input') as f:
    grid = [[c for c in line.strip()] for line in f]

height = len(grid)
width = len(grid[0])
steps = 0
while True:
    updated = False

    new_grid = [row[:] for row in grid]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == '>':
                next_x = (x + 1) % width
                if grid[y][next_x] == '.':
                    new_grid[y][next_x] = '>'
                    new_grid[y][x] = '.'
                    updated = True
    grid = new_grid

    new_grid = [row[:] for row in grid]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 'v':
                next_y = (y + 1) % height
                if grid[next_y][x] == '.':
                    new_grid[next_y][x] = 'v'
                    new_grid[y][x] = '.'
                    updated = True
    grid = new_grid

    steps += 1
    if not updated:
        break

print(steps)
