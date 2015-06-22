'''

    python CaseControlStream.py --t JSON_KEY_FILE --k KEYWORDFILE --o DIR_TO_PIPE_TWEETS -m MAX_NUM_TWEET [OPTIONAL]

'''
import json,os,twitter, dropbox, gzip

from datetime import datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from pprint import pprint
from optparse import OptionParser
from progress.bar import Bar

#--Load input from command line
op = OptionParser()
op.add_option('--t', dest='keys', type='str', help='Path of key files')
op.add_option('--k', dest='keywords',type='str',help='Path of keywords')
op.add_option('--o',type="str", dest="outpath")
op.add_option('--m',type='int',dest="MAX_NUMBER_OF_TWEETS",default=100)
op.add_option('--c', dest="isCase", action="store_false",default=True,help="Pass to sample without filters")
op.print_help()

opts,args = op.parse_args()
if len(args) > 0:
    op.error('This script only takes arguments preceded by command line options.')

if not opts.outpath:
    opts.corpus = os.getcwd()
    print 'No output path specified. Using current working directory.'

if not os.path.exists(opts.outpath):
    os.makedirs(opts.outpath)

control_path = os.path.join(opts.outpath,'control')
if not os.path.exists(control_path):
    os.makedirs(control_path)

case_path = os.path.join(opts.outpath,'case')
if not os.path.exists(case_path):
    os.makedirs(case_path)
    
if not opts.keys:
    opts.keys = json.load(open('keys.json','rb'))
    print 'No access token specified. Searching for default tokens'
else:     
    opts.keys = json.load(open(opts.keys,'rb'))
if not opts.keywords:
    search_terms = ''
    print 'No search terms specified.'
else:
    search_terms = open(opts.keywords).read().splitlines() #Assuming one word per line

client= dropbox.client.DropboxClient(opts.keys['dropbox']['access_token'])
class listener(StreamListener):
    
    def __init__(self, api=None, path=None,outname='output',MAX_NUMBER_OF_TWEETS=100,TWEETS_PER_FILE=10,progress_bar=None):
        #I don't remember exactly why I defined this.
        self.api = api

        #We'll need this later.
        self.path = path
        self.count = 0
        self.outname = outname 
        self.progress_bar = progress_bar
        self.MAX_NUMBER_OF_TWEETS = MAX_NUMBER_OF_TWEETS
        self.TWEETS_PER_FILE = TWEETS_PER_FILE

    def on_data(self, data):
        all_data = json.loads(data)       
        #tweet = all_data["text"]        
        #username = all_data["user"]["screen_name"]
        filename = os.path.join(self.path,'%s_%s'%(self.outname,datetime.now().strftime('%Y-%m-%d-%H-%M')))
        with gzip.open(filename,"a") as fid: #This open and closes the same file a lot of times. Hack for now. 
            print>>fid,all_data
            self.count += 1 
            if self.progress_bar:
                self.progress_bar.next()

        if self.count < self.MAX_NUMBER_OF_TWEETS:
            return True
        else:
            if self.progress_bar:
                self.progress_bar.finish()
            return False

    def on_error(self, status):
        return True #I believe this functions like pass in a try-except blocks

    def on_timeout(self):
        return True # Don't kill the stream

auth = OAuthHandler(opts.keys['twitter']['consumer_key'], opts.keys['twitter']['consumer_secret'])
auth.set_access_token(opts.keys['twitter']['access_token'],opts.keys['twitter']['access_token_secret'])

TWEETS_PER_FILE = 10000

bar = Bar('Acquiring control tweets', max=opts.MAX_NUMBER_OF_TWEETS)
control_stream = twitter.TwitterStream(
    auth=twitter.OAuth(opts.keys['twitter']['access_token'], opts.keys['twitter']['access_token_secret'], 
        opts.keys['twitter']['consumer_key'], opts.keys['twitter']['consumer_secret']), timeout=False, heartbeat_timeout=1000000)
iterator = control_stream.statuses.sample()
counter = 0

for tweet in iterator:
    filename = os.path.join(control_path,'control_%d'%(counter/TWEETS_PER_FILE))
    with gzip.open(filename,'a') as fid:
        print>>fid,tweet
        counter += 1
        bar.next()
    if counter > opts.MAX_NUMBER_OF_TWEETS:
        break
bar.finish()

if opts.isCase:
    try:
        bar = Bar('Acquiring case tweets', max=opts.MAX_NUMBER_OF_TWEETS)
        caseStream = Stream(auth, listener(path=case_path,
                outname='opioid', MAX_NUMBER_OF_TWEETS=opts.MAX_NUMBER_OF_TWEETS,TWEETS_PER_FILE=TWEETS_PER_FILE,
                progress_bar = bar)) 
        caseStream.filter(track=search_terms)
    except Exception as e:
        print e
