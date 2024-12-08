from abc import ABC, abstractmethod, abstractproperty
import pandas as pd
from sklearn.linear_model import LogisticRegression, LassoCV, RidgeCV, Lasso
from sklearn.metrics import accuracy_score, roc_curve, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import cross_val_predict, cross_val_score
import xgboost as xgb
from skopt import BayesSearchCV
from skopt.space import Real, Integer
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
import ndStepwise.includes.model_functions as mf
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

class model(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
    
    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def predict(self):
        pass

class single_model(model):
    # Name a model (x,)_(y,) to do x vs y regression pass list [(x,),(y,)]. 
    # E.g (1,2,3)_(4,5,6) to do a binary model of 123 vs 456 
    # 123 = 0 and 456 = 1
    def __init__(self, category_split: list, score_type='accuracy'):
        num_list_1 = [int(digit) for digit in category_split[0]]
        num_list_2 = [int(digit) for digit in category_split[1]]
        name = str(category_split[0]) + '_' + str(category_split[1])
        super().__init__(name)
        self.name = name
        self.all_cat_tested = list(set(num_list_1 + num_list_2))
        self.type_0_categories = category_split[0]
        self.type_1_categories = category_split[1]
        self.type_0_categories_name = category_split[0]
        self.type_1_categories_name = category_split[1]
        self.type_0 = num_list_1
        self.type_1 = num_list_2
        self.fitted_model = None
        self.predicted_df = None
        self.category_split = category_split
        self.score = None
        self.y_target = None
        self.cutoff = None
        self.model_type = None

        self.confusion_matrix = None
        self.incorrect_classified_dict = None
        if score_type == 'accuracy':
            self.score_type = 'accuracy'
        else:
            self.score_type = 'accuracy'
    def get_model_name(self):
        return self.name

    def kfold_train(self, df: pd.DataFrame, model_type = 'LogisticRegression', response_col = 'Y'):
        """
        Trains the model on a given set of data 
        input:
            df: pandas dataframe of the train data
            response_col: optional name of the column with response in it (defauls to Y)
        output:
            sds
        """
        # Setup
        if model_type is None:
            model_type = 'LogisticRegression'
        self.model_type = model_type
        train_df = df.copy()
        train_df[self.name] = train_df[response_col].apply(lambda x: 0 if x in self.type_0 else (1 if x in self.type_1 else 'ROW_NOT_IN_REG') )
        train_df = train_df.loc[train_df[self.name] != 'ROW_NOT_IN_REG']
        Y = train_df[self.name].astype(int)
        skip_cutoff = False
        score = None

        #Select model
        if model_type.lower() == 'logisticregression':
            model = make_pipeline(
                StandardScaler(), LogisticRegression(solver='lbfgs', max_iter=4000))
            # Find Cutoff using Youden's J statistic
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))
        elif model_type.lower() == 'logisticregressionlasso':
            model = make_pipeline(
                StandardScaler(),
                SelectFromModel(Lasso()),
                LogisticRegression(solver='lbfgs', max_iter=4000))
            param_grid = {
                'selectfrommodel__estimator__alpha': [0.01, 0.1],
                'logisticregression__C': [0.01, 0.1, 1]
            }

            model = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
            model.fit(train_df.drop([response_col,self.name], axis=1), Y)
            skip_cutoff = True
            self.score = model.best_score_
            self.fitted_model = model   
            return self.score
            # skip_cutoff = True
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'logisticregressionridge':
            model = make_pipeline(
                StandardScaler(), 
                SelectFromModel(RidgeCV(cv=3)), 
                LogisticRegression(solver='lbfgs', max_iter=4000))
            
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'xgboost':
            model = xgb.XGBClassifier(n_jobs = -1, objective="binary:logistic", eval_metric = 'auc')
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'xgboosthyper':
            model = xgb.XGBClassifier(objective="binary:logistic")
            # Find Cutoff using Youden's J statistic
            
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))

            xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
            # model = KNeighborsClassifier(n_neighbors=5)
            # Will have to do hyperparameter tuning
            # Define search space
            search_spaces = {   
                'learning_rate': Real(0.01, 1.0, 'log-uniform'),
                'max_depth': Integer(2, 20),
                'reg_lambda': Real(1e-9, 100., 'log-uniform'),
                'reg_alpha': Real(1e-9, 100., 'log-uniform'),
                'gamma': Real(1e-9, 0.5, 'log-uniform'),  
                'n_estimators': Integer(10, 1000)
            }
            bayes_cv = BayesSearchCV(
                                estimator = xgb_model,                                    
                                search_spaces = search_spaces,                      
                                scoring = 'roc_auc',                                  
                                cv = StratifiedKFold(n_splits=3, shuffle=True),                                
                                n_iter = 3,                                      
                                n_points = 5,                                       
                                n_jobs = -1,                                                                                
                                verbose = 1,
                                random_state=42,
                                refit=True
            )  
            
            np.int = int
            _ = bayes_cv.fit(train_df.drop([response_col,self.name], axis=1), Y)
            model = xgb.XGBClassifier(
                n_jobs = -1,
                objective = 'binary:logistic',
                eval_metric = 'auc', 
                **bayes_cv.best_params_
            )
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'svm':
            model = make_pipeline(StandardScaler(), svm.SVC(probability=True))
            # model = svm.SVC(probability=True)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'randomforest':
            model = RandomForestClassifier(n_estimators=100)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'knn':
            # model = KNeighborsClassifier()
            model = KNeighborsClassifier(n_neighbors=10)
            skip_cutoff = True
        elif model_type.lower() == 'knnhyper':
            # Set up GridSearchCV
            # model = KNeighborsClassifier()
            param_grid = {'kneighborsclassifier__n_neighbors': range(1,31)}
            knn = make_pipeline(StandardScaler(), KNeighborsClassifier())
            knn = make_pipeline(KNeighborsClassifier())
            model = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
            model.fit(train_df.drop([response_col,self.name], axis=1), Y)
            skip_cutoff = True
            self.score = model.best_score_
            self.fitted_model = model
            return self.score
        else:
            print(f"nothing found for {model_type.lower()}")
            model = LogisticRegression(solver='sag', max_iter=2000)

            # Find Cutoff using Youden's J statistic
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))

            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            # XGBoost, Neural Network, Stukel model, anyother will work 
            # beat multinomial regression 
        if not skip_cutoff:
            try:
                self.cutoff, model_score = mf.kfold_find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type, skip_cutoff=skip_cutoff)
                self.score = model_score
                self.fitted_model = model
                return self.score
            except Exception as e:
                print(f'Failed to find cutoff due to {e}')
                raise e
                self.cutoff = None
        else:
            return self.score

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        cross_val_scores = cross_val_score(model, train_df.drop([response_col,self.name], axis=1), Y, cv=kf)
        self.score = cross_val_scores.mean()
        # model.fit(train_df.drop([response_col,self.name], axis=1), Y)
        self.fitted_model = model

        return cross_val_scores.mean()
    
    def train(self, df: pd.DataFrame, model_type = 'LogisticRegression', response_col = 'Y'):
        """
        Trains the model on a given set of data 
        input:
            df: pandas dataframe of the train data
            response_col: optional name of the column with response in it (defauls to Y)
        output:
            sds
        """
        # Setup
        if model_type is None:
            model_type = 'LogisticRegression'
        self.model_type = model_type
        train_df = df.copy()
        train_df[self.name] = train_df[response_col].apply(lambda x: 0 if x in self.type_0 else (1 if x in self.type_1 else 'ROW_NOT_IN_REG') )
        train_df = train_df.loc[train_df[self.name] != 'ROW_NOT_IN_REG']
        Y = train_df[self.name].astype(int)
        skip_cutoff = False
        
        #Select model
        if model_type.lower() == 'logisticregression':
            model = make_pipeline(
                StandardScaler(), LogisticRegression(solver='lbfgs', max_iter=4000))
            # Find Cutoff using Youden's J statistic
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))
        elif model_type.lower() == 'logisticregressionlasso':
            model = make_pipeline(
                StandardScaler(), 
                SelectFromModel(LassoCV(cv=3)), 
                LogisticRegression(solver='lbfgs', max_iter=2000, C=0.1))
            # skip_cutoff = True
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'logisticregressionridge':
            model = make_pipeline(
                StandardScaler(), 
                SelectFromModel(RidgeCV(cv=3)), 
                LogisticRegression(solver='lbfgs', max_iter=2000))
            
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'xgboost':
            model = xgb.XGBClassifier(n_jobs = -1, objective="binary:logistic", eval_metric = 'auc')
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'xgboosthyper':
            model = xgb.XGBClassifier(objective="binary:logistic")
            # Find Cutoff using Youden's J statistic
            
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))

            xgb_model = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
            # model = KNeighborsClassifier(n_neighbors=5)
            # Will have to do hyperparameter tuning
            # Define search space
            search_spaces = {   
                'learning_rate': Real(0.01, 1.0, 'log-uniform'),
                'max_depth': Integer(2, 20),
                'reg_lambda': Real(1e-9, 100., 'log-uniform'),
                'reg_alpha': Real(1e-9, 100., 'log-uniform'),
                'gamma': Real(1e-9, 0.5, 'log-uniform'),  
                'n_estimators': Integer(10, 1000)
            }
            bayes_cv = BayesSearchCV(
                                estimator = xgb_model,                                    
                                search_spaces = search_spaces,                      
                                scoring = 'roc_auc',                                  
                                cv = StratifiedKFold(n_splits=3, shuffle=True),                                
                                n_iter = 3,                                      
                                n_points = 5,                                       
                                n_jobs = -1,                                                                                
                                verbose = 1,
                                random_state=42,
                                refit=True
            )  
            
            np.int = int
            _ = bayes_cv.fit(train_df.drop([response_col,self.name], axis=1), Y)
            model = xgb.XGBClassifier(
                n_jobs = -1,
                objective = 'binary:logistic',
                eval_metric = 'auc', 
                **bayes_cv.best_params_
            )
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'svm':
            model = make_pipeline(StandardScaler(), svm.SVC(probability=True))
            # model = svm.SVC(probability=True)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'randomforest':
            model = RandomForestClassifier(n_estimators=100)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
        elif model_type.lower() == 'knn':
            # model = KNeighborsClassifier()
            model = KNeighborsClassifier(n_neighbors=10)
            skip_cutoff = True
        elif model_type.lower() == 'knnhyper':
            # Set up GridSearchCV
            # model = KNeighborsClassifier()
            param_grid = {'kneighborsclassifier__n_neighbors': range(1,31)}
            knn = make_pipeline(StandardScaler(), KNeighborsClassifier())
            model = GridSearchCV(knn, param_grid, cv=5, scoring='accuracy')
            model.fit(train_df.drop([response_col,self.name], axis=1), Y)
            skip_cutoff = True
            self.score = model.best_score_
            self.fitted_model = model
            
        else:
            print(f"nothing found for {model_type.lower()}")
            model = LogisticRegression(solver='sag', max_iter=2000)

            # Find Cutoff using Youden's J statistic
            # predict_probabilities = cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba')[:, 1]
            # fpr, tpr, thresholds = roc_curve(Y, predict_probabilities)
            # optimal_idx = np.argmax(tpr - fpr)
            # self.cutoff = thresholds[optimal_idx]
            #mf.plot_roc_curve(Y, cross_val_predict(model, train_df.drop([response_col,self.name], axis=1), Y, method='predict_proba'))

            # self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            #self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type)
            # XGBoost, Neural Network, Stukel model, anyother will work 
            # beat multinomial regression 
        try:
            self.cutoff = mf.find_cutoff(model, train_df.drop([response_col,self.name], axis=1), Y, self.score_type, skip_cutoff=skip_cutoff)
        except Exception as e:
            print(f'Failed to find cutoff due to {e}')
            self.cutoff = None
        model.fit(train_df.drop([response_col,self.name], axis=1), Y)
        self.fitted_model = model

        return model

    def predict(self, df_original: pd.DataFrame):
        """
        Tests the model on a given set of data. Must be called after a model has been trained
        input:
            df: pandas dataframe of the test data
            response_col: optional name of the column with response in it (defaults to Y)
        output:
            sds
        """
        df = df_original.copy()
        df['key'] = df.index
        response_col = 'Y'
        # print(df[response_col])
        # train_df = df.copy()
        # train_df[self.name] = train_df[response_col].apply(lambda x: 0 if x in self.type_0 else (1 if x in self.type_1 else 'ROW_NOT_IN_REG') )
        # train_df = train_df.loc[train_df[self.name] != 'ROW_NOT_IN_REG']
        # df = train_df
        if self.fitted_model == None:
            raise Exception('Must train model on data before it can be tested.')

        if self.cutoff is not None:
            y_pred = self.fitted_model.predict_proba(df.drop(['key',response_col], axis=1))[:, 1]
            new_pred = np.where(y_pred > self.cutoff, 1, 0)
            df['y_pred'] = new_pred
            self.predicted_df = df[['key','y_pred']]
        else:
            y_pred = self.fitted_model.predict(df.drop(['key',response_col], axis=1))
            df['y_pred'] = y_pred
            self.predicted_df = df[['key','y_pred']]

        return self.predicted_df

    def model_score(self):
        if self.y_pred is None or self.y_target is None:
            raise Exception ('Must run predict on a model before scoring it.')
        else:
            if self.score_type == 'accuracy' or 'ROC':
                self.score = round(accuracy_score(self.y_target,self.y_pred.tolist()), 8)
            elif self.score_type == 'ROC':
                self.score = round(roc_auc_score(self.y_target,self.y_pred.tolist()), 8)
            elif self.score_type == 'f1':
                self.score = round(f1_score(self.y_target,self.y_pred.tolist()), 8)
            return self.score
        
    def predict_individual(self, df_original: pd.DataFrame):
        """
        Tests the model on a given set of data and scores the model independently of the others
        input:
            df: pandas dataframe of the test data
            response_col: optional name of the column with response in it (defauls to Y)
        output:
            sds
        """
        df = df_original.copy()
        df['key'] = df.index
        response_col = 'Y'
        train_df = df.copy()
        train_df[self.name] = train_df[response_col].apply(lambda x: 0 if x in self.type_0 else (1 if x in self.type_1 else 'ROW_NOT_IN_REG') )
        train_df = train_df.loc[train_df[self.name] != 'ROW_NOT_IN_REG']
       
        if self.fitted_model == None:
            raise Exception('Must train model on data before it can be tested.')
        # y_pred = self.fitted_model.predict(train_df.drop(['key',response_col, self.name], axis=1))
        # train_df['y_pred'] = y_pred
        # self.predicted_df = train_df[['key','y_pred']]
        if self.cutoff is not None:
            y_prob = self.fitted_model.predict_proba(train_df.drop(['key',response_col, self.name], axis=1))[:, 1]
            self.y_pred = np.where(y_prob > self.cutoff, 1, 0)
            train_df['y_pred'] = self.y_pred
            self.predicted_df = train_df[['key','y_pred']]

        else:
            self.y_pred = self.fitted_model.predict(train_df.drop(['key',response_col, self.name], axis=1))
            train_df['y_pred'] = self.y_pred
            self.predicted_df = train_df[['key','y_pred']]
        
        # y_prob = self.fitted_model.predict_proba(train_df.drop(['key',response_col, self.name], axis=1))[:, 1]
        # new_pred = np.where(y_prob > self.cutoff, 1, 0)
        # train_df['y_pred'] = new_pred
        # y_pred = new_pred
        # self.predicted_df = train_df[['key','y_pred']]
        # self.y_pred = y_pred

        self.y_target = train_df[self.name].tolist()
        self.confusion_matrix = confusion_matrix(self.y_target, self.y_pred.tolist(), normalize='true')

        total_counts = train_df['Y'].value_counts().reset_index()
        total_counts.columns = ['Y', 'total_count']
        incorrect_cat = train_df.loc[train_df[self.name] != train_df["y_pred"]]

        type_counts = incorrect_cat['Y'].value_counts().reset_index()
        type_counts.columns = ['Y', 'incorrect_count']

        merged_df = pd.merge(type_counts, total_counts, on='Y')
        merged_df['proportion'] = merged_df['incorrect_count']/merged_df['total_count']
        merged_df.index = merged_df['Y']
        merged_df = merged_df.reindex(self.all_cat_tested, fill_value=0)
        type_counts_dict = merged_df['proportion'].to_dict()
        self.incorrect_classified_dict = type_counts_dict

        # print(self.name)
        # print(self.confusion_matrix)
        if self.score_type == 'accuracy' or 'ROC':
            self.score = accuracy_score(self.y_target,self.y_pred.tolist())
        elif self.score_type == 'ROC':
            self.score = roc_auc_score(self.y_target,self.y_pred.tolist())
        elif self.score_type == 'f1':
            self.score = f1_score(self.y_target,self.y_pred.tolist())
        return self.predicted_df
    
    def get_prediction(self):
        return self.predicted_df
    
    def reset_labels(self, transform_label):
        # self.all_cat_tested = list(set(num_list_1 + num_list_2))
        self.name = str(transform_label.inverse_transform((self.category_split[0]))) + '_' + str(transform_label.inverse_transform((self.category_split[1])))
        self.type_0_categories_name = transform_label.inverse_transform(self.type_0_categories_name)
        self.type_1_categories_name = transform_label.inverse_transform(self.type_1_categories_name)

