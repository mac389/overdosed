import json, itertools

import utils as tech

from pprint import pprint 

data = json.load(open('hypothesis_testing.json','rb'))

print data
coordinates = {'positive':tech.get(data['positive'], 'coordinates'),
			   'negative':tech.get(data['negative'],'coordinates')}

pprint(coordinates)