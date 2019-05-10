import numpy as np
import pandas as pd

amazon=pd.read_csv('tableA')
goodreads=pd.read_csv('tableB')
candidate_set=pd.read_csv('stage3_1_apply_rules_ds')
#print(len(candidate_set))
final_set=[]


def check_jaccard(string1,string2):
    setA=[]
    setB=[]
    count=0
    for i in range(0, len(string1) - 2):
        setA.append(string1[i : i + 3])
    for i in range(0, len(string2) - 2):
        setB.append(string2[i : i + 3])
    for item in setA:
        if item in setB:
            count = count + 1
    return float(count) / (len(string1) + len(string2) - count)
    

if __name__ == '__main__':

    for i in range(0,len(candidate_set)):
        stringA=str(amazon.iloc[candidate_set.iloc[i,0],1]).upper()
        # print(str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper())
        stringB=str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper()
        if check_jaccard('##' + stringA + '##','##' + stringB + '##')<0.2:
            final_set.append(i)
    candidate_set.drop(final_set,inplace=True)
    print(len(candidate_set))
    candidate_set.to_csv('candidate_blocking.csv',sep=',',header=True,index=False)