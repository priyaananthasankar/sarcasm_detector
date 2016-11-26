"""
USC Computer Science 544: Applied Natural Language Processing

File name   : scikit_svm.py 
Usage       : python scikit_svm.py ../../data/training_tweets.csv ../../data/testing_tweets.csv
Description : This file used linear SVM algorithm to train and test classifier to detect sarcasm
	      in tweets.We crawled and annotated 3000 tweets to get this data set.Training and 
	      Testing data can be found under data folder at root of repository.

"""
__author__  = "Ravi Kiran Chadalawada"
__email__   = "rchadala@usc.edu"
__credits__ = ["Priya Ananthasankar","Niranjana Kandavel"]
__status__  = "Prototype"



import sys,csv,json
sys.path.append('../polarity/')
from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
from PolarityClassifier import get_polarity_per_tweet
import nltk 
import numpy as np
from sklearn import preprocessing

vec = DictVectorizer()
clf = svm.LinearSVC()
metrics_list ={}

def read_tweets_to_list(file_name,data_list_dict,total_labels,feature_set):
	fd = open(file_name,'r')
	csv_reader = csv.reader(fd)

	for row in csv_reader:
		interjection = 0;
		data_dict = {'tweet':None, 'length':None}

		data_dict['tweet'] = row[0]
		data_dict['length'] = row[4]

		if 'interjection' in feature_set:
			tokens = nltk.word_tokenize(row[0])
			pos_tuple = nltk.pos_tag(tokens)
			for pos in pos_tuple:
				word,ptag = pos
				if ptag == 'UH':
					interjection += 1
			data_dict['interjection'] = interjection

		if 'polarity' in feature_set:
			data_dict['ploarity'] = get_polarity_per_tweet(row[1])

		data_list_dict.append(data_dict)
		if row[5] == 'S':
			total_labels.append(1)
		else :
			total_labels.append(-1)
		#print(data_list_dict)
	fd.close()
	return

def list_to_features(data_list_dict):
	x_features = [];
	x_features = vec.fit_transform(data_list_dict).toarray()
        #print vec.get_feature_names()
	return x_features;


def train_svm(training_features,training_labels):
	clf.fit(training_features, training_labels)
	return


def test_svm(testing_features,actual_labels,feature_instance):
	
	predicted_labels = []
	metrics = {}
	temp_dict = {}

	for feature_set in testing_features:
		predicted_labels.extend(clf.predict([feature_set]))

	#print(len(predicted_labels))
	#print(len(actual_labels))
	accuracy = accuracy_score(actual_labels,predicted_labels)
	metrics_array = precision_recall_fscore_support(actual_labels,predicted_labels, average=None, labels=['1','-1'])
	#print(metrics_array)
	
	if feature_instance == 1:
		metrics['title'] = 'SVM with only tweet and length'
		temp_dict['svm_with_two_features'] = metrics
	elif feature_instance == 2:
		metrics['title'] = 'SVM with tweet,length and interjection'
		temp_dict['svm_with_three_features'] = metrics
	else:
		metrics['title'] = 'SVM with tweet,length,interjection and polarity'
		temp_dict['svm_with_four_features'] = metrics

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

	data_list_dict = []
	total_labels = []

	#1
	feature_set = []
	read_tweets_to_list(sys.argv[1],data_list_dict,total_labels,feature_set)
	read_tweets_to_list(sys.argv[2],data_list_dict,total_labels,feature_set)
	total_features = list_to_features(data_list_dict)
	
	training_features = total_features[:2250]
	training_labels = total_labels[:2250]
	train_svm(training_features,training_labels)
	
	testing_features = total_features[2250:]
	testing_labels = total_labels[2250:]
	test_svm(testing_features,testing_labels,1)
	
	#2	
	feature_set = ['interjection']
	del data_list_dict[:]
	del total_labels[:]
	read_tweets_to_list(sys.argv[1],data_list_dict,total_labels,feature_set)
	read_tweets_to_list(sys.argv[2],data_list_dict,total_labels,feature_set)
	total_features = list_to_features(data_list_dict)

	training_features = total_features[:2250]
	training_labels = total_labels[:2250]
	train_svm(training_features,training_labels)

	testing_features = total_features[2250:]
	testing_labels = total_labels[2250:]
	test_svm(testing_features,testing_labels,2)

        #3
	feature_set = ['interjection','polarity']
	del data_list_dict[:]
	del total_labels[:]
	read_tweets_to_list(sys.argv[1],data_list_dict,total_labels,feature_set)
	read_tweets_to_list(sys.argv[2],data_list_dict,total_labels,feature_set)
	total_features = list_to_features(data_list_dict)

	training_features = total_features[:2250]
	training_labels = total_labels[:2250]
	train_svm(training_features,training_labels)

	testing_features = total_features[2250:]
	testing_labels = total_labels[2250:]
	test_svm(testing_features,testing_labels,3)

	print("\n\n")
	json_data = json.dumps(metrics_list)
	print(json_data)
	fd = open("metrics.json","w")
	fd.write(json_data)
	fd.close
