import os, nltk, csv, itertools

import utils as tech
import matplotlib.pyplot as plt 

from pprint import pprint

CASE = os.path.join(os.getcwd(),'data','case')

def jaccard(one,two):
	one = one if type(one) == type(set) else set(one)
	two = two if type(two) == type(set) else set(two)

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

relevant = itertools.chain.from_iterable(tech.cleanse(relevant))
irrelevant =  itertools.chain.from_iterable(tech.cleanse(irrelevant))

tech.freqplot(list(relevant),filename='relevant')
tech.freqplot(list(irrelevant),filename='irrelevant')

#pprint(jaccard(relevant,irrelevant))