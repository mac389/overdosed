import json, os, itertools, calendar, pytz, langid

import utils as tech
import numpy as np 

from pprint import pprint
from scipy.stats import ks_2samp
from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from datetime import *


base_path = '/Volumes/My Book/twittwer-stream/control'

'''
data = []
for filename in os.listdir(base_path):
	with open(os.path.join(base_path,filename),'rb') as fid:
		data  += [json.load(fid)]

json.dump(data,open('/Volumes/My Book/twittwer-stream/amalgamated.json','wb'))
#--1 Classify
'''

data = json.load(open(os.path.join('/Volumes/My Book/twittwer-stream','amalgamated.json'),'rb'))
#data = json.load(open('control_tweets.json','rb'))

text = tech.cleanse([tweet['text'] for tweet in data])

#Why duplicating one tweet from test corpus?
classifications = {}

def iqr(data):
	try:
		return 0.5*(np.percentile(data,75) - np.percentile(data,25))
	except:
		print data
def get(lst,field):
	return [item[field] for item in lst]

for i,tweet in enumerate(text):
	if langid.classify(' '.join(tweet))[0] == 'en':
	  	tweet,usernames,hashtags =  tech.extract_tokens(tweet)
		classifications[i] =  tech.classify(tweet)

print len(classifications)
print len(text)

positive,negative, unsure = [],[], []

json.dump(classifications,open('case-control-classifications.json','wb'))

for idx,classification in classifications.iteritems():
	if classification == 1:
		positive.append(data[idx])
	elif classification ==0:
		negative.append(data[idx])
	else:
		unsure.append(data[idx])

p,n,u = [],[],[]
for idx,classification in classifications.iteritems():
	tweet,usernames,hashtags =  tech.extract_tokens(text[idx])
	item = {'tweet':list(tweet),'usernames':list(usernames),'hashtags':list(hashtags)}
	if classification == 1:
		p.append(item)
	elif classification ==0:
		n.append(item)
	else:
		u.append(item)

entities = {'positive':p,'negative':n,'unsure':u}

#--compare retweets and favorites
print len(positive),'pos'
print len(negative),'neg'
print len(unsure), 'unsure'

pprint(entities)

json.dump(entities,open('extracted-entities.json','wb'))

hypothesis_testing = {}

for field in ['retweet_count', 'favorite_count']:

	pos_group, neg_group = [], []
	for tweet in positive:
		age = datetime.now() - datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
		pos_group += [tweet[field]/float(1+age.days)]

	for tweet in negative:
		age = datetime.now() - datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
		neg_group += [tweet[field]/float(1+age.days)]


	hypothesis_testing[field] = {'mean':{'positive':np.mean(pos_group),'negative':np.mean(neg_group)},
									'iqr':{'positive':iqr(pos_group),'negative':iqr(neg_group)},
									'comparison':{'ks_2samp':ks_2samp(pos_group,neg_group)}}



#-- compare descriptions
hypothesis_testing['description'] = {'positive':[item['description'] for item in get(positive,'user')],
									'negative':[item['description'] for item in get(negative,'user')],}


hypothesis_testing['coordinates'] = {'positive':get(positive,'coordinates'),'negative':get(negative,'coordinates')}

#Language variability in stream vs directed search could be interesting

json.dump(hypothesis_testing,open('hypothesis_testing.json','wb'))
