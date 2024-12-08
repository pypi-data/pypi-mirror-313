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


def main(config):
    df = pd.read_csv('new_100k_10_cat.csv') 
    # df = df.head(10000)
    categories = tuple((0,1,2,3,4,5,6,7,8,9))
    # df = pd.read_csv('100k_6_cat.csv')
    # categories = tuple((1,2,3,4,5,6))
    df.drop(df.columns[0], axis=1,inplace=True)
    # X, y = make_classification(n_samples=100000,  # Number of samples
    #                        n_features=20,   # Total number of features
    #                        n_informative=17, # Number of informative features
    #                        n_redundant=3,   # Number of redundant features
    #                        n_classes=10,     # Number of classes
    #                        n_clusters_per_class=2, # Number of clusters per class
    #                        random_state=42)
    # df = pd.DataFrame(X, columns=[f'Feature_{i}' for i in range(X.shape[1])])
    # df['Y'] = y
    # df = pd.read_csv('100k_6_cat.csv')   
    # categories = tuple((1,2,3,4,5,6))
    
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42) 

    # df_x = df.drop('Y', axis=1)
    # X_train, X_test, y_train, y_test = train_test_split(df_x, df['Y'], test_size=0.2, random_state=42) 
    # model = LogisticRegression(multi_class='multinomial', solver='sag', max_iter=1000)
    # model.fit(X_train, y_train)

    # # Make predictions on the test set
    # y_pred = model.predict(X_test)

    # # Evaluate the model
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f'Accuracy: {accuracy:.2f}')
    # print(classification_report(y_test, y_pred, target_names=['0','1','2','3','4','5','6','7','8','9']))
    # return

    # stepwise_models = mf.stepwise_tree_layer_by_layer(categories, X1_train, X1_test, [])
    start_time = time.perf_counter()
    score_type='accuracy'
    best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, [], score_type=score_type)
    # best_tree = [((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4))]
    #best_tree = [((3,), (0, 1, 2, 4, 6, 7, 9)), ((7,), (6,)), ((9,), (7, 6)), ((8,), (0, 1, 2, 3, 4, 5, 6, 7, 9)), ((4,), (0, 1, 2)), ((1,), (0, 2)), ((5,), (0, 1, 2, 3, 4, 6, 7, 9)), ((0,), (2,)), ((7, 6, 9), (0, 1, 2, 4))]
    # best_tree = [[(0, 1, 2, 3, 4), (5, 6, 7, 8, 9)], [(0, 1, 2), (3, 4)], [(5, 6, 7, 8), (9,)], [(0, 2), (1,)], [(3,), (4,)], [(5, 6), (7, 8)], [(0,), (2,)], [(5,), (6,)], [(7,), (8,)]]    
    # print(mf.stepwise_inclusion((0, 1, 2, 3), (4, 5, 6, 7, 8, 9), X_train, X_test))
    # print(mf.stepwise_inclusion([], (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), X_train, X_test))
    # return
    #mf.stepwise_single_layer(categories, X_train, X_test, model_type='LogisticRegression')
    def sort_with_type_check(t):
        return sorted(t, key=lambda x: (str(type(x)), x))

    # Apply the sorting strategy considering type
    normalized_tree = [(tuple(sort_with_type_check(a)), tuple(sort_with_type_check(b))) for a, b in best_tree]
    built_mods = mf.build_single_models(config, normalized_tree, X_train, score_type=score_type)
    built_mods = list(built_mods.values())
    config.log.info(f'Best models are {built_mods}')
    tree_model = mod.tree_model('tree_mod1', built_mods, normalized_tree)
    print(tree_model.tree_struct)
    output = tree_model.predict(X_test)
    tree_model.model_score(y_test.tolist())
    accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
    print(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=['0','1','2','3','4','5','6','7','8','9']))
    config.log.info(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=['0','1','2','3','4','5','6','7','8','9']))
    # print(f1_score(y_test.tolist(), output['y_pred'].to_list(), average='weighted'))
    print(accuracy)

    print(f'Took {time.perf_counter() - start_time}')

if __name__ == '__main__':
    config = Config()
    main(config)