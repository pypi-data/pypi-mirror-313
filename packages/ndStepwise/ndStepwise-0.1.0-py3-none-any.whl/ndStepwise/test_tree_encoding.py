
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def encode_tree(comparisons):
    comparisons = [tuple(sorted(tup) for tup in pair) for pair in comparisons]
    tree = {}
    all_nodes = set()
    child_nodes = set()
    for left, right in comparisons:
        parent = tuple(sorted(left + right))
        tree[parent] = (tuple(left), tuple(right))
        all_nodes.add(parent)
        child_nodes.update([tuple(left), tuple(right)])
    
    possible_roots = all_nodes - child_nodes
    if len(possible_roots) != 1:
        return False
    else:
        root = possible_roots.pop()
    return tree


def generate_possible_structures():
    # Example function to generate possible structures (to be implemented)
    # Here, we use some manually defined examples for demonstration
    return [
        ((1, 2), (3,)),
        ((1,), (2,)),
        ((5,), (6,)),
        ((1, 2, 3), (4,)),
        ((1, 2, 3, 4), (5, 6))
    ]

trees = [
    ((1, 2), (3,)),
    ((1,), (2,)),
    ((5,), (6,)),
    ((1, 2, 3), (4,)),
    ((1, 2, 3, 4), (5, 6))
]

# Encode trees
max_depth = 3  # Define the maximum depth for encoding
# encoded_trees = [encode_tree(tree, max_depth) for tree in trees]
print(encode_tree(trees))

# # Ensure all vectors have the same length by padding with zeros
# max_length = max(len(tree) for tree in encoded_trees)
# encoded_trees = [tree + [0] * (max_length - len(tree)) for tree in encoded_trees]
# encoded_trees = np.array(encoded_trees)

# # Corresponding scores
# scores = np.array([0.8, 0.7, 0.87, 0.92, 0.63])

# # Generate and encode possible structures
# possible_structures = generate_possible_structures()
# encoded_possible_structures = [encode_tree(tree, max_depth) for tree in possible_structures]

# # Ensure all vectors have the same length by padding with zeros
# encoded_possible_structures = [tree + [0] * (max_length - len(tree)) for tree in encoded_possible_structures]
# encoded_possible_structures = np.array(encoded_possible_structures)

# # Predict scores for these structures
# predicted_scores = model.predict(encoded_possible_structures)

# # Find the structure with the highest predicted score
# optimal_structure_index = np.argmax(predicted_scores)
# optimal_structure = possible_structures[optimal_structure_index]
# print("Optimal Tree Structure:", optimal_structure)
# print("Predicted Score:", predicted_scores[optimal_structure_index])