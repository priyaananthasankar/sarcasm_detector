import os
import pickle
from collections import defaultdict
import random
import sys
import csv



# defining dictionary to store the weight-words, filename-contents
words = defaultdict(int)
main_dict = defaultdict(int)
tweets = defaultdict()

with open('cleaned_tweets_classify.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    tweetnum = ""
    for tweet, sarcastic in reader:
        count += 1
        if sarcastic == "yes":
            tweetnum = tweet + "_" + "yes" + "_" +str(count)
        else:
            tweetnum = tweet+"_"+"no"+"_"+str(count)
        tweets[tweetnum] = tweet.split()



# recursively going through each file and calculate all the weight of words
b = 0
items = list(tweets.keys())
for i in range(0, 20):
    random.shuffle(items)
    for tweetname in items:
        if "yes" in tweetname:
            y = 1
        elif "no" in tweetname:
            y = -1
        else:
            continue
        alpha = 0
        tokens = tweets[tweetname]
        for w in tokens:
            alpha += words[w]
        alpha += b
        if ((y * alpha) <= 0):
            for w in tokens:
                words[w] *= y
            b += y


# nested dictionary
main_dict["word_weights"] = words
main_dict["bias"] = b

# store it in a file
pickle.dump(main_dict, open("bw_model.txt","wb"))
