
# ---------------------------------------------------------------------
#   PROGRAM SPEC 
#   NAME: AUTO-REPORT
#   DATE OF CREATION: 13 SEPTEMBER 2019
#   PROGRAM TYPE: REPORT GENERATOR 
#   SUMMARY: This program uses pulls the most popular hashtag twitter topic
#            produces a series of complex analysis and writes to html
#            file that gets uploaded automatically to my website 
#           
# ---------------------------------------------------------------------



import datetime
import os
from ipywidgets import IntProgress
from IPython.display import display
from IPython.display import clear_output
import time
import sys
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the tweepy library
import tweepy
import get_trends
import get_token  

# ---------------------------------------------------------------------
#   AUTHENTICATION 
# ---------------------------------------------------------------------
auth = get_token.auth
api  = get_token.api


# ---------------------------------------------------------------------
#   GRABBING TOPIC  
# ---------------------------------------------------------------------
import random 
TOPIC = get_trends.TOPIC

# ---------------------------------------------------------------------
#   SET PARMS  
# ---------------------------------------------------------------------

max_count = 100
scantype = 2


# ---------------------------------------------------------------------
#   PERFORM SCAN
# ---------------------------------------------------------------------


if scantype == 1:
    status_array = []
    progress = 0

    f = IntProgress(description='Processing:',min=0, max=max_count,) # instantiate the bar
    display(f) # display the bar




    class StreamListener(tweepy.StreamListener):
        tweet_number=0   # class variable

        def on_status(self, status):
            self.max_tweets=max_count # max number of tweets
            self.tweet_number+=1   
            f.value += 1 # signal to increment the progress bar
            progress = (f.value/max_count) * 100
            progress = format(progress, '.2f')
            print('Progress: ' + str(progress) + " %")
            clear_output(wait=True)
            status_array.append(status._json)

            if self.tweet_number>=self.max_tweets:
                print('PROCESSING COMPLETE : '+str(self.max_tweets)+' tweets processed.')
                return False
                
                #sys.exit('PROCESSING COMPLETE : '+str(self.max_tweets)+' tweets processed.')


        def on_error(self, status_code):
            if status_code == 420:
                return False

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

    #print('Pulling down data.....')
    stream.filter(track=[TOPIC],languages=["en"])

elif scantype == 2:
    # HISTORICAL DATA SWITCHED OFF (IF YOU SWITCH ON, THEN SWITCH STREAM OFF ABOVE)

    status_array = []
    LOOP_COUNT = 0


    # ------ENTER YOUR SERACH TERM HER E--------
    tweets = tweepy.Cursor(api.search, q=TOPIC,lang='en', count=int(max_count))

    # TRACK PROGRESS
    f = IntProgress(min=0, max=max_count) # instantiate the bar
    display(f) # display the bar
    progress = 0

    print('Pulling down data.....')                    
    for tweet in tweets.items(int(max_count)):
        f.value+=1 # signal to increment the progress bar
        progress = (f.value/max_count) * 100
        progress = format(progress, '.2f')
        print('Progress: ' + str(progress) + " %")
        clear_output(wait=True)
        status_array.append(tweet._json)



    print('HISTORICAL Processing complete')
else:
    print('scantype fail')
    raise


    
# ---------------------------------------------------------------------
#   QUICK PEEK
# ---------------------------------------------------------------------


print('Number of records')
print(len(status_array))
print('')
print('An example element looks like: ')
print(status_array[0]['text'])


# ---------------------------------------------------------------------
#   TWEET NUMERICAL ANALYSIS
# ---------------------------------------------------------------------


linecount = 0
APPENDED_TEXT = ""

# CREATE FULL TEXT BLOB UPPER CASE 
for x in range(0, len(status_array)):
    linecount = linecount + 1
    text = str(status_array[x]['text']).upper()
    APPENDED_TEXT = APPENDED_TEXT + str(text)

# REMOVE PUNCTUATION FOR WORD COUNT
#APPENDED_TEXT = APPENDED_TEXT.replace('#', '')
APPENDED_TEXT = APPENDED_TEXT.replace('.', '')
APPENDED_TEXT = APPENDED_TEXT.replace(',', '')
APPENDED_TEXT = APPENDED_TEXT.replace(',', '')

print('')

print("Length of appended text array : " + str(len(APPENDED_TEXT)))
print('')

