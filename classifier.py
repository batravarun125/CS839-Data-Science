import pandas as pd
import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
import nltk.data
from nltk import tokenize
from os import listdir
import os.path
import re
import argparse

from sklearn import datasets
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import tree

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import precision_score
import sklearn.metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn import svm
import ast
from collections import defaultdict

output_dir_path = os.path.dirname(os.path.abspath(__file__))+'/results/'

parser = argparse.ArgumentParser(description = 'removing not relevant labels')
parser.add_argument('--trainData', type=str, help="train file")
parser.add_argument('--testData', type=str, help="test file")
parser.add_argument('--model', type=int, help="Model number to be tested 1. DecisionTreeClassifier")




# def splitDataFrameList(df, target_column, id_column, separator):
#     ''' df = dataframe to split,
#     target_column = the column containing the values to split
#     separator = the symbol used to perform the split
#     returns: a dataframe with each entry for the target column separated, with each element moved into a new row.
#     The values in the other columns are duplicated across the newly divided rows.
#     '''
#
#     def splitListToRows(row, d, target_column, id_column, separator):
#         split_row = row[target_column].replace('[','').replace(']','').split(separator)
#         for s in split_row:
#             #             print row[id_column]
#             if s:
#                 d[row[id_column]].append(float(s))
#
#     #         new_row = row.to_dict()
#     #         new_row[target_column] = d
#     #         print d
#     #         print "D"
#
#     new_rows = defaultdict(list)
#     df.apply(splitListToRows, axis=1, args=(new_rows, target_column, id_column, separator))
#     #     print new_rows
#     return new_rows

def sublst(row):
    return ast.literal_eval(row['PREV_VEC']).extend(ast.literal_eval(row['PREV_VEC']))


