import sys
from collections import Counter


class Amphipod(object):
    energy_table = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    bad_spaces = ['hallway2', 'hallway4', 'hallway6', 'hallway8']

    def __init__(self, name, space):
        self.name = name
        self.energy_step = self.energy_table[name]
        self.energy_used = 0
        self.space = space
        self.space.occupant = self

    def __str__(self):
        return f'Amphipod({self.name})'

    __repr__ = __str__

    def move_to(self, space):
        possible_moves = self.possible_moves()
        if space not in possible_moves:
            raise RuntimeError('Amphipod tried to move to inaccessible space!')

        self.space.occupant = None
        self.energy_used += possible_moves[space] * self.energy_step
        space.occupant = self
        self.space = space

    def possible_moves(self):
        accessible_spaces = self.space.other_accessible_spaces()
        res = {}
        if self.space.name == f'room{self.name}3':
            # don't ever move out of this spot
            return res
        if (self.space.name == f'room{self.name}2' and
                spaces[f'room{self.name}3'].occupant.name == self.name):
            # don't ever move out of this spot
            return res
        if (self.space.name == f'room{self.name}1' and
                spaces[f'room{self.name}2'].occupant.name == self.name and
                spaces[f'room{self.name}3'].occupant.name == self.name):
            # don't ever move out of this spot
            return res
        if (self.space.name == f'room{self.name}0' and
                spaces[f'room{self.name}1'].occupant.name == self.name and
                spaces[f'room{self.name}2'].occupant.name == self.name and
                spaces[f'room{self.name}3'].occupant.name == self.name):
            # don't ever move out of this spot
            return res

        for space, distance in accessible_spaces.items():
            if space.name in self.bad_spaces:
                # can't stand right outside room
                continue
            if space.name.startswith('room'):
                if space.name.endswith('0') and not spaces[space.name[:5] + '1'].occupied:
                    # don't move into the inner room if you could move into the outer room
                    continue
                if space.name.endswith('1') and not spaces[space.name[:5] + '2'].occupied:
                    # don't move into the inner room if you could move into the outer room
                    continue
                if space.name.endswith('2') and not spaces[space.name[:5] + '3'].occupied:
                    # don't move into the inner room if you could move into the outer room
                    continue
                if space.name[:5] not in [self.space.name[:5], f'room{self.name}']:
                    # can't go to wrong room if we're not already in it
                    continue
                if space.name[:5] == self.space.name[:5]:
                    # don't move within same room
                    continue
                if any([a.name != self.name for a in space.room_occupants()]):
                    # can't go to right room with wrong occupants
                    continue
            if self.space.name.startswith('hallway') and space.name.startswith('hallway'):
                # can't go from hallway to hallway
                continue
            res[space] = distance

        return res

    def state(self):
        return self.space, self.energy_used

    def reset(self, state):
        space, energy_used = state
        self.space.occupant = None
        self.space = space
        self.space.occupant = self
        self.energy_used = energy_used


class Space(object):
    def __init__(self, name):
        self.name = name
        self.neighbors = []
        self.occupant = None

    def __str__(self):
        return f'Space({self.name})'

    __repr__ = __str__

    def __hash__(self):
        return hash(self.name)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def pp(self):
        if self.occupant is None:
            return '.'
        return self.occupant.name

    @property
    def occupied(self):
        return self.occupant is not None

    def room_occupants(self):
        res = []
        if self.name.startswith('hallway'):
            return res
        room_spaces = [s for s in spaces.values() if s.name.startswith(self.name[:5])]
        for space in room_spaces:
            if space.occupant is not None:
                res.append(space.occupant)
        return res

    def other_accessible_spaces(self):
        """
        Returns {Space: int} dict mapping spaces accessible from
        this space to their distances away.
        """
        res = {}
        to_check = self.neighbors
        distance = 0
        while len(to_check) > 0:
            distance += 1
            new_to_check = []
            for space in to_check:
                if space.occupied:
                    continue
                res[space] = distance
                for next_space in space.neighbors:
                    if next_space is self or next_space in res or next_space.occupied:
                        continue
                    new_to_check.append(next_space)
            to_check = new_to_check

        return res


