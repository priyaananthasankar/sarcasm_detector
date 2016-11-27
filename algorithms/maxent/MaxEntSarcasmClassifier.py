"""
USC Computer Science 544: Applied Natural Language Processing

File name   : MaxEntSarcasmClassifier.py
Usage       : python3 MaxEntSarcasmClassifier.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : A Maximum Entropy Sarcasm Classifier using NLTK + MegaM library
"""
__author__  = "Priya Ananthasankar"
__email__   = "panantha@usc.edu"
__credits__ = ["Ravi Kiran Chadalawada","Niranjana Kandavel"]
__status__  = "Prototype"

import sys
sys.path.append('../polarity/')
import nltk
import nltk.data
from nltk.metrics.scores import   (accuracy, precision, recall, f_measure,
                                          log_likelihood, approxrand)
from nltk import precision
import random
from nltk import classify
from nltk.classify import MaxentClassifier
from nltk.classify.megam import call_megam, write_megam_file, parse_megam_weights
from nltk.corpus import names
import collections,re
import csv
import PolarityClassifier as polarity
import json

train_data = sys.argv[1]
test_data = sys.argv[2]

# Sample using Gender Features
#names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
#random.shuffle(names)
#def gender_features3(name):
#    features = {}
#    features["fl"] = name[0].lower()
#    features["ll"] = name[-1].lower()
#    features["fw"] = name[:2].lower()
#    features["lw"] = name[-2:].lower()
#    return features

#featuresets = [(gender_features3(n), g) for (n, g) in names]
#train_set,test_set = featuresets[500:],featuresets[:500]
#me_classifier = MaxentClassifier.train(train_set,"megam")

#print(me_classifier.classify(gender_features3('Gary')))
#print(me_classifier.classify(gender_features3('Niranjana')))
nltk.data.load('nltk:tokenizers/punkt/english.pickle')

onomatopoeia = ["bang","bark", "bash", "beep", "biff", "blah", "blare", "blat", "bleep",
                "blip","boo", "boom", "bump", "burr", "buzz", "caw","chink", "chuck",
                "clang", "clank", "clap", "clatter", "click", "cluck", "coo", "crackle", "crash",
                "creak", "cuckoo", "ding", "dong", "fizz", "flump", "gabble", "gurgle" ,"hiss",
                "honk", "hoot" ,"huff", "hum", "hush" ,"meow", "moo", "murmur", "pitapat",
                "plunk", "pluck" ,"pop" ,"purr", "ring", "rip" ,"roar", "rustle" ,"screech"
                "scrunch", "sizzle", "splash", "splat", "squeak", "tap-tap", "thud", "thump", "thwack",
                "tick", "ting", "toot", "twang", "tweet", "whack", "wham", "wheeze", "whiff",
                "whip", "whir", "whiz", "whomp" ,"whoop" ,"whoosh" ,"wow" ,"yak", "yawp",
                "yip", "yowl" ,"zap", "zing", "zip", "zoom"]


all_features = ["words","length","hashtag","pos","interjection","onomatopoeia","polarity","question"]
metrics = {
            
          }
def feature_set_generator(original_tweet,text,hashtags,users,length,label, include_list):
    features = {}
    words = text.split()

    if not include_list:
        include_list = all_features

    # Bag of words
    if("words" in include_list):
        features["words"] = tuple((word,True) for word in words)

    # Length
    if("length" in include_list):
        features["length"] = length

    # Hash tags
    if("hashtag" in include_list):
        features["hashtags"] = hashtags

    # Part of speech tagging
    pos = nltk.word_tokenize(text)
    if("pos" in include_list):
        set_of_pos_tags = nltk.pos_tag(pos)
        features["pos"] = tuple(t for t in set_of_pos_tags)


    # Interjections - SUBSTANTIAL INCREASE IN ACCURACY
    if("interjection" in include_list):
        set_of_pos_tags = nltk.pos_tag(pos)
        interjection_tags = 0
        for tag in set_of_pos_tags:
            if tag == "UH":
                interjection_tags += 1
        features["interjection"] = interjection_tags

    # Onomatopoeia - SUBSTANTIAL DROP IN ACCURACY
    if("onomatopoeia" in include_list):
        onomatopoeia_count = 0
        for text in words:
            if text in onomatopoeia:
                onomatopoeia_count += 1
        features["onomatopoeia"] = onomatopoeia_count

    if("question" in include_list):
        question_count = 0
        for text in words:
            if "?" in text:
                question_count += 1
        features["question"] = question_count

    # Polarity of text - SUBSTANTIAL INCREASE IN ACCURACY
    if("polarity" in include_list):
        features["polarity"] = polarity.get_polarity_per_tweet(text)

    return features

