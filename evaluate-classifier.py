
import json

import numpy as np
import utils as tech

from pprint import pprint
from nltk.corpus import wordnet as wn 

def classify(tweet_as_set_of_words):
	tweet_as_set_of_words,_ = tweet_as_set_of_words #Ignoring usernames
	copy_of_tweet_as_set_of_words = tweet_as_set_of_words
	tweet_as_set_of_words -= set(informative_tokens['common']['tokens'])

	positive_overlap = 	tweet_as_set_of_words & set(informative_tokens['positive']['tokens'])
	negative_overlap = tweet_as_set_of_words & set(informative_tokens['negative']['tokens'])

	if len(negative_overlap) == 0 and len(positive_overlap) == 0:
		tweet_synset = {synset for token in copy_of_tweet_as_set_of_words for synset in wn.synset(token)}
		print tweet_synset
		positive_overlap = tweet_synset & synsets['positive']
		negative_overlap = tweet_synset & synsets['negative']

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

informative_tokens = json.load(open('feature-tokens.json','rb'))

synsets = {'positive' :{synset for token in informative_tokens['positive']['tokens'] for synset in wn.synsets(token)},
			'negative':{synset for token in informative_tokens['negative']['tokens'] for synset in wn.synsets(token)}}


data = [item.strip().split('|') for item in open('evaluation-rating','r').read().splitlines()]

tweets,my_ratings = zip(*[(item[0],int(item[2])) for item in data if len(item)>2])

print tech.extract_tokens([' '.join(tweet) for tweet in tech.cleanse(tweets)])

'''
automatic = [classify(tech.extract_tokens(tweet)) for tweet in tweets]
pprint(automatic)
'''