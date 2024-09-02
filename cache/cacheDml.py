from cache.cache import LocalCache

class CacheDml:
    async def upsertItemsInCache(data):
        for item in data:
            cacheData = LocalCache.getData(item['name'])
            if cacheData is None:
                LocalCache.setData(item['name'], item)
            else:
                if cacheData['price'] != item['price']:
                    LocalCache.setData(item['name'], item)
            # print(f"{item['name']} added/ updated in cache")
        print('cache update successfully')

    async def getItemFromCache(data):
        objects_list = []
        for item in data:
            objects_list.append(LocalCache.getData(item))
        return objects_list