class tree_model(model):
    # name of model needs to be recognizable or some combination of the submodels
    def __init__(self, name, model_list, tree_struct, score_type='accuracy'):
        """
        
        input:
            name: name of this model
            model_list: list of all models in order that make up the regression
        output:
            sds
        """
        super().__init__(name)
        self.models = sorted(model_list, key=lambda x: len(x.name), reverse=True)
        #sort model list
        self.predicted_df = None
        self.tree_struct = tree_struct
        self.score = None
        if score_type == 'accuracy':
            self.score_type = 'accuracy'
        elif score_type == 'f1':
            self.score_type = 'f1'
        else:
            self.score_type = 'accuracy'

    def train(self):
        """
        By design we feed tree model pretrained models
        """
        pass

    def predict(self, df:pd.DataFrame):
        predicted_dfs = dict()
        df_key = df.copy()
        df_key['key'] = df_key.index
        for model in self.models:
            df_pred = df.copy()
            y_pred = model.predict(df_pred)
            predicted_dfs.update({model:y_pred})

        df_key['total_pred'] = None

        # for index, row in df_key.iterrows():
        #     df_key.loc[df_key['key'] == row['key']] = 'max_' + str(row['key'])
        # print(df_key)
        # for model in self.models:
        #     predicted_dfs[model_check].loc[predicted_dfs[model_check]['key'] == [row['key']]]
        list_pred = list()
        for index, row in df_key.iterrows():
            model_check = self.models[0]
            while(True):
                y_pred_df = predicted_dfs[model_check]
                if int(y_pred_df.loc[y_pred_df['key'] == row['key']]['y_pred'].iloc[0]) == 1:
                    next_step = model_check.type_1
                else:
                    next_step = model_check.type_0
                if len(next_step) == 1:
                    list_pred.append(int(next_step[0]))
                    break
                else:
                    try:
                        model_check = [x for x in self.models if sorted(x.all_cat_tested) == sorted(next_step)][0]
                    except Exception as e:
                        print(e)
                        raise e

        df_key['y_pred'] = list_pred
        self.predicted_df= df_key[['key','y_pred']]
        return self.predicted_df
    
    def model_score(self, y_test):
        df_pred = self.predicted_df['y_pred']
        if self.score_type == 'accuracy' or 'ROC':
            self.score = accuracy_score(y_test,df_pred.tolist())
        elif self.score_type == 'ROC':
            self.score = roc_auc_score(y_test,df_pred.tolist())
        elif self.score_type == 'f1':
            self.score = f1_score(y_test,df_pred.tolist())
        return self.score
        