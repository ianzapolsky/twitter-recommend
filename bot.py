# bot.py, an experimentation with Twitter bots
#
# Replies to tweets with a book recommendation fetched via the Amazon Product
# Advertising API based on hashtags contained within the tweet. 
# 
# by Ian Zapolsky - 3.29.14

import os
import time
from twitter import Twitter, OAuth, TwitterHTTPError
from amazonproduct import API

# screen name of the twitter account this bot will be operating under
BOT_NAME = 'ianzapolsky'

# Twitter API authentication
OAUTH_TOKEN     = os.environ['OAUTH_TOKEN']
OAUTH_SECRET    = os.environ['OAUTH_SECRET']
CONSUMER_KEY    = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']

# Amazon API authentication
amzn_cfg = {
  'access_key': os.environ['AMZN_K'],
  'secret_key': os.environ['AMZN_SK'],
  'associate_tag': os.environ['AMZN_AT'],
  'locale': 'us'
}

# return data for all tweets mentioning @BOT_NAME that have been created
# since latest_id
def fetch_unseen_mentions(latest_id):
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', since_id=latest_id)['statuses']

# return the id of the latest tweet mentioning @BOT_NAME
def fetch_latest_id():
  return t.search.tweets(q='@'+BOT_NAME, result_type='recent', count=1)['statuses'][0]['id']
  
# convert hashtags dict into a space-separated string
def tags_to_string(hashtags):
  tag_list = ''
  for tag in hashtags:
    tag_list += tag['text']+' '
  return tag_list


if __name__ == '__main__':

  # initialize Twitter connection
  t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
                         CONSUMER_KEY, CONSUMER_SECRET))

  # initialize Amazon connection
  a = API(cfg=amzn_cfg)

  # initialize latest_id to the most recent mention of @BOT_NAME
  latest_id = fetch_latest_id()

  # infinite loop to continously reply to new, properly formatted tweets
  while True:

    print 'waking up!'
    results = fetch_unseen_mentions(latest_id)
  
    if not results:
      print 'no new tweets'
    else: 
      for tweet in reversed(results):

        tweeter  = tweet['user']['screen_name']
        hashtags = tweet['entities']['hashtags']
        text     = tweet['text']
        tag_list = tags_to_string(hashtags)
      
        if tag_list != '':
          # search amazon product API 
          try:
            amzn_books = a.item_search('Books', Keywords=tag_list)

            for book in amzn_books:
              t.statuses.update(
                status='Hey there @'+tweeter+'!! Try "%s" by %s!' % 
                                                  (book.ItemAttributes.Title,
                                                   book.ItemAttributes.Author))
              # we only want the first result
              break
          except:
            t.statuses.update(
              status="Hey there @"+tweeter+"!! We coudn't find any matches for those hashtags. Sorry!")

      latest_id = tweet['id']

    # sleep 30 seconds at the end of each loop to avoid going over API 
    # restrictions (180 per 15-minute-window in 1.1)
    print 'going to sleep...'
    time.sleep(30)




