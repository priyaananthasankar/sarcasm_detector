import re,string,os
import csv,sys
import collections

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def extract_hash_tags(s):
	return set(part[1:] for part in s.split() if part.startswith('#'))
def extract_user_tags(s):
        return set(part[1:] for part in s.split() if part.startswith('@'))

tweets_list = []
fd = open(sys.argv[2],'w')
csv_writer = csv.writer(fd, delimiter=',',quoting=csv.QUOTE_ALL)

with open(sys.argv[1], 'rb') as csvfile:
	tweets = csv.reader(csvfile)
	for row in tweets:
		tweets_list.append(row)
		#print row[0]
	

tests = [
    "@peter I really love that shirt at #Macy. http://bet.ly//WjdiW4",
    "@shawn Titanic tragedy could have been prevented Economic Times: Telegraph.co.ukTitanic tragedy could have been preve... http://bet.ly/tuN2wx",
    "I am at Starbucks http://4sh.com/samqUI (7419 3rd ave, at 75th, Brooklyn)",
]
for t in tweets_list:
	sub_list = []
	label_list = []
	sub_list.append(t[0])
	text = strip_all_entities(strip_links(t[0]))
	sub_list.append(text)

	hash_tags = extract_hash_tags(t[0])
	users = extract_user_tags(t[0])

	hash_tag_string = ""
	user_string = " "

	for hash_tag in hash_tags:
		hash_tag_string += hash_tag + " "
	sub_list.append(hash_tag_string)

	for user in users:
		user_string += user + " "
	sub_list.append(user_string)

	sub_list.append(len(t[0]))
	"""label_list.append(t[1].lower())
	label_list.append(t[2].lower())
	label_list.append(t[3].lower())
	counter=collections.Counter(label_list)
	if counter['yes'] > counter['no']:
		sub_list.append('S')
	else :
		sub_list.append('NS')"""
	sub_list.append('S')
	csv_writer.writerow(sub_list)
