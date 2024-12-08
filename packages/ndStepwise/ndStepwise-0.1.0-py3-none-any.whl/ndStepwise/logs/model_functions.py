from joblib import dump, load
import pandas as pd
import includes.model as mod
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve, f1_score, precision_recall_curve, classification_report
from sklearn.model_selection import cross_val_predict
from sklearn import metrics
import random 
import numpy as np
import matplotlib.pyplot as plt
import scikitplot as skplt
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
from datetime import datetime 
import os

def read_arff(file_path, columns = None):
    with open(file_path, 'r') as file:
        data = file.readlines()

    # Find the lines between the '@data' tag and the end of the file
    start_index = 0
    for index, line in enumerate(data):
        if '@data' in line.lower():
            start_index = index + 1
            break

    # Now extract the data, removing any empty lines
    data = data[start_index:]
    data = [line.strip() for line in data if line.strip()]

    # Convert list of strings to a large string to imitate a CSV file reading
    from io import StringIO
    data_str = '\n'.join(data)
    data_io = StringIO(data_str)  # Use StringIO to convert string to file-like object

    # Assuming that the data part is comma-separated
    df = pd.read_csv(data_io, names=columns)
    return df

def save_model(path, model):
    """
    Saves a model to joblib file
    input:
        path: string to where file should be saved
        model: model to be saved
    output:
        returns none
    """
    dump(model, path)

def read_model(path: str):
    """
    Saves a model to joblib file
    input:
        path: string to where file should be saved
    output:
        returns none
    """
    return load(path)

def build_single_models(config, models_list: list, train_data, score_type='accuracy', train_type='LogisticRegression') -> list:
    """
    Builds all single models
    input:
        config: config object
        models_list: list of 2 elements lists with models to be produced e.g [[(1,2,3),(4,)],[(1,3), (2,)]]
        train_data: data that will be used to train all models 
        score_type: The metric we are looking to maximise
    output:
        returns list of models
    """
    trained_model_lists = dict()

    if isinstance(train_type, list):
        for i in range(len(models_list)):
            new_mod = mod.single_model(models_list[i], score_type=score_type)
            new_mod.train(train_data, model_type = train_type[i])
            trained_model_lists[tuple(models_list[i])] = new_mod
            config.log.debug(f'Finished training model {models_list[i]}')
    else:
        for i in range(len(models_list)):
            new_mod = mod.single_model(models_list[i], score_type=score_type)
            new_mod.train(train_data, model_type = train_type)
            trained_model_lists[tuple(models_list[i])] = new_mod
            config.log.debug(f'Finished training model {models_list[i]}')
    return trained_model_lists

def test_single_models(models: list, x_test_data):
    """
    Check all single models
    """
    tested_models = dict()
    for key in models:
        model = models[key]
        model.predict_individual(x_test_data)
        tested_models[key] = model.model_score()
    return tested_models

def find_best_mod_given_categories(categories, all_model_struc, X1_train, X1_test):
    """
    Finds the split of a model that has the highest accuracy/f1/metric
    input:
        categories: a tuple of the lists 
        all_model_struc: a list of all models
        X1_train: the x train data
        X1_test: the x test data
        total_tree: a list of the biggest models
    output:
        The top model
    """  
    layered_models = [model for model in all_model_struc if sorted(list(categories)) == sorted(list(set(model[0]+model[1])))]
    all_layer_models = build_single_models(config, layered_models, X1_train)

    scores_2_r = test_single_models(all_layer_models, X1_test)
    highest_model = all_layer_models[max(scores_2_r, key=scores_2_r.get)] 
    return highest_model

def build_tree_layer_by_layer(categories, all_model_struc, X1_train, X1_test, total_tree):
    """
    Build this tree in a recursive way
    input:
        categories: a tuple of the lists 
        all_model_struc: a list of all models
        X1_train: the x train data
        X1_test: the x test data
        total_tree: a list pf the biggest models
    output:
        list of binary comparisons
    """
    if len(categories) < 2:
        return total_tree
    
    highest_model = find_best_mod_given_categories(categories, all_model_struc, X1_train, X1_test)
    total_tree.append(highest_model)

    total1 = build_tree_layer_by_layer(highest_model.type_0_categories, all_model_struc, X1_train, X1_test, total_tree)
    total2 = build_tree_layer_by_layer(highest_model.type_1_categories, all_model_struc, X1_train, X1_test, total1+total_tree)

    return list(set(total_tree + total2))

