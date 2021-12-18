class Tree(object):
    def __init__(self, data=None, lchild=None, rchild=None, parent=None):
        self.parent = parent
        if data is not None:
            if type(data) is int:
                self.value = data
                self.lchild = None
                self.rchild = None
            else:
                self.value = None
                self.lchild = Tree(data[0], parent=self)
                self.rchild = Tree(data[1], parent=self)
        elif lchild is not None and rchild is not None:
            self.value = None
            self.lchild = lchild
            self.rchild = rchild
        else:
            raise RuntimeError('Incorrect arguments to Tree()!')

    def to_list(self):
        if self.value is not None:
            return self.value
        return [self.lchild.to_list()] + [self.rchild.to_list()]

    def __str__(self):
        return f'Tree({self.to_list()})'

    __repr__ = __str__

    @property
    def leaves(self):
        if self.value is not None:
            return [self]
        return self.lchild.leaves + self.rchild.leaves

    @property
    def depth(self):
        if self.parent is None:
            return 0
        return 1 + self.parent.depth

    @property
    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3 * self.lchild.magnitude + 2 * self.rchild.magnitude

    def reduce_step(self):
        """
        Does one reduce step. Returns bool indicating
        whether or not any changes were made.
        """
        # first consider explosions
        leaves = self.leaves
        for i in range(len(leaves) - 1):
            leaf = leaves[i]
            if leaf.depth > 4:
                next_leaf = leaves[i+1]
                if next_leaf.depth != leaf.depth:
                    raise RuntimeError('Encountered non-pair at depth >= 4!')
                if i > 0:
                    leaves[i-1].value += leaf.value
                if i < len(leaves) - 2:
                    leaves[i+2].value += next_leaf.value
                parent = leaf.parent
                parent.value = 0
                parent.lchild = None
                parent.rchild = None
                return True

        # if there were no explosions, consider splits
        for leaf in leaves:
            if leaf.value > 9:
                l_val = leaf.value // 2
                if leaf.value % 2:
                    r_val = l_val + 1
                else:
                    r_val = l_val
                leaf.value = None
                leaf.lchild = Tree(l_val, parent=leaf)
                leaf.rchild = Tree(r_val, parent=leaf)
                return True

        return False

    def reduce(self):
        keep_going = True
        while keep_going:
            keep_going = self.reduce_step()

    def __add__(self, other):
        res = Tree(lchild=self, rchild=other)
        self.parent = res
        other.parent = res
        res.reduce()
        return res


with open('input') as f:
    data = [eval(line) for line in f]

part_1_res = Tree(data[0]) + Tree(data[1])
for d in data[2:]:
    part_1_res += Tree(d)
print(part_1_res.magnitude)

part_2_res = 0
for i in range(len(data)):
    for j in range(len(data)):
        if i == j:
            continue
        magnitude = (Tree(data[i]) + Tree(data[j])).magnitude
        part_2_res = max(part_2_res, magnitude)

print(part_2_res)
