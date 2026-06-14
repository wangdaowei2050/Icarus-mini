from app.core.config import REDIS_URL
import json
import redis
from app.core.memory.base import BaseMemory

class ShortTermMemory(BaseMemory):

    def __init__(self):
        redis_url = REDIS_URL
        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def _key(self, user_id: int):
        return f"user:{user_id}:short_memory"

    def write(self, user_id: int, content: str):
        key = self._key(user_id)

        self.client.rpush(key, content)
        self.client.ltrim(key, -20, -1)

        self.client.expire(key, 60*60*24)
        
    def read(self, user_id: int):
        key = self._key(user_id)
        return self.client.lrange(key, 0, -1)