def get_iterations_num(cat_num:int):
    """
    Get the number of iterations needed for a given number of categories 
    input:
        cat_num: int of number of categories
    output:
        returns int of how many iterations needed for stepwise
    """
    list_of_counts = [0, 0, 10, 40, 50, 90, 100, 300, 500, 700, 1000, 1000, 1000, 1000, 1000, 1000]
    return list_of_counts[cat_num]

def single_step_wise(categories, X1_train, X1_test, model_type='LogisticRegression'):
    model_score = 0
    return_model_first = None
    model_list = dict()
    accepted_count = 0
    iterations = get_iterations_num(len(categories))
    model_type = 'svm'
    model_type = 'LogisticRegression'

    for i in categories:
        first_category = i
        left_category = tuple(x for x in categories if int(x) != first_category)
        right_category = tuple(x for x in categories if int(x) == first_category)
        first_model_struc = [[left_category, right_category]]

        first_model = build_single_models(first_model_struc, X1_train, train_type=model_type)
        prop_model_score = list(test_single_models(first_model, X1_test).values())[0]
        return_model = first_model
        if prop_model_score > model_score:
            return_model_first = return_model
            model_score = prop_model_score
            model_list[prop_model_score] = list(first_model.values())[0]
    

    for i in range(0,iterations):
        select_category_int = random.choice(tuple((0,1)))
        random_noise = np.random.normal(loc=0, scale=0.06)
        #TODO cleanup this if mess

        if (select_category_int == 0 and len(left_category) >= 2) or (len(right_category) == 1):
            # Select the left category
            selected_cat = left_category
            next_category = random.choice(selected_cat)
            prop_left_category = tuple(x for x in categories if x in left_category and int(x) != next_category)
            prop_right_category = tuple(x for x in categories if x in right_category or int(x) == next_category)
        elif (select_category_int == 1 and len(right_category) >= 2) or (len(left_category) == 1):
            # Select the right category
            selected_cat = right_category
            next_category = random.choice(selected_cat)
            prop_right_category = tuple(x for x in categories if x in right_category and int(x) != next_category)
            prop_left_category = tuple(x for x in categories if x in left_category or int(x) == next_category)

        # print(f'Prop left things {prop_left_category}')
        # print(f'Prop right things {prop_right_category}')
        prop_next_model_struc = [[prop_left_category, prop_right_category]]
        # print(prop_next_model_struc)
        prop_model = build_single_models(prop_next_model_struc, X1_train, train_type=model_type)
        prop_model_score = list(test_single_models(prop_model, X1_test).values())[0]

        if model_score < prop_model_score + random_noise:
            model_score = prop_model_score
            return_model = prop_model
            left_category = prop_left_category
            right_category = prop_right_category
            accepted_count += 1
            model_list[prop_model_score] = list(prop_model.values())[0]
    values = [x for x in model_list]
    return(model_list.get(max(values)))

def stepwise_tree_layer_by_layer(categories, X1_train, X1_test, total_tree):
    """
    Build this tree in a stepwise recursive way
    input:
        categories: a tuple of the lists 
        all_model_struc: a list of all models
        X1_train: the x train data
        X1_test: the x test data
        total_tree: a list pf the biggest models
    output:
        list of binary comparisons
    """
    if len(categories) <= 2:
        if len(categories) == 2:
            two_cat_mod = list(build_single_models([[(categories[0],), (categories[1],)]], X1_train).values())[0]
            return list(set(total_tree + [two_cat_mod]))
        else:
            return total_tree
    
    highest_model = single_step_wise(categories, X1_train, X1_test)
    total_tree.append(highest_model)

    total1 = stepwise_tree_layer_by_layer(highest_model.type_0_categories, X1_train, X1_test, total_tree)
    total2 = stepwise_tree_layer_by_layer(highest_model.type_1_categories, X1_train, X1_test, total1+total_tree)

    return list(set(total_tree + total2))

