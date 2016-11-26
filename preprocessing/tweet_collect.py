import tweepy
import json
import csv
import sys
import re
from tweepy import OAuthHandler
 
consumer_key = 'keiKqTJjSuWIPZl0FJQXQK8OE'
consumer_secret = 'eVnNYSdx8cfwZh2Avms1OJTCR3t78hR5PgNITOwFARVXetrSbq'
access_token = '79692412-rXYTuU1ah2sHi2t4lTLYp4LQVECu4QX749JedO3f7'
access_secret = 'L6qj68O4kXQxiAr80PZgWhSnAQDCYqxZF9pION3kSjqKP'
 
def process_or_store(tweet):
    print json.dumps(tweet)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
f = open(sys.argv[1], 'wt')
writer = csv.writer(f)
for tweet in tweepy.Cursor(api.search, q='#politicalSarcasm',lang="en").items(400):
	if (not tweet.retweeted) and ('RT @' not in tweet.text):
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.text)
		if (len(urls) == 0):
			writer.writerow([tweet.text.encode("utf-8")]) 


