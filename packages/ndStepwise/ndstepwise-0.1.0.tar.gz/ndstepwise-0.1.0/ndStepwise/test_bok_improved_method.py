import itertools
import numpy as np
import pandas as pd
import concurrent.futures
import numpy as np
import math
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, ConfusionMatrixDisplay, auc, roc_auc_score, f1_score
from sklearn import datasets
from statistics import mean
import includes.model as mod
import pandas as pd
from joblib import dump, load
from includes.config import Config;
import includes.model_functions as mf
import time
from itertools import combinations
import random
from graphviz import Digraph
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from datetime import datetime 
import os
import argparse
from itertools import count

def main(filename, model_types):
    # config.log.info('Max Rocks')
    # config.log.error('This is an extra long message about how there was an error because Max wants to see if there is a weird format when messages get extra long.')
    # config.log.debug('THIS SHOULDNT LOG')
    # return
    # cats = 'EDCBA'
    # for k in itertools.combinations(cats,3):
    #     print(k)
    # return
    print(filename)
    if len(filename) <= 1:
        raise Exception(f"Improper filename of: {filename}")
    dataset = filename
    config = Config(dataset)
    config.log.info(f'Beginning of {dataset}.')
    df = pd.read_csv(dataset)
    df.drop(df.columns[0], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42)
    score_type = 'accuracy'
    # categories = tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))  
    categories = tuple(df['Y'].unique())

    # config.log.info('Beginning of stepwise tree finder.')
    # best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
    # config.log.info('Finished stepwise tree finder.')
    # model_strucs = list(best_tree.keys())
    # tree_types = list(best_tree.values())
    # best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
    # mf.graph_model(config, best_trained_model, filename)

    def parse_comparisons(comparisons):
        # Build a tree like structure
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

        # Now check if the tree is full from the root
        stack = [root]
        while stack:
            node = stack.pop()
            if node in tree:
                left_child, right_child = tree[node]
                stack.extend([left_child, right_child])
            elif len(node) != 1:
                #if it's not a leaf node and not in my tree
                return False

        return True

    def check_if_tree(comparisons):
        # Build a tree like structure
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

        # Now check if the tree is full from the root
        stack = [root]
        visited = set()
        while stack:
            node = stack.pop()
            if node in visited:
                return False  # Detect cycles
            visited.add(node)
            if node in tree:
                left_child, right_child = tree[node]
                stack.extend([left_child, right_child])
            else:
                if len(node) > 1:  # Non-leaf node must be found in the tree dictionary
                    return False

        # Ensure all nodes are visited (no disconnected nodes)
        if visited != all_nodes.union(child_nodes):
            return False

        return True


    def find_root(all_nodes, children_nodes):
        possible_roots = all_nodes - children_nodes
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


    # Example comparisons in the specified format
    comparisons = [   
        ((1,2,3), (4,5,6)),
        ((1,2), (3,)),
        ((1,), (2,)),
        ((5,), (6,)),
        ((4,), (6,)),
        ((1,2,3), (4,)),
        ((1, 2, 3, 4), (5, 6)),
    ]


    comparisons = [   
        ((1,2), (3,)),
        ((1,), (2,)),
        ((5,), (6,)),
        ((1, 2, 3), (4,)),
        ((1, 2, 3, 4), (5, 6)),
    ]  
    best_cutoff_tree = [((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))]

    def check_if_works(comparisons):
        tree, all_nodes, children_nodes = parse_comparisons(comparisons)
        root = find_root(all_nodes, children_nodes)
        return check_full_tree(tree, root)

    def combinations_generator(main_list, n):
        for combination in itertools.combinations(main_list, n):
            yield combination


    best_cutoff_tree = [((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))]
    best_overall_tree = [[(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)], [(0, 1, 2), (3, 4)], [(5, 6, 7, 8), (9,)], [(0, 2), (1,)], [(3,), (4,)], [(5, 6), (7, 8)], [(0,), (2,)], [(5,), (6,)], [(7,), (8,)]]    
    bad_tree = [((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4))]
    cut_off_again = [((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))]

    best_cutoff_tree = [
        ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4)),
        ((3,), (4,)), 
        # ((3,), (0, 1, 2, 4, 6, 7, 9)), 
        ((6,), (7, 8)), 
        ((7,), (8,)), 
        ((5,), (6, 7, 8)), 
        ((1,), (0, 2)), 
        ((0,), (2,)), 
        ((9,), (6, 7, 8, 5)), 
        # ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), 
        ((3, 4), (0, 1, 2)),
        ((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))
        ]

    best_cutoff_tree = [
        ((3,), (4,)), 
        ((6,), (7, 8)), 
        ((7,), (8,)), 
        ((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4)),
    ]
    is_tree = [((6,), (2,)), ((6,), (1,)), ((4, 2), (1, 6)), ((4,), (6, 2)), ((4, 6, 2), (1,))]
    print("is this a tree ",check_if_tree(is_tree))

    result = None
    n = 10
    # return
    # for tree in combinations_generator(list(dict.fromkeys(best_cutoff_tree)), n-1):
    #     if tree == tuple(bad_tree):
    #         print("bad tree has been spotted")
    #         # break
    #     if check_if_works(tree):
    #         # print(f"Found my tree is {tree}")
    #         result = tree
    #         break

    # taken from https://github.com/v-melnikov/nested-dichotomies/blob/master/nd/BBoK.py from paper
    # paper is "On the Effectiveness of Heuristics for Learning Nested Dichotomies: An Empirical Analysis"
    def generate_bbok_split(enc):
        c = len(bin(enc)[2:])
        a = np.arange(c, dtype=int)
        rc = a[(1 << a & enc).astype(bool)]

        if len(rc) == 1:
            return (1 << rc[0], 0)

        sub_id = np.random.randint(1, np.power(2, len(rc) - 1))
        mask = format(sub_id, 'b').zfill(len(rc))
        mask = np.array(list(mask), dtype=int)

        c1_group = rc[mask.astype(bool)]
        c2_group = np.setdiff1d(rc, c1_group)

        return (np.sum(1 << np.array(c1_group)), np.sum(1 << np.array(c2_group)))

    def decode_split(split, labels):
        """Convert binary splits into subsets of elements."""
        c1_bin, c2_bin = split
        c1 = [i for i in labels if (1 << i) & c1_bin]
        c2 = [i for i in labels if (1 << i) & c2_bin]
        return (tuple(c1), tuple(c2))

    def generate(n, labels=None, seed=42):
        ds = []  # dichotomies
        s = []  # stack
        if labels is None:
            labels = np.arange(n, dtype=int)
        rc = np.sum([1 << i for i in labels])
        np.random.seed(seed)

        root_split = generate_bbok_split(rc)
        s.append(root_split)
        while len(s) != 0:
            split = s.pop()
            ds.append(split)

            if split[1] != 0:
                s.append(generate_bbok_split(split[1]))
                s.append(generate_bbok_split(split[0]))
            else:
                ds.pop()
        decoded_splits = [decode_split(split, labels) for split in ds]
        decoded_splits = [tuple(tuple(sorted(tup)) for tup in pair) for pair in decoded_splits]
        return tuple(decoded_splits)
    
    def custom_combinations(elements, order):

        def generate_combinations(prefix, start, order):
            if order == 0:
                yield prefix
                return
            
            for i in range(start, len(elements)):
                next_prefix = prefix + (elements[i],)
                yield from generate_combinations(next_prefix, i + 1, order - 1)
    
        yield from generate_combinations((), 0, order)

    def prioritized_combinations(elements, order):
        def generate_combinations(prefix, start, remaining_order):
            if remaining_order == 0:
                yield prefix
                return

            for i in range(len(elements) - 1, start - 1, -1):
                next_prefix = (elements[i],) + prefix
                yield from generate_combinations(next_prefix, i - 1, remaining_order - 1)

        yield from generate_combinations((), len(elements) - 1, order)

    def find_tree(config, binary_comparisons, n):
        config.log.info(f'Starting combinations.')
        counter = 0
        result = None
        for tree in custom_combinations(binary_comparisons, n):
            counter +=1
            if (counter % 1000000) == 0:
                print(tree)
                print(counter)

            if check_if_tree(tree):
                config.log.info(f"Found my tree is {tree}")
                result = tree
                break
        return result
    # categories = 10
    comparisons = [   
        ((1,2), (3,)),
        ((1,), (2,)),
        ((5,), (6,)),
        ((1, 2, 3), (4,)),
        ((1, 2, 3, 4), (5, 6)),
        ((4,), (6,)),
        ((8,), (9,))
    ]  


    comparisons = 'abcdef'
    def coolCombinations(n, w):
        #n <- number of elements, w <- how many to choose, n > w
        b = n - w
        combo = (1,)*w + (0,)*b
        inc = n-2
        while inc != n-1:
            index = min(inc+2,n-1)
            combo = (combo[index],) + combo[:index] + combo[index+1:]
            inc = 0 if combo[0] < combo[1] else inc+1
            yield combo

    w = 3  # number of 1's
    b = 1  # number of 0's

    # Call the function and iterate over the generator
    for combination in coolCombinations(5, 3):
        print(combination)
    
    # for tree in graded_lexicographic_combinations(comparisons, 3):
    #     print(tree)
            # counter +=1
            # if (counter % 1000000) == 0:
            #     print(tree)
            #     print(counter)

            # if check_if_tree(tree):
            #     config.log.info(f"Found my tree is {tree}")
            #     result = tree
            #     break
    # return
    number_of_trees = 50
    # best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
    # mf.graph_model(config, best_trained_model, filename)
    # filtered_tuples = [item for item in list_of_tuples if item not in dictionary.keys()]
    all_binary_comparisons = {}
    all_full_trees = []
    for i in range(number_of_trees):
        random_mod_structure = generate(len(categories), categories, seed=i)
        print(random_mod_structure)
        all_full_trees.append(random_mod_structure)
        new_binary_comparisons = tuple(item for item in random_mod_structure if item not in all_binary_comparisons.keys())
        first_model = mf.build_single_models(config, new_binary_comparisons, X_train, train_type='LogisticRegression')
        prop_model_scores = mf.test_single_models(first_model, X_test)
        all_binary_comparisons.update(prop_model_scores)

    sorted_binary_comparisons = sorted(all_binary_comparisons.items(), key=lambda item: item[1], reverse=True)
    print(sorted_binary_comparisons)
    only_comparisons = [item[0] for item in sorted_binary_comparisons]
    print(len(only_comparisons))
    config.log.info(f'Finished {dataset}.')
    # all_combos = itertools.combinations(first_50, n)
    # print(len(all_combos))

    
    result = find_tree(config, only_comparisons[:50], len(categories)-1)
    # for tree in custom_combinations(first_few, len(categories)-1):
    #     counter +=1
    #     if (counter % 1000000) == 0:
    #         print(tree)
    #         print(counter)

    #     if check_if_tree(tree):
    #         print(f"Found my tree is {tree}")
    #         result = tree
    #         break
    if not result:
        config.log.info(f'No tree was found so we have to expand the search.')
        result = find_tree(config, only_comparisons, len(categories)-1)
        ##TODO expand the search 
        raise Exception('No tree was found.')
    config.log.info(f'Ending combinations with tree {result}.')
    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, ['LogisticRegression']*5, result, categories)
    mf.graph_model(config, best_trained_model, filename)
    print(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename', required=True, type=str, help='The name of the file to process')
    parser.add_argument('-m', '--model_types', type=str, nargs='*', default=['randomForest', 'LogisticRegression', 'xgboost'], help='An optional list models to be tested out of randomForest, LogisticRegression, xgboost, svm.')
    args = parser.parse_args()  
    main(args.filename, args.model_types)