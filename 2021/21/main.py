from itertools import cycle

with open('input') as f:
    p1_start = int(next(f).strip().split()[-1])
    p2_start = int(next(f).strip().split()[-1])


def m(x):
    return ((x - 1) % 10) + 1


p1_turn = cycle([
    m(p1_start + 6),
    p1_start,
    m(p1_start + 2),
    m(p1_start + 2),
    p1_start
])

p2_turn = cycle([
    m(p2_start + 5),
    m(p2_start + 8),
    m(p2_start + 9),
    m(p2_start + 8),
    m(p2_start + 5),
    p2_start,
    m(p2_start + 3),
    m(p2_start + 4),
    m(p2_start + 3),
    p2_start
])

p1_score = 0
p2_score = 0
rolls = 0

while True:
    p1_score += next(p1_turn)
    rolls += 3
    if p1_score >= 1000:
        break

    p2_score += next(p2_turn)
    rolls += 3
    if p2_score >= 1000:
        break

part_1_res = min(p1_score, p2_score) * rolls
print(part_1_res)

dice_rolls = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]
cache = {}  # will map (pos1, pos2, score1, score2) tuples to [wins1, wins2] pairs


def winning_universes(pos1, pos2, score1, score2):
    if (pos1, pos2, score1, score2) in cache:
        return cache[(pos1, pos2, score1, score2)]

    wins = [0, 0]
    for p1, u1 in dice_rolls:
        new_pos1 = m(pos1 + p1)
        new_score1 = score1 + new_pos1
        if new_score1 >= 21:
            wins[0] += u1
            continue

        for p2, u2 in dice_rolls:
            new_pos2 = m(pos2 + p2)
            new_score2 = score2 + new_pos2
            if new_score2 >= 21:
                wins[1] += u1 * u2
                continue

            later_wins1, later_wins2 = winning_universes(
                new_pos1, new_pos2, new_score1, new_score2
            )
            wins[0] += u1 * u2 * later_wins1
            wins[1] += u1 * u2 * later_wins2

    cache[(pos1, pos2, score1, score2)] = wins
    return wins


universes = winning_universes(p1_start, p2_start, 0, 0)
part_2_res = max(universes)
print(part_2_res)