def pp(spaces):
    print('#' * 13)
    print(f'#{"".join([spaces[f"hallway{x}"].pp() for x in range(11)])}#')
    print(f'###{spaces["roomA0"].pp()}#{spaces["roomB0"].pp()}#{spaces["roomC0"].pp()}#{spaces["roomD0"].pp()}###')
    print(f'  #{spaces["roomA1"].pp()}#{spaces["roomB1"].pp()}#{spaces["roomC1"].pp()}#{spaces["roomD1"].pp()}#  ')
    print('  #########  ')
    print()


def pp2(spaces, indent):
    print(' ' * indent + '#' * 13)
    print(' ' * indent + f'#{"".join([spaces[f"hallway{x}"].pp() for x in range(11)])}#')
    print(' ' * indent + f'###{spaces["roomA0"].pp()}#{spaces["roomB0"].pp()}#{spaces["roomC0"].pp()}#{spaces["roomD0"].pp()}###')
    for n in range(1, 4):
        print(' ' * indent + f'  #{spaces[f"roomA{n}"].pp()}#{spaces[f"roomB{n}"].pp()}#{spaces[f"roomC{n}"].pp()}#{spaces[f"roomD{n}"].pp()}#  ')
    print(' ' * indent + '  #########  ')
    print()


def energy(amphipods):
    return sum([a.energy_used for a in amphipods])


def initialize_part1():
    spaces = {}
    for n in range(11):
        name = f'hallway{n}'
        spaces[name] = Space(name)
    for r in ['A', 'B', 'C', 'D']:
        for n in range(2):
            name = f'room{r}{n}'
            spaces[name] = Space(name)
        spaces[f'room{r}0'].add_neighbor(spaces[f'room{r}1'])
        spaces[f'room{r}1'].add_neighbor(spaces[f'room{r}0'])

    spaces['hallway0'].add_neighbor(spaces['hallway1'])
    spaces['hallway10'].add_neighbor(spaces['hallway9'])
    for n in range(1, 10):
        spaces[f'hallway{n}'].add_neighbor(spaces[f'hallway{n-1}'])
        spaces[f'hallway{n}'].add_neighbor(spaces[f'hallway{n+1}'])

    spaces['roomA0'].add_neighbor(spaces['hallway2'])
    spaces['roomB0'].add_neighbor(spaces['hallway4'])
    spaces['roomC0'].add_neighbor(spaces['hallway6'])
    spaces['roomD0'].add_neighbor(spaces['hallway8'])
    spaces['hallway2'].add_neighbor(spaces['roomA0'])
    spaces['hallway4'].add_neighbor(spaces['roomB0'])
    spaces['hallway6'].add_neighbor(spaces['roomC0'])
    spaces['hallway8'].add_neighbor(spaces['roomD0'])

    amphipods = [
        Amphipod('D', spaces['roomA0']),
        Amphipod('B', spaces['roomA1']),
        Amphipod('C', spaces['roomB0']),
        Amphipod('A', spaces['roomB1']),
        Amphipod('D', spaces['roomC0']),
        Amphipod('A', spaces['roomC1']),
        Amphipod('B', spaces['roomD0']),
        Amphipod('C', spaces['roomD1'])
    ]

    return spaces, amphipods


def amphipodhash(amphipods):
    return ''.join(sorted([f'{a.name}{a.space.name}' for a in amphipods]))


def reset(amphipods, states):
    if len(amphipods) != len(states):
        raise RuntimeError('Bad arguments to reset!')
    for amphipod, state in zip(amphipods, states):
        amphipod.reset(state)


final_hash = 'AroomA0AroomA1BroomB0BroomB1CroomC0CroomC1DroomD0DroomD1'
seen_hashes = set()
cache = {final_hash: 0}


def recurse(amphipods, r=0):
    current_hash = amphipodhash(amphipods)
    if current_hash in cache:
        return cache[current_hash]
    if current_hash in seen_hashes:
        return 10 ** 100
    seen_hashes.add(current_hash)

    state = [a.state() for a in amphipods]
    res = 10 ** 100
    for a in amphipods:
        for space in a.possible_moves():
            start_energy = energy(amphipods)
            a.move_to(space)
            next_energy = energy(amphipods)
            energy_downstream = recurse(amphipods, r+1)
            energy_maybe = (next_energy - start_energy) + energy_downstream
            res = min(res, energy_maybe)
            reset(amphipods, state)
    cache[current_hash] = res
    return res


