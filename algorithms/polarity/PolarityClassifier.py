"""
USC Computer Science 544: Applied Natural Language Processing

File name   : PolarityClassifier.py
Usage       : python PolarityClassifier.py ../../data/combined.csv ../../data/training_tweets.csv
Description : This file calculates the polarity of a  sentence.
              For a sarcastic sentence, we need to calculate a situational or contextual polarity/
              alongwith a seed word polarity. If contrasting polarities are found then the tweet
              is tagged as sarcastics
"""
__author__  = "Priya Ananthasankar"
__email__   = "panantha@usc.edu"
__credits__ = ["Ravi Kiran Chadalawada","Niranjana Kandavel"]
__status__  = "Prototype"

import sys
import csv
from nltk import ngrams
import collections
from nltk.metrics.scores import   (accuracy, precision, recall, f_measure,
                                          log_likelihood, approxrand)
from nltk import precision
from textblob import TextBlob
from nltk.corpus import opinion_lexicon as lexicon
import json

combined_data = sys.argv[1]
train_data = sys.argv[2]

positive_words = []
negative_words = []


sp = 0
sn =0
nsp = 0
nsn = 0

classified = collections.defaultdict(set)
observed = collections.defaultdict(set)
correct_tags = 0
incorrect_tags = 0

# get all the words from Opinion Lexicon of Liu
for positive in lexicon.positive():
    positive_words.append(positive)
for negative in lexicon.negative():
    negative_words.append(negative)

feature_set = {}

def polarizer(dir):
    with open(dir, 'r',encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        global correct_tags, incorrect_tags
        for original_tweet,text,hashtags,users,length,label in reader:
            feature_set[text] = TextBlob(text).sentiment.polarity
            words = text.split()
            seed_word = ""
            isSeedWordPositive = False

            # find a seed word which represents the positivity/negativity of the sentence
            # Then find the prefix and suffix of the seed word as bigrams.
            for word in words:
                if word in positive_words:
                    seed_word = word
                    isSeedWordPositive = True
                    prefix_suffix = text.partition(seed_word)
                    break
                elif word in negative_words:
                    seed_word = word
                    prefix_suffix = text.partition(seed_word)
                    break

            if seed_word:
                if isSeedWordPositive:
                    prefix = prefix_suffix[0]
                    suffix = prefix_suffix[2]
                else:
                    prefix = prefix_suffix[0]
                    suffix = prefix_suffix[2]

                bi_gram_prefix = ngrams(prefix.split(), 2)
                bi_gram_suffix = ngrams(suffix.split(), 2)

                pol_prefix = 0.0
                pol_suffix = 0.0

                # for each prefix and suffix, find out sentiments of individual bi grams
                for bg in bi_gram_prefix:
                    blob = TextBlob(" ".join(bg))
                    pol_prefix += blob.sentiment.polarity

                for bg in bi_gram_suffix:
                    blob = TextBlob(" ".join(bg))
                    pol_suffix += blob.sentiment.polarity

                # add all the bigram sentiments and test for contrasting polarities

                # if you got a positive seed word, then take all the bigram prefix and suffix-
                # look for a negative score

                # if you got a negative seed, then take all the bigram prefix and suffix -
                # look for a positive score

                if (pol_prefix + pol_suffix) > 0 and isSeedWordPositive == False:
                    c_label = "S"
                elif (pol_prefix + pol_suffix) < 0 and isSeedWordPositive:
                    c_label = "S"
                else:
                    c_label = "NS"

            else:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity

                if polarity < 0 :
                    c_label = "S"
                else:
                    c_label = "NS"

            observed[label].add(i)
            classified[c_label].add(i)
            if c_label == label:
                correct_tags += 1
            else:
                incorrect_tags += 1

            i += 1



def generate_polarity_feature_set(dir):
    with open(dir, 'r',encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        for original_tweet,text,hashtags,users,length,label in reader:
            feature_set[text] = TextBlob(text).sentiment.polarity
    return feature_set

def get_polarity_per_tweet(tweet):
    return TextBlob(tweet).sentiment.polarity

def get_polarity_feature_set():
    return feature_set


polarizer(combined_data)

metrics = {}

polarity_for_sarcasm = {}
polarity_for_sarcasm["accuracy"] = correct_tags/(correct_tags + incorrect_tags)
polarity_for_sarcasm["sarcasm_precision"] = precision(observed["S"], classified["S"])
polarity_for_sarcasm["sarcasm_recall"] = recall(observed['S'], classified['S'])
polarity_for_sarcasm["sarcasm_f_measure"] = f_measure(observed['S'], classified['S'])
polarity_for_sarcasm["not_sarcasm_precision"] = precision(observed['NS'], classified['NS'])
polarity_for_sarcasm["not_sarcasm_recall"] = recall(observed['S'], classified['NS'])
polarity_for_sarcasm["not_sarcasm_f_measure"] = f_measure(observed['S'], classified['NS'])

metrics["polarity_for_sarcasm"] = polarity_for_sarcasm

json_data = json.dumps(metrics)
output_json = open('metrics.json','w')
output_json.write(json_data)
output_json.close()


def get_json_data():
    return json_data


