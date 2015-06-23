import csv, langid, nltk, re, string, collections, json

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

def isdecimal(aStr):
	return all([ch.isdigit() or ch in string.punctuation for ch in aStr])

def isusername(aStr):
	return all([any([ch.isdigit() for ch in aStr]), any([ch.isalpha() for ch in aStr]),len(aStr)>3])

def count_usernames(set_of_words):
	return [word for word in set_of_words if isusername(word)]

def extract_tokens(list_of_tweets_as_str, count_usernames=True):
	list_of_words_in_tweet = set([word for tweet in list_of_tweets_as_str for word in nltk.word_tokenize(tweet) 
			if not word.isdigit() and not isdecimal(word)])
	list_of_words_in_tweet -= set(string.punctuation)
	list_of_words_in_tweet = {token.replace('-','').replace('_','').replace('.','').replace("'",'').replace('/','') 
								for token in list_of_words_in_tweet if len(token)>3}
	list_of_words_in_tweet = {token if token not in standard_spelling else standard_spelling[token] for token in list_of_words_in_tweet}

	list_of_words_in_tweet =  {lemmatizer.lemmatize(token,'v' if len(token)>4 and token.endswith('ing') or token.endswith('ed') else 'n')
					for token in list_of_words_in_tweet}
	
	usernames = {token for token in list_of_words_in_tweet if isusername(token)} if count_usernames else {}
	return ({token for token in list_of_words_in_tweet 
					if all([token not in stopwords.words('english'),len(token)>3, not isusername(token)])},usernames)

positive, negative = [],[]

#print len(corpus) #1307

standard_spelling = {'whaaaattttt':'what','annnnnnnd':'and','yeahh':'yeah','yeahhh':'yeah','wwhite':'white'}

for tweet,rating in corpus:
	language,confidence = langid.classify(tweet)
	if language == ENGLISH and confidence > CONFIDENCE_THRESHOLD:
		positive.append(tweet) if rating == 1 else negative.append(tweet)

positive,positive_usernames = extract_tokens(positive)
negative,negative_usernames = extract_tokens(negative)

to_save = {'positive':{'tokens':list(positive),'usernames':list(positive_usernames)},
			'negative':{'tokens':list(negative),'usernames':list(negative_usernames)}}

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
