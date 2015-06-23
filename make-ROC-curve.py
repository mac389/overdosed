import matplotlib.pyplot as plt
import csv

import numpy as np 
import utils as tech 

from pprint import pprint
from scipy.integrate import trapz

automatic_ratings =  {}
for threshold in np.arange(10,100,10):
	filename = 'testing-sample-w-ratings-%d'%threshold
	with open(filename,'rb') as fid:
		automatic_ratings[threshold] = [int(row[-1]) for row in csv.reader(fid,delimiter='\t')]

with open('testing-sample-MC-ratings.csv','rU') as fid:
	my_text,my_ratings = zip(*[(row[0],int(row[-1])) for row in csv.reader(fid)])

#get fuzzy agreement
with open('fuzzy-testing-sample-w-ratings-10','rU') as fid:
	fuzzy_rating = [int(row[-1]) for row in csv.reader(fid,delimiter='\t')]

with open('excluding-fuzzy-testing-sample-w-ratings-10','rU') as fid:
	exclusive_fuzzy_rating = [int(row[-1]) for row in csv.reader(fid,delimiter='\t')]

#Fuzzy based on fewer data points, measurements are less accurate
fuzzy_ratings =  {}
fuzzy_idx = {}
for threshold in np.arange(10,100,10):
	filename = 'fuzzy-sample-automatically-rated-%d'%threshold
	with open(filename,'rb') as fid:
		fuzzy_ratings[threshold],fuzzy_idx[threshold] = zip(*[(int(row[-2]),int(row[-1])) 
														for row in csv.reader(fid,delimiter='\t')])


print my_text[76]
def calculate_agreement(truth,test):
	'''Assuming possible scores are 1 (yes), 0 (no) '''

	#Assuming len(truth) == len(test)
	tp = len([i for i in xrange(len(truth)) if truth[i]==1 and test[i]==1])
	fp = len([i for i in xrange(len(truth)) if truth[i]==0 and test[i]==1])
	tn = len([i for i in xrange(len(truth)) if truth[i]==0 and test[i]==0])
	fn = len([i for i in xrange(len(truth)) if truth[i]==1 and test[i]==0])

	tpr = tp/float(tp+fn)
	fpr = fp/float(tn+fp)

	return (tpr,fpr)


#print calculate_agreement(my_ratings,fuzzy_rating)
print calculate_agreement(my_ratings,exclusive_fuzzy_rating)
data = {}
fuzzy_data = {}
for threshold in np.arange(10,100,10):
	data[threshold] = calculate_agreement(my_ratings,automatic_ratings[threshold])
	fuzzy_data[threshold] = calculate_agreement([my_ratings[x] for x in fuzzy_idx[threshold]],fuzzy_ratings[threshold])

tpr,fpr = zip(*sorted(data.values(),key=lambda item:item[0]))
fuzzy_tpr,fuzzy_fpr = zip(*sorted(fuzzy_data.values(),key=lambda item:item[0]))

#print sorted(zip(tpr,fpr),key=lambda item:item[0])
#print np.dot(tpr,fpr)/float(len(tpr))
#(0.6529680365296804, 0.6295955882352942)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(fpr,tpr,'k.-',label=tech.format('tokens'))
ax.plot([0.6666666666666666], [0.6341911764705882],'k*',markersize=8,clip_on=False)
ax.plot([0.6529680365296804], [0.7795955882352942],'kD',markersize=8,clip_on=False)
ax.plot(fuzzy_fpr,fuzzy_tpr,'r.-',label=tech.format('fuzzy match'))

ax.plot([0,1],[0,1],'k-')
tech.adjust_spines(ax)
ax.set_aspect('equal')
ax.set_xlabel(tech.format('False Positive Rate'))
ax.set_ylabel(tech.format('True Positive Rate'))
plt.legend(frameon=False,numpoints=1)
plt.savefig('all-fuzzy-roc-curve.png')
plt.savefig('all-fuzzy-roc-curve.tiff')


