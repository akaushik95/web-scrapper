# create a basic authorisation mechanism
# we can add slack integration here to notify the user which has started the scraping
# or we can also fire an event to which can be consumed by comm-service which can handle all the stuff like which mode of comms to be used.
from scrape_service.interface import NotificationRequest

class Notifier:
    # create slack connection
    # This should be moved to a central place as connection should be made
    # only once during service startup and can be reused again and again
    async def createConnection():
        connection = ''
        return connection
    
    async def sendMessage(data: NotificationRequest):
        print(f"Parsing status of transaction_id :: {data.transaction_id}")
        print(f"Total pages requested :: {data.pagesToBeScraped}")
        print(f"Pages scraped successfully :: {data.pagesScrapedSuccessfully}")
        print(f"Pages up for retry :: {data.pagesToBeScraped-data.pagesScrapedSuccessfully}")
        print(f"Total products scraped :: {data.productsScraped}")
