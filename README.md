1. clone the repo
2. create a virtual env
3. install the required dependencies 
    1. pip3 install "fastapi[standard]"
    2. pip3 install cachetools
    3. pip3 install aiohttp
    4. pip3 install requests_html
4. To start the server: uvicorn main:app --reload / fastapi dev main.py 
5. Routes
    1. GET /scrapePages?<pg_no>=&<proxy>=
        X-Token=
    2. POST /getScrapedDataFromCacheById
        {
            "item_name": ["3m Espe Relyx Ceramic Primer..."]
        }
    3. GET /getAllItemsFromDatabase
6. Folder structure
    ├── README.md
    ├── authentication.py
    ├── cache
    │   ├── cache.py    // this can be changes with redis
    │   └── cacheDml.py
    ├── dataStore
    │   ├── connection.py
    │   ├── localstorage.csv    // this can be changes with mongo/mysql
    │   ├── model.py
    │   └── modelDml.py
    ├── flowlogs.log    // this contains all the logs generated when we call api.
    ├── main.py
    ├── notifier.py
    ├── requirements.txt
    └── scrape_service
        ├── constants.py
        ├── interface.py
        ├── scraper.py
        └── utils.py
7. Max retries = 3 and delay in retry of of 3sec.
8. can incorporate any db like mongo/mysql (comments in the actual file)
9. can include slack api to send message after scrapping. (comments in the actual file)
10. Authentication token: "testing-token"
11. Steps to start a proxy
    1. pip3 install proxy.py
    2. proxy --hostname 127.0.0.1 --port 8765

