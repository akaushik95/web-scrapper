from typing import Dict, Optional, List
from dataStore.modelDml import StorageDml
from cache.cacheDml import CacheDml
from notifier import Notifier
from scrape_service.utils import Product, retryFailedPages, scrapePageTask
from scrape_service.interface import GetDataFromCacheRequest, NotificationRequest
import asyncio

class Scrapper:
    def __init__(self, proxy: Optional[str] = None):
        self.proxy = proxy
    
    async def scrapePages(self, pg_no: int, proxy: Optional[str], transaction_id: str = 'default') -> Dict[str, List[Product]]:
        all_products: List[Product] = []
        failed_pages: List[int] = []
        proxies = {}
        if proxy:
            proxies = {
                "http": f'http://{proxy}',
                "https": f'http://{proxy}',
            }
        tasks = []
        for page in range(1, pg_no + 1):
            tasks.append(scrapePageTask(page, proxies, failed_pages, all_products))

        await asyncio.gather(*tasks)

        await CacheDml.upsertItemsInCache(data=all_products)
        await StorageDml.writeToFile(data=all_products, transaction_id=transaction_id)

        if failed_pages:
            asyncio.create_task(retryFailedPages(failed_pages=failed_pages, proxies=proxies))

        asyncio.create_task(Notifier.sendMessage(NotificationRequest(pagesToBeScraped=pg_no, transaction_id=transaction_id, pagesScrapedSuccessfully=pg_no-len(failed_pages), productsScraped=len(all_products))))

        return {'data': all_products}
    
    async def getDataFromCache(self, request: GetDataFromCacheRequest)-> Dict[str, List[Product]]:
        return {'data': await CacheDml.getItemFromCache(request.item_name)}
    
    async def getAllItemsFromDatabase(self) -> Dict[str, List[Product]]:
        return {'data': await StorageDml.readFromFile()}
