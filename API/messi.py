from time import perf_counter
import tweepy as tp
import json
import requests
from datetime import datetime
from tweepy.cursor import PageIterator

API_KEY = 'f7aJjJEna3hHD8VbZ3Uft2rAc'
API_SECRET_KEY = 'IP2kAZ3qDnDeERGgUIY5IDneMwQc5UZF5L5rK4o6DG3YLXbr0V'
Bearer_Token = 'AAAAAAAAAAAAAAAAAAAAAGtASgEAAAAAAs1deHYkPJcYag7Jq8%2F1LzSi6Ts%3Dy5PCiPvsKAmNBzdoxpKvtlkiojBXFNz9PJ8xvBVCTEXggDgaPu'

Access_Token = '1422638221100523520-7NDNqGwF3vmMaZEkmoAluuYEL5YAJJ'
Access_Token_Secret = 'jUVIjE0WdnUTGTxMMyaGoNRnMQfY6v4pKyQiEhF5KfpMw'
'''Getting started - Auth'''
TWITTER_ID = '1422638221100523520'

auth = tp.OAuthHandler(API_KEY,API_SECRET_KEY)
auth.set_access_token(Access_Token,Access_Token_Secret)
api = tp.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# trends = api.trends_place('44418')
# print(trends[0])

# for trend in trends[0]['trends']:
#   print([trend['name']])
  
# a = [trend['name'] for trend in trends[0]['trends']]
# print(a)

'''Making event listener class that inherites from tweepy.StreamListener'''
def add_into_plain_txt(status):
  '''Add into txt file that handles plain tweets from Users'''
  with open('plain_tweets.txt','a',newline='',encoding='utf-8') as fp:
    status = status.replace('\n','').replace('\r','')
    fp.write(status)
    fp.write('\n')
    
def add_into_qouted_txt(status):
  with open('retweeted_tweets.txt','a',newline='',encoding='utf-8') as fp:
    status = status.replace('\n','').replace('\r','')
    fp.write(status)
    fp.write('\n')

class StreamListener(tp.StreamListener):
  def on_status(self,status):
    '''Triggered when new status arrives'''
    if not hasattr(status,'quoted_status') and not hasattr(status,'retweeted_status') and status.user.id_str != '1422638221100523520':
      '''If block triggered is status model object(Tweet) does not have a retweeted attribute and qoute status attribute. Hence, is triggered when real time tweets are tweeted'''
      tweet_id = status.id_str # Returns string representation of the unique id for this Tweet
      username = status.user.screen_name # Returns user name of account that tweeted
      try:
        '''This blocks follows the user'''
        status = status.extended_tweet['full_text']
        add_into_plain_txt(status)
        '''Reply to all instances of tweets'''
        api.update_status('@'+username + ' ' + 'This is a twitter bot that has detected the word "Somalian(s)" in your tweet. The correct word to use instead is somali/somalis. For more nationality demonyn(s) use this link - https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations',tweet_id)
        print('Plain Tweets added')
      
      except AttributeError:
        status = status.text
        add_into_plain_txt(status)
        '''Reply to all instances of tweets'''
        api.update_status('@'+username + ' ' + 'This is a twitter bot that has detected the word "Somalians" in your tweet. The correct word to use instead is somali/somalis. For more nationality demonyn(s) use this link - https://en.wikipedia.org/wiki/List_of_adjectival_and_demonymic_forms_for_countries_and_nations',tweet_id)
        print('Plain Tweets added 2')
      
    elif hasattr(status,'qouted_status'):
      '''Block triggered if status has attribute 'qouted_status' '''
      try:
        status = status.qouted_status.extended_status['full_text']
        add_into_qouted_txt(status)
        print('Qouted Tweet added')

      
      except AttributeError:
        status = status.text
        add_into_qouted_txt(status)
        print('Qoute Tweet added 2')
        
  
  def on_error(self, status_code):
    if status_code == 402:
      #returning False in on_error disconnects the stream
      print('Stream disconnected')
  
  def on_disconnect(self, notice):
    date_now = datetime.now()
    date_now = date_now.strftime('%d-%m-%Y')
    api.send_direct_message('1422638221100523520','Program ended at:' + date_now) 
    # return super().on_disconnect(notice)
    
  def on_connect(self):
    date_now = datetime.now()
    date_now = date_now.strftime('%d-%m-%Y')
    api.send_direct_message('1422638221100523520','Program started at:' + date_now) 
    
  def on_delete(self, status_id, user_id):
    print('Status deleted:',status_id)
    
  def start_time_noti(self):
    pass
  
  
s = StreamListener() # Instantiates StreamListener class into Object

stream = tp.Stream(api.auth,s)

stream.filter(track=['somalians'],languages=['en']) # Tracks statuses from the unique twitter ID for a specific User



def unfollow_everyone():
  '''Small method that returns an array containing the IDs of users being followed by the specified user. Then loops through each intenger in the list to peform the destroy_friendship method'''
  ids_of_friends = api.friends_ids('1422638221100523520')
  for friend in ids_of_friends:
    api.destroy_friendship(str(friend))
    



  
  
  

  
  
  
  
  

