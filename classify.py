import random, itertools, nltk

from pprint import pprint
from matplotlib import rcParams

import matplotlib.pyplot as plt 
import numpy as np 
import utils as tech

from nltk.corpus import wordnet as wn 
rcParams['text.usetex'] = True

RELEVANT = set(open('relevant-tokens','r').read().splitlines())
IRRELEVANT = set(open('irrelevant-tokens','r').read().splitlines())

#In later versions, could weight each term by frequency, omitting that now for the sake of simplicity.

ALL_TOKENS = RELEVANT & IRRELEVANT
RELEVANT_SPECIFIC = RELEVANT - IRRELEVANT
IRRELEVANT_SPECIFIC = IRRELEVANT - RELEVANT
THRESHOLD = 75
RELEVANT_SPECIFIC_SYNSETS = {synset for token in RELEVANT_SPECIFIC for synset in wn.synsets(token)}
IRRELEVANT_SPECIFIC_SYNSETS = {synset for token in IRRELEVANT_SPECIFIC for synset in wn.synsets(token)}

def assign_category(list_of_tokens,threshold=75):
	return np.percentile()

def score(list_of_tokens):
	if len(list_of_tokens) > 0:
		list_of_tokens = set(list_of_tokens)
		return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
	else:
		return np.nan
#Don't forget to do the controls

## Could look for words sufficiently semantically similar to the tokens, first see if direct similarity works

test_corpus = tech.cleanse(set([item.split('|')[0] for item in open('test-high-prevalence.txt','r').read().splitlines()]))
#random.shuffle(test_corpus)

#print len(test_corpus)
words = set(nltk.word_tokenize(' '.join(itertools.chain.from_iterable(test_corpus))))
omitted = []
senses = []
irrelevant = []
for word in words:
	print word
	if len(wn.synsets(word)) > 0:
		senses += [len(set(wn.synsets(word)) & RELEVANT_SPECIFIC_SYNSETS)/float(len(wn.synsets(word)))]
		irrelevant += [len(set(wn.synsets(word)) & IRRELEVANT_SPECIFIC_SYNSETS)/float(len(wn.synsets(word)))]
		
	else:
		omitted += [word]	

print omitted		
print len(RELEVANT_SPECIFIC)
print len(RELEVANT_SPECIFIC_SYNSETS)
print len(omitted)
print len(senses)
np.savetxt('senses-count',senses,fmt='%d')
np.savetxt('irrelevant-senses-count',irrelevant,fmt='%d')
#for fuzzy match, distribution of number of sense of word in wordnet

#scores = np.array(map(score,test_corpus))
#np.savetxt('scores',scores,delimiter='\t')
'''
sample_idx = random.sample(xrange(len(test_corpus)),int(len(test_corpus)/10))
for percentile in np.arange(10,110,10):
	print 'testing-sample-w-ratings-%d'%percentile
	with open('testing-sample-w-ratings-%d'%percentile,'w') as fcomputer:
		print>>fcomputer,'%s\t%s\t%s'%(' '.join(test_corpus[idx]),str(scores[idx]>threshold),idx)


threshold = np.percentile(scores,75)
'''

'''
with open('testing-sample-no-ratings.csv','w') as fhuman:
	for idx in sample_idx:
		print>>fhuman,' '.join(test_corpus[idx])

'''
#NEED ROC curve for percentile, do I? (Perhaps for completeness sake)

'''
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(scores[~np.isnan(scores)],color='k',bins=20)
tech.adjust_spines(ax)
ax.set_xlabel(tech.format('Jaccard Similarity with Tokens Specific for Drug Discussions'))
ax.set_ylabel(tech.format('Count'))
plt.tight_layout()
plt.savefig('distribution-scores-test.png')
'''