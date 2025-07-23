# app/utils/cache.py
import redis, os, json
from dotenv import load_dotenv
load_dotenv()

redis_url = os.getenv("REDIS_URL")
valkey = redis.from_url(redis_url, decode_responses=True)

def get_cache(key):
    value = valkey.get(key)
    return json.loads(value) if value else None

def set_cache(key, value, ttl=3600):
    valkey.setex(key, ttl, json.dumps(value))
