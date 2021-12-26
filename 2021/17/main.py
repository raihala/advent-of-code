import re
from collections import defaultdict

with open('input') as f:
    pattern = 'target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)'
    line = next(f).strip()
    match = re.match(pattern, line)
    x_min, x_max, y_min, y_max = map(int, match.groups())

# pretty sure this only works if y_min < 0
part_1_res = (y_min**2 + y_min) // 2
print(part_1_res)

valid_y_velocities = defaultdict(list)
vy_min = y_min
vy_max = -1 - y_min
for vy in range(vy_min, vy_max + 1):
    y = 0
    t = 0
    v = vy
    while y >= y_min:
        if y_min <= y <= y_max:
            valid_y_velocities[t].append(vy)
        y += v
        t += 1
        v -= 1

t_max = max(valid_y_velocities)

valid_x_velocities = defaultdict(list)
vx_min = 0
vx_max = x_max
for vx in range(vx_min, vx_max + 1):
    for t in range(vx + 1):
        x = vx*t - t*(t-1)//2
        if x_min <= x <= x_max:
            valid_x_velocities[t].append(vx)
            if t == vx:
                for future_t in range(t+1, t_max+1):
                    valid_x_velocities[future_t].append(vx)

valid_velocities = []
for t in valid_x_velocities:
    if t not in valid_y_velocities:
        continue
    valid_velocities.extend([
        (vx, vy)
        for vx in valid_x_velocities[t]
        for vy in valid_y_velocities[t]
    ])

part_2_res = len(set(valid_velocities))
print(part_2_res)
