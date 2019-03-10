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

dir_path = str(sys.argv[1])
string_to_search = str(sys.argv[2])
print("searching "+string_to_search)

for filename in listdir(dir_path):
    if not filename.endswith('.txt'):
        continue
    fp = open(dir_path + '/' +filename)
    data = fp.read()

    start_count = data.count('<name>')
    end_count = data.count('</name')

    # print(filename+" "+str(len(data)))
    # print(str(start_count-end_count) +" " + str(filename)+" "+str(start_count)+" "+str(end_count))

    if string_to_search in data:
        print("found text in "+filename)


