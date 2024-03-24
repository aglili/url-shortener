import redis,os
from dotenv import load_dotenv
load_dotenv()


class RedisConfig:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0,password=os.getenv("REDIS_PASSWORD"))

    def get_redis(self):
        return self.redis
    

