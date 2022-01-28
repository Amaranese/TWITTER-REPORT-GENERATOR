# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json
# Import the tweepy library
import tweepy
import get_token

# ---------------------------------------------------------------------
#   selecting topic 
# ---------------------------------------------------------------------

import random 

# ---------------------------------------------------------------------
#   GRAB TRENDS
# ---------------------------------------------------------------------


WOE_ARRAY = ['44418,London','2442047,LA', '2487889,sandiego', '2459115,NEWYORK', '2424766,TEXAS', '2471390,arizona','2471217,philly','2383660,ohio', '2487956,SanFransisco', '23424977,USA','23424775,CANADA', '23424975,UK']
WOE_CHOICE = random.choice(WOE_ARRAY)
WOE_CITY = WOE_CHOICE.split(',')[1]
WOE_CHOICE=WOE_CHOICE.split(',')[0]

print('')
print('WOEID CHOICE:' + str(WOE_CHOICE) + ', ' + str(WOE_CITY))
print('')

trend_array = []
local_trends = get_token.api.trends_place(WOE_CHOICE)


trends = json.loads(json.dumps(local_trends, indent=1))
 
for trend in trends[0]["trends"]:
    trend_array.append(trend["name"])

# ---------------------------------------------------------------------
#   selecting topic 
# ---------------------------------------------------------------------

TOPIC = random.choice(trend_array)

print('Chosen Topic is ' + str(TOPIC))
print('')