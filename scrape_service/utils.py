import aiohttp
import asyncio
from typing import List, Dict, Optional
from scrape_service.interface import Product
from cache.cacheDml import CacheDml
from dataStore.modelDml import StorageDml
from requests_html import HTMLResponse, HTMLSession, HTML
from scrape_service.constants import DELAY_IN_SECONDS, MAX_RETRIES

async def getPageHTML(pg_no: int, proxies) -> Dict[str, Optional[str]]:
    url = f'https://dentalstall.com/shop/page/{pg_no}' if pg_no != 1 else f'https://dentalstall.com/shop/'
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False, proxy=proxies.get('http') if proxies else None) as response:
                if response.status == 500:
                    print('retry mechanism', pg_no, response.status)
                    return {
                        'retry_required': True,
                        'data': None
                    }
                else:
                    return {
                        'retry_required': False,
                        'data': await response.text()  # We return the HTML content as text
                    }
        except Exception as e:
            return {
                'retry_required': True,
                'data': None
            }

def extractDataFromHtml(data: str) -> List[Product]:
    html_response = HTML(html=data)
    scrapedProducts: List[Product] = []
    productsHTML = html_response.find('div.mf-shop-content ul.products li')

    for product in productsHTML:
        try:
            name = product.find('h2.woo-loop-product__title a', first=True).text.strip()
            price = product.find('span.price .woocommerce-Price-amount', first=True).text.strip()

            img_element = product.find('img', first=True)
            image_uri = img_element.attrs.get('data-lazy-src') or img_element.attrs.get('data-src') or img_element.attrs.get('src')

            scrapped_product: Product = {
                "name": name,
                "price": price,
                "image_uri": image_uri
            }
            scrapedProducts.append(scrapped_product)
        except Exception as e:
            print(e)
    return scrapedProducts

async def retryFailedPages(failed_pages: List[int], proxies: Dict[str, str]):
    all_products = []
    await asyncio.sleep(DELAY_IN_SECONDS)
    for page in failed_pages:
        print(f"Retrying page {page}")
        for attempt in range(MAX_RETRIES):
            try:
                response = await getPageHTML(page, proxies)
                if response['data']:
                    data = extractDataFromHtml(response['data'])
                    all_products.extend(data)
                    await CacheDml.upsertItemsInCache(data=data)
                    await StorageDml.writeToFile(data=data, transaction_id="retry")
                    break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    print("Retrying...")
                    await asyncio.sleep(3)
                else:
                    print("Max retries reached. Operation failed.")
       
    print(len(all_products))

async def scrapePageTask(page: int, proxies: Dict[str, str], failed_pages: List[int], all_products: List[Product]):
        response = await getPageHTML(page, proxies)
        if response['retry_required']:
            failed_pages.append(page)
        else:
            if response['data']:
                data = extractDataFromHtml(response['data'])
                all_products.extend(data)