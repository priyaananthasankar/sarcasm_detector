
import csv
import algorithms.knn.tfidf1 as ti
#in Scikit-Learn

#sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=False, sublinear_tf=True, tokenizer=tokenize)
#sklearn_representation = sklearn_tfidf.fit_transform(all_documents)
print("hi")
#fin = open("/home/ninja/sarcasm_detector/corpus/final_tweets.csv", "rt")
import sys

max = 0

tweets = []
feature1 = []
feature2 = []

fout = open('f1.txt','w')
fout = open('f2.txt','w')

with open('/home/ninja/sarcasm_detector/data/training_tweets.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for tweet, test, hashtag, user, length, sarc in reader:
        tweets.append(tweet)
        feature2.append(len(tweet))


feature1 = ti.tfidf(tweets)
print(len(tweets))
for f in feature1:
    fout.write(str(f)+"\n")
