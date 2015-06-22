import json
import random 

from pprint import pprint
'''
	Question is what metadata are associated with +opioid usage
'''
corpus = json.load(open('../Maui/#birthday-birthday-20140626-082517.json','r'))
extract_text = lambda item: item['text']

def partition(data,parse_function=None, partition_function=None):
	'''Assuming binary classification'''
	
	parse_function = parse_function if parse_function else lambda aStr: aStr.split()
	partition_function = partition_function if partition_function else lambda x: random.random() > 0.5
	data = map(parse_function,data)

	true, false  = [], []

	for i in xrange(len(data)):
		true.append(i) if partition_function(data[i]) else false.append(i)

	return {'True':true, 'False':false} #Is this variable a dangerous name

#pprint(partition(map(extract_text,corpus)))
x = partition(map(extract_text,corpus), partition_function=lambda x: len(x)>10)
print len(x['True'])
print len(x['False'])
'''
	TF-IDF score for both Yi and Devraj
'''