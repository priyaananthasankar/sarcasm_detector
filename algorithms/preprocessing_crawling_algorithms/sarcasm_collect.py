import tweepy
import json
import csv
import sys
from tweepy import OAuthHandler
 
consumer_key = '<enter your consumer key>'
consumer_secret = '<enter your consumer secret>'
access_token = '<enter your access token>'
access_secret = '<enter your access secret>'
 
#def process_or_store(tweet):
#    print json.dumps(tweet)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
f = open(sys.argv[1], 'wt')
writer = csv.writer(f)
for status in tweepy.Cursor(api.search, q='#sarcasm',lang="en").items(100):
	writer.writerow([status.text.encode("utf-8")]) 


