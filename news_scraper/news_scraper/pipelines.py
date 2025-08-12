from datetime import datetime
import pymongo
from urllib.parse import urlparse
from scrapy.utils.project import get_project_settings

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.settings = get_project_settings()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_news')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            self.mongo_uri,
            connectTimeoutMS=30000,
            socketTimeoutMS=None,
            socketKeepAlive=True
        )
        self.db = self.client[self.mongo_db]
        
        # Create indexes
        self.db.articles.create_index([('url', pymongo.ASCENDING)], unique=True)
        self.db.articles.create_index([('type', pymongo.ASCENDING)])
        
        # For portal-specific headline collections
        if hasattr(spider, 'portal'):
            portal_collection = f"{spider.portal}_headlines"
            self.db[portal_collection].create_index([('url', pymongo.ASCENDING)])

    def process_item(self, item, spider):
        item['scraped_at'] = datetime.now()
        
        try:
            if item['type'] == 'headline':
                # Store in portal-specific collection
                portal = urlparse(item['url']).netloc.replace('.', '_')
                collection = f"{portal}_headlines"
                
                self.db[collection].update_one(
                    {'url': item['url']},
                    {'$set': dict(item)},
                    upsert=True
                )
                spider.logger.debug(f"Stored headline in {collection}: {item['url']}")
                
            else:  # article or video
                self.db.articles.update_one(
                    {'url': item['url']},
                    {'$set': dict(item)},
                    upsert=True
                )
                spider.logger.debug(f"Stored article/video: {item['url']}")
                
        except Exception as e:
            spider.logger.error(f"Error storing item in MongoDB: {str(e)}")
            raise
        
        return item

    def close_spider(self, spider):
        self.client.close()