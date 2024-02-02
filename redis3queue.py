"""The queue comes here to either post tweets or retreive user timelines"""
import redis

HOST = "localhost"
PORT = 6379
DECODE = True


def main():
    connection = redis.Redis(host=HOST, port=PORT, decode_responses=DECODE)
    sub = connection.pubsub()
    sub.subscribe('post')
    sub.subscribe('timelines')
    while True:
        for message in sub.listen():
            if message['type'] == 'message':
                data = message['data']
                vals = [x for x in data.split(',')]
                print(vals)

                if len(vals) == 2:

                    # find current time and id of tweet
                    connection.msetnx({"next_tweet_id": 1})
                    n = connection.get("next_tweet_id")
                    time = connection.time()
                    time = time[0] + time[1] / 100000

                    # set the tweet key
                    connection.hset(f"tweet:{n}", mapping={
                        "text": vals[0],
                        "user": vals[1],
                        "time": time,
                        "tweet_id": n
                    })

                    # adding all elements of tweet to user timeline

                    followers = connection.smembers(f"followers:{vals[1]}")
                    for follower in followers:
                        connection.zadd(f"timeline:{follower}", mapping={n: time})

                    connection.incr("next_tweet_id")


                elif len(vals) ==1:

                    user_id = int(vals[0])
                    tweet_ids = connection.zrevrange(f"timeline:{user_id}", 0, 9)

                    tweets = []
                    for tweet_id in tweet_ids:
                        tweets.append(connection.hgetall(f"tweet:{tweet_id}"))
                    print(tweets)



main()
