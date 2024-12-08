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
import includes.model_functions as mf
import time
from itertools import combinations

def main(config):
    # From stack exchange there are this many trees for a given n: (2n-3)!!
    tree_len = 6
    start = time.perf_counter()
    all_tree_struc = mf.defined_all_trees(tree_len)
    print(all_tree_struc)
    print(len(all_tree_struc))
    print(f"Took: {round(time.perf_counter()-start,3)} to do {tree_len} categories")


if __name__ == '__main__':
    config = Config()
    main(config)