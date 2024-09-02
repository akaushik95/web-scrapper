from typing import Optional
from fastapi import Depends, FastAPI
from scrape_service.scraper import Scrapper
from authentication import Authenticator
import logging
import uuid
from scrape_service.interface import ScrapeRequest, GetDataFromCacheRequest
import asyncio 

ScaperService = Scrapper()

# setting up logger config
logging.basicConfig(
    filename='flowlogs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()

# API endpoints
@app.get("/scrapePages/{pg_no}")
async def scrapePages(pg_no: int, proxy: Optional[str] = None, token: str = Depends(Authenticator.basicAuthentication)):
    transaction_id = uuid.uuid1()
    logging.info({'transaction_id': transaction_id, 'pg_no': pg_no, 'proxy': proxy, 'methodName': 'scrapePage'})
    return await ScaperService.scrapePages(pg_no=pg_no, proxy=proxy, transaction_id=transaction_id)

@app.post("/getScrapedDataFromCacheById")
async def getDataFromCache(request: GetDataFromCacheRequest):
    transaction_id = uuid.uuid1()
    logging.info({'transaction_id': transaction_id, 'methodName': 'getDataFromCache'})
    return await ScaperService.getDataFromCache(request=request)

@app.get("/getAllItemsFromDatabase")
async def getAllItemsFromDatabase():
    transaction_id = uuid.uuid1()
    logging.info({'transaction_id': transaction_id, 'methodName': 'getAllItemsFromDatabase'})
    return await ScaperService.getAllItemsFromDatabase()

