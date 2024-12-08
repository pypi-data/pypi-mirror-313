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
from ucimlrepo import fetch_ucirepo 

config = Config("testing_datasets")
# ABALONE dataset
abalone = fetch_ucirepo(id=1) 
  
# data (as pandas dataframes) 
X = abalone.data.features 
y = abalone.data.targets 
abalone_data = abalone.data.original
abalone_data.rename({'Rings': 'Y'}, axis=1, inplace=True)
# print(abalone_data)
X_train, X_test, y_train, y_test = train_test_split(abalone_data, abalone_data['Y'], test_size=0.2, random_state=42)
score_type = 'accuracy'
# categories = tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))  
categories = tuple(abalone_data['Y'].unique())

# ANNEALING dataset 
# annealing = fetch_ucirepo(id=3) 
# print(annealing.data.original)
# for i in range(1,100):
#     try:
#         annealing = fetch_ucirepo(id=i) 
#         # print(f"id={i} is dataset {annealing.metadata.name}")
#         print(f"{annealing.metadata.name} = fetch_ucirepo(id={i})")
#     except Exception as e:
#         pass

# ECOLI dataset
ecoli = fetch_ucirepo(id=39)
filename = "ecoli_classifier"
# model_types = ['randomForest', 'LogisticRegression', 'xgboost']
model_types = ['LogisticRegression'] 
ecoli_data = ecoli.data.original
# ecoli_data = ecoli_data.head(1000)
print(ecoli_data)
# letter_recognition_data.rename({'lettr': 'Y'}, axis=1, inplace=True)
ecoli_data['Y'], unique_strings = pd.factorize(ecoli_data['class'])
# ecoli_data['Sequence_numerical'], unique_seq_strings = pd.factorize(ecoli_data['Sequence'])
ecoli_data.drop(['class', 'Sequence'], axis=1, inplace=True)
# ecoli_data['Y'] = ecoli_data['encoded_Y']
print(ecoli_data)
df = ecoli_data
# Mapping back from integers to strings using the unique_strings array
print(unique_strings)

X_train, X_test, y_train, y_test = train_test_split(df, ecoli_data['Y'], stratify=ecoli_data['Y'], test_size=0.2, random_state=43)
score_type = 'accuracy'
# categories = tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))  
categories = tuple(ecoli_data['Y'].unique())
print(categories)

best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
config.log.info('Finished stepwise tree finder.')
model_strucs = list(best_tree.keys())
tree_types = list(best_tree.values())
best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
mf.graph_model(config, best_trained_model, filename)

# # PEN DIGITS dataset 
pen_based_recognition_of_handwritten_digits = fetch_ucirepo(id=81) 
filename = "pen_based_classifier"
# model_types = ['randomForest', 'LogisticRegression', 'xgboost']
model_types = ['LogisticRegression'] 
ecoli_data = pen_based_recognition_of_handwritten_digits.data.original
print(ecoli_data)
# ecoli_data = ecoli_data.head(1000)
print(ecoli_data)
# letter_recognition_data.rename({'lettr': 'Y'}, axis=1, inplace=True)
ecoli_data['Y'], unique_strings = pd.factorize(ecoli_data['class'])
# ecoli_data['Sequence_numerical'], unique_seq_strings = pd.factorize(ecoli_data['Sequence'])
ecoli_data.drop(['class', 'Sequence'], axis=1, inplace=True)
# ecoli_data['Y'] = ecoli_data['encoded_Y']
print(ecoli_data)
df = ecoli_data

# Mapping back from integers to strings using the unique_strings array
print(unique_strings)

X_train, X_test, y_train, y_test = train_test_split(df, df['Y'], stratify=df['Y'], test_size=0.2, random_state=43)
score_type = 'accuracy'
# categories = tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))  
categories = tuple(ecoli_data['Y'].unique())
print(categories)

best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
config.log.info('Finished stepwise tree finder.')
model_strucs = list(best_tree.keys())
tree_types = list(best_tree.values())
best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
mf.graph_model(config, best_trained_model, filename)


# # LETTER dataset
# # Dataset of letters
# filename = "letters_classification"
# # model_types = ['randomForest', 'LogisticRegression', 'xgboost']
# model_types = ['LogisticRegression']
# letter_recognition = fetch_ucirepo(id=59) 
# letter_recognition_data = letter_recognition.data.original
# letter_recognition_data = letter_recognition_data.head(1000)
# # letter_recognition_data.rename({'lettr': 'Y'}, axis=1, inplace=True)
# letter_recognition_data['Y'], unique_strings = pd.factorize(letter_recognition_data['lettr'])
# letter_recognition_data.drop('lettr', axis=1, inplace=True)
# # letter_recognition_data['Y'] = letter_recognition_data['encoded_Y']
# print(letter_recognition_data)

# # Mapping back from integers to strings using the unique_strings array
# print(unique_strings)

# X_train, X_test, y_train, y_test = train_test_split(letter_recognition_data, letter_recognition_data['Y'], test_size=0.2, random_state=42)
# score_type = 'accuracy'
# # categories = tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))  
# categories = tuple(letter_recognition_data['Y'].unique())
# best_tree = mf.stepwise_tree_finder(config, categories, X_train, X_test, {}, model_types=model_types, score_type=score_type)
# config.log.info('Finished stepwise tree finder.')
# model_strucs = list(best_tree.keys())
# tree_types = list(best_tree.values())
# best_trained_model = mf.build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, model_strucs, categories)
# mf.graph_model(config, best_trained_model, filename)
# # letter_recognition_data['decoded'] = letter_recognition_data['Y'].map(lambda x: unique_strings[x])