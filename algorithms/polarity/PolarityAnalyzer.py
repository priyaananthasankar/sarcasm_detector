"""
USC Computer Science 544: Applied Natural Language Processing

File name   : PolarityAnalyzer.py
Usage       : python3 PolarityAnalyzer.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : This file is used to just show some numbers on how many tweets in
              sarcasm labelled corpus are positive/negative

"""
__author__  = "Priya Ananthasankar"
__email__   = "panantha@usc.edu"
__credits__ = ["Ravi Kiran Chadalawada","Niranjana Kandavel"]
__status__  = "Prototype"


import sys
import csv
train_data = sys.argv[1]
test_data = sys.argv[2]

positive_lexicon = "./lexicon/positive-words.txt"
negative_lexicon = "./lexicon/negative-words.txt"

positive_words = []
negative_words = []

positive_words = [line.rstrip('\n') for line in open(positive_lexicon,'r',encoding='utf-8', errors='ignore')]
negative_words = [line.rstrip('\n') for line in open(negative_lexicon,'r',encoding='utf-8', errors='ignore')]

sp = 0
sn =0
nsp = 0
nsn = 0

def pol_stats(dir):
    global sp,sn,nsp,nsn
    with open(dir, 'r',encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for original_tweet,text,hashtags,users,length,label in reader:
            words = text.split()
            positive_per_tweet = []
            negative_per_tweet = []
            for word in words:
                if word in positive_words:
                    positive_per_tweet.append(word)
                    if label == "S":
                        sp += 1
                    if label == "NS":
                        sn += 1
                if word in negative_words:
                    negative_per_tweet.append(word)
                    if label == "S":
                        nsp += 1
                    if label == "NS":
                        nsn += 1

pol_stats(train_data)
print ("TRAINING DATA :")
print ("Sarcastic Positive: " , sp)
print ("Sarcastic Negative" , sn)

print ("Non Sarcastic Positive: " , nsp)
print ("Non Sarcastic Negative" , nsn)

sp = 0
sn =0
nsp = 0
nsn = 0

pol_stats(test_data)

print ("TESTING DATA :")
print ("Sarcastic Positive: " , sp)
print ("Sarcastic Negative" , sn)
print ("Non Sarcastic Positive: " , nsp)
print ("Non Sarcastic Negative" , nsn)