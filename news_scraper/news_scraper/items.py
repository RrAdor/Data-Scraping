import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    headline = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    portal_name = scrapy.Field()
    scraped_at = scrapy.Field()