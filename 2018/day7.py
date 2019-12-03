import re
import sys

from collections import defaultdict


def available_steps(steps):
    return [s for s in steps if not steps[s]['parents']]


def next_step(steps):
    return sorted(available_steps(steps))[0]


def take_step(steps, step):
    del steps[step]
    for other_step in steps.values():
        if step in other_step['parents']:
            other_step['parents'].remove(step)


pattern = 'Step (.*) must be finished before step (.*) can begin.'
regex = re.compile(pattern)

steps = defaultdict(lambda: {'parents': [], 'children': []})
with open('day-7-input.txt') as f:
    for line in f:
        res = regex.match(line.strip())
        if res is None:
            print("Input line could not be parsed! Input was: '{}'".format(line.strip()))
            sys.exit(1)
        step_a = res.group(1)
        step_b = res.group(2)
        steps[step_a]['children'].append(step_b)
        steps[step_b]['parents'].append(step_a)

completed_steps = []
while steps:
    n = next_step(steps)
    completed_steps.append(n)
    take_step(steps, n)

print(''.join(completed_steps))
