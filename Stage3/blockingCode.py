import numpy as np
import pandas as pd


def check_jaccard(string1,string2):
    string1 ='##' + string1 + '##'
    string2 ='##' + string2 + '##'
    setA=[]
    setB=[]
    for j in range(0,len(string1)-2):
        setA.append(string1[j:j+3])
    for j in range(0,len(string2)-2):
        setB.append(string2[j:j+3])
    count=0
    for j in setA:
        if j in setB:
            count = count + 1
    return float(count)/(len(string1)+len(string2)-count)
    

amazon=pd.read_csv('/Users/varunbatra/Downloads/tableA')
goodreads=pd.read_csv('/Users/varunbatra/Downloads/tableB')
candidate_set=pd.read_csv('/Users/varunbatra/Downloads/stage3_1_apply_rules_ds')
#print(len(candidate_set))
t=[]
for i in range(0,len(candidate_set)):
    flag=0
    stringA=str(amazon.iloc[candidate_set.iloc[i,0],1]).upper()
    # print(str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper())
    stringB=str(goodreads.iloc[candidate_set.iloc[i,1],1]).upper()
    if check_jaccard(stringA,stringB)<0.2:
        t.append(i)
candidate_set.drop(t,inplace=True)
print(len(candidate_set))
candidate_set.to_csv('/Users/varunbatra/Downloads/candidate_blocking.csv',sep=',',header=True,index=False)