from collections import defaultdict
import sys
import csv
import algorithms.knn as k_func
import re
import string
tweets=[]
pattern=[]
import math



import sys


def clean_tweet_wo_punc(tweet):
    tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", tweet, flags=re.MULTILINE)
    tweet = re.sub(r"([@])(\w+)\b", "", tweet, flags=re.MULTILINE)
    tweet = "".join(l for l in tweet if l not in string.punctuation)
    return(tweet)



def pattern_extraction(dir_name, sar):
    words_dict = defaultdict(int)
    max = 0
    tweets = []
    #build dictionary
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for tweet, test, hashtag, user, length, sarc in reader:
            cleaned_tweet = clean_tweet_wo_punc(tweet)
            if sarc == sar:
                tweets.append(cleaned_tweet)
                for w in cleaned_tweet.split():
                    words_dict[w] += 1
                    if max < words_dict[w]:
                        max = words_dict[w]
    threshold = max / 10
    if threshold < 1:
        threshold = 2
    #for "hlhl" kind of pattern
    all_patterns = []
    for t in tweets:
        pattern = ""
        for tokens in t.split():
            if (words_dict[tokens] >= threshold):
                pattern += "h"
            else:
                pattern += "l"
        all_patterns.append(pattern)
    #take all pattern starting with h and ending with h
    many_patterns = set()
    for pat in all_patterns:
        pat_arr = list(pat)
        for i in range (0,len(pat_arr)):

            if pat_arr[i] == 'h':
                lval = 0
                for j in range (i+1,len(pat_arr)):
                    if (lval == 1 and pat_arr[j] == 'h'):
                        str = pat[i:(j+1)]
                        many_patterns.add(str)
                        lval = 0
                    if (pat_arr[j] == 'l'):
                        lval = 1
    return many_patterns

def feature_create(dir_name, sar_patterns, nonsar_patterns):
    words_dict = defaultdict(int)
    max = 0
    #build dictionary
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for tweet, test, hashtag, user, length, sarc in reader:
            cleaned_tweet = clean_tweet_wo_punc(tweet)
            for w in cleaned_tweet.split():
                words_dict[w] += 1
                if max < words_dict[w]:
                    max = words_dict[w]
    threshold = max / 10
    if threshold < 1:
        threshold = 2
    feature = []
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for tweet, test, hashtag, user, length, sarc in reader:
            pattern = ""
            #form hl kind of pattern for the test tweet
            for tokens in tweet.split():
                if (words_dict[tokens] >= threshold):
                    pattern += "h"
                else:
                    pattern += "l"

            if sarc == "S":
                #find matching sarcastic patterns for a tweet
                featureval = 0
                for pat in sar_patterns:
                    if pattern.find(pat) > 0:
                        featureval += 1
                    else:
                        featureval += 0.1
                feature.append(math.log(featureval))
            else:
                #find matching non sarcastic patterns for a tweet
                featureval = 0
                for pat in nonsar_patterns:
                    if pattern.find(pat) > 0:
                        featureval += 1
                    else:
                        featureval += 0.1
                feature.append(math.log(featureval))
    return feature

def pattern_feature(dir_name):
    #get all sarcastic pattern
    sar_patterns = pattern_extraction(dir_name, "S")

    # get all non sarcastic pattern
    nonsar_patterns = pattern_extraction(dir_name, "NS")
    intersect = sar_patterns.intersection(nonsar_patterns)

    #ignoring unwanted patterns
    sar_patterns = sar_patterns.difference(intersect)
    nonsar_patterns = nonsar_patterns.difference(intersect)

    #feature vector creation
    feature_list = feature_create(dir_name, sar_patterns, nonsar_patterns)

    return feature_list





pattern_feature(sys.argv[2])











