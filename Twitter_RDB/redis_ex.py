import redis
import time


# create connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.flushall()

# add some keys
r.set('foo', 100)
r.incr('foo')
x = r.get('foo')
print(x)

r.lpush('Friends', 'joe', 'ann', 'cal')
friends = r.lrange('Friends', 0, -1)
print(friends, type(friends))


# store 1000000 keys
N = 100000
now = time.time()
r.flushall()
for i in range(N):
    r.set(f'key:{i}', f"this is tweet {i}")

new = time.time()

print("total time:", new-now)
print("total time/tweet:", (new-now)/N)
print("tweet/sec:", N/(new-now))
