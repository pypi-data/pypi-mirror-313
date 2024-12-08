import pandas as pd
# import sklearn as sk
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


def main(config):
    # config.log.info('Max Rocks')
    # config.log.error('This is an extra long message about how there was an error because Max wants to see if there is a weird format when messages get extra long.')
    # config.log.debug('THIS SHOULDNT LOG')
    # return
    config.log.info('Beginning of the function.')
    df = pd.read_csv('new_100k_10_cat.csv')
    df.drop(df.columns[0], axis=1,inplace=True)  
    # df = df.head(1000)  
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42) 
    score_type = 'accuracy'
    categories = tuple((0,1,2,3,4,5,6,7,8,9))
    model_types = ['randomForest', 'LogisticRegression', 'xgboost']
    config.log.info('Beginning of stepwise tree finder.')
    best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
    config.log.info('Finished stepwise tree finder.')
    model_strucs = list(best_tree.keys())
    tree_types = list(best_tree.values())
    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
    mf.graph_model(best_trained_model)
    return

    best_cutoff_tree = [((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))]
    best_overall_tree = [[(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)], [(0, 1, 2), (3, 4)], [(5, 6, 7, 8), (9,)], [(0, 2), (1,)], [(3,), (4,)], [(5, 6), (7, 8)], [(0,), (2,)], [(5,), (6,)], [(7,), (8,)]]    
    bad_tree = [((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4))]
    cut_off_again = [((3,), (4,)), ((6,), (7, 8)), ((7,), (8,)), ((5,), (6, 7, 8)), ((1,), (0, 2)), ((0,), (2,)), ((9, 6, 7, 8, 5), (0, 1, 2, 3, 4)), ((9,), (6, 7, 8, 5)), ((3, 4), (0, 1, 2))]

    def sort_with_type_check(t):
        return sorted(t, key=lambda x: (str(type(x)), x))

    # Apply the sorting strategy considering type
    my_tree = best_overall_tree
    sorted_tree = [(tuple(sort_with_type_check(a)), tuple(sort_with_type_check(b))) for a, b in my_tree]
    concatenated_tree = [sorted(a + b) for a, b in sorted_tree]
    built_mods = mf.build_single_models(config, sorted_tree, X_train, score_type='accuracy')
    mf.test_single_models(built_mods, X_test)

    built_mods = list(built_mods.values())
    tree_model = mod.tree_model('tree_mod1', built_mods, concatenated_tree)
    output = tree_model.predict(X_test)
    tree_model.model_score(y_test.tolist())
    mf.graph_model(tree_model)
    return
    max_width_px, max_height_px = 1920, 1080  # Adjust as needed
    dpi = 300  # High DPI for good quality

    # Calculate figure size in inches
    fig_width_inch = max_width_px / dpi
    fig_height_inch = max_height_px / dpi

    # Create figure with calculated size
    plt.figure(figsize=(fig_width_inch, fig_height_inch))
    G = nx.DiGraph()
    edges = []
    for i in tree_model.models:
        G.add_node(i.name, info=f"{i.model_type} \n {i.score_type} is {i.score}")
        type_0 = i.type_0_categories
        if len(type_0) > 1:
            type_0_obj = [obj for obj in tree_model.models if sorted(obj.all_cat_tested) == sorted(type_0)][0]
            edges += [(str(i.name),str(type_0_obj.name))]
        else:
            edges += [(str(i.name),str(type_0))]
        
        type_1 = i.type_1_categories
        if len(type_1) > 1:
            type_1_obj = [obj for obj in tree_model.models if sorted(obj.all_cat_tested) == sorted(type_1)][0]
            edges += [(str(i.name),str(type_1_obj.name))]
        else:
            edges += [(str(i.name),str(type_1))]

    print(edges)
    G.add_edges_from(edges)

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    pos = graphviz_layout(G, prog="dot")
    plt.figure(figsize=(fig_width_inch, fig_height_inch))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=400, edge_color='k', linewidths=1, font_size=7, arrows=True)
    # Custom step: Add node names above and additional information below the nodes
    for node, (x, y) in pos.items():
        plt.text(x, y-25, G.nodes[node].get("info", ""), ha='center', fontsize=3, bbox=dict(facecolor='white', alpha=0.8))

    plt.figtext(0.85, 0.95, f"The {tree_model.score_type} of this tree is {tree_model.score}", ha="center", fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', edgecolor='black'))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Saving the plot to the specified directory
    plt.savefig(f'models/plot_{timestamp}.png', dpi=600, bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    config = Config()
    main(config)