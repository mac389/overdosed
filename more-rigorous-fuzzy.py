import csv, nltk,langid

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
		return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
	else:
		return np.nan

def fuzzy_score(list_of_tokens,verbose=False):
	token_synsets = {synset for token in list_of_tokens for synset in  wn.synsets(token)}	
	if len(token_synsets) == 0:
		return np.nan
	else:
		if verbose:
			print token_synsets,'Token Synsets'
			print token_synsets & RELEVANT_SPECIFIC_SYNSETS
		return len(token_synsets & RELEVANT_SPECIFIC_SYNSETS)  

with open('testing-sample-w-ratings') as fid:
	to_automatically_rate = [row for row in csv.reader(fid, delimiter='\t')] 
'''
Threshold score = 1.000
Threshold score = 1.000
Threshold score = 2.000
Threshold score = 2.000
Threshold score = 3.000
Threshold score = 4.000
Threshold score = 5.000
Threshold score = 7.000
Threshold score = 11.000
'''
valid = lambda tup: tup[1]>0.9 and tup[0]=='en'
comments_to_rate = [row[0] for row in to_automatically_rate]
distribution = np.loadtxt('senses-count')
for threshold in np.arange(10,100,10):
	print 'Threshold score = %.03f'%np.percentile(distribution,threshold)
	with open('fuzzy-sample-automatically-rated-%d'%threshold,'w') as fcomputer:
		for i,comment in enumerate(comments_to_rate):
			if valid(langid.classify(comment)):
				print>>fcomputer,'%s\t%s\t%d'%(comment,1 if fuzzy_score(nltk.word_tokenize(comment))>threshold else 0,i)
