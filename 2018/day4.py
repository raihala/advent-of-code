from collections import defaultdict

# Part 1
# NB I already sorted and modified the input using bash:
# tr '\n' ' '
# | sed 's/shift /shift\n/g'
# | sed 's/up /up\n/g'
# | sed 's/.*Guard #\(.*\) begins shift/\1/'
# | sed 's/.*:\(..\)] falls asleep.*:\(..\)] wakes up/\1 \2/'

with open('day-4-input.txt') as f:
    events = [[int(x) for x in line.strip().split()] for line in f]

current_guard = None
sleep_counts = defaultdict(lambda: defaultdict(int))
for event in events:
    if len(event) == 1:
        current_guard = event[0]
    else:
        sleep_start = event[0]
        sleep_end = event[1]
        for i in range(sleep_start, sleep_end):
            sleep_counts[current_guard][i] += 1

sleep_totals = [(guard_id, sum(counts.values())) for guard_id, counts in sleep_counts.items()]
sleepiest_guard_1 = max(sleep_totals, key=lambda x: x[1])[0]
sleepiest_minute_1 = max(range(60), key=lambda x: sleep_counts[sleepiest_guard_1][x])
print(
    "Guard {} sleeps the most at minute {} (a total {} times!)".format(
        sleepiest_guard_1,
        sleepiest_minute_1,
        sleep_counts[sleepiest_guard_1][sleepiest_minute_1]
    )
)
print(f'{sleepiest_guard_1} x {sleepiest_minute_1} = {sleepiest_guard_1 * sleepiest_minute_1}')

# Part 2
sleepiest_guard_2 = max(sleep_counts.keys(), key=lambda x: max(sleep_counts[x].values()))
sleepiest_minute_2 = max(range(60), key=lambda x: sleep_counts[sleepiest_guard_2][x])

print(
    "Guard {} sleeps the most at minute {} (a total {} times!)".format(
        sleepiest_guard_2,
        sleepiest_minute_2,
        sleep_counts[sleepiest_guard_2][sleepiest_minute_2]
    )
)
print(f'{sleepiest_guard_2} x {sleepiest_minute_2} = {sleepiest_guard_2 * sleepiest_minute_2}')