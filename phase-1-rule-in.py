import os, nltk, csv

import utils as tech
import matplotlib.pyplot as plt 

CASE = os.path.join(os.getcwd(),'data','case')

with open(os.path.join(CASE,'combined-deduplicated-rated.csv'),'r') as infile:
	items = [row for row in csv.reader(infile)]


TEXT = 0
RATING = 2
text = tech.cleanse([item[0] for item in items])
tokens = [word for tweet in text for word in tweet]

with open('rule-in-tokens.txt','wb') as outfile:
	for token in set(tokens):
		print>>outfile,token

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
