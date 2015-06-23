import os, nltk, csv, itertools

import utils as tech
import matplotlib.pyplot as plt 

from pprint import pprint

CASE = os.path.join(os.getcwd(),'data','case')

def jaccard(one,two,verbose=False):
	one = one if type(one) == type(set) else set(one)
	two = two if type(two) == type(set) else set(two)

	if verbose:
		print 'Numerator %d'%len(one & two)
		print 'Denominator %d'%len(one | two)
	if len(one & two) == 0:
		return 0 
	else:
		return len(one & two)/float(len(one | two))

TEXT = 0
RATING = 2
with open(os.path.join(CASE,'combined-deduplicated-rated.csv'),'r') as infile:
	items = [row for row in csv.reader(infile)]

relevant, irrelevant  = [], []

for item in items:
	relevant.append(item[TEXT]) if int(item[RATING]) == 1 else irrelevant.append(item[TEXT])

relevant = list(itertools.chain.from_iterable(tech.cleanse(relevant)))
relevant += ['purple']
irrelevant =  list(itertools.chain.from_iterable(tech.cleanse(irrelevant)))

'''
Numerator 527
Denominator 3832
0.13752609603340293
'''


for key,value in [('relevant',relevant),('irrelevant',irrelevant)]:
	with open('%s-tokens'%key,'w') as outfile:
		for token in value:
			print>>outfile,token

tech.freqplot(relevant,filename='relevant')
tech.freqplot(irrelevant,filename='irrelevant')
tech.freqplot([word for word in relevant if word not in irrelevant],filename='specific-to-relevant')
tech.freqplot([word for word in irrelevant if word not in relevant],filename='specific-to-irrelevant')

pprint(jaccard(relevant,irrelevant,verbose=True))