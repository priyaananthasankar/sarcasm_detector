"""
USC Computer Science 544: Applied Natural Language Processing
File name   : knn.py
Usage       : python perceptron.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : This file used linear KNN algorithm to train and test classifier to detect sarcasm
	      in tweets.We crawled and annotated 3000 tweets to get this data set.Training and
	      Testing data can be found under data folder at root of repository.
"""
__author__ = "Niranjana Kandavel"
__email__ = "kandavel@usc.edu"
__credits__ = ["Priya Ananthasankar", "Ravi"]
__status__ = "Prototype"

import re
import string
import csv
import algorithms.knn.tfidf1 as ti
import sys
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support
import json
import pattern_feature as pf




def clean_tweet_with_punc(tweet):
    tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", tweet, flags=re.MULTILINE)
    tweet = re.sub(r"([@])(\w+)\b", "", tweet, flags=re.MULTILINE)
    return(tweet)

def clean_tweet_wo_punc(tweet):
    tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", tweet, flags=re.MULTILINE)
    tweet = re.sub(r"([@])(\w+)\b", "", tweet, flags=re.MULTILINE)
    tweet = "".join(l for l in tweet if l not in string.punctuation)
    return(tweet)




def makeseq(dir_name):
    x_seq = []
    y_seq = []
    tweets = []

    token_count = []
    tweet_length = []
    c = 0
    max = 0
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for tweet, test, hashtag, user, length, sarc in reader:
            cleaned_tweet = clean_tweet_wo_punc(tweet)
            cleaned_tweet_punc = clean_tweet_with_punc(tweet)
            sub_seq = []
            if c == 0:
                c += 1
                continue
            else:
                tweets.append(cleaned_tweet)

                tweet_length.append(len(cleaned_tweet))

                count_punc = sum((not c.isdigit() and not c.isalpha()) for c in cleaned_tweet_punc)
                count_capital = sum((c.isupper()) for c in cleaned_tweet_punc)
                count_s = count_punc+count_capital
                words = cleaned_tweet.split()
                token_count.append(count_s)
                if max < len(words):
                    max = len(words)
                x_seq.append(sub_seq)

                if sarc == "S":
                    y_seq.append(1)
                else:
                    y_seq.append(0)
                c += 1

    tfidf_val = ti.tfidf(tweets)
    i = 0
    for t in tweets:
        #token_count feature (normalised)
        x_seq[i].append(token_count[i]/max)
        #tfidf feature
        x_seq[i].append(tfidf_val[i])
        #length_feature
        x_seq[i].append(tweet_length[i])
        i += 1
    return x_seq, y_seq

def add_pattern_feature(dir_name, x_seq):
    #to add pattern feature
    pattern_fetaure_list = pf.pattern_feature(dir_name)
    for i in range(0, len(x_seq)):
        x_seq[i].append(pattern_fetaure_list[i])
    return x_seq


def main():
    classify_dir = sys.argv[1]
    test_dir = sys.argv[2]
    x_seq, y_seq = makeseq(classify_dir)
    test_x_seq, test_y_seq = makeseq(test_dir)




    #knn
    neigh = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=3, p=2,
               weights='uniform')
    neigh.fit(x_seq, y_seq)
    op_y_seq = neigh.predict(test_x_seq)
    print("Accuracy : "+str(accuracy_score(op_y_seq, test_y_seq)))



    prf = precision_recall_fscore_support(op_y_seq, test_y_seq, average=None, labels=['1', '0'])


    metrics = {}
    metrics["title"] = "knn_without_pattern_feature"
    metrics["accuracy"] = accuracy_score(op_y_seq, test_y_seq)
    metrics["sarcasm_precision"] = prf[0][0]
    metrics["not_sarcasm_precision"] = prf[0][1]
    metrics["sarcasm_recall"] = prf[1][0]
    metrics["not_sarcasm_recall"] = prf[1][1]
    metrics["sarcasm_f_measure"] = prf[2][0]
    metrics["not_sarcasm_f_measure"] = prf[2][1]
    all_metrics = {}
    all_metrics["knn_without_pattern_feature"] = metrics


    x_seq = add_pattern_feature(classify_dir, x_seq)
    test_x_seq = add_pattern_feature(test_dir, test_x_seq)
    print (x_seq)


    #knn
    neigh = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
               metric_params=None, n_jobs=1, n_neighbors=3, p=2,
               weights='uniform')
    neigh.fit(x_seq, y_seq)
    op_y_seq = neigh.predict(test_x_seq)
    print("Accuracy : "+str(accuracy_score(op_y_seq, test_y_seq)))



    prf = precision_recall_fscore_support(op_y_seq, test_y_seq, average=None, labels=['1', '0'])




    metrics = {}
    metrics["title"] = "knn_all_features"
    metrics["accuracy"] = accuracy_score(op_y_seq, test_y_seq)
    metrics["sarcasm_precision"] = prf[0][0]
    metrics["not_sarcasm_precision"] = prf[0][1]
    metrics["sarcasm_recall"] = prf[1][0]
    metrics["not_sarcasm_recall"] = prf[1][1]
    metrics["sarcasm_f_measure"] = prf[2][0]
    metrics["not_sarcasm_f_measure"] = prf[2][1]
    all_metrics["knn_all_features"] = metrics

    fout = open("metrics.json", "wt")
    json_data = json.dumps(all_metrics)
    fout.write(json_data)
    print(json_data)

if __name__ == '__main__':
    main()