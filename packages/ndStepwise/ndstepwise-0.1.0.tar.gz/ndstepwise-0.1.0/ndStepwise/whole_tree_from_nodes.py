import itertools
import numpy as np
import pandas as pd
import concurrent.futures
import numpy as np
import math
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_curve, ConfusionMatrixDisplay, auc, roc_auc_score, f1_score, confusion_matrix
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

def main():

    # #generate 4 cat data 
    # num_categories = 4
    # num_samples = 10000
    # num_features = 7

    # target_probabilities = [1/num_categories] * num_categories
    # targets = np.random.choice(np.arange(1, num_categories + 1), size=num_samples, p=target_probabilities)
    # features = np.zeros((num_samples, num_features))
    # noise_factor = 1.1

    # for i in range(num_categories):
    #     category_indices = np.where(targets == (i + 1))[0]
    #     mean = i * 1.5  # Change mean for each category
    #     features[category_indices] = np.random.randn(len(category_indices), num_features) + mean

    # noise = np.random.randn(num_samples, num_features) * noise_factor
    # features += noise

    # df = pd.DataFrame(features, columns=[f'Feature_{i+1}' for i in range(num_features)])
    # df['Y'] = targets
    # df.to_csv("4_cat_whole_tree_check.csv")

    dataset = "new_100k_6_cat.csv"
    config = Config(dataset)
    df = pd.read_csv(dataset)
    # df = df.head(100)
    df.drop(df.columns[0], axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], test_size=0.5, random_state=42)
    score_type = 'accuracy' 
    categories = tuple(df['Y'].unique())


    # test if my data is any good

    # Y = df['Y']
    # df_x = df.drop('Y', axis=1)
    # X_train, X_test, y_train, y_test = train_test_split(df_x, Y, test_size=0.2, random_state=42)
    # model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    # model.fit(X_train, y_train)

    # # Make predictions on the test set
    # y_pred = model.predict(X_test)

    # # Evaluate the model
    # accuracy = accuracy_score(y_test, y_pred)
    # print(f'Accuracy: {accuracy:.2f}')
    # print(classification_report(y_test, y_pred, target_names=['1','2','3','4']))

    comparisons = [
        ((1, 2, 3), (4,)),
        ((1, 2), (3,)),
        ((1,), (2,))
    ]

    comparisons = [   
        ((1, 2, 3, 4), (5, 6)),
        ((1, 2, 3), (4,)),
        ((1,2), (3,)),
        ((1,), (2,)),
        ((5,), (6,)),
    ]  
    # comparisons = [   
    #     ((1, 2), (3, 4)),
    #     ((3,), (4,)),
    #     ((1,), (2,))
    # ]  

    # Total count (sum of all categories) * confusion_matrix 
    # Count of each * dictionary of probability
    inital_count = X_test['Y'].value_counts().to_dict()
    total_count = sum(inital_count.values())
    correctly_categorized = inital_count

    for model in comparisons:
        separate_models = mf.build_single_models(config, [model], X_train, train_type='LogisticRegression')
        prop_model_scores = mf.test_single_models(separate_models, X_test)
        node_model = separate_models[model]
        incorrect_class = node_model.incorrect_classified_dict
        print(node_model.confusion_matrix*total_count)
        print(f"incorrect_class dict from node {node_model.name} is {incorrect_class}")
        # Multiplying the matching values
        result = {key: inital_count[key] * incorrect_class[key] for key in inital_count.keys() & incorrect_class.keys()}
        print(f"Number of incorrect {result}")
        result = {key: inital_count[key] - result[key] for key in inital_count.keys() & result.keys()}
        print(f"Number of each left for the next {result}")
        correctly_categorized.update(result)

        inital_count = result
    print(correctly_categorized)
    print(f"estimated accuracy={sum(correctly_categorized.values())/total_count}")
    separate_models = mf.build_single_models(config, comparisons, X_train, train_type='LogisticRegression')
    mf.test_single_models(separate_models, X_test)
    built_mods = list(separate_models.values())
    config.log.info(f'Best models are {built_mods}')
    tree_model = mod.tree_model('tree_mod1', built_mods, comparisons)
    output = tree_model.predict(X_test)

    tree_model.model_score(y_test.tolist())
    accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
    print(f"Accuracy is {accuracy}")
    print(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=[str(i) for i in categories]))
    disp = ConfusionMatrixDisplay.from_predictions(y_test.tolist(), output['y_pred'].to_list())
    disp.plot()
    plt.show()
    return
    string_categories = [str(i) for i in categories]
    config.log.info(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=string_categories))

    print(prop_model_scores)
    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, 'LogisticRegression', comparisons, categories, built_mods=separate_models)
    # mf.graph_model(config, best_trained_model, filename)
    return
    
    for i in range(number_of_trees):
        random_mod_structure = generate(len(categories), categories, seed=i)
        print(random_mod_structure)
        all_full_trees.append(random_mod_structure)
        new_binary_comparisons = tuple(item for item in random_mod_structure if item not in all_binary_comparisons.keys())
        all_binary_comparisons.update(prop_model_scores)

    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, ['LogisticRegression']*5, result, categories)
    mf.graph_model(config, best_trained_model, filename)

    tree_model = mod.tree_model('tree_mod1', built_mods, best_tree)
    output = tree_model.predict(X_test)
    tree_model.model_score(y_test.tolist())
    accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
    config.log.info(f'Accuracy is {accuracy}')
    string_categories = [str(i) for i in categories]
    config.log.info(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=string_categories))
    print(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=string_categories))


    best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, ['LogisticRegression']*5, result, categories)
    mf.graph_model(config, best_trained_model, filename)

if __name__ == "__main__":
    main()