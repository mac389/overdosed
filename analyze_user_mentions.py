import json, itertools

import utils as tech

from pprint import pprint 
from scipy.stats import ks_2samp
#Analyze hashtags

data = json.load(open('extracted-entities.json','rb'))

positive_hashtags = tech.get(data['positive'],'usernames')
negative_hashtags = tech.get(data['negative'],'usernames') 
unsure_hashtags =  [x['usernames'] for x in data['unsure']]

#Are the distributions of hashtags different in positive vs negative?
#(0.057821013342485683, 0.99471276105427964) #Omitting zeros
print ks_2samp([len(item) for item in positive_hashtags if len(item)>0],[
				len(item) for item in negative_hashtags if len(item)>0]) #Omitting zeros
print ks_2samp(map(len,positive_hashtags),map(len,negative_hashtags)) # Including zeros
#(0.037270251872021709, 0.9999118016934464) #Including zeros 
#How to control for unequal sample sizes?

#What is the Jaccard similarity of positive vs negative?
#0.00303336703741

#print tech.jaccard(list(itertools.chain.from_iterable(positive_hashtags)),
#					list(itertools.chain.from_iterable(negative_hashtags)))

#What is the Jaccard similarity of unsure vs negative?
#0.0151754663294
#print tech.jaccard(list(itertools.chain.from_iterable(unsure_hashtags)),
#					list(itertools.chain.from_iterable(negative_hashtags)))

#What is the Jaccard similarity of unsure vs positive?
#0.00221565731167 <- ONLY THIS UPDATED
#print tech.jaccard(list(itertools.chain.from_iterable(unsure_hashtags)),
#					list(itertools.chain.from_iterable(positive_hashtags)))
#How to control for unequal sample sizes? Resampling? 

