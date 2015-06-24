import csv, langid, nltk json

import utils as tech 
from pprint import pprint
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#Determine words specific each class I rated

filename = 'testing-sample-MC-ratings.csv'
ENGLISH = 'en' #langid abbreviation
CONFIDENCE_THRESHOLD = 0.9
lemmatizer = WordNetLemmatizer()

with open(filename,'rU') as fid:
	corpus = [(row[0],int(row[1])) for row in csv.reader(fid)]

positive, negative = [],[]

#print len(corpus) #1307

for tweet,rating in corpus:
	language,confidence = langid.classify(tweet)
	if language == ENGLISH and confidence > CONFIDENCE_THRESHOLD:
		positive.append(tweet) if rating == 1 else negative.append(tweet)

positive,positive_usernames = tech.extract_tokens(positive)
negative,negative_usernames = tech.extract_tokens(negative)

to_save = {'positive':{'tokens':list(positive - negative),'usernames':list(positive_usernames - negative_usernames)},
			'negative':{'tokens':list(negative - positive),'usernames':list(negative_usernames - positive_usernames)},
			'common':{'tokens':list(positive & negative), 'usernames':list(positive_usernames & negative_usernames)}}

json.dump(to_save,open('feature-tokens.json','wb'))
'''
print 'Names'
print len(positive_usernames)
print len(negative_usernames)
print len(positive_usernames & negative_usernames)
print '-----'
print len(positive & negative)
print len(positive - negative)
print len(negative - positive)
'''
'''
pprint(positive_usernames)
pprint(negative_usernames)
'''
