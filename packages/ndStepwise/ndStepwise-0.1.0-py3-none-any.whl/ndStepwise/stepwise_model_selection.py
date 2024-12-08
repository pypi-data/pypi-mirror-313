import pandas as pd
# import sklearn as sk
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
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

def main(config):
    df = pd.read_csv('100k_6_cat.csv')     
    categories = tuple((1,2,3,4,5,6))
    df.drop(df.columns[0], axis=1,inplace=True)
    X1_train, X1_test, y1_train, y1_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42) 
    stepwise_models = mf.stepwise_tree_layer_by_layer(categories, X1_train, X1_test, [])
    
    # With model now decided, we can score and solve for accuracy
    tree_names = [model.category_split for model in stepwise_models]
    normalized_tree = sorted(tree_names, key=len, reverse=True)
    tree_model = mod.tree_model('tree_mod1', stepwise_models, normalized_tree)
    print(tree_model.tree_struct)
    output = tree_model.predict(X1_test)
    accuracy = accuracy_score(y1_test.to_list(), output['y_pred'].to_list())
    print(accuracy)

if __name__ == '__main__':
    config = Config()
    main(config)