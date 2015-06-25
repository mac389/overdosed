import json, itertools

import utils as tech

from pprint import pprint 
from scipy.stats import ks_2samp
#Analyze hashtags

data = json.load(open('extracted-entities.json','rb'))

positive_hashtags = tech.get(data['positive'],'hashtags')
negative_hashtags = tech.get(data['negative'],'hashtags') 
unsure_hashtags =  [x['hashtags'] for x in data['unsure']]

#Are the distributions of hashtags different in positive vs negative?
#print ks_2samp(map(len,positive_hashtags),map(len,negative_hashtags))
#(0.14098360655737707, 0.99777571184658753) #Omitting zeros
#(0.13518266394372591, 0.11495613813102157) #Including zeros 
#How to control for unequal sample sizes?

#What is the Jaccard similarity of positive vs negative?
#0.0014409221902
#print tech.jaccard(list(itertools.chain.from_iterable(positive_hashtags)),
#					list(itertools.chain.from_iterable(negative_hashtags)))

#What is the Jaccard similarity of unsure vs negative?
#0.0473372781065
#print tech.jaccard(list(itertools.chain.from_iterable(unsure_hashtags)),
#					list(itertools.chain.from_iterable(negative_hashtags)))

#What is the Jaccard similarity of unsure vs positive?
#0.0048309178744
#print tech.jaccard(list(itertools.chain.from_iterable(unsure_hashtags)),
#					list(itertools.chain.from_iterable(positive_hashtags)))
#How to control for unequal sample sizes? Resampling? 


