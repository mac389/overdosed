import random, itertools, nltk, csv, langid

from pprint import pprint

import numpy as np 
import utils as tech

from nltk.corpus import wordnet as wn 

RELEVANT = set(open('relevant-tokens','r').read().splitlines())
IRRELEVANT = set(open('irrelevant-tokens','r').read().splitlines())

ALL_TOKENS = RELEVANT | IRRELEVANT
RELEVANT_SPECIFIC = RELEVANT - IRRELEVANT
IRRELEVANT_SPECIFIC = IRRELEVANT - RELEVANT

RELEVANT_SPECIFIC_SYNSETS = {synset for token in RELEVANT_SPECIFIC for synset in wn.synsets(token)}
IRRELEVANT_SPECIFIC_SYNSETS = {synset for token in IRRELEVANT_SPECIFIC for synset in wn.synsets(token)}


def score(list_of_tokens):
	if len(list_of_tokens) > 0:
		list_of_tokens = set(list_of_tokens)
		return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
	else:
		return np.nan
'''
test_corpus = tech.cleanse(set([item.split('|')[0] for item in open('test-high-prevalence.txt','r').read().splitlines()]))
words = set(nltk.word_tokenize(' '.join(itertools.chain.from_iterable(test_corpus))))
with open('test-tokens','w') as fid, open('test-tokens-in-wordnet','w') as wn_fid:
	for word in words:
		print>>fid, word
		if len(wn.synsets(word))>0:
			print>>wn_fid, word
'''

words = open('test-tokens-in-wordnet','r').read().splitlines()
#counts = [len(wn.synsets(word)) for word in words]
#np.savetxt('senses-count',counts,fmt='%d',delimiter='\t')
#scores = np.array(map(score,test_corpus))
#np.savetxt('scores',scores,delimiter='\t')

#What percent of testing-sample has wordnet coverage
with open('testing-sample-no-ratings.csv','rU') as fid:
	test_tweets = [item[0] for item in csv.reader(fid) if len(item)>0 
	 													and langid.classify(item[0])[0]=='en']

all_words_in_test_tweets = set(itertools.chain.from_iterable([nltk.word_tokenize(tweet) for tweet in test_tweets]))
all_words_in_test_tweets_in_wordnet = [word for word in all_words_in_test_tweets if len(wn.synsets(word)) > 0]
print len(all_words_in_test_tweets)#3260
print len(all_words_in_test_tweets_in_wordnet) #2152


'''
sample_idx = random.sample(xrange(len(test_corpus)),int(len(test_corpus)/10))
for percentile in np.arange(10,110,10):
	print 'testing-sample-w-ratings-%d'%percentile
	with open('testing-sample-w-ratings-%d'%percentile,'w') as fcomputer:
		print>>fcomputer,'%s\t%s\t%s'%(' '.join(test_corpus[idx]),str(scores[idx]>threshold),idx)
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