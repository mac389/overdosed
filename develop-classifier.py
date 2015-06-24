import json, csv, langid, nltk

import utils as tech 

from pprint import pprint

informative_tokens = json.load(open('feature-tokens.json','rb'))
ENGLISH = 'en' #langid abbreviation

filename = 'testing-sample-MC-ratings.csv'
with open(filename,'rU') as fid:
	corpus_to_test,my_ratings = zip(*[(row[0],int(row[1])) for row in csv.reader(fid)])

def classify(tweet_as_set_of_words):
	tweet_as_set_of_words,_ = tweet_as_set_of_words #Ignoring usernames
	tweet_as_set_of_words -= set(informative_tokens['common']['tokens'])

	positive_overlap = 	tweet_as_set_of_words & set(informative_tokens['positive']['tokens'])

	negative_overlap = tweet_as_set_of_words & set(informative_tokens['negative']['tokens'])
	return 1 if len(positive_overlap) > len(negative_overlap) else 0

def calculate_agreement(truth,test):
	'''Assuming possible scores are 1 (yes), 0 (no) '''

	#Assuming len(truth) == len(test)
	tp = len([i for i in xrange(len(truth)) if truth[i]==1 and test[i]==1])
	fp = len([i for i in xrange(len(truth)) if truth[i]==0 and test[i]==1])
	tn = len([i for i in xrange(len(truth)) if truth[i]==0 and test[i]==0])
	fn = len([i for i in xrange(len(truth)) if truth[i]==1 and test[i]==0])

	tpr = tp/float(tp+fn)
	fpr = fp/float(tn+fp)

	return (tpr,fpr)


#print len(corpus_to_test) #1307

#--Preprocess corpus, must keep track of indices to coregister with my data 
corpus_to_test = zip(xrange(len(corpus_to_test)),corpus_to_test)
corpus_to_test = [item for item in corpus_to_test if langid.classify(item[1])[0]==ENGLISH]

corpus = [(idx,classify(tech.extract_tokens(tweet,is_single=True))) for idx,tweet in corpus_to_test]

#Compare to my ratings
idxs = [item[0] for item in corpus]

print corpus_to_test[4]

print calculate_agreement([my_ratings[idx] for idx in idxs],[item[1] for item in corpus])


#print len(corpus_to_test) #927

'''
  Rationale for establishing thresholds:
  	A tweet discusses drug use if enough of its tokens are positive informative tokens and not too many are negative informative tokens

  	1. Remove from the tweet any token common to both the positive and negative informative tokens
  	2. If the tweet contains more positive informative tokens than negative informative tokens, we assign it to positive 
  	    and vice versa. 
'''

