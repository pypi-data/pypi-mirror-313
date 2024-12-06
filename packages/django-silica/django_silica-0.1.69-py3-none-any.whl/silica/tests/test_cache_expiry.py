pass

"""
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://default:{CFG_REDIS_PASSWORD}@{CFG_REDIS_HOST}:{CFG_REDIS_PORT}",
        "TIMEOUT": 1 * 60 * 60 * 24,
        # "TIMEOUT": 1,
    }
}"""

# test an exception is raised when cache expires
# test when cache expires, we get an alert telling us we must refresh page