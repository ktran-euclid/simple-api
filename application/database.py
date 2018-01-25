from redis import StrictRedis

class Database(object):
    def __init__(self, index, redis_host='localhost'):
        self.database = StrictRedis(host=redis_host, db=index, port=6379)

    def get_entry(self, key):
        return self.database.hgetall(key)

    def save_entry(self, name, key, value):
        self.database.hset(name, key, value)

    def keys(self):
        return self.database.keys()

    def delete(self, key):
        self.database.delete(key)
