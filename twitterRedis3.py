"""Twitter api implementation using Redis must be run at the same time as redis3queue.py"""
import redis
from profiler import Profiler
from twitterObjects import Tweet

class TwitterAPI:

    def __init__(self, host="localhost", port=6379, decode=True):
        """initialize connection to database"""
        self.db = redis.Redis(host=host, port=port, decode_responses=decode)


    def clear_db(self):
        """empty database"""
        self.db.flushall()

    def randomUser(self):
        """Select a random user from database"""
        user = self.db.srandmember("users")
        return user


    def insert_followers(self, follow_obj):
        """Insert a single follower relationship in database"""
        self.db.sadd(f"followed_list:{follow_obj.user}", follow_obj.follow)

        # make sure the user is in the table
        self.db.sadd("users", follow_obj.user)
        self.db.sadd(f"followers:{follow_obj.follow}", follow_obj.user)



    @Profiler.profile
    def getTimelime(self, user_id):
        """Gets one user's home timeline"""
        self.db.publish("timelines", user_id)

        return


    @Profiler.profile
    def postTweet(self, tweet_obj):
        """Post a single tweet"""

        """
        # find current time and id of tweet
        self.db.msetnx({"next_tweet_id": 1})
        n = self.db.get("next_tweet_id")
        time = self.db.time()
        time = time[0] + time[1]/100000
        """

        # publish tweet to queue
        tweet = str(tweet_obj.text) +","+ str(tweet_obj.user) #  +"," + str(time) + "," + str(n)
        self.db.publish("post", tweet)

        # increment tweet id
        #self.db.incr("next_tweet_id")


    def close(self):
        """close all connections"""
        self.db.close()
        return