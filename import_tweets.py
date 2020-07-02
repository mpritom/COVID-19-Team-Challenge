#Thanks to Ruizhu Xiong for providing the code.

import tweepy, xlsxwriter
from datetime import datetime
          
#####################################################################################################################
#Here is your consumer keys and access tokens. You should use your own corresponding to your Tweeter Developer Account.
#####################################################################################################################
consumer_key = "XXXX"
consumer_secret = "XXXX"
access_token = "XXXX"
access_token_secret = "XXXX"
    
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

####################################################################################################################
#Here you can configure the spreadsheet name and which sheet to use.
####################################################################################################################
outBook = xlsxwriter.Workbook("data_key_mybodymychoice_Jun29toJul1.xlsx")
outSheet = outBook.add_worksheet("Sheet1")

count = 0 
outSheet.write(0,0,'userName')
outSheet.write(0,1,'screenName')
outSheet.write(0,2,'userLocation')
outSheet.write(0,3,'tweetText')
outSheet.write(0,4,'tweetId')
outSheet.write(0,5,'favorites')
outSheet.write(0,6,'in_reply_to_user')
outSheet.write(0,7,'creationTime')
outSheet.write(0,8,'geo')
outSheet.write(0,9,'source')
outSheet.write(0,10,'retweetedTo')
outSheet.write(0,11,'retweetCounts')
outSheet.write(0,12,'user_descrip')
outSheet.write(0,13,'followers')                                               
outSheet.write(0,16,'user_url')
outSheet.write(0,17,'user_ctime')
#outSheet.write(0,18,'hashtags')
#outSheet.write(0,20,'')
#outSheet.write(0,21,'')
#outSheet.write(0,22,'')

search_words = ["#covid-19", "covid19", "coronavirus","#Covid-19","#covid19"]

tweet = tweepy.Cursor(api.search,
                           q="my body my choice", ####### This is the keyword used for searching the tweets.
                           count=100,
                           #geocode="29.424349,-98.491142,50km", ####### This is tailored for San Antonio area.
                           since='2020-06-29', ####### Date from.
                           until='2020-07-01', ####### Date to.
                           result_type='recent',
                           include_entities=True,
                           monitor_rate_limit=True, 
                           wait_on_rate_limit=True,
                           sleep_on_rate_limits=True,
                           tweet_mode='extended',
                           lang="en").items()

try:  
  for status in tweet:
      
    tweets = tweet.next()
      
    count += 1 

    print(type(status), status)
    userName = status.user.name
    screenName = status.user.screen_name
    userLocation = status.user.location
    user_descrip = status.user.description
    followers = status.user.followers_count
    friends = status.user.friends_count
    created_at = status.created_at
    user_url = status.user.url
    user_ctime = status.user.created_at
    #hashtags = status.entities['hashtags']
    
    created_at_formatted = datetime.strftime(created_at,'%a %b %d %H:%M:%S %z %Y')
    user_ctime_formatted = datetime.strftime(user_ctime,'%a %b %d %H:%M:%S %z %Y')
    
    #tweetText = status.extended_tweet['entities']
    tweetText = status.full_text
    tweetId = status.id_str 
    favorites = status.favorite_count 
    in_reply_to_user = ''
    if type(status.in_reply_to_user_id_str) == str or type(status.in_reply_to_user_id_str) == type(None): 
      in_reply_to_user = status.in_reply_to_user_id_str
    else:
      print(type(status.in_reply_to_user_id_str))
    retweetCounts = 0 
    retweetedTo = ''
    try:
      retweetCounts = status.retweet_count 
      retweetedTo = status.retweeted_status.user.screen_name
    except Exception as e: 
      retweetCounts = 0 
      retweetedTo = ''

    creationTime = created_at_formatted #status.created_at
    geo = status.coordinates
    source = status.source

    outSheet.write(count,0,userName)
    outSheet.write(count,1,screenName)
    outSheet.write(count,2,userLocation)
    outSheet.write(count,3,tweetText)
    outSheet.write(count,4,tweetId)
    outSheet.write(count,5,favorites)
    outSheet.write(count,6,in_reply_to_user)
    outSheet.write(count,7,creationTime)
    try:
      outSheet.write(count,8,geo)
    except:
      print('Exception writing geo ', geo)
    outSheet.write(count,9,source)
    outSheet.write(count,10,retweetedTo)
    outSheet.write(count,11,retweetCounts)
    outSheet.write(count,12,user_descrip)
    outSheet.write(count,13,followers)
    outSheet.write(count,14,friends)
    outSheet.write(count,15,created_at_formatted)
    outSheet.write(count,16,user_url)
    outSheet.write(count,17,user_ctime_formatted)
#    outSheet.write(count,18,hashtags)
#    outSheet.write(count,20,source_url)
#    outSheet.write(count,21,source_url)
#    outSheet.write(count,22,source_url)
except Exception as e: 
  print('Exception caught in Tweepy: ', e)

outBook.close()
