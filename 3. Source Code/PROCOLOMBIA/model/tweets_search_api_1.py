
#%%

# library

import tweepy
import pandas as pd

#%%

# API Twitter Connection

# Tokens Procolombia
consumer_key =  'nv1kVSjb4KjZUyKLujQyW9H3J'
consumer_secret = 'r998nFG17MpEqhwltPCGfzYZcjlHgh6q4rci839crkJ44yMcf7'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHF8TAEAAAAAcRbH9PGBxTWc%2F8GkAW5RBh2ZWmQ%3DaDitIgAexjEIBz6XUWy0yoqKicvogsdaQGHZqAxbRfUpOwvgpW'
access_token = '1431382977968283648-467KIdZCHgOp8s2Ehpd7otw8kG3Pqf'
access_token_secret ='0vp7I66V0ZRjM7v74CqboiTYhbE39SidfLIJISvyTbToH'

# Authentication process.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Calling API.
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

try:
    api.verify_credentials()
    print('Authentication OK')
except:
    print('Error during authentication')

#%%

# Download twitter information function

def search_Tweets(query, lang, geo, country):
    
    path = '/home/ubuntu/PROCOLOMBIA/data/'
    
    tweets = tweepy.Cursor(api.search,
                           q = query,
                           lang = lang,
                           geo = geo,
                           result_type = 'mixed').items(1500)


    data = [[query, tweet.created_at, tweet.id, tweet.user.screen_name, tweet.text, tweet.geo] for tweet in tweets]
    df_tw = pd.DataFrame(data = data, columns = ['query', 'date', 'id', 'user', 'text','geo'])

    return df_tw.to_csv(path + country + '_df_tw.csv')

#%%

# Download twitter information function

q ='Colombia -filter:retweets'

#search_Tweets(q, 'en', '39.764095,-98.017321, 1300', 'USA')
#search_Tweets(q, 'en', '54.342920,-4.434833, 550', 'UK')
search_Tweets(q, 'en', '48.431292,-80.213672, 650', 'Canada') 
