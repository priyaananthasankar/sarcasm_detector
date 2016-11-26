"""
USC Computer Science 544: Applied Natural Language Processing

File name   : scikit_nb.py 
Usage       : python scikit_nb.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : This file used multivariate Naive bayes algorithm to train and test classifier 
	      to detect sarcasm in tweets.We crawled and annotated 3000 tweets to get this 
	      data set.Training and Testing data can be found under data folder at root of 
	      repository.

"""
__author__  = "Ravi Kiran Chadalawada"
__email__   = "rchadala@usc.edu"
__credits__ = ["Priya Ananthasankar","Niranjana Kandavel"]
__status__  = "Prototype"


import sys,csv,json
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import numpy as np

vec = DictVectorizer()
data_list_dict =[]
total_labels = []
metrics_list ={}


def read_tweets_to_list(file_name):
	fd = open(file_name,'r')
	csv_reader = csv.reader(fd)
	for row in csv_reader:
		data_dict = {'tweet':None, 'length':None}
		#print row
		data_dict['tweet'] = row[0]
		data_dict['length'] = row[4]
		data_list_dict.append(data_dict)
		if row[5] == 'S':
			total_labels.append(1)
		else :
			total_labels.append(-1)
		#print row[0] + " " + row[4] + " " + row[5]

	return

def list_to_features(data_list_dict):
	x_features = [];
	x_features = vec.fit_transform(data_list_dict).toarray()
        #print x_features
        #print vec.get_feature_names()
	return x_features;


def train_svm(clf,training_features,training_labels):
	clf.fit(training_features, training_labels)
	return


def test_svm(clf,testing_features,actual_labels,feature_instance):
	
	predicted_labels = []
	metrics = {}
	temp_dict = {}

	for feature_set in testing_features:
		predicted_labels.extend(clf.predict([feature_set]))
	#print predicted_labels
	accuracy = accuracy_score(actual_labels,predicted_labels)
	metrics_array = precision_recall_fscore_support(actual_labels,predicted_labels, average=None, labels=['1','-1'])
	
	if feature_instance == 1:
		metrics['title'] = 'MultinomialNB'
		temp_dict['multinomialnb'] = metrics
	elif feature_instance == 2:
		metrics['title'] = 'BernoulliNB'
		temp_dict['BernoulliNB'] = metrics
	else:
		metrics['title'] = ' GaussianNB'
		temp_dict['gaussiannb'] = metrics

	metrics["accuracy"] = accuracy
	metrics["sarcasm_precision"] = metrics_array[0][0]
	metrics["sarcasm_recall"] = metrics_array[1][0]
	metrics["sarcasm_f_measure"] = metrics_array[2][0]
	metrics["not_sarcasm_precision"] = metrics_array[0][1]
	metrics["not_sarcasm_recall"] = metrics_array[1][1]
	metrics["not_sarcasm_f_measure"] = metrics_array[2][1]

	metrics_list.update(temp_dict)
	return


if __name__ == '__main__':
	read_tweets_to_list(sys.argv[1])
	read_tweets_to_list(sys.argv[2])
	total_features = list_to_features(data_list_dict)
	#print len(total_features[0])
	
	training_features = total_features[:2250]
	training_labels = total_labels[:2250]
	testing_features = total_features[2250:]
	testing_labels = total_labels[2250:]

	clf = MultinomialNB()
	train_svm(clf,training_features,training_labels)	
	test_svm(clf,testing_features,testing_labels,1)
	
	clf = BernoulliNB()
	train_svm(clf,training_features,training_labels)
	test_svm(clf,testing_features,testing_labels,2)

	clf = GaussianNB()
	train_svm(clf,training_features,training_labels)
	test_svm(clf,testing_features,testing_labels,3)
	
	print("\n\n")
	json_data = json.dumps(metrics_list)
	fd = open("metrics.json","w")
	fd.write(json_data)
	fd.close
	print(json_data)
