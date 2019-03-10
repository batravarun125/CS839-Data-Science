import pandas as pd
import os, sys
import argparse
import string

parser = argparse.ArgumentParser(description = 'removing not relevant labels')
parser.add_argument('--notRemoveVerbs', action='store_true')
parser.add_argument('--notRemovePrefixes', action='store_true')
parser.add_argument('--notRemoveCountries', action='store_false')
parser.add_argument('--notRemoveStopWords', action='store_true')
parser.add_argument('--notRemoveDigits', action='store_true')
parser.add_argument('--notRemoveLowerCase', action='store_true')
parser.add_argument('--splitType', type=str, help="data file", default='train')
#parser.add_argument('--notRemoveStopWords', action='store_true')

parser.add_argument('--dataFile', type=str, help="data file", default='results/Tokenizedtest.csv')
parser.add_argument('--verbFile', type=str, help='verbs ', default='./specials/verbs.txt')
parser.add_argument('--prefixesFile', type=str, help='verbs ', default='./specials/prefixes.txt')

parser.add_argument('--countryFile', type=str, help = 'country file', default='./specials/country.txt')
parser.add_argument('--prepositionsFile', type=str, help = 'prep file', default='./specials/prepositions.txt')
parser.add_argument('--stopwordsFile', type=str, help='stopwords file', default='./specials/stopwords.txt')

parser.add_argument('--outFile', type=str, help='outFile path', default='results/PreProcessedTest.csv')

def readFile(file, lower=False):
    
    if lower:
        return [x.strip().lower() for x in open(file).readlines()]
    else:
        return [x.strip() for x in open(file).readlines()]


if __name__ == '__main__':


    args = parser.parse_args()

    if args.splitType.startswith('train'):
        args.dataFile = 'results/Tokenizedtrain.csv'
        args.outFile = 'results/PreProcessedTrain.csv'
    else:
        args.dataFile = 'results/Tokenizedtest.csv'
        args.outFile = 'results/PreProcessedTest.csv'

    print("Input file:"+args.dataFile)
    print("Output file:" + args.outFile)
    # only filter on `Tokens` col
    data = pd.read_csv(args.dataFile, delimiter='`')
    #Create a DataFrame
    #d = {
    #        'Tokens':['play','is','india','jack','raghu','Cathrine',
    #                'Alisa','Bobby','kum2ar','Alisa','Alex','Cathrine'],
    #        'Age':[26,24,23,22,23,24,26,24,22,23,24,24],
    #  
    #        'Score':[85,63,55,74,31,77,85,63,42,62,89,77]}
 
    #data = pd.DataFrame(d,columns=['Tokens','Age','Score'])
    
    totalRowsRemoved = 0
    
    if not args.notRemoveVerbs:

        print("Removing Versbs")
        #load verbs
        verbs = readFile(args.verbFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(verbs)]
        finRow = data.shape[0]
        print("VERBS: Removed {} rows".format(initRow-finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemovePrefixes:

        print("Removing Only Prefixes")
        #load verbs
        prefixes = readFile(args.prefixesFile)
        print(prefixes)
        initRow = data.shape[0]
        # print(data[:100]['Tokens'].replace('<name>', ''))
        data = data[~data['Tokens'].str.replace('<location>', '').isin(prefixes)]
        finRow = data.shape[0]
        print("PREFIXES: Removed {} rows".format(initRow-finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemoveCountries:
        print("Removing Countries")
        countries = readFile(args.countryFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(countries)]
        finRow = data.shape[0]
        print('COUNTRIES: Removed {} rows'.format(initRow-finRow))
        totalRowsRemoved += initRow - finRow


    if not args.notRemoveStopWords:
        print("Removing Stop Words")
        stopwords = readFile(args.stopwordsFile)
        initRow = data.shape[0]
        data = data[~data['Tokens'].isin(stopwords)]
        finRow = data.shape[0]
        print("STOPWORDS: Removed {} rows".format(initRow-finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemoveDigits:
        print("Removing Names with Digits")
        initRow = data.shape[0]
        data = data[~data['Tokens'].str.contains(r'[0-9]')]
        finRow = data.shape[0]
        print("DIGITS: Removed {} rows".format(initRow - finRow))
        totalRowsRemoved += initRow - finRow

    if not args.notRemoveLowerCase:
        remove_list = []
        for idx, row in zip(range(len(data)),data['Tokens']):
            # print(row['Tokens'], idx)
            if(idx%10000 == 0):
                print("done"+str(idx) +row)

            for j in row.split():
                if (j[0] in string.ascii_lowercase):
                    remove_list.append(idx)

        # for i in range(len(data)):
        #     print(data.loc[i]['Tokens'])
        #     for j in (data.loc[i]['Tokens'].split()):
        #         if (j[0] in string.ascii_lowercase):
        #             if not (i in remove_list):
        #                 remove_list.append(i)
        #         if j[0] == '\'':
        #             if not (i in remove_list):
        #                 remove_list.append(i)

        data = data.drop(data.index[remove_list])
        data = data.reset_index(drop=True)

        
    
    print('TOTAL: {} rows removed'.format(totalRowsRemoved))

    data.to_csv(args.outFile, sep = '`', index=False)
