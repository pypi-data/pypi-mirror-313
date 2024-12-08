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

def main(config):
    df = pd.read_csv('100k_6_cat.csv')
    df.drop(df.columns[0], axis=1,inplace=True)
    X1_train, X1_test, y1_train, y1_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42) 
    tree_len = 6
    all_tree_struc = mf.defined_all_trees(tree_len)
    all_model_struc = mf.single_models_from_trees(all_tree_struc)

    layer_1 = [tree for tree in all_model_struc if sum(len(t) for t in tree) == 6]
    all_layer1_models = mf.build_single_models(layer_1, X1_train)
    scores = mf.test_single_models(all_layer1_models, X1_test)
    print(scores)
    # run all layer_1, then pick the best one, then find all trees under this layer 1
    #Now, pick the highest 
    highest_l1_model = all_layer1_models[max(scores, key=scores.get)]
    print(f"Highest layer1 model is {highest_l1_model.name} with score of {highest_l1_model.model_score()}")
    #Now, we consider these models: pick the left and right models and keep doing the same thing 
    layer_2 = [tree for tree in all_tree_struc if highest_l1_model.category_split in tree]
    # print(layer_2)
    #Now generate all for the left
    layer_2_left = highest_l1_model.type_0_categories
    layer_2_l = [model for model in all_model_struc if sorted(list(layer_2_left)) == sorted(list(set(model[0]+model[1])))]
    all_layer2_l_models = mf.build_single_models(layer_2_l, X1_train)

    scores_2_l = mf.test_single_models(all_layer2_l_models, X1_test)
    highest_2_l_model = all_layer2_l_models[max(scores_2_l, key=scores_2_l.get)]
    print(f"Highest layer1 left model is {highest_2_l_model.name} with score of {highest_2_l_model.model_score()}")

    #Now generate all for the right
    layer_2_right = highest_l1_model.type_1_categories
    layer_2_r = [model for model in all_model_struc if sorted(list(layer_2_right)) == sorted(list(set(model[0]+model[1])))]
    all_layer2_r_models = mf.build_single_models(layer_2_r, X1_train)

    scores_2_r = mf.test_single_models(all_layer2_r_models, X1_test)
    highest_2_r_model = all_layer2_r_models[max(scores_2_r, key=scores_2_r.get)]
    print(f"Highest layer1 right model is {highest_2_r_model.name} with score of {highest_2_r_model.model_score()}")

    # Layer 2 LL
    layer_2_left_left = highest_2_l_model.type_0_categories
    layer_2_l_l = [model for model in all_model_struc if sorted(list(layer_2_left_left)) == sorted(list(set(model[0]+model[1])))]
    all_layer2_l_l_models = mf.build_single_models(layer_2_l_l, X1_train)

    scores_2_l_l = mf.test_single_models(all_layer2_l_l_models, X1_test)
    highest_2_l_l_model = all_layer2_l_l_models[max(scores_2_l_l, key=scores_2_l_l.get)]
    print(f"Highest layer1 left left model is {highest_2_l_l_model.name} with score of {highest_2_l_l_model.model_score()}")

    # Layer 2 RL
    layer_2_right_left = highest_2_r_model.type_0_categories
    layer_2_r_l = [model for model in all_model_struc if sorted(list(layer_2_right_left)) == sorted(list(set(model[0]+model[1])))]
    all_layer2_r_l_models = mf.build_single_models(layer_2_r_l, X1_train)

    scores_2_r_l = mf.test_single_models(all_layer2_r_l_models, X1_test)
    highest_2_r_l_model = all_layer2_r_l_models[max(scores_2_r_l, key=scores_2_r_l.get)]
    print(f"Highest layer1 right model is {highest_2_r_l_model.name} with score of {highest_2_r_l_model.model_score()}")


if __name__ == '__main__':
    config = Config()
    main(config)