from pydantic import BaseModel
from typing import List, TypedDict

class Product(TypedDict):
    name: str
    price: str
    image_uri: str

class ScrapeRequest(BaseModel):
    pg_no: int
    proxy: str

class GetDataFromCacheRequest(BaseModel):
    item_name: List[str]

class NotificationRequest(BaseModel):
    pagesToBeScraped: int
    proxy: str
    transaction_id: str
    pagesScrapedSuccessfully: int
    productsScraped: int
