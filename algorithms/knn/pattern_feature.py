from collections import defaultdict
import sys
import csv
import algorithms.knn as k
tweets=[]
pattern=[]


freq_words = defaultdict(str)
classify_dir = sys.argv[1]
test_dir = sys.argv[2]

fin = open(classify_dir, "rt")
import sys

max = 0

def count(dir_name):
    words_dict = defaultdict(int)
    max = 0
    tweets = []
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for tweet, test, hashtag, user, length, sarc in reader:
            cleaned_tweet = k.clean_tweet_wo_punc(tweet)
            tweets.append(tweet)
            for w in cleaned_tweet.split():
                words_dict[w] += 1
                if max < words_dict[w]:
                    max = words_dict[w]
    cd


for line in fin:
    t = line.split(",")
    tweets.append(t[0])
    for w in t[0].split(" "):
        count_words[w] += 1
        if (count_words[w] > max):
            max = count_words[w]


threshold = max / 10


print(count_words)

words = count_words.keys()
for w in words:
    if (count_words[w] >= threshold):
        freq_words[w] = "a"
    else:
        freq_words[w] = "b"


print(freq_words)

patterns = defaultdict(int)
pattern_arr = []

for t in tweets[1:10]:
    pat = ""
    print(t)
    for w in t.split(" "):
        #print("hi"+freq_words[w])
        pat = pat + freq_words[w]
    print(pat)
    pattern.append(pat)
    #rint(freq_words[w])
    #attern.append(pat)


#print(pattern)