# COUNT WORDS AND REMOVE ADJECTIVES/NOUNDS
from collections import Counter, OrderedDict
DISC = APPENDED_TEXT.split()
x = Counter(DISC)
del x['⠀'],x['AND'],x['THE'],x['OF'],x['TO'],x['A'],x['IN'],x['&'],x['MY'],x['FOR'],x['I'],x['NOT'],x['IS'],x['ARE']
del x['WITH'],x['ALL'],x['ON'],x['-'],x['YOU'],x['BY'],x['IT'],x['NO'],x['OR'],x['OWN'],x['THAT'],x['AT'],x['BE'],x['|'],x['WILL'],
del x['BUT'],x['AN'],x['ABOUT'],x['AS'],x['FROM'],x['WHO'],x['ME'],x['WE'],x['HAVE'],x['OUR'],x['AM'],x['LIKE'],x['JUST']
del x['THIS'],x['THEY'],x['IF'],x['HAS'],x['&AMP'],x['HAS'],x['CAN'],x['NOW'],x['SO'],x['ONLY'],x['WAS'],x['WHAT'],x['THEIR'],x['YOUR'],x['WOULD']
del x['DO'],x['&AMP;'],x['ONE'],x['WANT'],x['BEEN'],x['THEM'],x['MORE'],x['TODAY'],x['GET'],x['WHEN'],x['COMMENT'],x['HER'],x['SHE'],x['FURTHER']
del x['HE'],x['HIS'],x['OUT'],x['HOW'],x['BECAUSE'],x['HIM'],x['WHY'],x['THINK'],x["IT'S"],x['TAKE'],x['OVER'],x[''],x[''],
del x['END'], x['ALSO'],x['SINCE'],x['END'],x['THAT'],x['UP'],x['IT’S'],x['SEE'],x['KNOW'],x['SHOULD'],x['HAD'],x['SAYS'],x['SAID'],x['DID'],x['—'],x['EVERY']
del x['YOU'],x['J'],x['WERE'],x['THERE'],x['“YOU'],x['THOSE'],x['OFTEN'],x['RIGHT'],x['•']
del x[TOPIC.upper()]

large_top_tweets = OrderedDict(x.most_common(50))
top_tweets = OrderedDict(x.most_common(20))
print('Top Tweets are:')
print(top_tweets)


# ---------------------------------------------------------------------
#   TWEET VISUALIZATION
# ---------------------------------------------------------------------


import os
import matplotlib.pyplot as plt

E = top_tweets
one = (0.1, 0.1, 0.1, 0.1)
two = (0.1, 0.1, 0.1, 0.1)
three = (0.1, 0.1, 0.1, 0.1)
four= (0.1, 0.1, 0.1, 0.1)
five= (0.1, 0.1, 0.1, 0.1)
six= (0.1, 0.1, 0.1, 0.1)
seven= (0.1, 0.1, 0.1, 0.1)
eight= (0.1, 0.1, 0.1, 0.1)
nine= (0.1, 0.1, 0.1, 0.1)
ten= (0.1, 0.1, 0.1, 0.1)
eleven= (0.1, 0.1, 0.1, 0.1)
twelve= (0.1, 0.1, 0.1, 0.1)
thirteen= (0.1, 0.1, 0.1, 0.1)
fourteen= (0.1, 0.1, 0.1, 0.1)
fithteen= (0.1, 0.1, 0.1, 0.1)
sixteen= (0.1, 0.1, 0.1, 0.1)
seventeen= (0.1, 0.1, 0.1, 0.1)
eighteen= (0.1, 0.1, 0.1, 0.1)
nineteen= (0.1, 0.1, 0.1, 0.1)
twenty= (0.1, 0.1, 0.1, 0.1)



color_last = [one, two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fithteen,sixteen,seventeen,eighteen,nineteen,twenty]
color = (0.1, 0.1, 0.1, 0.1)
plt.bar(range(len(E)), list(E.values()), align='center', color=color_last,  edgecolor='blue')

plt.xticks(range(len(E)), list(E.keys()), rotation='vertical', fontsize=10)
plt.title("Most Frequently Tweeted Words", fontsize=30)
plt.ylabel('# Of Occurrences (k)', fontsize=20 )
plt.xlabel('Tweeted term by Frequency', horizontalalignment='left', position=(0,10),fontsize=18)
plt.rcParams["figure.figsize"] = (20,10)

exists = os.path.isfile('TWEETS.png')
if exists:
    os.remove("TWEETS.png")

    
plt.savefig("TWEETS", bbox_inches="tight")
plt.close()



# ---------------------------------------------------------------------
#   USER DESCRIPTION NUMERICAL ANALYSIS
# ---------------------------------------------------------------------


linecount = 0
APPENDED_DESCRIPTION = ""
for x in range(0, len(status_array)):
    linecount = linecount + 1
    description = str(status_array[x]['user']['description']).upper()
    APPENDED_DESCRIPTION = APPENDED_DESCRIPTION + str(description)
    

APPENDED_DESCRIPTION = APPENDED_DESCRIPTION.replace('.', '')
APPENDED_DESCRIPTION = APPENDED_DESCRIPTION.replace(',', '')
APPENDED_DESCRIPTION = APPENDED_DESCRIPTION.replace(',', '')

