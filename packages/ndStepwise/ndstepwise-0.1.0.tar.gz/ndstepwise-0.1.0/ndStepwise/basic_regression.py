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
from includes.config import Config

def main(config):
    # df = pd.read_csv('model_data1.csv')
    df = pd.read_csv('tiny_one.csv')
    df.drop(df.columns[0], axis=1,inplace=True)
    X1_train, X1_test, y1_train, y1_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42)
    # loaded_model = load(config.model_path + '\\model.joblib')
    # # output = loaded_model.predict(X1_test)
    # print(classification_report(y1_test.to_list(), output['y_pred'].to_list(), target_names=['1','2','3','4']))

    # df = pd.read_csv('model_data1.csv')
    # df = pd.read_csv('tiny_one.csv')
    df.drop(df.columns[0], axis=1,inplace=True)
    X1_train, X1_test, y1_train, y1_test = train_test_split(df, df['Y'], test_size=0.2, random_state=42)

    #build little models
    my_mod1 = mod.single_model([(1,2,3), (4,)])
    my_mod1.train(X1_train)
    print(my_mod1.fitted_model)

    my_mod2 = mod.single_model([(1,3), (2,)])
    my_mod2.train(X1_train)   
    # my_mod2.test(X1_test)

    my_mod3 = mod.single_model([(1,), (3,)])
    my_mod3.train(X1_train)
    

    #build tree_model
    tree_model = mod.tree_model('tree_mod1', [my_mod1, my_mod2, my_mod3], [[(1,2,3), (4,)], [(1,3), (2,)], [(1,), (3,)]])
    output = tree_model.predict(X1_test)
    print(classification_report(y1_test.to_list(), output['y_pred'].to_list(), target_names=['1','2','3','4']))
    dump(tree_model, config.model_path + '\\model.joblib')


if __name__ == '__main__':
    config = Config()
    main(config)