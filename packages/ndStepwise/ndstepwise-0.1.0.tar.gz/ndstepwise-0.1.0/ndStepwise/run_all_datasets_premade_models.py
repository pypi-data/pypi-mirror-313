import pandas as pd
import concurrent.futures
import numpy as np
import math
from sklearn.model_selection import train_test_split, cross_val_predict, cross_val_score, cross_validate, cross_val_score
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
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.multiclass import OneVsOneClassifier
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn import svm
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neural_network import MLPClassifier

def main():
    # config.log.info('Max Rocks')
    # config.log.error('This is an extra long message about how there was an error because Max wants to see if there is a weird format when messages get extra long.')
    # config.log.debug('THIS SHOULDNT LOG')
    # return
    start = time.perf_counter()

    files = [
        # 'letter_recognition.csv',
        # 'mfeat-factors.csv',
        # 'mfeat-fouriers.csv',
        # 'mfeat-karhunen.csv',
        # 'mfeat-morphological.csv',
        # 'mfeat-pixel.csv',
        # 'mfeat-zernlike.csv',
        # 'optdigits.csv',
        # 'pageblocks.csv',
        # 'handwritten_digits.csv',
        # 'satimage.csv',
        # 'image_segment.csv',
        # 'beans_data.csv',
        'car_evaluation.csv'
    ]

    # print(f'Accuracy: {accuracy:.10f}')
    # print(scores)
    # model_name = "LDA"
    model_name = "Neural_Network"
    # model_name = "knn"
    config = Config(model_name)
    config.log.info(f'Beginning of {model_name}.')
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for filename  in files:
        dataset = filename
        dataset_location = "data/" + dataset
        df = pd.read_csv(dataset_location)
        df.drop(df.columns[0], axis=1, inplace=True)
        transform_label = mf.map_categorical_target(config, df)
        df_x = df.drop('Y', axis=1)
        Y = df['Y']
        # model = LinearDiscriminantAnalysis()
        model = make_pipeline(StandardScaler(), MLPClassifier(max_iter = 200))
        # model = xgb.XGBClassifier(n_jobs = -1, objective="binary:logistic")
        # model = OneVsRestClassifier(model)

        # Set up GridSearchCV
        # param_grid = {'n_neighbors': range(1, 31)}
        # knn = KNeighborsClassifier()
        # model = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')

        scores = cross_val_score(model, df_x, Y, cv=cv, scoring='accuracy')
        accuracy = scores.mean()
        print(f"Dataset {dataset}, {model_name} - {accuracy}")
        config.log.info(f"Dataset {dataset}, {model_name} - {accuracy}")

        print(f"{scores}")
        config.log.info(f"scores {scores}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    main()