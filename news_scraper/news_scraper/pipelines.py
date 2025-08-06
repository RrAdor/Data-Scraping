import pymongo
from urllib.parse import urlparse
from itemadapter import ItemAdapter

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_news'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

        # Dynamically set collection based on domain
        if spider.start_urls:
            parsed_url = urlparse(spider.start_urls[0])
            domain = parsed_url.netloc.replace('www.', '').replace('.', '_')
            self.collection_name = f"{domain}_articles"
        else:
            self.collection_name = "default_articles"

        self.collection = self.db[self.collection_name]
        spider.logger.info(f"Using collection: {self.collection_name}")

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check for duplicate by URL
        if adapter.get('url'):
            existing = self.collection.find_one({'url': adapter['url']})
            if existing:
                spider.logger.info(f"Duplicate found. Skipping: {adapter['url']}")
                return item

        self.collection.insert_one(adapter.asdict())
        spider.logger.info(f"Inserted into {self.collection_name}: {adapter.get('headline')}")
        return item
