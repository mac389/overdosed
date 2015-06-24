
import json, langid

import numpy as np
import utils as tech

from pprint import pprint
from nltk.corpus import wordnet as wn 

def classify(tweet):
	copy_of_tweet = tweet
	tweet -= set(informative_tokens['common']['tokens'])

	positive_overlap = 	tweet & set(informative_tokens['positive']['tokens'])
	negative_overlap = tweet & set(informative_tokens['negative']['tokens'])

	if len(negative_overlap) == 0 and len(positive_overlap) == 0:
		tweet_synset = {synset for token in copy_of_tweet for synset in wn.synsets(token) if len(wn.synsets(token))>0}
		if len(tweet_synset) > 0:
			positive_overlap = tweet_synset & synsets['positive']
			negative_overlap = tweet_synset & synsets['negative']
		else:
			return np.nan	
	return 1 if len(positive_overlap) > len(negative_overlap) else 0


def calculate_agreement(truth,test):
	'''Assuming possible scores are 1 (yes), 0 (no) '''

	#Not count idxs where classifier could not decide and returned np.nan

	verboten = np.nonzero(np.isnan(test).astype(int))[0]

	#Assuming len(truth) == len(test)
	tp = len([i for i in xrange(len(truth)) if all([truth[i]==1, test[i]==1, i not in verboten])])
	fp = len([i for i in xrange(len(truth)) if all([truth[i]==0, test[i]==1, i not in verboten])])
	tn = len([i for i in xrange(len(truth)) if all([truth[i]==0, test[i]==0, i not in verboten])])
	fn = len([i for i in xrange(len(truth)) if all([truth[i]==1, test[i]==0, i not in verboten])])

	tpr = tp/float(tp+fn)
	fpr = fp/float(tn+fp)

	return (tpr,fpr)

informative_tokens = json.load(open('feature-tokens.json','rb'))

synsets = {'positive' :{synset for token in informative_tokens['positive']['tokens'] for synset in wn.synsets(token)},
			'negative':{synset for token in informative_tokens['negative']['tokens'] for synset in wn.synsets(token)}}


data = [item.strip().split('|') for item in open('evaluation-rating','r').read().splitlines()]

tweets,my_ratings = zip(*[(item[0],int(item[2])) for item in data if len(item)>2])

positive, negative = [],[]

for i in xrange(len(tweets)):
	if langid.classify(tweets[i])[0] == 'en':
		positive.append(tweets[i]) if my_ratings[i] == 1 else negative.append(tweets[i])

positive,p_users = tech.extract_tokens([' '.join(tweet) for tweet in tech.cleanse(positive)])
negative,n_users = tech.extract_tokens([' '.join(tweet) for tweet in tech.cleanse(negative)])

tmp = informative_tokens['positive']['tokens']
tmp += list(positive)
del tmp

tmp = informative_tokens['negative']['tokens']
tmp += list(negative)
del tmp

tmp = informative_tokens['positive']['usernames']
tmp += list(p_users)
del tmp

tmp = informative_tokens['positive']['usernames']
tmp += list(n_users)
del tmp


english_idx = [i for i in xrange(len(tweets)) if langid.classify(tweets[i])[0] == 'en']
automatic_ratings = [classify(set(tweet)) for tweet in tech.cleanse([tweets[i] for i in english_idx])]
my_english_ratings = [my_ratings[i] for i in english_idx]

print calculate_agreement(my_english_ratings,automatic_ratings)