def stepwise_inclusion(config, left_list, right_list, X_train, X_test, train_type='LogisticRegression', score_type='accuracy'): 
    # Returns best_model and best_score as tuple (best_model, best_score)
    model_list = []
    for i in right_list:
        all_but_one = tuple(x for x in right_list if x != i)
        model_def = [tuple(tuple(left_list) + (i,)), all_but_one]
        model_list.append(model_def)
    model = build_single_models(config, model_list, X_train, score_type=score_type, train_type=train_type)
    tested_mods = test_single_models(model,X_test)
    sorted_d_desc = sorted(tested_mods.items(), key=lambda item: item[1], reverse=True)
    best_mod = sorted_d_desc[0][0]
    best_score = sorted_d_desc[0][1]
    return best_mod, best_score
    
def stepwise_exclusion(config, left_list, right_list, X_train, X_test, train_type='LogisticRegression', score_type='accuracy'):
    # Returns best_model and best_score as tuple (best_model, best_score)
    model_list = []
    for i in left_list:
        all_but_one = tuple(x for x in left_list if x != i)
        model_def = [tuple(tuple(right_list) + (i,)), all_but_one]
        model_list.append(model_def)
    
    model = build_single_models(config, model_list, X_train, score_type=score_type, train_type=train_type)
    tested_mods = test_single_models(model, X_test)
    sorted_d_desc = sorted(tested_mods.items(), key=lambda item: item[1], reverse=True)
    best_mod_ordered = (sorted_d_desc[0][0][1], sorted_d_desc[0][0][0])
    best_score = sorted_d_desc[0][1]
    return best_mod_ordered, best_score
    
def stepwise_single_layer(categories, X_train, X_test, model_type='LogisticRegression'):
    best_mod, best_score = stepwise_inclusion([], categories, X_train, X_test)
    while True:
        new_mod, new_score = stepwise_inclusion(best_mod[0], best_mod[1], X_train, X_test, model_type)
        if new_score > best_score:
            best_mod = new_mod
            best_score = new_score
        else:
            if len(new_mod[1]) > 1:
                second_inclusion_mod, second_inclusion_score = stepwise_inclusion(new_mod[0], new_mod[1], X_train, X_test, model_type)
                if second_inclusion_score > best_score:
                    best_mod = second_inclusion_mod
                    best_score = second_inclusion_score
                else:
                    if len(second_inclusion_mod[1]) > 1:
                        third_inclusion_mod, third_inclusion_score = stepwise_inclusion(second_inclusion_mod[0], second_inclusion_mod[1], X_train, X_test, model_type)
                        if third_inclusion_score > best_score:
                            best_mod = third_inclusion_mod
                            best_score = third_inclusion_score
                        else:
                            break
                    else:
                        break
            else:
                break
        new_backward_mod, new_backward_score = stepwise_exclusion(best_mod[0], best_mod[1], X_train, X_test, model_type)
        if new_backward_score > best_score:
            best_mod = new_backward_mod
            best_score = new_backward_score      
        else:
            continue
    return best_mod

def stepwise_layer_finder(config, categories, X_train, X_test, model_type='LogisticRegression', score_type='accuracy'):
    best_mod, best_score = new_mod, new_score = stepwise_inclusion(config, [], categories, X_train, X_test, train_type=model_type)
    failed_model_counter = 0
    run_inclusion = True
 
    while True:
        if failed_model_counter > 3:
            break
        elif failed_model_counter == 0:
            best_mod = run_mod = new_mod
            best_score = run_score = new_score
        else:
            run_mod = new_mod
            run_score = new_score       

        if run_inclusion:
            new_mod, new_score = stepwise_inclusion(config, run_mod[0], run_mod[1], X_train, X_test, model_type, score_type)
            if new_score > best_score:
                best_mod = new_mod
                best_score = new_score
                run_inclusion = False
                failed_model_counter = 0
            else:
                if len(new_mod[1]) == 1:
                    run_inclusion = False
                else:
                    run_inclusion = True
                failed_model_counter += 1
        else:
            new_mod, new_score = stepwise_exclusion(config, run_mod[0], run_mod[1], X_train, X_test, model_type, score_type)
            if new_score > best_score:
                best_mod = new_mod
                best_score = new_score      
                run_inclusion = True
                failed_model_counter = 0
                if len(new_mod[0]) > 1:
                    run_inclusion = False
            else:
                run_inclusion = True
                failed_model_counter += 1
    return best_mod, best_score

