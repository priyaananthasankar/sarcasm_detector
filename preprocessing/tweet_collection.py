#Niranjana Kandavel
#To collect tweets using tweepy
import tweepy
import json
import csv
import sys
from tweepy import OAuthHandler

consumer_key = '2jWw8XLpvmL0kwno1RZnvx37h'
consumer_secret = 'ylHmLFd3e9YXJ67LnCWI8JkWlGESoswsdJ2SYVnLXpn8IxF9Us'
access_token = '783495370835832832-WjjbpKmwahAsyJ13C1iFyUjz49Msafm'
access_secret = 'kaL1Hm2GD3rvYfQp2ZhUyQyk2OvrhMIbGFKbDOANp2hc0'


def process_or_store(tweet):
    print(json.dumps(tweet))


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
f = open(sys.argv[1], 'wt')
writer = csv.writer(f)
for status in tweepy.Cursor(api.search, q='#sarcasm AND #politics', lang="en").items(400):
    writer.writerow([status.text.encode("utf-8")])