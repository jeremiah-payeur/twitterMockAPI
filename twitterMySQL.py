from profiler import Profiler
from dbutils import DBUtils

class TwitterAPI:

    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def randomUser(self):
        """Select a random user from database"""
        query = "select user_id from follows order by rand() limit 1"
        random_user = self.dbu.execute_query(query)

        return random_user

    def insert_followers(self, follow_obj):
        """Insert a single follower relationship in database"""
        self.dbu.insert_one("INSERT INTO FOLLOWS (user_id, follow_id) VALUES(%s, %s)",
                            (follow_obj.user, follow_obj.follow))

    @Profiler.profile
    def getTimelime(self, user_id):
        """Gets one user's home timeline"""
        all_posts = self.dbu.execute('find_timeline', (user_id,))
        return all_posts

    @Profiler.profile
    def postTweet(self, tweet_obj):
        """Post a single tweet"""
        self.dbu.insert_one("INSERT INTO TWEET (user_id, tweet_text) VALUES(%s, %s)", (tweet_obj.user, tweet_obj.text))
        return

    def close(self):
        """close all connections"""
        self.dbu.close()
        return
