import re
import string
import csv
import algorithms.knn.tfidf1 as ti




def remove_urls_wo_punc (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", vTEXT, flags=re.MULTILINE)
    vTEXT = re.sub(r"([@])(\w+)\b", "", vTEXT, flags=re.MULTILINE)
    return(vTEXT)

def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", vTEXT, flags=re.MULTILINE)
    vTEXT = re.sub(r"([@])(\w+)\b", "", vTEXT, flags=re.MULTILINE)
    vTEXT = "".join(l for l in vTEXT if l not in string.punctuation)
    return(vTEXT)

classify_dir = '/home/ninja/sarcasm_detector/data/training_tweets.csv'
test_dir = '/home/ninja/sarcasm_detector/data/testing_tweets.csv'



def makeseq(dir_name):
    x_seq = []
    y_seq = []
    tweets = []
    token_count = []
    c = 0
    max = 0
    with open(dir_name, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for tweet, test, hashtag, user, length, sarc in reader:
            cleaned_tweet = remove_urls(tweet)
            cleaned_tweet_punc = remove_urls_wo_punc(tweet)
            sub_seq = []
            if c == 0:
                c += 1
                continue
            else:
                tweets.append(cleaned_tweet)
                sub_seq.append(len(cleaned_tweet))

                count_punc = sum((not c.isdigit() and not c.isalpha()) for c in cleaned_tweet_punc)
                count_capital = sum((c.isupper()) for c in cleaned_tweet_punc)
                count_s = count_punc+count_capital
                words = cleaned_tweet.split()
                token_count.append(len(words))
                if max < len(words):
                    max = len(words)


                x_seq.append(sub_seq)

                if sarc == "S":
                    y_seq.append(1)
                else:
                    y_seq.append(0)
                c += 1
    feature1 = ti.tfidf(tweets)
    print(len(tweets))
    i = 0
    for f in feature1:
        x_seq[i].append(token_count[i]/max)
        x_seq[i].append(f)
        i += 1
    return x_seq, y_seq




x_seq, y_seq = makeseq(classify_dir)

print(y_seq)
print(x_seq)

test_x_seq, test_y_seq = makeseq(test_dir)

print(test_x_seq)
print(test_y_seq)



from sklearn.neighbors import KNeighborsClassifier
neigh = KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
           metric_params=None, n_jobs=1, n_neighbors=5, p=2,
           weights='uniform')
neigh.fit(x_seq, y_seq)
op = neigh.predict(test_x_seq)

k = 0
match = 0
mismatch = 0

for val in op:
    if val == test_y_seq[k]:
        match += 1
    else:
        mismatch += 1
    k += 1

acc = match/(match+mismatch)
print(acc)


