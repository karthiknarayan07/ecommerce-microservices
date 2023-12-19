import json
from django.conf import settings
import redis
import pickle

class RedisSingleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RedisSingleton, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def __init__(self):
        if not self.connection:
            self.connection = redis.StrictRedis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                # password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )

    def get_connection(self):
        return self.connection

redis_instance = RedisSingleton()

def SetValue(key, value, ttl=0):
    data = {key: value}
    if ttl:
        redis_connection = redis_instance.get_connection()
        redis_connection.set(key, json.dumps(data), ttl)
    else:
        redis_connection = redis_instance.get_connection()
        redis_connection.set(key, json.dumps(data))

def SetValueWithExpiry(key, value, ttl):
    redis_connection = redis_instance.get_connection()
    redis_connection.set(key, value, ttl)

def DeleteKey(key):
    redis_connection = redis_instance.get_connection()
    redis_connection.delete(key)

def GetValue(key):
    redis_connection = redis_instance.get_connection()
    value = redis_connection.get(key)
    return value

def CheckExist(key):
    redis_connection = redis_instance.get_connection()
    value = redis_connection.exists(key)
    return value


def SetModelObject(key, model_instance, ttl=0):
    serialized_model = pickle.dumps(model_instance)
    redis_connection = redis_instance.get_connection()
    redis_connection.set(key, serialized_model, ttl)
    

def GetModelObject(key):
    redis_connection = redis_instance.get_connection()
    serialized_model = redis_connection.get(key)
    if serialized_model is not None:
        model_instance = pickle.loads(serialized_model)
        return model_instance
    else:
        return None



# Example usage:
# setvalue("example_key", "example_value", ttl=3600)
# retrieved_value = getvalue("example_key")
# print("Retrieved value from Redis:", retrieved_value)
# deleteKey("example_key")
# exists = checkExist("example_key")
# print("Key exists in Redis:", exists)
