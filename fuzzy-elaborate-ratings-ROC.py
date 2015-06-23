import csv, nltk

import utils as tech 
import numpy as np 

from pprint import pprint 
from nltk.corpus import wordnet as wn
#load data with percentile 75

RELEVANT = set(open('relevant-tokens','r').read().splitlines())
IRRELEVANT = set(open('irrelevant-tokens','r').read().splitlines())

#In later versions, could weight each term by frequency, omitting that now for the sake of simplicity.

ALL_TOKENS = RELEVANT & IRRELEVANT
RELEVANT_SPECIFIC = RELEVANT - IRRELEVANT
IRRELEVANT_SPECIFIC = IRRELEVANT - RELEVANT

RELEVANT_SPECIFIC_SYNSETS = {synset for token in RELEVANT_SPECIFIC for synset in wn.synsets(token)}
IRRELEVANT_SPECIFIC_SYNSETS = {synset for token in IRRELEVANT_SPECIFIC for synset in wn.synsets(token)}

def score(list_of_tokens,verbose=False,fuzzy=True):
	if len(list_of_tokens) > 0:
		list_of_tokens = set(list_of_tokens)
		if verbose:
			pass
		if not fuzzy:
			return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
		else:
			token_synsets = {synset for token in list_of_tokens for synset in  wn.synsets(token)}
			if len(token_synsets) == 0:
				return 0
			else:
				return len(token_synsets & RELEVANT_SPECIFIC_SYNSETS) > 1 and len(token_synsets & IRRELEVANT_SPECIFIC_SYNSETS) >= 1 
	else:
		return np.nan

with open('testing-sample-w-ratings') as fid:
	to_automatically_rate = [row for row in csv.reader(fid, delimiter='\t')] 

'''
Threshold score = 1.000
Threshold score = 2.000
Threshold score = 2.000
Threshold score = 3.000
Threshold score = 4.000
Threshold score = 5.000
Threshold score = 6.600
Threshold score = 9.000
Threshold score = 12.200
'''

comments_to_rate = [row[0] for row in to_automatically_rate]
#distribution = np.loadtxt('scores',delimiter='\t')
distribution = np.loadtxt('senses-count')
pprint(distribution)
for threshold in np.arange(10,100,10):
	print 'Threshold score = %.03f'%np.percentile(distribution,threshold)
	with open('excluding-fuzzy-testing-sample-w-ratings-%d'%threshold,'w') as fcomputer:
		for comment in comments_to_rate:
			print>>fcomputer,'%s\t%s'%(comment,1 
				  if score(nltk.word_tokenize(comment),verbose=True,fuzzy=True) else 0)

