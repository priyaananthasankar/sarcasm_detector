


import os
import pickle
from collections import defaultdict
import sys
import csv



# defining dictionary
main_dict = pickle.load(open("bw_model.txt", "rb"))
words = main_dict["word_weights"]
bias = main_dict["bias"]

cal_sar_cnt = 0
cal_nonsar_cnt = 0
act_sar_cnt = 0
act_nonsar_cnt = 0

match = 0
mismatch = 0
sar_match = 0
nonsar_match = 0


tweets = defaultdict(int)



with open('cleaned_tweets_test.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    count = 0
    tweetnum = ""
    for tweet, sarcastic in reader:
        tokens = tweet.split()
        alpha = 0
        for w in tokens:
            if w in words:
                alpha += words[w]
        alpha += bias
        isSar = 0
        if (alpha > 0):
            cal_sar_cnt += 1
            isSar += 1
        else:
            cal_nonsar_cnt += 1

        if sarcastic == "yes":
            act_sar_cnt += 1
            if isSar == 1:
                match += 1
                sar_match += 1
            else:
                mismatch += 1
        else:
            act_nonsar_cnt += 1
            if isSar == 0:
                match += 1
                nonsar_match += 1
            else:
                mismatch += 1


# calculations
print ("Calculated Sar  : "+str(cal_sar_cnt))
print ("Calculated NonSar : "+str(cal_nonsar_cnt))
print ("Actual Sar : "+str(act_sar_cnt))
print ("Actual NonSar : "+str(act_nonsar_cnt))
print ("Match : "+str(match))
print ("Mismatch : "+str(mismatch))


pre_sar = sar_match*100/cal_sar_cnt
print("Nonsar Precision : "+str(pre_sar))
recall_sar = sar_match*100/act_sar_cnt
print("Nonsar Recall : "+str(recall_sar))
f1_sar = (2 * pre_sar * recall_sar) / (pre_sar + recall_sar)
print("Nonsar F1 score : "+str(f1_sar))

pre_nonsar = nonsar_match*100/cal_nonsar_cnt
print("Sar Precision : "+str(pre_nonsar))
recall_nonsar = nonsar_match*100/act_nonsar_cnt
print("Sar Recall : "+str(recall_nonsar))
f1_nonsar = (2 * pre_nonsar * recall_nonsar) / (pre_nonsar + recall_nonsar)
print("Sar F1 Score : "+str(f1_nonsar))

accuracy = match*100/(act_sar_cnt+act_nonsar_cnt)
print("Accuracy : "+str(accuracy))
