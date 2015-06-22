#!/usr/local/bin/bash

MAX_NUM_TWEET=1000000

mkdir -p ./data/
python CaseControlStream.py --t keys.json --k keywords --o ./data -m $MAX_NUM_TWEET

#Maybe code hear to combine all the JSON files, extract the text of tweets from them
#Would be quicker in bash

python develop-classifier.py
python analyze-classifier.py
python test-classifier.py