def me_classifier(exclude_list):
    me_classifier = 0

    with open(train_data, 'r',encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        feature_set = [(feature_set_generator(original_tweet,text,hashtags,users,length,label,exclude_list),label) for original_tweet,text,hashtags,users,length,label in reader]
        #print(feature_set)
        me_classifier = MaxentClassifier.train(feature_set,"megam")

    accuracy = 0.0
    with open(test_data,'r',encoding='utf-8', errors='ignore') as testcsvfile:
        test_reader = csv.reader(testcsvfile)
        test_feature_set = [(feature_set_generator(original_tweet,text,hashtags,users,length,label,exclude_list),label) for original_tweet,text,hashtags,users,length,label in test_reader]
        accuracy = classify.accuracy(me_classifier, test_feature_set)

    classified = collections.defaultdict(set)
    observed = collections.defaultdict(set)
    i=1
    with open(test_data,'r',encoding='utf-8', errors='ignore') as testcsvfile:
        test_reader = csv.reader(testcsvfile)
        for original_tweet,text,hashtags,users,length,label in test_reader:
            observed[label].add(i)
            classified[me_classifier.classify(feature_set_generator(original_tweet,text,hashtags,users,length,label,exclude_list))].add(i)
            i+=1

    return accuracy,precision(observed["S"], classified["S"]),recall(observed['S'], classified['S']),\
           f_measure(observed['S'], classified['S']),precision(observed['NS'], classified['NS']),recall(observed['S'], classified['NS']),f_measure(observed['S'], classified['NS'])


def print_stats(a,ps,rs,fs,pns,rns,fns):
    print()
    print("****************** MAX ENTROPY STATISTICS******************************")
    print('Accuracy:', a)
    print('Sarcasm precision:', ps)
    print('Sarcasm recall:', rs)
    print('Sarcasm F-measure:', fs)
    print('Not Sarcasm precision:',pns)
    print('Not Sarcasm recall:', rns)
    print('Not Sarcasm F-measure:', fns)
    print("***********************************************************************")


def prepare_dict(dict,a,ps,rs,fs,pns,rns,fns):
    dict = {}
    dict["title"] = "Maximum Entropy with all features"
    dict["accuracy"] = a
    dict["sarcasm_precision"] = ps
    dict["sarcasm_recall"] = rs
    dict["sarcasm_f_measure"] = fs
    dict["not_sarcasm_precision"] = pns
    dict["not_sarcasm_recall"] = rns
    dict["not_sarcasm_f_measure"] = fns
    return dict

a,ps,rs,fs,pns,rns,fns = me_classifier([])
max_ent_with_all_features = {}
metrics["max_ent_with_all_features"]=prepare_dict(max_ent_with_all_features,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

a,ps,rs,fs,pns,rns,fns = me_classifier(["pos"])
max_ent_with_only_pos = {}
metrics["max_ent_with_only_pos"]=prepare_dict(max_ent_with_only_pos,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

a,ps,rs,fs,pns,rns,fns = me_classifier(["polarity"])
max_ent_with_only_polarity = {}
metrics["max_ent_with_only_polarity"]=prepare_dict(max_ent_with_only_polarity,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

a,ps,rs,fs,pns,rns,fns = me_classifier(["interjection"])
max_ent_with_only_interjection = {}
metrics["max_ent_with_only_interjection"]=prepare_dict(max_ent_with_only_interjection,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

a,ps,rs,fs,pns,rns,fns = me_classifier(["words","length","hashtag","pos","interjection","polarity"])
max_ent_without_onamatopoeia_and_question = {}
metrics["max_ent_without_onamatopoeia_and_question"]=prepare_dict(max_ent_without_onamatopoeia_and_question,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

a,ps,rs,fs,pns,rns,fns = me_classifier(["question","length","interjection"])
max_ent_with_question_length_interjection = {}
metrics["max_ent_with_question_length_interjection"]=prepare_dict(max_ent_with_question_length_interjection,a,ps,rs,fs,pns,rns,fns)
print_stats(a,ps,rs,fs,pns,rns,fns)

json_data = json.dumps(metrics)
output_json = open('metrics.json','w')
output_json.write(json_data)
output_json.close()




