import os
import sys


try:
    sys.argv[1]
except IndexError:
    split_type = "all"
else:
    split_type = sys.argv[1]


if not os.path.isfile( os.path.dirname(os.path.abspath(__file__)) +'/specials/crawl-300d-2M.vec'):
    os.chdir('specials/')
    os.system('unzip specials/crawl-300d-2M.vec.zip')
    os.chdir('..')


if split_type.startswith("train"):
    os.system('python tokenization.py dev_data/ train')
    os.system('python preProcessing.py --splitType train')
    os.system('python extract_feature.py results/PreProcessedTrain.csv train')


elif split_type.startswith("test"):
    os.system('python tokenization.py test_data/ test')
    os.system('python preProcessing.py --splitType test')
    os.system('python extract_feature.py results/PreProcessedTest.csv test')

else:

    os.system('python tokenization.py dev_data/ train')
    os.system('python preProcessing.py --splitType train')
    os.system('python extract_feature.py results/PreProcessedTrain.csv train')

    os.system('python tokenization.py test_data/ test')
    os.system('python preProcessing.py --splitType test')
    os.system('python extract_feature.py results/PreProcessedTest.csv test')


os.system('python classifier.py --trainData input_featurestrain.csv --testData input_featurestest.csv')