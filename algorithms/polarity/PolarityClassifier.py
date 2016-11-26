import nltk
import sys
import csv
from nltk import ngrams
import collections
from nltk.metrics.scores import   (accuracy, precision, recall, f_measure,
                                          log_likelihood, approxrand)
from nltk import precision
from textblob import TextBlob

train_data = sys.argv[1]

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


classified = collections.defaultdict(set)
observed = collections.defaultdict(set)
correct_tags = 0
incorrect_tags = 0

def polarizer(dir):
    with open(dir, 'r',encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        global correct_tags, incorrect_tags
        for original_tweet,text,hashtags,users,length,label in reader:
            words = text.split()
            seed_word = ""
            isSeedWordPositive = False

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
                    # if you got a positive seed word, then take all the bigram prefix and suffix- look for a negative score
                    prefix = prefix_suffix[0]
                    suffix = prefix_suffix[2]
                else:
                    # if you got a negative seed, then take all the bigram prefix and suffix - look for a positive score
                    prefix = prefix_suffix[0]
                    suffix = prefix_suffix[2]

                bi_gram_prefix = ngrams(prefix.split(), 2)
                bi_gram_suffix = ngrams(suffix.split(), 2)

                pol_prefix = 0.0
                pol_suffix = 0.0

                for bg in bi_gram_prefix:
                    blob = TextBlob(" ".join(bg))
                    pol_prefix += blob.sentiment.polarity

                for bg in bi_gram_suffix:
                    blob = TextBlob(" ".join(bg))
                    pol_suffix += blob.sentiment.polarity

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
                #print("POLARITY_PREFIX: ", pol_prefix)
                #print("POLARITY_SUFFIX: ", pol_suffix)
                #print("SEED WORD:",seed_word, "POLARITY", isSeedWordPositive)
                #print("PREFIX:",prefix)
                #print("SUFFIX:",suffix)

polarizer(train_data)

print("Accuracy: ", correct_tags/(correct_tags + incorrect_tags))
print('Sarcasm precision:', precision(observed["S"], classified["S"]))
print('Sarcasm recall:', recall(observed['S'], classified['S']))
print('Sarcasm F-measure:', f_measure(observed['S'], classified['S']))
print('Not Sarcasm precision:',precision(observed['NS'], classified['NS']))
print('Not Sarcasm recall:', recall(observed['S'], classified['NS']))
print('Not Sarcasm F-measure:', f_measure(observed['S'], classified['NS']))