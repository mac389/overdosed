import csv 

import numpy as np 

from pprint import pprint

with open('testing-sample-MC-ratings.csv','rU') as my_rating_file:
	my_ratings = [row for row in csv.reader(my_rating_file)]

#Automatic ratings
with open('testing-sample-w-ratings','rU') as automatic_rating_file:
	automatic_ratings = [row for row in csv.reader(automatic_rating_file,delimiter='\t')]


my_rating_numbers = np.array([x[-1] for x in my_ratings]).astype(int)
automatic_rating_numbers = np.array([True if x[1]=='True' else False for x in automatic_ratings]).astype(int)
pprint(automatic_rating_numbers)


#me, them
yes_yes = len([i for i in xrange(len(my_rating_numbers)) if my_rating_numbers[i] == 1 and automatic_rating_numbers[i] == 1])
yes_no =  len([i for i in xrange(len(my_rating_numbers)) if my_rating_numbers[i] == 1 and automatic_rating_numbers[i] == 0])
no_yes = len([i for i in xrange(len(my_rating_numbers)) if my_rating_numbers[i] == 0 and automatic_rating_numbers[i] == 1])
no_no = len([i for i in xrange(len(my_rating_numbers)) if my_rating_numbers[i] == 0 and automatic_rating_numbers[i] == 0])

print '      Them'
print 'Me',yes_yes,yes_no
print 'Me',no_yes, no_no