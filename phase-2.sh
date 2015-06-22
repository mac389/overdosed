#!/usr/local/bin/bash

MAX_NUM_TWEET=1000000
python CaseControlStream.py --t keys.json --k keywords --o ./data -m $MAX_NUM_TWEET --c 
python partition-tweet-records.py
python digital-epidemiology.py
