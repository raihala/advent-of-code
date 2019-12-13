from itertools import combinations
from operator import add, sub


class Moon(object):
    def __init__(self, name, pos, vel):
        self.name = name
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return self.name

    def update_position(self):
        self.pos = tuple(map(add, self.pos, self.vel))

    def status(self):
        return (f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, "
                f"vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>")

    @property
    def potential_energy(self):
        return sum(map(abs, self.pos))

    @property
    def kinetic_energy(self):
        return sum(map(abs, self.vel))

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy


test_moons = [
    Moon('Io', pos=(-1, 0, 2), vel=(0, 0, 0)),
    Moon('Europa', pos=(2, -10, -7), vel=(0, 0, 0)),
    Moon('Ganymede', pos=(4, -8, 8), vel=(0, 0, 0)),
    Moon('Callisto', pos=(3, 5, -1), vel=(0, 0, 0))
]


moons = [
    Moon('Io', pos=(-16, -1, -12), vel=(0, 0, 0)),
    Moon('Europa', pos=(0, -4, -17), vel=(0, 0, 0)),
    Moon('Ganymede', pos=(-11, 11, 0), vel=(0, 0, 0)),
    Moon('Callisto', pos=(2, 2, -6), vel=(0, 0, 0))
]


def sign(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:  # not worrying here about anything funny like nan
        return 0


def time_step(system):
    # update velocities
    for moon1, moon2 in combinations(system, 2):
        acceleration = tuple(map(sign, map(sub, moon2.pos, moon1.pos)))
        moon1.vel = tuple(map(add, moon1.vel, acceleration))
        moon2.vel = tuple(map(sub, moon2.vel, acceleration))

    # update positions
    for moon in system:
        moon.update_position()


for n in range(1000):
    time_step(moons)

system_energy = sum([moon.total_energy for moon in moons])
print(system_energy)
