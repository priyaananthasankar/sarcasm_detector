import sys
import csv
from nltk import ngrams
import collections
from nltk.metrics.scores import   (accuracy, precision, recall, f_measure,
                                          log_likelihood, approxrand)
from nltk import precision
from textblob import TextBlob
from nltk.corpus import opinion_lexicon as lexicon

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

print("******************POLARIZER STATISTICS******************************")
print("Accuracy: ", correct_tags/(correct_tags + incorrect_tags))
print('Sarcasm precision:', precision(observed["S"], classified["S"]))
print('Sarcasm recall:', recall(observed['S'], classified['S']))
print('Sarcasm F-measure:', f_measure(observed['S'], classified['S']))
print('Not Sarcasm precision:',precision(observed['NS'], classified['NS']))
print('Not Sarcasm recall:', recall(observed['S'], classified['NS']))
print('Not Sarcasm F-measure:', f_measure(observed['S'], classified['NS']))
print("********************************************************************")
