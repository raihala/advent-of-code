import itertools
from collections import Counter

# Part 1
with open('day-2-input.txt') as f:
    box_ids = [line.strip() for line in f]

letters_repeated_x2 = [b for b in box_ids if 2 in Counter(b).values()]
letters_repeated_x3 = [b for b in box_ids if 3 in Counter(b).values()]

print(len(letters_repeated_x2) * len(letters_repeated_x3))


# Part 2
class StringTree(object):
    def __init__(self, parent=None, value=None):
        self.parent = parent
        self.value = value
        self.children = []

    def get_child_node_with_value(self, value):
        for child in self.children:
            if child.value == value:
                return child
        return None

    def add_string(self, string):
        if string == '':
            return

        existing_child_node = self.get_child_node_with_value(string[0])
        if existing_child_node is not None:
            existing_child_node.add_string(string[1:])
        else:
            new_child_node = StringTree(parent=self, value=string[0])
            new_child_node.add_string(string[1:])
            self.children.append(new_child_node)

    def current_substring(self):
        """
        Build the unique substring attained by walking from the root
        node down through and including the current node.
        """
        if self.parent is None:
            return self.value or ''
        else:
            return self.parent.current_substring() + (self.value or '')

    def descendant_substrings(self):
        """
        Get a list of all substrings attained by descending from the
        current node down through all possible paths (does not include
        the current node's value).
        """
        substrings = []
        for child in self.children:
            grandchild_substrings = child.descendant_substrings()
            if grandchild_substrings:
                child_substrings = [child.value + s for s in grandchild_substrings]
            else:
                child_substrings = [child.value]
            substrings.extend(child_substrings)
        return substrings

    def strings_including_node(self):
        """
        Get a list of all full-length strings that pass through the current node.
        """
        return [self.current_substring() + s for s in self.descendant_substrings()]

    def all_nodes_at_depth(self, depth):
        """
        Get a list of all nodes at the specified depth relative to the current node.
        """
        if depth == 0:
            return [self]
        list_of_lists = [child.all_nodes_at_depth(depth-1) for child in self.children]
        return list(itertools.chain.from_iterable(list_of_lists))

    def strings_with_common_prefix_of_length(self, length):
        anchor_nodes = self.all_nodes_at_depth(length)
        string_lists = [node.strings_including_node() for node in anchor_nodes]
        return [strings for strings in string_lists if len(strings) > 1]

    def __str__(self):
        return "StringTree({} => {})".format(self.value, [c.value for c in self.children])


forward_tree = StringTree()
reverse_tree = StringTree()

for box_id in box_ids:
    forward_tree.add_string(box_id)
    reverse_tree.add_string(box_id[::-1])

length = len(box_ids[0])  # IDs must all be the same length

for i in range(length):
    same_prefix = forward_tree.strings_with_common_prefix_of_length(i)
    same_suffix = reverse_tree.strings_with_common_prefix_of_length(length-i-1)
    same_suffix = [[string[::-1] for string in string_list] for string_list in same_suffix]  # un-reverse all strings

    for string_list_1 in same_prefix:
        for string_list_2 in same_suffix:
            intersection = set(string_list_1) & set(string_list_2)
            if len(intersection) > 1:
                print(intersection)
                s = list(intersection)[0]  # arbitrarily choose a string to print
                print(s[:i] + s[i+1:])  # skip offending character
