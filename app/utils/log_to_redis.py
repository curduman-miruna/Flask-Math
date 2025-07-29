import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def log_to_redis(level, message, extra=None):
    log_entry = {
        "level": level,
        "message": message,
        "extra": extra or {},
        "timestamp": redis_client.time()[0]
    }
    redis_client.rpush(f"{level}-{redis_client.time()[0]}", json.dumps(log_entry))
