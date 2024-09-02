from pydantic import BaseModel
from typing import List, TypedDict
from uuid import UUID

class Product(BaseModel):
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
    transaction_id: UUID
    pagesScrapedSuccessfully: int
    productsScraped: int
