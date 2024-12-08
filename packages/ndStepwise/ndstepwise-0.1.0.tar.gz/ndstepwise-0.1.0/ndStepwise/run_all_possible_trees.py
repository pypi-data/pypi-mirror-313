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


def main(filename, model_types):
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
    transform_label = mf.all_trees_map_categorical_target(config, df)
    # df['Y'] = df['Y'] + 1
    # transform_label = None
    X2_train, X2_test, y_train, y2_test = train_test_split(df, df['Y'], stratify=df['Y'], test_size=0.2, random_state=42)
    score_type = 'accuracy'
    categories = tuple(df['Y'].unique())
    trees_defined = mf.defined_all_trees(len(categories))
    best_accuracy = 0
    best_model = ()
    # X_train, X_test, y_train, y_test = train_test_split(X2_train, X2_train['Y'], stratify=X2_train['Y'], test_size=0.2, random_state=42)
    
    unique_elements = set()
    for sublist in trees_defined:
        lil_one = list()
        for i in sublist:
            lil_one.append(tuple(i))
        unique_elements.add(tuple(lil_one))

    # Convert set back to list if needed
    unique_list = list(unique_elements)
    model_types = model_types[0]
    X_train, X_test, y_train, y_test = train_test_split(X2_train, X2_train['Y'], test_size=0.2, random_state=43)
    for tree in unique_list:
        built_mods_dict = dict()
        for node in tree:
            # X_train, X_test = mf.split_data_set(categories, X2_train)
            single_mods = mf.build_single_models(config, [node], X_train, score_type=score_type, train_type=model_types)
            built_mods_dict.update(single_mods) 
            # mf.test_single_models(single_mods, X_test)

        built_mods = list(built_mods_dict.values())
        tree_model = mod.tree_model('tree_mod1', built_mods, tree)
        output = tree_model.predict(X_test)
        tree_model.model_score(y_test.tolist())
        accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = tree
            best_built_models=built_mods_dict
            config.log.info(f'current best accuracy is {accuracy}')

    if transform_label:
        output['y_pred'] = transform_label.inverse_transform(output['y_pred'])
        y_test = transform_label.inverse_transform(y_test)
        string_categories = transform_label.classes_
    else:
        string_categories = [str(i) for i in categories]

    config.log.info(f'Best model is {best_model}')
    # best_tree = mf.thread_stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
    # config.log.info('Finished stepwise tree finder.')
    # config.log.info(f"Took: {round(time.perf_counter()-start,3)} to do find best tree.")
    model_strucs = best_model
    tree_types = [model_types]*len(best_model)
    config.log.info(model_strucs)
    config.log.info(tree_types)
    best_trained_model = mf.build_best_tree(config, X2_test, X2_train, y2_test, score_type, tree_types, best_model, categories, built_mods=best_built_models, transform_label=transform_label)[0]
    mf.graph_model(config, best_trained_model, filename, transform_label=transform_label, model_types=[model_types])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--filename', required=True, type=str, help='The name of the file to process')
    parser.add_argument('-m', '--model_types', type=str, nargs='*', default=['randomForest', 'LogisticRegression', 'xgboost'], help='An optional list models to be tested out of randomForest, LogisticRegression, xgboost, svm.')
    args = parser.parse_args()  
    main(args.filename, args.model_types)