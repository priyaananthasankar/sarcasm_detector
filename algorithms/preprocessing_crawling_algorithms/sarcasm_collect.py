import tweepy
import json
import csv
import sys
from tweepy import OAuthHandler
 
consumer_key = 'YJY4dHW1CKjZAWLpl4IbmpPUM'
consumer_secret = 'dZLTYfNwfYdahzmHYVsIyAOluRG2T6n0wd84xQvNpxZJnXjHsk'
access_token = '34634614-Fztsrk8J7aBN2E3ON4QQwkH6DoL2yqHQ9gLpoCYY1'
access_secret = 'wUEY47V6eJlhvkk7bnJkTE7WxZigx7hJJh9bvhPmcNC7h'
 
#def process_or_store(tweet):
#    print json.dumps(tweet)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
f = open(sys.argv[1], 'wt')
writer = csv.writer(f)
for status in tweepy.Cursor(api.search, q='#sarcasm',lang="en").items(100):
	writer.writerow([status.text.encode("utf-8")]) 


