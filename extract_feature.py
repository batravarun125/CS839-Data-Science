import pandas as pd
import string
import sys
import re
import os
import io
import numpy as np

output_dir_path = os.path.dirname(os.path.abspath(__file__))+'/results/'

df = pd.read_csv(sys.argv[1],delimiter='`')

PATH_TO_VEC = os.path.dirname(os.path.abspath(__file__))+'/specials/crawl-300d-2M.vec'

if str(sys.argv[2]).lower().startswith('train'):
    var = "train"
else:
    var = "test"

def insert_csv_col(header,value):
    df.insert(len(df.columns),header,value)

def prefixMatch(instance):
    l = instance.split(" ")

    if l[0] in prefixes or (l[0] + ".") in prefixes:
        return True
    return False
def postApostropheMatch(instance):
    l = instance.split(" ")
    val = l[-1]


    if len(val)>2 and (val[-1] == "\'" or val[-2:] == "\'s" or val[-1] == "’" or val[-2:] == "’s"):

        return True
    return False

def get_wordvec(path_to_vec):
    word_vec = {}

    with io.open(path_to_vec, 'r', encoding='utf-8') as f:
        # if word2vec or fasttext file : skip first line "next(f)"
        for line in f:
            word, vec = line.split(' ', 1)
            word_vec[word] = np.fromstring(vec, sep=' ')

    # logging.info('Found {0} words with word vectors, out of \
    #     {1} words'.format(len(word_vec), len(word2id)))
    return word_vec

def create_dictionary(sentences, threshold=0):
    words = {}
    for s in sentences:
        for word in s:
            words[word] = words.get(word, 0) + 1

    if threshold > 0:
        newwords = {}
        for word in words:
            if words[word] >= threshold:
                newwords[word] = words[word]
        words = newwords
    words['<location>'] = 1e9 + 4
    words['</location>'] = 1e9 + 3
    # words['<p>'] = 1e9 + 2

    sorted_words = sorted(words.items(), key=lambda x: -x[1])  # inverse sort
    id2word = []
    word2id = {}
    for i, (w, _) in enumerate(sorted_words):
        id2word.append(w)
        word2id[w] = i

    return id2word, word2id

def has_keywords_before(previous_word, word_context):
    keywords = ["at", "in"]

    previous_word = get_previous_word(word, word_context)

    if not previous_word:
        return 0

    if previous_word in keywords:
        return 1

    previous_previous_word = get_previous_word(previous_word, word_context)
    if previous_previous_word:
        return 1 if previous_previous_word in keywords else 0

    return 0

