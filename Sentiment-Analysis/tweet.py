import os
import tweepy as tw
import pandas as pd

def get_user_details(username):
        userobj = api.get_user(username)
        return userobj
consumer_key= 'vWdJyOoVeTu4VEzboZSgSd7NP'
consumer_secret= 'hP9okVJkz0Tt4AVZyHdNfi1VGNqUuWNftaGyz95uQPY7uTg5wQ'
access_token= '1319181878927093760-Qj0Ggbis389Y8378hNQIDp9sGLjqfr'
access_token_secret= '2QI7YvflA639EA4CcHtsnpMEQjoCJCzELaQAMT4LW4qh8'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "#elections -filter:retweets"
date_since = '2018-01-01'

tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since='2020-01-01',
                until = date_since).items(10)


for i in tweets:
        print(i.text)
    
