def parse_comparisons(comparisons):
    comparisons = [tuple(sorted(tup) for tup in pair) for pair in comparisons]
    tree = {}
    all_nodes = set()
    children_nodes = set()
    
    for left, right in comparisons:
        parent = tuple(sorted(left + right))
        tree[parent] = (tuple(left), tuple(right))
        all_nodes.add(parent)
        children_nodes.update([tuple(left), tuple(right)])
    
    return tree, all_nodes, children_nodes

def find_root(all_nodes, children_nodes):
    possible_roots = all_nodes - children_nodes
    print(f"possible roots are {possible_roots}")
    return possible_roots.pop() if len(possible_roots) == 1 else None

def check_full_tree(tree, root):
    if not root:
        return False
    stack = [root]
    while stack:
        node = stack.pop()
        if node in tree:
            left_child, right_child = tree[node]
            stack.extend([left_child, right_child])
        elif len(node) != 1:
            return False
    return True

def custom_combinations(elements, order):
    # elements = sorted(elements, reverse=True)  # Start with the highest elements

    def generate_combinations(prefix, start, order):
        if order == 0:
            yield prefix
            return
        
        for i in range(start, len(elements)):
            next_prefix = prefix + (elements[i],)
            yield from generate_combinations(next_prefix, i + 1, order - 1)

    yield from generate_combinations((), 0, order)

elements = ['A', 'B', 'C', 'D', 'E']
order = 3

for comb in custom_combinations(elements, order):
    print(comb)

comparisons = [   
    ((1,2), (3,)),
    ((1,), (2,)),
    ((5,), (6,)),
    ((1, 2, 3), (4,)),
    ((1, 2, 3, 4), (5, 6)),
]  
best_cutoff_tree = [
    ((3,), (4,)), 
    ((6,), (7, 8)), 
    ((7,), (8,)), 
    ((5,), (6, 7, 8)), 
    ((1,), (0, 2)), 
    ((0,), (2,)), 
    ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), 
    ((9,), (6, 7, 8, 5)), 
    ((3, 4), (0, 1, 2)),
]


tree, all_nodes, children_nodes = parse_comparisons(best_cutoff_tree)
root = find_root(all_nodes, children_nodes)
is_full_tree = check_full_tree(tree, root)

print(tree)
print(all_nodes)
print(children_nodes)
print(f"root is {root}")
print("Is the structure a full tree?", is_full_tree)