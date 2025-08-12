import time
import pymongo
from urllib.parse import urlparse
from itemadapter import ItemAdapter

class MongoDBPipeline:
    """Pipeline for storing headlines and URLs only"""
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

        if adapter.get('url'):
            self.collection.update_one(
                {'url': adapter['url']},
                {'$set': {
                    'headline': adapter.get('headline'),
                    'url': adapter.get('url'),
                    'timestamp': time.time(),
                    'scraped_full_content': False  # Mark as not fully scraped
                }},
                upsert=True
            )
            spider.logger.info(f"Stored headline: {adapter.get('headline')}")
        return item


class FullContentPipeline:
    """Pipeline for updating articles with full content"""
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
        # Use collection name passed from spider
        self.collection = self.db[getattr(spider, 'collection_name', 'default_articles')]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter.get('url'):
            self.collection.update_one(
                {'url': adapter['url']},
                {'$set': {
                    'body': adapter.get('body'),
                    'scraped_full_content': True,
                    'full_content_timestamp': time.time()
                }}
            )
            spider.logger.info(f"Updated full content for: {adapter.get('headline')}")
        return item