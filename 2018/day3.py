import re


def ranges_overlap(a, b):
    """
    Determine whether two ranges (inclusive on both ends) overlap.
    """
    a_min, a_max = a
    b_min, b_max = b
    return b_max >= a_min and b_min <= a_max


class Claim(object):
    def __init__(self, claim_id, min_x, min_y, width, height):
        self.claim_id = claim_id
        self.min_x = min_x
        self.min_y = min_y
        self.width = width
        self.height = height
        self.max_x = self.min_x + width - 1
        self.max_y = self.min_y + height - 1

    def intersects(self, other):
        return (ranges_overlap((self.min_x, self.max_x), (other.min_x, other.max_x)) and
                ranges_overlap((self.min_y, self.max_y), (other.min_y, other.max_y)))

    def __contains__(self, item):
        x, y = item  # unpack 2-tuple
        return (self.min_x <= x <= self.max_x and
                self.min_y <= y <= self.max_y)

    def __str__(self):
        return "Claim(#{} @ {},{}: {}x{})".format(
            self.claim_id,
            self.min_x,
            self.min_y,
            self.width,
            self.height
        )

    __repr__ = __str__


number = '([0-9]+)'
pattern = '#{0} @ {0},{0}: {0}x{0}'.format(number)
regex = re.compile(pattern)

claims = []
with open('day-3-input.txt') as f:
    for line in f:
        res = regex.match(line.strip())
        if res is None:
            print("Input line could not be parsed! Input was: '{}'".format(line.strip()))
        else:
            claim = Claim(
                claim_id=int(res.group(1)),
                min_x=int(res.group(2)),
                min_y=int(res.group(3)),
                width=int(res.group(4)),
                height=int(res.group(5))
            )
            claims.append(claim)

# sort from biggest to smallest (maybe helpful for part 2??)
claims = sorted(claims, key=lambda x: x.width * x.height, reverse=True)


def part_one():
    overall_min_x = min([c.min_x for c in claims])
    overall_min_y = min([c.min_y for c in claims])
    overall_max_x = max([c.max_x for c in claims])
    overall_max_y = max([c.max_y for c in claims])

    contested_points = []
    for x in range(overall_min_x, overall_max_x+1):
        print("Column {}...".format(x))
        for y in range(overall_min_y, overall_max_y+1):
            covered_by = 0
            for c in claims:
                if (x, y) in c:
                    covered_by += 1
                    if covered_by >= 2:
                        break
            if covered_by >= 2:
                contested_points.append((x, y))

    print(len(contested_points))


def part_two():
    unchecked_claims = list(claims)  # copy list, not reference to list
    while unchecked_claims:
        claim = unchecked_claims[0]
        unchecked_claims.remove(claim)

        uncontested = True
        for other_claim in claims:
            if other_claim is claim:
                continue
            if claim.intersects(other_claim):
                # print(f"{claim} and {other_claim} overlap!")
                try:
                    unchecked_claims.remove(other_claim)
                except:
                    pass
                uncontested = False
                break
        if uncontested:
            print(f"{claim} is uncontested!")
            # break


# part_one()
part_two()