# spaces, amphipods = initialize_part1()
# x = recurse(amphipods)
# print(x)


def initialize_part2():
    spaces = {}

    for n in range(11):
        name = f'hallway{n}'
        spaces[name] = Space(name)
    spaces['hallway0'].add_neighbor(spaces['hallway1'])
    spaces['hallway10'].add_neighbor(spaces['hallway9'])
    for n in range(1, 10):
        spaces[f'hallway{n}'].add_neighbor(spaces[f'hallway{n-1}'])
        spaces[f'hallway{n}'].add_neighbor(spaces[f'hallway{n+1}'])

    for r in ['A', 'B', 'C', 'D']:
        for n in range(4):
            name = f'room{r}{n}'
            spaces[name] = Space(name)
        spaces[f'room{r}0'].add_neighbor(spaces[f'room{r}1'])
        spaces[f'room{r}3'].add_neighbor(spaces[f'room{r}2'])
        for n in range(1, 3):
            spaces[f'room{r}{n}'].add_neighbor(spaces[f'room{r}{n-1}'])
            spaces[f'room{r}{n}'].add_neighbor(spaces[f'room{r}{n+1}'])

    spaces['roomA0'].add_neighbor(spaces['hallway2'])
    spaces['roomB0'].add_neighbor(spaces['hallway4'])
    spaces['roomC0'].add_neighbor(spaces['hallway6'])
    spaces['roomD0'].add_neighbor(spaces['hallway8'])
    spaces['hallway2'].add_neighbor(spaces['roomA0'])
    spaces['hallway4'].add_neighbor(spaces['roomB0'])
    spaces['hallway6'].add_neighbor(spaces['roomC0'])
    spaces['hallway8'].add_neighbor(spaces['roomD0'])

    amphipods = [
        Amphipod('D', spaces['roomA0']),
        Amphipod('B', spaces['roomA3']),
        Amphipod('C', spaces['roomB0']),
        Amphipod('A', spaces['roomB3']),
        Amphipod('D', spaces['roomC0']),
        Amphipod('A', spaces['roomC3']),
        Amphipod('B', spaces['roomD0']),
        Amphipod('C', spaces['roomD3']),
        Amphipod('D', spaces['roomA1']),
        Amphipod('D', spaces['roomA2']),
        Amphipod('C', spaces['roomB1']),
        Amphipod('B', spaces['roomB2']),
        Amphipod('B', spaces['roomC1']),
        Amphipod('A', spaces['roomC2']),
        Amphipod('A', spaces['roomD1']),
        Amphipod('C', spaces['roomD2']),
    ]

    return spaces, amphipods


spaces, amphipods = initialize_part2()



final_hash2 = ('AroomA0AroomA1AroomA2AroomA3BroomB0BroomB1BroomB2BroomB3' +
               'CroomC0CroomC1CroomC2CroomC3DroomD0DroomD1DroomD2DroomD3')
seen_hashes2 = set()
cache2 = {final_hash2: 0}

def recurse2(amphipods, r=0):
    global num
    current_hash = amphipodhash(amphipods)
    # pp2(spaces, r*2)
    if current_hash in cache2:
        return cache2[current_hash]
    if current_hash in seen_hashes2:
        return 10 ** 100
    seen_hashes2.add(current_hash)

    state = [a.state() for a in amphipods]
    res = 10 ** 100
    for a in amphipods:
        for space in a.possible_moves():
            start_energy = energy(amphipods)
            a.move_to(space)
            next_energy = energy(amphipods)
            energy_downstream = recurse2(amphipods, r+1)
            energy_maybe = (next_energy - start_energy) + energy_downstream
            res = min(res, energy_maybe)
            reset(amphipods, state)
    cache2[current_hash] = res
    return res


x = recurse2(amphipods)
print(x)

# for s in spaces.values():
#     print(f'{s}: {len(s.neighbors)}')
