import os, gzip, json,tokenize,token
import nltk, csv

from nltk.corpus import stopwords

import utils as tech
import matplotlib.pyplot as plt 
from pprint import pprint
#Rule-in component

CONTROL = os.path.join(os.getcwd(),'data','control')
CASE = os.path.join(os.getcwd(),'data','case')


corpus = {'case':CASE}
text = {}
for condition,path in corpus.iteritems():
	if not os.path.isfile(os.path.join(path,'combined.txt')):
		for filename in os.listdir(path):
			if filename.endswith('.gz'):
				'''
					Salvaging attempt, this will only pull one tweet text and id from each file.
					This will hurt controls more than case tweets, which is ok.  
				'''
				with gzip.open(os.path.join(path,filename),'rb') as fid, open(os.path.join(path,'combined.txt'),'a+') as outfile:
					print>>outfile, '\t '.join(tech.get_field_damaged_string(fid.read()))
	else:
		text[condition] = open(os.path.join(path,'combined.txt'),'rb').read().splitlines()

#reddit and r/Drugs in particular another good source of information

#Identify most common words that are not stopwords in case series

with open(os.path.join(CASE,'combined-deduplicated-rated.csv'),'r') as infile:
	items = [row for row in csv.reader(infile)]

TEXT = 0
RATING = 2
text = tech.cleanse([item[0] for item in items])
tokens = [word for tweet in text for word in tweet]
word_frequencies = nltk.FreqDist(tokens)

fig = plt.figure()
ax = fig.add_subplot(111)
words,freqs = zip(*word_frequencies.most_common(25))
ax.plot(freqs,'k--',linewidth=2) 
tech.adjust_spines(ax)
ax.set_xticks(range(len(words)))
ax.set_xticklabels(words,rotation='vertical',weight='bold')
ax.set_ylabel('Count')
plt.tight_layout()
plt.savefig('word-frequency-lemmatized')
