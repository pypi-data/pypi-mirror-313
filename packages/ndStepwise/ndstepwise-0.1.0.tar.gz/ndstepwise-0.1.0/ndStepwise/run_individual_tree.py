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
from .includes.config import Config;
from .includes import model_functions as mf
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
import ast

def main(filename, model_types, tree_structure):
    # config.log.info('Max Rocks')
    # config.log.error('This is an extra long message about how there was an error because Max wants to see if there is a weird format when messages get extra long.')
    # config.log.debug('THIS SHOULDNT LOG')
    # return
    print(filename)
    if len(filename) <= 1:
        raise Exception(f"Improper filename of: {filename}")
    start = time.perf_counter()
   
    dataset = filename
    config = Config(dataset)
    config.log.info(f'Beginning of {dataset}.')
    dataset_location = "data/" + dataset
    df = pd.read_csv(dataset_location)
    df.drop(df.columns[0], axis=1, inplace=True)
    transform_label = mf.map_categorical_target(config, df)
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], stratify=df['Y'], test_size=0.2, random_state=42)
    score_type = 'accuracy' 
    categories = tuple(df['Y'].unique())
    model_strucs = list(tree_structure) 
    tree_types = list(model_types)

    config.log.info('Testing individual tree.')
    config.log.info(model_strucs)
    config.log.info(tree_types)

    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories, transform_label=transform_label)
    mf.graph_model(config, best_trained_model, filename, transform_label=transform_label, model_types=model_types)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename', required=True, type=str, help='The name of the file to process')
    parser.add_argument('-m', '--model_types', type=str, default=['randomForest', 'LogisticRegression', 'xgboost'], help='An optional list models to be tested out of randomForest, LogisticRegression, xgboost, svm.')
    parser.add_argument('-t', '--tree_structure', type=str, help='A list of the tree to be made.')
    args = parser.parse_args()  
    main(args.filename, ast.literal_eval(args.model_types), ast.literal_eval(args.tree_structure))

# [((3,), (2, 0, 1)), ((2, 0), (1,)), ((2,), (0,))]
# ['svm', 'svm', 'svm']