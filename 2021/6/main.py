DESCENDENTS_AFTER_N_DAYS = {}


def descendents_after_n_days(days_remaining):
    if days_remaining in DESCENDENTS_AFTER_N_DAYS:
        return DESCENDENTS_AFTER_N_DAYS[days_remaining]

    children = range(7, days_remaining, 7)
    if len(children) == 0:
        DESCENDENTS_AFTER_N_DAYS[days_remaining] = 0
        return 0
    children_days_remaining = [(days_remaining - x - 2) for x in children]

    descendents = len(children) + sum([descendents_after_n_days(c) for c in children_days_remaining])
    DESCENDENTS_AFTER_N_DAYS[days_remaining] = descendents
    return descendents


def calculate(initial_state, total_days):
    effective_days = [total_days + (7 - x) for x in initial_state]
    num_fish = len(initial_state)
    for days in effective_days:
        num_fish += descendents_after_n_days(days)
    return num_fish


with open('input') as f:
    initial_state = [int(x) for x in next(f).strip().split(',')]


print(calculate(initial_state, 80))
print(calculate(initial_state, 256))
