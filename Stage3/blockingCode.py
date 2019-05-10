import numpy as np
import pandas as pd

amazon=pd.read_csv('tableA')
goodreads=pd.read_csv('tableB')
temp_set=[]
    

if __name__ == '__main__':
    candidate_set=pd.read_csv('stage3_1_apply_rules_ds')
    for i in range(0,len(candidate_set)):
        stringA=str(amazon.iloc[candidate_set.iloc[i,0],1]).upper()
        # print(str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper())
        stringB=str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper()
        stringA = '##' + stringA + '##'
        stringB = '##' + stringB + '##'
        setA=[]
        setB=[]
        count=0
        for j in range(0, len(stringA) - 2):
            setA.append(stringA[j : j + 3])
        for j in range(0, len(stringB) - 2):
            setB.append(stringB[j : j + 3])
        for item in setA:
            if item in setB:
                count = count + 1
        den = len(stringA) + len(stringB) - count
        if float(count) / den < 0.2:
            temp_set.append(i)
    candidate_set.drop(temp_set, inplace=True)
    print(len(candidate_set))
    candidate_set.to_csv('candidate_set_reduced.csv', sep=',', header=True, index=False)
    print("here")