def stepwise_tree_finder(config, categories, X1_train, X1_test, total_tree, model_types=['LogisticRegression'], score_type='accuracy'):
    """
    Build this tree in a stepwise recursive way
    input:
        config: config object
        categories: a tuple of the lists 
        all_model_struc: a list of all models
        X1_train: the x train data
        X1_test: the x test data
        total_tree: a list pf the biggest models
    output:
        list of binary comparisons
    """
    X_train, X_test = split_data_set(categories, X1_train)
    if len(categories) <= 2:
        if len(categories) == 2:
            two_cat_mod = ((categories[0],), (categories[1],))
            top_score = 0
            top_model = 0
            for mod_type in model_types:
                new_mod = build_single_models(config, [two_cat_mod], X_train, score_type=score_type, train_type=mod_type)
                tested_mods = test_single_models(new_mod, X_test)
                sorted_d_desc = sorted(tested_mods.items(), key=lambda item: item[1], reverse=True)
                score = sorted_d_desc[0][1]
                if score > top_score:
                    top_score = score
                    top_model_type = mod_type
            total_tree[two_cat_mod] = top_model_type
            config.log.info(f'Stepwise layer found best split: {two_cat_mod} with mod type {top_model_type}')

            return total_tree
        else:
            return total_tree
    
    top_score = 0
    top_model = None
    top_model_type = None
    for mod_type in model_types:
        config.log.info(f'Finding stepwise layer for {mod_type} with categories: {categories}')
        highest_model, best_score = stepwise_layer_finder(config, categories, X_train, X_test, mod_type, score_type)
        config.log.info(f'Stepwise layer for {mod_type}: {highest_model} is {best_score}')
        if best_score > top_score:
            top_score = best_score
            top_model = highest_model
            top_model_type = mod_type
            
    config.log.info(f'Stepwise layer found best split: {top_model} with mod type {top_model_type}')
    total_tree[top_model] = top_model_type
    total1 = stepwise_tree_finder(config, tuple(top_model[0]), X1_train, X1_test, total_tree, model_types=model_types, score_type=score_type)
    total2 = stepwise_tree_finder(config, tuple(top_model[1]), X1_train, X1_test, total1, model_types=model_types, score_type=score_type)
    
    return total2

def stepwise_tree(categories, X1_train, X1_test, total_tree):
    """
    Build this tree in a stepwise recursive way
    input:
        categories: a tuple of the lists 
        all_model_struc: a list of all models
        X1_train: the x train data
        X1_test: the x test data
        total_tree: a list pf the biggest models
    output:
        list of binary comparisons
    """
    if len(categories) <= 2:
        if len(categories) == 2:
            two_cat_mod = ((categories[0],), (categories[1],))
            return list(set(total_tree + [two_cat_mod]))
        else:
            return total_tree
    X_train, X_test = split_data_set(categories, X1_train)
    highest_model = stepwise_single_layer(categories, X_train, X_test)
    total_tree.append(highest_model)

    total1 = stepwise_tree(tuple(highest_model[0]), X1_train, X1_test, total_tree)
    total2 = stepwise_tree(tuple(highest_model[1]), X1_train, X1_test, total1+total_tree)

    return list(set(total_tree + total2))

def split_data_set(categories, data):
    cut_data_set = data.loc[data['Y'].isin(categories)]
    X_train, X_test, y_train, y_test = train_test_split(cut_data_set, cut_data_set['Y'], test_size=0.2, random_state=42)
    return (X_train, X_test)

def to_labels(probs: np.ndarray, threshold: float) -> np.ndarray:
    """Convert probabilities to binary labels based on the given threshold."""
    return (probs >= threshold).astype(int)
    