from collections import Counter, OrderedDict
DISC = APPENDED_DESCRIPTION.split()
x = Counter(DISC)
del x['⠀'],x['AND'],x['THE'],x['OF'],x['TO'],x['A'],x['IN'],x['&'],x['MY'],x['FOR'],x['I'],x['NOT'],x['IS'],x['ARE']
del x['WITH'],x['ALL'],x['ON'],x['-'],x['YOU'],x['BY'],x['IT'],x['NO'],x['OR'],x['OWN'],x['THAT'],x['AT'],x['BE'],x['|'],x['WILL'],
del x['BUT'],x['AN'],x['ABOUT'],x['AS'],x['FROM'],x['WHO'],x['ME'],x['WE'],x['HAVE'],x['OUR'],x['AM'],x['LIKE'],x['JUST']
del x['THIS'],x['THEY'],x['IF'],x['HAS'],x['&AMP'],x['HAS'],x['CAN'],x['NOW'],x['SO'],x['ONLY'],x['WAS'],x['WHAT'],x['THEIR'],x['YOUR'],x['WOULD']
del x['DO'],x['&AMP;'],x['ONE'],x['WANT'],x['BEEN'],x['THEM'],x['MORE'],x['/'],x['•'],x["I'M"],x['UP'],x['THINGS'],x[''],x['']

large_bio_desc = OrderedDict(x.most_common(50))
top_bio_desc = OrderedDict(x.most_common(20))
print('')
print(top_bio_desc)


# ---------------------------------------------------------------------
#   USER DESCRIPTION VISUALIZATION
# ---------------------------------------------------------------------


import matplotlib.pyplot as plt

D = top_bio_desc

plt.bar(range(len(D)), list(D.values()), align='center', color=(0.1, 0.5, 1, 0.1),  edgecolor='blue')

plt.xticks(range(len(D)), list(D.keys()), rotation='vertical', fontsize=10)
plt.title("Tweeters Bio - Most popular Self Description", fontsize=30)
plt.ylabel('Number of Occurrences (thousands)', fontsize=18)
plt.xlabel('These are the words in which Tweeters describe themselves', horizontalalignment='left', position=(0,25), fontsize=18)
plt.rcParams["figure.figsize"] = (20,10)


exists = os.path.isfile('BIO.png')
if exists:
    os.remove("BIO.png")


plt.savefig("BIO", bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------------
#   SENTIMENT
# ---------------------------------------------------------------------

from textblob import TextBlob
import tweepy

VALUE = TOPIC

public_tweets = api.search(VALUE)

objective_tweet=0
subjective_tweet=0
negitively_subjective=0
for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    if analysis.sentiment[0]>0:
       subjective_tweet = subjective_tweet + 1
       print('Subjective')
    elif analysis.sentiment[0]<0:
       negitively_subjective = negitively_subjective  + 1
       print('Negatively subjective')
    else:
       objective_tweet = objective_tweet + 1
       print('objective')
    print('\n')

    
sentiment_total = objective_tweet + subjective_tweet + negitively_subjective  

objective_tweet = round(((objective_tweet/sentiment_total) * 100),2)
subjective_tweet = round(((subjective_tweet/sentiment_total) * 100),2)
negitively_subjective = round(((negitively_subjective/sentiment_total) * 100),2)






# ---------------------------------GRAPH-------------------------------------


import matplotlib.pyplot as plt

B = {
     str('Objective'):int(objective_tweet),
     str('Subjective'):int(subjective_tweet),
     str('Negatively Subjective'):int(negitively_subjective),
     str('Total'):int(100)
    
    
    }


one = ('#3498DB')
two = ('#3498DB')
three = ('#FF0000')
four = ('#ADD8E6')
five = ('#ff8c66')

color_options = [one, two,three,four,five]


plt.bar(range(len(B)), list(B.values()), align='center', color=color_options,  edgecolor='blue')

"""
COLOR OPTIONS
color=('#ff8c66'),
, alpha=0.1
"""



plt.xticks(range(len(B)), list(B.keys()), rotation='horizontal', fontsize=30)
plt.title(str("Sentiment Breakdown"), fontsize=30)
plt.ylabel('Number of Occurrences (%)', fontsize=18)
#plt.xlabel('These are the words in which Tweeters describe themselves', horizontalalignment='left', position=(0,25), fontsize=18)
plt.rcParams["figure.figsize"] = (20,10)


exists = os.path.isfile('sentiment.png')
if exists:
    os.remove("sentiment.png")



plt.savefig("sentiment")
plt.show()




print('objective_tweets : '+ str(objective_tweet) + " %")
print('subjective_tweets : '+ str(subjective_tweet) + " %")
print('negitively_subjective tweets: '+ str(negitively_subjective) + " %")
print("Total sentiments: " + str(sentiment_total))


