import token, tokenize, json, re

from cStringIO import StringIO

'''
    
     This is psanchez's answer to:

      http://stackoverflow.com/questions/4033633/handling-lazy-json-in-python-expecting-property-name

'''

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
