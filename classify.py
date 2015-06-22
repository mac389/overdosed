from pprint import pprint

RELEVANT = set(open('relevant-tokens','r').read().splitlines())
IRRELEVANT = set(open('irrelevant-tokens','r').read().splitlines())

#In later versions, could weight each term by frequency, omitting that now for the sake of simplicity.

ALL_TOKENS = RELEVANT & IRRELEVANT
RELEVANT_SPECIFIC = RELEVANT - IRRELEVANT
IRRELEVANT_SPECIFIC = IRRELEVANT - RELEVANT

def score(list_of_tokens):
	list_of_tokens = set(list_of_tokens)
	return len(RELEVANT_SPECIFIC & list_of_tokens)/float(len(list_of_tokens))
#Don't forget to do the controls

print score(['heroin','heroin'])