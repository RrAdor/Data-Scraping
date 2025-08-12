import scrapy
from urllib.parse import urlparse
import trafilatura
from news_scraper.items import NewsItem

class FullContentSpider(scrapy.Spider):
    name = 'full_content'
    
    def __init__(self, url=None, collection_name=None, *args, **kwargs):
        super(FullContentSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
            self.collection_name = collection_name

    def parse(self, response):
        """Extract full content for a single article"""
        news_data = NewsItem()
        news_data['url'] = response.url
        
        # Extract content using trafilatura
        download = trafilatura.fetch_url(response.url)
        if download:
            result = trafilatura.extract(download)
            if result:
                parts = result.split('\n', 1)
                news_data['headline'] = parts[0].strip()
                news_data['body'] = parts[1].strip() if len(parts) > 1 else ""
        
        yield news_data