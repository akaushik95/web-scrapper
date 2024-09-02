from cachetools import TTLCache
cache = TTLCache(maxsize=10000, ttl=3000)

class LocalCache:
    def getData(key: str):
        return cache.get(key)
    
    def setData(key: str, value: dict):
        cache[key] = value