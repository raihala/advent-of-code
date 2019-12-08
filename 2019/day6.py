from collections import defaultdict, namedtuple

"""
For this problem, we need to find the sum of the depths of each node
in a tree. This can be done recursively--the cumulative depth at a given
node is its own depth, plus the sum of the cumulative depths at each of
its children.
"""


orbits = defaultdict(lambda: {'parent': None, 'children': []})
with open('day-6-input.txt') as f:
    for line in f:
        parent_name, name = line.strip().split(')')
        orbits[parent_name]['children'].append(name)
        orbits[name]['parent'] = parent_name


def cumulative_tree_depth(node, depth=0):
    return depth + sum([cumulative_tree_depth(child, depth+1) for child in orbits[node]['children']])


# Part 1
print(cumulative_tree_depth('COM'))

# Part 2
src = orbits['YOU']['parent']
dst = orbits['SAN']['parent']


def find_santa(curr_pos=src, prev_pos='YOU', transfers=0):
    """
    Recursively determine the distance to santa by testing
    each possible next orbital transfer at each juncture.
    """
    if curr_pos == dst:  # base case: we found it!
        return transfers

    # let's try moving inward (unless that would be retracing our steps)
    parent = orbits[curr_pos]['parent']
    if parent is not None and parent != prev_pos:
        possible_route = find_santa(curr_pos=parent, prev_pos=curr_pos, transfers=transfers+1)
        if possible_route is not False:
            return possible_route

    # if we're still here, inward didn't work. let's move outward...
    children = [c for c in orbits[curr_pos]['children'] if c != prev_pos]  # don't retrace steps
    for child in children:
        possible_route = find_santa(curr_pos=child, prev_pos=curr_pos, transfers=transfers+1)
        if possible_route is not False:
            return possible_route

    # at this point there are no possible routes. return false
    return False


print(find_santa())
