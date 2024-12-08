import pandas as pd
# import sklearn as sk
import numpy as np
import math
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, ConfusionMatrixDisplay, auc
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

def main(config):
    df = pd.read_csv('new_100k_10_cat.csv') 
    categories = tuple((0,1,2,3,4,5,6,7,8,9))

    # df = pd.read_csv('100k_6_cat.csv')   
    # categories = tuple((1,2,3,4,5,6))
    df.drop(df.columns[0], axis=1,inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42) 
    #cross_val_predict()
    # stepwise_models = mf.stepwise_tree_layer_by_layer(categories, X1_train, X1_test, [])
    start_time = time.perf_counter()
    # best_tree = mf.stepwise_tree_finder(categories, X_train, X_test, [])
    # best_tree = [((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4))]
    # best_tree = [[(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)], [(0, 1, 2), (3, 4)], [(5, 6, 7, 8), (9,)], [(0, 2), (1,)], [(3,), (4,)], [(5, 6), (7, 8)], [(0,), (2,)], [(5,), (6,)], [(7,), (8,)]]    
    # print(mf.stepwise_inclusion((0, 1, 2, 3), (4, 5, 6, 7, 8, 9), X_train, X_test))
    # print(mf.stepwise_inclusion([], (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), X_train, X_test))
    # return
    # mf.stepwise_single_layer(categories, X_train, X_test, model_type='LogisticRegression')
    # normalized_tree = sorted(best_tree, key=len, reverse=True)

    # Your provided list
    tuples_list = [((1,2,3),(4,5,6)), ((1,2),(3,)), ((1,),(2,)), ((4,5),(6,)), ((4,),(5,))]

    # Initialize a Digraph object for visualization
    dot = Digraph()

    def add_nodes_edges(tuples_list, parent=None, side=None):
        if tuples_list:
            # Create a unique node name based on its content and whether it's left or right (L/R) from its parent
            node_name = '_'.join(map(str, tuples_list[0])) + ('L' if side == 'left' else 'R' if side == 'right' else '')
            # Label for the node
            node_label = f'{tuples_list[0]} vs {tuples_list[1]}'
            # Add the node to the graph
            dot.node(node_name, label=node_label)
            
            if parent:
                # Link this node to its parent
                dot.edge(parent, node_name)
            
            # Recursive calls for each child node in the structure, if any
            for i, child in enumerate(tuples_list[2:], start=2):
                add_nodes_edges(child, parent=node_name, side='left' if i == 2 else 'right')

    # The initial call to start adding nodes and edges
    add_nodes_edges(tuples_list)

    # Display the decision tree
    dot.render(r'C:\Users\maxdi\OneDrive\Documents\uni_honours\decision_tree', format='png', cleanup=True)
    return
    built_mods = mf.build_single_models(normalized_tree, X_train)
    built_mods = list(built_mods.values())
    tree_model = mod.tree_model('tree_mod1', built_mods, normalized_tree)
    print(tree_model.tree_struct)
    output = tree_model.predict(X_test)
    accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
    print(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=['0','1','2','3','4','5','6','7','8','9']))
    print(accuracy)
    print(f'Took {time.perf_counter() - start_time}')

if __name__ == '__main__':
    config = Config()
    main(config)