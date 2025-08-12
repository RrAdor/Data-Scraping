import scrapy

class NewsItem(scrapy.Item):
    headline = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    portal = scrapy.Field()
    scraped_at = scrapy.Field()
    scraped_full_content = scrapy.Field(default=False)