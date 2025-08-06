# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from datetime import datetime
from itemadapter import ItemAdapter
from urllib.parse import urlparse


class NewsScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Add timestamp if not already present
        if not adapter.get('scraped_at'):
            adapter['scraped_at'] = datetime.now().isoformat()
        
        # Clean headline
        if adapter.get('headline'):
            adapter['headline'] = adapter['headline'].strip()
        
        # Add portal name from URL if not already present
        if adapter.get('url') and not adapter.get('portal_name'):
            domain = urlparse(adapter['url']).netloc
            adapter['portal_name'] = domain
        
        # Clean body text
        if adapter.get('body'):
            adapter['body'] = adapter['body'].strip()
        
        return item


class JsonWriterPipeline:
    def open_spider(self, spider):
        self.file = open('scraped_news.json', 'w', encoding='utf-8')
        self.file.write('[\n')
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()
        spider.logger.info("News data saved to scraped_news.json")

    def process_item(self, item, spider):
        if not self.first_item:
            self.file.write(',\n')
        else:
            self.first_item = False
            
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=2)
        self.file.write(line)
        return item


class CsvWriterPipeline:
    def open_spider(self, spider):
        import csv
        self.file = open('scraped_news.csv', 'w', newline='', encoding='utf-8')
        self.fieldnames = ['headline', 'url', 'body', 'portal_name', 'scraped_at']
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()
        spider.logger.info("News data saved to scraped_news.csv")

    def process_item(self, item, spider):
        self.writer.writerow(ItemAdapter(item).asdict())
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        url = adapter.get('url')
        
        if url:
            if url in self.seen_urls:
                spider.logger.info(f"Duplicate item found: {url}")
                raise DropItem(f"Duplicate item found: {url}")
            else:
                self.seen_urls.add(url)
        
        return item