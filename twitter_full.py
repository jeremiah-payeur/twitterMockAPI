import pandas as pd
import os
#from twitterMySQL import TwitterAPI
from twitterRedis2 import TwitterAPI
#from twitterRedis import TwitterAPI
from twitterObjects import Tweet, Follow
from profiler import Profiler
import csv

TWEETS = 'tweet.csv'
FOLLOWS = 'follows.csv'

def createTweets(file, user_col, text_col):
    """Takes in csv file of tweets and creates tweet objects
    user_col int: index of user column
    text_col int: index of text column
    returns list of tweet objects"""
    df = pd.read_csv(file)
    return [Tweet(row[user_col], row[text_col]) for row in df.itertuples()]

def createFollowing(file, user_col, follow_col):
    """Takes in csv file of following relationship and creates follow objects
    user_col int: index of user column
    follow_col int: index of follow column
    returns list of tweet objects"""
    df = pd.read_csv(file)
    return [Follow(row[user_col], row[follow_col]) for row in df.itertuples()]


def read_tweet_csv(api, file, user_col, text_col):
    """Takes a file of tweets and inserts them one at a time
    api - api connection name
    user_col int: index of user column
    text_col int: index of text column
    returns nothing - inserts tweets"""
    # open file and read into csv
    with open(file) as tweet_file:
        # ignore header
        next(tweet_file)
        tweets = csv.reader(tweet_file)

        # create a tweet object for each tweet and post the tweet
        for tweet in tweets:
            tweet = Tweet(tweet[user_col], tweet[text_col])
            api.postTweet(tweet)

    return

def insert_tweets(api, tweets):
    """Insert a list of tweets one at a time
    takes in name of api and list of tweet objects and posts tweets one at a time"""
    for tweet in tweets:
        api.postTweet(tweet)
    return

def insert_follows(api, follows):
    """Insert a list of follows one at a time
    takes an api name and list of follow objects and posts follows one at a time"""
    for follow in follows:
        api.insert_followers(follow)
    return

def get_timelines(api, n):
    """Get n number of user timelines
    takes the name of an api and n(int) and calls the api to retrieve n home timelines"""
    timelines = []
    for i in range(n):
        # select random user and find timeline
        user = api.randomUser()
        timeline = api.getTimelime(user)
        timelines.append(timeline)
    return timelines



def main():

    # Authenticate
    # api = TwitterAPI(os.environ["TWITTER_USER"], os.environ["TWITTER_PASSWORD"], "twitter")
    api = TwitterAPI()
    api.clear_db()

    # tests first create tweets (if desired method) and follow objects
    # tweets = createTweets(TWEETS, 1, 2) -- we would use this if we wanted to retrieve all tweets at once
    follows = createFollowing(FOLLOWS, 1, 2)

    # post all tweets and insert all follows relations
    # insert_tweets(api, tweets) -- we would use this if we had a list of tweet objects we wanted to insert
    insert_follows(api, follows)
    read_tweet_csv(api, TWEETS, 0, 1)

    # get 100 user timelines
    # select random user and find timeline
    all_timelines = get_timelines(api, 100)

    # close all connections

    # print home timeline and find report
    print(all_timelines)
    Profiler.report()




if __name__ == '__main__':
    main()