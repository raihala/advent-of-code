# Part 1
with open('day-1-input.txt') as f:
    module_masses = [int(line.strip()) for line in f]

fuel_requirements = [m//3 - 2 for m in module_masses]
total_fuel_required = sum(fuel_requirements)
print(total_fuel_required)


# Part 2
def fuel(m):
    """
    Determine the total fuel required for a given module mass,
    taking into account the mass of the fuel itself.
    """
    while True:
        m = m//3 - 2
        if m > 0:
            yield m
        else:
            break


fuel_requirements = [sum(fuel(m)) for m in module_masses]
total_fuel_required = sum(fuel_requirements)
print(total_fuel_required)
