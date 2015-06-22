import os, gzip, json,tokenize,token

from pprint import pprint
#Rule-in component

CONTROL = os.path.join(os.getcwd(),'data','control')
CASE = os.path.join(os.getcwd(),'data','case')


corpus = {'case':[],'control':[]}


case_contents = []
for filename in os.listdir(CASE):
	if filename.endswith('.gz'):
		with gzip.open(os.path.join(CASE,filename),'rb') as fid:
			print json.loads(fid.read())

