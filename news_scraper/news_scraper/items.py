import scrapy

class NewsItem(scrapy.Item):
    headline = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    type = scrapy.Field()  # 'article' or 'video'
    portal = scrapy.Field()
    scraped_at = scrapy.Field()
   