if __name__ == '__main__':
    insert_csv_col("POST_VERB_DISTANCE",100)
    insert_csv_col("PRE_TITLE", False)
    insert_csv_col("PRE_ARTICLE_DISTANCE", False)
    insert_csv_col("LOCATION_BASED", False)
    insert_csv_col("PRE_POSITION_DISTANCE", 100)
    insert_csv_col("POST_POSITION_DISTANCE", 100)
    insert_csv_col("IS_PRE_POSITION", False)
    insert_csv_col("EXTRAS", False)
    insert_csv_col("PRE_POST_CAPITAL", False)
    insert_csv_col("POST_APOSTROPHE", False)
    insert_csv_col("POST_PREPOSITION", False)
    insert_csv_col("RELATIONSHIP", False)
    insert_csv_col("POST_SAY_SYNONYM", False)
    insert_csv_col("PRE_SAY_SYNONYM", False)
    insert_csv_col("POSITION", False)
    insert_csv_col("COUNTRY", False)
    insert_csv_col("PRE_VERB_DISTANCE", 100)
    insert_csv_col("IS_START_WORD", False)
    insert_csv_col("IS_END_WORD", False)
    insert_csv_col("IS_PREV_LOCATION_DESCRIPTOR", False)
    insert_csv_col("IS_POST_LOCATION_DESCRIPTOR", False)
    insert_csv_col("TOKEN_LENGTH", 100)
    df["PREV_VEC"] = [[0.0]*300]*len(df)
    df["POST_VEC"] = [[0.0]*300]*len(df)
    # insert_csv_col("PREV_VEC", [0]*300)
    # insert_csv_col("POST_VEC", [0]*300)

    print("started feature extraction for " + var)

    verbs_file = open('./specials/verbs4.txt')
    stopwords_file = open('./specials/stopwords.txt')
    prepositions_file=open('./specials/prepositions.txt')
    articles_file=open('./specials/articles.txt')
    prefixes_file = open('./specials/prefixes.txt')
    saySynonmys_file = open('./specials/saySynonyms.txt')
    relationships_file = open('./specials/relations.txt')
    positions_file = open('./specials/positions.txt')
    country_file = open('./specials/country.txt')
    locations_file = open('./specials/locations.txt')

    word_vec = get_wordvec(PATH_TO_VEC)
    # print(word_vec['believe'].tolist())

    verbs = verbs_file.read().lower().split()
    stopwords = stopwords_file.read().lower().split()
    prepositions=prepositions_file.read().lower().split()
    articles=articles_file.read().lower().lower().split()
    prefixes=prefixes_file.read().split()
    # print(prefixes)
    saySynonmys=saySynonmys_file.read().lower().split()
    relationships = relationships_file.read().lower().split()
    positions = positions_file.read().lower().split()
    # print(positions)
    country = country_file.read().lower().split()
    locations = locations_file.read().lower().split()

    print("Files read.")

    file_data_dict = dict()


    for j in range(len(df)):
        if j % 10000 == 0:
            print(j)


        # if df.loc[j]['filename'][-7:] not in file_data_dict.keys():
        #     sfile = open('./data/raw/' + df.loc[j]['filename'][-7:])
        #     file_data_dict[df.loc[j]['filename'][-7:]] = sfile.read().split()
        #     print("read file"+df.loc[j]['filename'][-7:])
        #
        # ls = file_data_dict[df.loc[j]['filename'][-7:]]

        # start = df.loc[j]['start_ind']
        # end = df.loc[j]['end_ind']
        instance = df.iloc[j]["Tokens"]

        # if df.loc[j]['filename'][-7:] not in file_data_dict.keys():
        #     sfile = open('./data/raw/' + df.loc[j]['filename'][-7:])
        #     file_data_dict[df.loc[j]['filename'][-7:]] = sfile.read().split()
        #     print("read file"+df.loc[j]['filename'][-7:])
        #
        # ls = file_data_dict[df.loc[j]['filename'][-7:]]

        start = df.loc[j]['start_ind']
        end = df.loc[j]['end_ind']
        instance = df.loc[j]["Tokens"]

        instance = re.sub('<location>', '', instance)
        instance = re.sub('</location>', '', instance)

        # if start>5:
        #     prestring = ls[start-5:start]
        #     if '.' in prestring:
        #         prestring = prestring[prestring.index('.')+1:]
        # else:
        #     prestring = ls[0:start]
        #     if '.' in prestring:
        #         prestring = prestring[prestring.index('.')+1:]
        # if end< len(ls)-5:
        #     postring = ls[end+1:end + 5]
        #     if '.' in postring:
        #         postring = postring[0:postring.index('.')]
        # else:
        #     postring = ls[end+1:len(ls)-1]
        #     if '.' in postring:
        #         postring = postring[0:postring.index('.')]
        #
        # if start>1:
        #     preword = ''.join(ls[start-1:start])
        # else:
        #     preword = ''.join(ls[0:start])
        #
        # if end< len(ls)-1:
        #     postword = ''.join(ls[end+1:end+2])
        #
        # else:
        #     postword = ''.join(ls[end+1:len(ls)-1])

        prestring_upper = re.sub('[\',\[\]]','',df.loc[j]["pre_string"]).replace('<location>','').replace('</location>','')
        postring_upper = re.sub('[\',\[\]]','',df.loc[j]["pos_string"]).replace('<location>','').replace('</location>','')
        prestring = prestring_upper.lower()
        postring = postring_upper.lower()
        prestring_upper = prestring_upper.split()
        postring_upper = postring_upper.split()
        prestring = prestring.split()
        postring = postring.split()
        preword = ''
        postword = ''
        if len(prestring)>0:
            preword = prestring[len(prestring)-1].lower()

        if len(postring)>0:
            postword = postring[0].lower()

        # if(j<10):
        #     print(str(prestring)+"~@@~"+str(postring)+"~@@~"+preword+"~@@~"+postword)




        for i in postring:
            if i in verbs:
                df.at[j,"POST_VERB_DISTANCE"]=postring.index(i)
                break

        df.at[j, "PRE_TITLE"] = prefixMatch(instance)
        df.at[j, "POST_APOSTROPHE"] = postApostropheMatch(instance.lower())

        if postword in prepositions:
            df.at[j,"POST_PREPOSITION"]=True

        if preword in articles:
            df.at[j,"PRE_ARTICLE_DISTANCE"]= True

        if postword.lower() in saySynonmys:
            df.at[j,"POST_SAY_SYNONYM"]= True

        if preword.lower() in saySynonmys:
            df.at[j,"PRE_SAY_SYNONYM"]= True

        if postword.lower() in relationships:
            df.at[j,"RELATIONSHIP"]= True

        for word in prestring:
            if word in verbs:
                df.at[j,"PRE_VERB_DISTANCE"]=len(prestring)- prestring.index(word)

        for word in prestring:
            if word in positions or word[:-1] in positions:
                df.at[j,"PRE_POSITION_DISTANCE"]=len(prestring)- prestring.index(word)
                break


        for word in postring:
            if word in positions or word[:-1] in positions:
                df.at[j,"POST_POSITION_DISTANCE"] = postring.index(word)
                break

        if preword.lower() in positions or preword[:-1].lower() in positions:
            df.at[j, "IS_PRE_POSITION"] = True


        if instance.lower() in positions:
            df.at[j,"POSITION"]=True

        if instance.lower() in country:
            df.at[j,"COUNTRY"]=True

        for word in prestring:
            if word in locations:
                df.at[j,"LOCATION_BASED"] = True

        prev_vec = np.zeros(300)
        count = 0
        for word in instance.split():
            if word in word_vec:
                # print(word_vec[word])
                prev_vec = prev_vec + word_vec[word]
                count = count+1
                # df.at[j,"PRE_VERB_DISTANCE"]=len(prestring)- prestring.index(word)
        if count > 0:
            prev_vec = prev_vec/count
        df.at[j, "PREV_VEC"] = prev_vec.tolist()


        # for word in postring[:1]:
        #     post_vec = np.zeros(300)
        #     count = 0
        #     if word in word_vec:
        #         post_vec = post_vec + word_vec[word]
        #         count = count+1
        #         # df.at[j,"PRE_VERB_DISTANCE"]=len(prestring)- prestring.index(word)
        #     if count > 0:
        #         post_vec = post_vec/count
        #     df.at[j, "POST_VEC"] = post_vec.tolist()

        # df.at[j, "PREV_VEC"] = np.concatenate((prev_vec, post_vec), axis=None).tolist()


        extra_positives = ['himself','herself','themselves','who']
        for k in postring:
            if k in extra_positives:
                df.at[j, "EXTRAS"] = True

        if(len(prestring_upper)>0):
            if prestring_upper[len(prestring_upper)-1][0] in string.ascii_uppercase:
                    df.at[j,"PRE_POST_CAPITAL"] = True
        if(len(postring_upper)>0):
            if postring_upper[0][0] in string.ascii_uppercase:
                    df.at[j, "PRE_POST_CAPITAL"] = True


        if (len(postring) == 0):
            df.at[j, "IS_END_WORD"] = True

        if (len(prestring) == 0):
            df.at[j, "IS_START_WORD"] = True


        prev_location_descriptors = ["at", "in"]
        if preword in prev_location_descriptors:
            df.at[j, "IS_PREV_LOCATION_DESCRIPTOR"] = True

        df.at[j, "TOKEN_LENGTH"] = len(instance.split(' '))

        post_location_descriptors = ["'s", "based", "region", "square", "country", "city", "town", "county", "creek", "avenue", "court", "block", "street", "block", "drive",
            "centre", "center", "ramp", "exit", "boulevard", "states", "kingdom"]
        if postword.lower() in post_location_descriptors:
            df.at[j, "IS_POST_LOCATION_DESCRIPTOR"] = True







    df.to_csv(output_dir_path+"input_features" + var +".csv",  sep = '`',index = False)
