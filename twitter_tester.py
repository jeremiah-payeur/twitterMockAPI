import pandas as pd
import os
#rom twitterMySQL import TwitterAPI
#from twitterRedis import TwitterAPI
from twitterRedis2 import TwitterAPI
from twitterObjects import Tweet, Follow
from profiler import Profiler
import csv

TEST_TWEETS = 'tweets_sample.csv'
TEST_FOLLOWS = 'follows_sample.csv'

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

def insert_follows(api, follows):
    """Insert a list of follows one at a time"""
    for follow in follows:
        api.insert_followers(follow)
    return



def main():

    # Authenticate
    #api = TwitterAPI(os.environ["TWITTER_USER"], os.environ["TWITTER_PASSWORD"], "twitter")
    api = TwitterAPI()
    api.clear_db()

    # tests first create tweets and follow objects
    #tweets = createTweets(TEST_TWEETS, 1, 2)
    follows = createFollowing(TEST_FOLLOWS, 1, 2)

    # post all tweets and insert all follows relations
    #insert_tweets(api, tweets)
    insert_follows(api, follows)
    read_tweet_csv(api, TEST_TWEETS, 0, 1)

    # test to see if it can get a random user home timeline
    user = api.randomUser()
    timeline = api.getTimelime(user)

    # print home timeline and report
    print(timeline)

    Profiler.report()



if __name__ == '__main__':
    main()