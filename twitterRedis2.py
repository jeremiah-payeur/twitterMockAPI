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
        tweet_ids = self.db.zrevrange(f"timeline:{user_id}", 0, 9)

        tweets = []
        for i in range(len(tweet_ids)):
            tweets.append(self.db.hgetall(f"tweet:{i}"))

        sorted_tweets = [Tweet(tweet['text'], tweet['user'], tweet['time'], tweet['tweet_id'])
                         for tweet in tweets if tweet]

        return sorted_tweets


    @Profiler.profile
    def postTweet(self, tweet_obj):
        """Post a single tweet"""

        # find current time and id of tweet
        self.db.msetnx({"next_tweet_id": 1})
        n = self.db.get("next_tweet_id")
        time = self.db.time()
        time = time[0] + time[1]/100000

        # set the tweet key
        self.db.hset(f"tweet:{n}", mapping={
            "text":tweet_obj.text,
            "user":tweet_obj.user,
            "time":time,
            "tweet_id":n
        })

        # adding all elements of tweet to user timeline
        followers = self.db.smembers(f"followers:{tweet_obj.user}")
        for follower in followers:
            self.db.zadd(f"timeline:{follower}", {time: n})

        # increment tweet id
        self.db.incr("next_tweet_id")