def find_cutoff(model, data_df, Y, type='ROC'):
    """
    Find the cutoff point for a given model
    input:
        model: Model to find cutoff for. Only models that work with predict_proba will work
        data_df: Dataframe with data
        Y: target column 
        type: which cutoff to look for: default to ROC
    output:
        list of binary comparisons
    """
    predict_probabilities = cross_val_predict(model, data_df, Y, method='predict_proba')[:, 1]

    if type == 'ROC' or type == 'accuracy':
        # Find Cutoff using Youden's J statistic
        fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
        optimal_idx = np.argmax(tpr - fpr)
        cutoff = thresholds[optimal_idx]
    
    elif type == 'precision-recall':
        #Used https://machinelearningmastery.com/threshold-moving-for-imbalanced-classification/?fbclid=IwAR1PQcjZVTuAIQrWsYiaB32h2iao5zBl8UP8oIQgPcD76QPOQjBO8ggoqj0
        precision, recall, thresholds = precision_recall_curve(Y, predict_probabilities)
        fscore = (2 * precision * recall) / (precision + recall)
        ix = np.argmax(fscore)
        cutoff = thresholds[ix]
    
    elif type == 'f1':
        #Used https://machinelearningmastery.com/threshold-moving-for-imbalanced-classification/?fbclid=IwAR1PQcjZVTuAIQrWsYiaB32h2iao5zBl8UP8oIQgPcD76QPOQjBO8ggoqj0
        thresholds = np.arange(0, 1, 0.01)
        scores = [(Y, to_labels(predict_probabilities, t)) for t in thresholds]
        # y_pred = predict_probabilities[:, None] >= thresholds
        # scores = [f1_score(Y, y_pred[:, i].astype(int)) for i in range(y_pred.shape[1])]
        cutoff = thresholds[np.argmax(scores)]
    
    elif type == 'accuracy':
        #Used https://machinelearningmastery.com/threshold-moving-for-imbalanced-classification/?fbclid=IwAR1PQcjZVTuAIQrWsYiaB32h2iao5zBl8UP8oIQgPcD76QPOQjBO8ggoqj0
        thresholds = np.arange(0, 1, 0.001)
        scores = [accuracy_score(Y, to_labels(predict_probabilities, t)) for t in thresholds]
        cutoff = thresholds[np.argmax(scores)]
    return cutoff

