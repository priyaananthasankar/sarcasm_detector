# Author: Priya Ananthasankar
# Year: 2016
# Description: Maximum Entropy Classifier for Sarcasm Classification using NLTK + MegaM
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

train_data = sys.argv[1]
test_data = sys.argv[2]

print (sys.path)

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



def feature_set_generator(original_tweet,text,hashtags,users,length,label):
    features = {}
    words = text.split()
    pos = nltk.word_tokenize(text)
    # Bag of words
    features["words"] = tuple((word,True) for word in words)
    # Length
    features["length"] = length
    # Hashtags
    features["hashtags"] = hashtags
    set_of_pos_tags = nltk.pos_tag(pos)

    # Part of speech tagging
    features["pos"] = tuple(t for t in set_of_pos_tags)

    features["polarity"] = polarity.get_polarity_per_tweet(text)

    return features

me_classifier = 0
with open(train_data, 'r',encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile)
    feature_set = [(feature_set_generator(original_tweet,text,hashtags,users,length,label),label) for original_tweet,text,hashtags,users,length,label in reader]
    #print(feature_set)
    me_classifier = MaxentClassifier.train(feature_set,"megam")

with open(test_data,'r',encoding='utf-8', errors='ignore') as testcsvfile:
    test_reader = csv.reader(testcsvfile)
    test_feature_set = [(feature_set_generator(original_tweet,text,hashtags,users,length,label),label) for original_tweet,text,hashtags,users,length,label in test_reader]
    print("Accuracy: " ,classify.accuracy(me_classifier, test_feature_set))

classified = collections.defaultdict(set)
observed = collections.defaultdict(set)
i=1
with open(test_data,'r',encoding='utf-8', errors='ignore') as testcsvfile:
    test_reader = csv.reader(testcsvfile)
    for original_tweet,text,hashtags,users,length,label in test_reader:
        observed[label].add(i)
        classified[me_classifier.classify(feature_set_generator(original_tweet,text,hashtags,users,length,label))].add(i)
        i+=1


print('Sarcasm precision:', precision(observed["S"], classified["S"]))
print('Sarcasm recall:', recall(observed['S'], classified['S']))
print('Sarcasm F-measure:', f_measure(observed['S'], classified['S']))
print('Not Sarcasm precision:',precision(observed['NS'], classified['NS']))
print('Not Sarcasm recall:', recall(observed['S'], classified['NS']))
print('Not Sarcasm F-measure:', f_measure(observed['S'], classified['NS']))
