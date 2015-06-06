#!/usr/local/bin/bash

mkdir -p ./data/
MAX_NUM_TWEET=1000000
python CaseControlStream.py --t keys.json --k keywords --o ./data -m $MAX_NUM_TWEET
python develop-classifier.py
python analyze-classifier.py
python test-classifier.py