def graph_model(config, tree_model):
    """
    Draws the dot graph for a given model
    input:
        tree_model: A fully trained tree model
    output:
        saves the image of a model to the /models folder
    """
    config.log.info(f'Plotting tree: {tree_model}')
    max_width_px, max_height_px = 1920, 1080  # Adjust as needed
    dpi = 300  # High DPI for good quality

    # Calculate figure size in inches
    fig_width_inch = max_width_px / dpi
    fig_height_inch = max_height_px / dpi

    # Create figure with calculated size
    plt.figure(figsize=(fig_width_inch, fig_height_inch))
    G = nx.DiGraph()
    edges = []
    for i in tree_model.models:
        G.add_node(i.name, info=f"{i.model_type} \n {i.score_type} is {i.score}")
        type_0 = i.type_0_categories
        if len(type_0) > 1:
            type_0_obj = [obj for obj in tree_model.models if sorted(obj.all_cat_tested) == sorted(type_0)][0]
            edges += [(str(i.name),str(type_0_obj.name))]
        else:
            edges += [(str(i.name),str(type_0))]
        
        type_1 = i.type_1_categories
        if len(type_1) > 1:
            type_1_obj = [obj for obj in tree_model.models if sorted(obj.all_cat_tested) == sorted(type_1)][0]
            edges += [(str(i.name),str(type_1_obj.name))]
        else:
            edges += [(str(i.name),str(type_1))]
    G.add_edges_from(edges)

    # Draw the graph
    pos = nx.spring_layout(G)  # positions for all nodes
    pos = graphviz_layout(G, prog="dot")
    plt.figure(figsize=(fig_width_inch, fig_height_inch))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=400, edge_color='k', linewidths=1, font_size=7, arrows=True)
    # Custom step: Add node names above and additional information below the nodes
    for node, (x, y) in pos.items():
        plt.text(x, y-25, G.nodes[node].get("info", ""), ha='center', fontsize=3, bbox=dict(facecolor='white', alpha=0.8))

    plt.figtext(0.85, 0.95, f"The {tree_model.score_type} of this tree is {tree_model.score}", ha="center", fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', edgecolor='black'))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Saving the plot to the specified directory
    plt.savefig(f'models/plot_{timestamp}.png', dpi=600, bbox_inches='tight')
    config.log.info(f'Model diagram saved here: models/plot_{timestamp}.png')

def defined_all_models(n: int):
    """
    TODO remove this method and use something more rigourous. This function creates a list of all single models to be produced
    input:
        n: number of categories/classes
    output:
        list of binary comparisons
    """
    all_comparisons = list()
    # set(), sort, sort all strings 
    if n == 4:
        all_comparisons = [['1','2'], ['1','3'], ['1','4'], ['2','3'], ['3','4'], ['12','3'], ['12','4'], ['13','4'], 
                           ['13', '2'], ['23','4'], ['24','3'], ['123','4'], ['124','3'], ['134','2'], ['234','1']]
    return all_comparisons

def defined_all_trees(n: int):
    """
    TODO remove this method and use something more rigourous. This function creates a list of all trees or combined models for a given 
    number of categories. 
    input:
        n: number of categories/classes
    output:
        list of all trees
    """
    categories = tuple(range(1, n+1))
    all_trees_normalized = generate_normalized_branches(categories)

    # Convert frozensets back to lists for readability
    all_trees_normalized_list = [sorted(list(map(list, tree))) for tree in all_trees_normalized]
    all_trees_normalized_list = [[sorted(branch, key=len, reverse=True) for branch in tree] for tree in all_trees_normalized_list]
    return all_trees_normalized_list

def stringify(node):
    """ Convert a tuple of numbers into a concatenated string. """
    return node

def generate_normalized_branches(categories):
    """
    Recursively generate all branches for the given categories with normalized order.
    This function ensures that each branch is represented in a standardized way to eliminate duplicates.
    """
    if len(categories) <= 1:
        return [set()]  # No branches can be formed from a single category

    branches_set = set()
    for left in generate_subsets(categories):
        right = tuple(set(categories) - set(left))

        # Generate branches for left and right subsets
        left_branches = generate_normalized_branches(left)
        right_branches = generate_normalized_branches(right)

        for l_branch_set in left_branches:
            for r_branch_set in right_branches:
                # Combine current split with left and right branches
                new_branch = tuple(sorted([left, right]))
                combined_branches = {new_branch}.union(l_branch_set, r_branch_set)
                branches_set.add(frozenset(combined_branches))  # Using frozenset to allow set of sets
    return branches_set

def generate_subsets(s):
    """ Generate all non-empty subsets of a set s. """
    subsets = []
    for r in range(1, len(s)):
        subsets.extend(combinations(s, r))
    return subsets

def single_models_from_trees(trees_total):
    """Get list of all models to be generated from the trees"""
    total_models = [sorted(branch, key=lambda x: len(x), reverse=True)  for tree in trees_total for branch in tree]
    return_model = [list(t) for t in set(tuple(e) for e in total_models)]
    return return_model

def plot_roc_curve(y_true, y_probs):
    
    #used code from stack overflow: https://stackoverflow.com/questions/25009284/how-to-plot-roc-curve-in-python
    skplt.metrics.plot_roc_curve(y_true, y_probs)
    plt.show()

def sort_with_type_check(t):
        return sorted(t, key=lambda x: (str(type(x)), x))
    
def build_best_tree(config, X_test, X_train, y_test, score_type, tree_types, best_tree, categories):
    # normalized_tree = [(tuple(sort_with_type_check(a)), tuple(sort_with_type_check(b))) for a, b in best_tree] 
    built_mods = build_single_models(config, best_tree, X_train, score_type=score_type, train_type=tree_types)
    test_single_models(built_mods, X_test)
    built_mods = list(built_mods.values())
    config.log.info(f'Best models are {built_mods}')
    tree_model = mod.tree_model('tree_mod1', built_mods, best_tree)
    output = tree_model.predict(X_test)
    tree_model.model_score(y_test.tolist())
    accuracy = accuracy_score(y_test.tolist(), output['y_pred'].to_list())
    config.log.info(f'Accuracy is {accuracy}')
    string_categories = [str(i) for i in categories]
    config.log.info(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=string_categories))
    print(classification_report(y_test.tolist(), output['y_pred'].to_list(), target_names=string_categories))
    return tree_model