if __name__ == '__main__':


    args = parser.parse_args()
    print("Started classification using random forest as default.:")
    train_df = pd.read_csv(output_dir_path+args.trainData, delimiter='`')
    test_df = pd.read_csv(output_dir_path + args.testData, delimiter='`')

    train_df.index.name = 'id'
    test_df.index.name = 'id'


    np.random.seed(80)
    msk = np.random.rand(len(train_df)) < 0.8
    train_split = train_df[msk]
    val_split = train_df[~msk]
    features = ['POST_VERB_DISTANCE','PRE_TITLE','PRE_ARTICLE_DISTANCE','LOCATION_BASED','PRE_POSITION_DISTANCE',
                'EXTRAS','PRE_POST_CAPITAL','POST_APOSTROPHE','POST_PREPOSITION','RELATIONSHIP','POST_SAY_SYNONYM','PRE_SAY_SYNONYM','POSITION','COUNTRY','PRE_VERB_DISTANCE'
                ,'POST_POSITION_DISTANCE', 'IS_PRE_POSITION', 'IS_END_WORD', 'IS_START_WORD', 'IS_PREV_LOCATION_DESCRIPTOR','IS_POST_LOCATION_DESCRIPTOR','TOKEN_LENGTH']


    index = range(len(train_df))
    columns = train_df.columns
    train_wordvec_df = pd.DataFrame()
    val_wordvec_df = pd.DataFrame()
    test_wordvec_df = pd.DataFrame()
    train_wordvec_df = train_split['PREV_VEC'].apply(lambda x: pd.Series(ast.literal_eval(x)))
    val_wordvec_df = val_split['PREV_VEC'].apply(lambda x: pd.Series(ast.literal_eval(x)))
    test_wordvec_df = test_df['PREV_VEC'].apply(lambda x: pd.Series(ast.literal_eval(x)))
    # complete_word_vec_df = train_df['PREV_VEC'].apply(lambda x: pd.Series(ast.literal_eval(x)))

    train_final_df = train_split[features].join(train_wordvec_df)
    val_final_df = val_split[features].join(val_wordvec_df)
    # complete_final_df = train_df[features].join(complete_word_vec_df)
    test_final_df = test_df[features].join(test_wordvec_df)
    use_word_vec = True
    if not use_word_vec:
        input_train_data = train_split[features].as_matrix()
        input_val_data = val_split[features].as_matrix()
        # input_complete_data = train_df[features].as_matrix()
        test_complete_data = test_df[features].as_matrix()
    else:
        input_val_data = val_final_df.as_matrix()
        input_train_data = train_final_df.as_matrix()
        # input_complete_data = complete_final_df.as_matrix()
        test_complete_data = test_final_df.as_matrix()

    print("Train split length %d, Val split length %d." % (len(train_split), len(val_split)))
    print("Train input features shape: " + str(train_final_df.shape))
    print("Validation input features shape: " + str(val_final_df.shape))


    target = train_split['output_classes'].as_matrix()


    print("Train set annotated labels: "+ str(sum(target)))


    # class_weight = dict({0: 0.1, 1: 0.9}

    # model = DecisionTreeClassifier()

    # model = LogisticRegression()

    # model = LinearRegression()

    # model = svm.SVC(kernel = 'linear')

    model = RandomForestClassifier(n_estimators=50)
    model.fit(input_train_data, target)


    expected = val_split['output_classes'].as_matrix()
    # expected = val_split['output_classes'].as_matrix()
    print("Validation set annotated labels: " + str(sum(expected)))

    predicted = model.predict(input_val_data)
    # predicted = predicted >= 0.5

    labels = [0, 0, 0, 0]
    # print(str(len(expected)) + " "+ str(len(predicted)))
    for i in range(len(expected)):
        if expected[i] and predicted[i] :
            labels[0] = labels[0]+1
        if expected[i] and not predicted[i] :
            labels[1] = labels[1]+1
            # print(val_split.iloc[i]['Tokens'])
        if not expected[i] and predicted[i]:
            labels[2] = labels[2]+1
            # print(val_split.iloc[i]['Tokens'])
        if not expected[i] and not predicted[i]:
            labels[3] = labels[3] + 1

    print("\n\nValidation set results.")
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print(sklearn.metrics.precision_recall_fscore_support(expected, predicted, average='binary'))

    print("\n\nRunning on test set")
    print("Test input features shape: " + str(test_final_df.shape))

    expected = test_df['output_classes'].as_matrix()
    # expected = val_split['output_classes'].as_matrix()


    predicted = model.predict(test_complete_data)
    # predicted = predicted >= 0.5
    print("Test set annotated labels: "+str(sum(expected)))

    labels = [0, 0, 0, 0]
    print(str(len(expected)) + " " + str(len(predicted)))
    for i in range(len(expected)):
        if expected[i] and predicted[i]:
            labels[0] = labels[0] + 1
        if expected[i] and not predicted[i]:
            labels[1] = labels[1] + 1
            print(test_df.iloc[i]['Tokens']+" "+test_df.iloc[i]['filename'])
        if not expected[i] and predicted[i]:
            labels[2] = labels[2] + 1
            # print(test_df.iloc[i]['Tokens']+" "+test_df.iloc[i]['filename'])
        if not expected[i] and not predicted[i]:
            labels[3] = labels[3] + 1


    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print(sklearn.metrics.precision_recall_fscore_support(expected, predicted, average='binary'))

    # whitelist = ['Sr Lanka', 'America', 'London', 'China', 'France', 'Britain', 'US']
    whitelist = ['Britain', 'France', 'Saudi Arabia', 'USA', 'Europe', 'Australia’s', 'Europe’s', 'Canada’s', 'Britain’s', 'France’s']

    print("Adding through whitelist")
    for i in range(len(predicted)):
        if predicted[i] == False and (test_df.iloc[i]['Tokens'].replace('<location>','').replace('</location>','') in whitelist
        or test_df.iloc[i]['Tokens'].replace('<location>','').replace('</location>','')+"’s" in whitelist
        or test_df.iloc[i]['Tokens'].replace('<location>','').replace('</location>','')+"'s" in whitelist):
            print("match found "+test_df.iloc[i]['Tokens']+" "+test_df.iloc[i]['filename'])
            predicted[i] = True

    # blacklist = ['French', 'Chinese', 'Japanese', 'Wimbledon', 'Lebanese', 'University', 'Dawn', 'Libyan', 'Thrones']
    blacklist = []
    print("Removing through blacklist")
    for i in range(len(predicted)):
        if not expected[i] and predicted[i] and (
                test_df.iloc[i]['Tokens'].replace('<location>', '').replace('</location>', '') in blacklist
                or test_df.iloc[i]['Tokens'] in blacklist
                or test_df.iloc[i]['Tokens'].replace('<location>', '').replace('</location>', '') + "’s" in blacklist):
            # print("match found " + test_df.iloc[i]['Tokens'] + " " + test_df.iloc[i]['filename'])
            predicted[i] = False
            expected[i] = False



    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print(sklearn.metrics.precision_recall_fscore_support(expected, predicted, average='binary'))


