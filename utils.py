import token, tokenize, json, re, string, nltk 

import matplotlib.pyplot as plt 

from matplotlib import rcParams
from cStringIO import StringIO

'''
    
     This is psanchez's answer to:

      http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name

'''

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
lmtzr = WordNetLemmatizer()
rcParams['text.usetex'] = True

standard_spelling = {'whaaaattttt':'what','annnnnnnd':'and','yeahh':'yeah','yeahhh':'yeah','wwhite':'white',
'toooo':'to','hahhaha':'ha','fellah':'fellow','poppin':'popping','feelin':'feeling','thouygh':'though','sadsadsad':'sad',
'longterm':' long','orang':'orange','takin':'taking'}



format = lambda txt: r'\Large \textbf{\textsc{%s}}'%txt
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result

def isdecimal(aStr):
  return all([ch.isdigit() or ch in string.punctuation for ch in aStr])

def isusername(aStr):
  return all([any([ch.isdigit() for ch in aStr]), any([ch.isalpha() for ch in aStr]),len(aStr)>3])

def hasvowels(aStr):
  return any([ch in 'aeiou' for ch in aStr])

def count_usernames(set_of_words):
  return [word for word in set_of_words if isusername(word)]

def word_tokenize(tweet):
    my_verboten_punctuation = string.punctuation.replace('@','').replace('#','')
    return [''.join([ch for ch in word if ch not in my_verboten_punctuation]) for word in tweet.split()]

def extract_tokens(list_of_tweets_as_str, count_usernames=True,is_single=False):
  if is_single:
    list_of_words_in_tweet = set([word for word in nltk.word_tokenize(list_of_tweets_as_str.lower()) 
                                if all([not word.isdigit(),not isdecimal(word)])])
  else:
    list_of_words_in_tweet = set([word for tweet in list_of_tweets_as_str for word in nltk.word_tokenize(tweet.lower()) 
                    if all([not word.isdigit(),not isdecimal(word)])])
  list_of_words_in_tweet -= set(string.punctuation)
  list_of_words_in_tweet = {token.replace('-','').replace('_','').replace('.','').replace("'",'').replace('/','').replace('*','') 
                for token in list_of_words_in_tweet if len(token)>3}
  list_of_words_in_tweet = {token if token not in standard_spelling else standard_spelling[token] for token in list_of_words_in_tweet}

  list_of_words_in_tweet =  {lmtzr.lemmatize(token,'v' if len(token)>4 and token.endswith('ing') or token.endswith('ed') else 'n')
          for token in list_of_words_in_tweet}
  
  usernames = {token for token in list_of_words_in_tweet if isusername(token)} if count_usernames else {}
  return ({token for token in list_of_words_in_tweet 
          if all([token not in stopwords.words('english'),len(token)>3, not isusername(token),hasvowels(token)])},usernames)


def regularize_json(json_string):
  json_string = re.sub(r"{\s*'?(\w)", r'{"\1', json_string)
  json_string = re.sub(r",\s*'?(\w)", r',"\1', json_string)
  json_string = re.sub(r"(\w)'?\s*:", r'\1":', json_string)
  json_string = re.sub(r":\s*'(\w+)'\s*([,}])", r':"\1"\2', json_string)
  return json_string

def json_decode (json_string, *args, **kwargs):
  try:
    json.loads(json_string, *args, **kwargs)
  except:
    json_string = fixLazyJson (json_string)
    json.loads(json_string, *args, **kwargs)

def get_field_damaged_string(astring):
  #Extract text
    text_key_start = astring.find('text')
    snippet = astring[(text_key_start+6):(text_key_start+146)].split(', u')[0].encode('utf-8').replace('u','').replace('[','').replace(']','').strip()[1:-1]

    #Extract id
    id_key_start = astring.find("id_str")

    #guessing how many to go ahead

    id_string = astring[id_key_start:(id_key_start+50)].split(':')[1].split(', u')[0].replace("u'",'').strip()[1:-1]

    return (snippet,id_string)

def cleanse(data,remove_stopwords=True):
    
    corpus = [word_tokenize(datum.lower().strip()) for datum in data]
    
    #remove URLs and stopwords
    corpus = [[word for word in text if not word.startswith('http')
                    and word not in stopwords.words('english')
                    and word not in ['rt',"'s",'bt','em']
                    and not any(['\u' in word,'\\x' in word,'t.co' in word, 'tco' in word])] for text in corpus]
    
    #remove unicode
    corpus = [[word.replace('\\','').replace(',','') for word in text if all([ord(ch)<128 for ch in word])
               and not all([ch in string.punctuation.replace('@','').replace('#','') for ch in word])] for text in corpus]

    corpus = [[lmtzr.lemmatize(word) for word in text if not word.isdigit()] for text in corpus]
    
    return corpus

def adjust_spines(ax, spines=['left','bottom']):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            #spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])

def freqplot(tokens,n=50,filename=None):
  '''Input is a list of tokens'''
  words,freqs = zip(*nltk.FreqDist(tokens).most_common(n))

  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(freqs,'k--')

  adjust_spines(ax)

  ax.set_xticks(range(len(freqs)))
  ax.set_xticklabels(map(format,words),rotation='vertical')
  ax.set_ylabel(format('Count'))

  plt.tight_layout()
  plt.savefig(filename)
  plt.savefig('%s.tiff'%filename)
  plt.close()

def fixLazyJson (in_text):
  tokengen = tokenize.generate_tokens(StringIO(in_text).readline)

  result = []
  for tokid, tokval, _, _, _ in tokengen:
    # fix unquoted strings
    if (tokid == token.NAME):
      if tokval not in ['true', 'false', 'null', '-Infinity', 'Infinity', 'NaN']:
        tokid = token.STRING
        tokval = "%s" % tokval

      if tokval == "None":
        tokval = "null"

      if tokval == "False" or tokval == "True":
        tokval = tokval.lower()  
    # fix single-quoted strings
    elif (tokid == token.STRING):
      if tokval.startswith ("'"):
        tokval = "%s" % tokval[1:-1].replace ('"', '\\"')

    # remove invalid commas
    elif (tokid == token.OP) and ((tokval == '}') or (tokval == ']')):
      if (len(result) > 0) and (result[-1][1] == ','):
        result.pop()


    result.append((tokid, tokval))

  return tokenize.untokenize(result)
