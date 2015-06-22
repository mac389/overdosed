import token, tokenize, json, re, string
from cStringIO import StringIO

'''
    
     This is psanchez's answer to:

      http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name

'''

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
lmtzr = WordNetLemmatizer()


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
    #extract text
    corpus = [datum.lower().split() for datum in data]
    
    #remove URLs and stopwords
    corpus = [[word for word in text if not word.startswith('http')
                    and word not in stopwords.words('english')] for text in corpus]
    
    #remove unicode
    corpus = [[word for word in text if all([ord(ch)<128 for ch in word])
               and not all([ch in string.punctuation for ch in word])] for text in corpus]

    corpus = [[lmtzr.lemmatize(word) for word in text] for text in corpus]
    
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
