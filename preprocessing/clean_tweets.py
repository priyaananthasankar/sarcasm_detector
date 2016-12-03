import re
import string
import csv

fc = open("cleaned_tweets_classify.csv", 'wt')
ft = open("cleaned_tweets_test.csv", 'wt')
sarcasm_writer_class = csv.writer(fc)
sarcasm_writer_test = csv.writer(ft)
#Niranjana Kandavel
#To clean tweets

def remove_urls (vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", vTEXT, flags=re.MULTILINE)
    vTEXT = re.sub(r"([@])(\w+)\b", "", vTEXT, flags=re.MULTILINE)
    vTEXT = "".join(l for l in vTEXT if l not in string.punctuation)
    return(vTEXT)

count_yes = 0
count_no = 0
tot_count = 0

with open('sar_tweets.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for tweet, r1, r2, r3 in reader:
        score = 0
        sarcastic = ""
        csv_row = []
        if tweet and r1 and r2 and r3:
            if (r1.lower() == "yes"):
                score += 1
            if (r2.lower() == "yes"):
                score += 1
            if (r3.lower() == "yes"):
                score += 1
            if (score >= 2):
                sarcastic = "yes"
                count_yes += 1
            else:
                sarcastic = "no"
                count_no += 1
            tot_count += 1
            if tot_count <= 200:
                sarcasm_writer_test.writerow([remove_urls(tweet),sarcastic])
            else:
                sarcasm_writer_class.writerow([remove_urls(tweet),sarcastic])

print(count_yes)
print(count_no)
