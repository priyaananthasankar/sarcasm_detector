"""
USC Computer Science 544: Applied Natural Language Processing
File name   : perceptron.py
Usage       : python perceptron.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : This file used linear SVM algorithm to train and test classifier to detect sarcasm
	      in tweets.We crawled and annotated 3000 tweets to get this data set.Training and
	      Testing data can be found under data folder at root of repository.
"""
__author__ = "Niranjana Kandavel"
__email__ = "kandavel@usc.edu"
__credits__ = ["Priya Ananthasankar", "Ravi"]
__status__ = "Prototype"

import sys, csv
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import re
import string
from sklearn.linear_model import Perceptron
from sklearn.feature_extraction.text import HashingVectorizer
import json




def clean_tweet (tweet):
    tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", tweet, flags=re.MULTILINE)
    tweet = re.sub(r"([@])(\w+)\b", "", tweet, flags=re.MULTILINE)
    tweet = "".join(l for l in tweet if l not in string.punctuation)
    return(tweet)


def read_tweets_to_list(file_name):
    c = -1
    tweets = []
    tags = []
    fd = open(file_name, 'r')
    csv_reader = csv.reader(fd)
    for row in csv_reader:
        c += 1
        if c == 0:
            continue
        else:

            cleaned_tweet = clean_tweet(row[0])
            tweets.append(cleaned_tweet)

            if row[5] == 'S':
                tags.append(1)
            else:
                tags.append(-1)
    return tweets, tags


def main():
    classify_dir = sys.argv[1]
    test_dir = sys.argv[2]
    hv = HashingVectorizer(stop_words='english', analyzer='word')
    tweets, tags = read_tweets_to_list(classify_dir)
    trainset = hv.transform(tweets)

    #perceptron
    pct = Perceptron(n_iter=400, alpha=0.0001, shuffle=True, warm_start=True)
    pct.fit(trainset, tags)

    tweets, tags_actual = read_tweets_to_list(test_dir)
    testset = hv.transform(tweets)
    tags_predicted = pct.predict(testset)

    print ("Accuracy : "+str(accuracy_score(tags_actual, tags_predicted)))

    prf = precision_recall_fscore_support(tags_actual, tags_predicted, average=None, labels=['1', '-1'])

    metrics = {}
    metrics["title"] = "perceptron_all_features"
    metrics["accuracy"] = accuracy_score(tags_actual, tags_predicted)
    metrics["sarcasm_precision"] = prf[0][0]
    metrics["not_sarcasm_precision"] = prf[0][1]
    metrics["sarcasm_recall"] = prf[1][0]
    metrics["not_sarcasm_recall"] = prf[1][1]
    metrics["sarcasm_f_measure"] = prf[2][0]
    metrics["not_sarcasm_f_measure"] = prf[2][1]
    all_metrics = {}
    all_metrics["perceptron"] = metrics

    if "pol" in test_dir:
        fout = open("political_metrics.json","wt")
    else:
        fout = open("metrics.json", "wt")
    json_data = json.dumps(all_metrics)
    fout.write(json_data)
    print(json_data)


if __name__ == '__main__':
    main()







