import csv, nltk

import utils as tech 
import numpy as np 

from nltk.corpus import wordnet as wn 
from pprint import pprint 
#load data with percentile 75

RELEVANT = set(open('relevant-tokens','r').read().splitlines())
IRRELEVANT = set(open('irrelevant-tokens','r').read().splitlines())

#In later versions, could weight each term by frequency, omitting that now for the sake of simplicity.

ALL_TOKENS = RELEVANT & IRRELEVANT
RELEVANT_SPECIFIC = RELEVANT - IRRELEVANT
IRRELEVANT_SPECIFIC = IRRELEVANT - RELEVANT

def score(list_of_tokens,verbose=False):
	if len(list_of_tokens) > 0:
		list_of_tokens = set(list_of_tokens)
		if verbose:
			print list_of_tokens
			print RELEVANT_SPECIFIC & list_of_tokens
		return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
	else:
		return np.nan

with open('testing-sample-w-ratings') as fid:
	to_automatically_rate = [row for row in csv.reader(fid, delimiter='\t')] 

comments_to_rate = [row[0] for row in to_automatically_rate]
distribution = np.loadtxt('scores',delimiter='\t')

for threshold in np.arange(10,100,10):
	print 'Threshold score = %.03f'%np.percentile(distribution,threshold)
	with open('testing-sample-w-ratings-%d'%threshold,'w') as fcomputer:
		for comment in comments_to_rate:
			print>>fcomputer,'%s\t%s'%(comment,1 
				  if score(nltk.word_tokenize(comment),verbose=False) > np.percentile(distribution,threshold) else 0)

