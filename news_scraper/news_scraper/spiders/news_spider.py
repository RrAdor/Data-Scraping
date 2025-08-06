import scrapy
from urllib.parse import urljoin, urlparse
import trafilatura
import time
from news_scraper.items import NewsItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    
    # Portal configurations
    portal_configs = {
        'bbc.com': {
            'headline_selectors': [
                'h2[data-testid="card-headline"]',
                'h3[data-testid="card-headline"]',
                'h2',
                'h3.gs-c-promo-heading__title'
            ],
            'link_selectors': [
                'a[data-testid="internal-link"]',
                'h2[data-testid="card-headline"] a',
                'h3[data-testid="card-headline"] a'
            ],
            'article_content_selectors': [
                '[data-component="text-block"] p',
                'div[data-component="text-block"]',
                '.story-body p',
                'article p'
            ]
        },
        'prothomalo.com': {
            'headline_selectors': [
                'h1.headline',
                'h2.headline',
                'h3.story_title',
                '.title a',
                'h2',
                'h3'
            ],
            'link_selectors': [
                '.title a',
                '.story_title a',
                'h2 a',
                'h3 a'
            ],
            'article_content_selectors': [
                '.story_content p',
                '.news_content p',
                'article p',
                '.content p'
            ]
        },
        'thedailystar.net': {
            'headline_selectors': [
                'h2.title',
                'h3.title',
                '.article-title',
                '.news-title',
                '.story-title',
                'h2',
                'h3'
            ],
            'link_selectors': [
                '.title a',
                '.article-title a',
                '.news-title a',
                'h2 a',
                'h3 a',
                'a[href*="/news/"]',
                'a[href*="/article/"]'
            ],
            'article_content_selectors': [
                '.article-content p',
                '.news-content p',
                '.story-content p',
                '.content-body p',
                'article p',
                '.content p'
            ]
        },
        'cnn.com': {
            'headline_selectors': [
                'h3.cd__headline',
                '.cd__headline',
                'h2.headline',
                'h3.headline',
                '.card-media__headline',
                '.article-title',
                'h2',
                'h3'
            ],
            'link_selectors': [
                '.cd__headline a',
                'h3.cd__headline a',
                '.card-media__headline a',
                'a[data-link-type="article"]',
                'h2 a',
                'h3 a',
                'a[href*="/2024/"]',
                'a[href*="/2025/"]'
            ],
            'article_content_selectors': [
                '.article__content p',
                '.zn-body__paragraph',
                'div[data-module="ArticleBody"] p',
                '.pg-rail-tall__body p',
                'article p',
                '.content p'
            ]
        },
        'news24bd.tv': {
            'headline_selectors': [
                '.news-title',
                '.article-title',
                '.post-title',
                'h2.title',
                'h3.title',
                '.headline',
                'h2',
                'h3'
            ],
            'link_selectors': [
                '.news-title a',
                '.article-title a',
                '.post-title a',
                'h2.title a',
                'h3.title a',
                '.headline a',
                'h2 a',
                'h3 a',
                'a[href*="/news/"]'
            ],
            'article_content_selectors': [
                '.news-content p',
                '.article-content p',
                '.post-content p',
                '.story-content p',
                '.content-body p',
                'article p',
                '.content p'
            ]
        },
        'default': {
            'headline_selectors': [
                'h1', 'h2', 'h3',
                '.headline', '.title',
                '[class*="headline"]', '[class*="title"]'
            ],
            'link_selectors': [
                'h1 a', 'h2 a', 'h3 a',
                '.headline a', '.title a',
                'article a'
            ],
            'article_content_selectors': [
                'article p', '.content p', '.article-content p',
                '.post-content p', '.entry-content p',
                '.story-content p', '.news-content p'
            ]
        }
    }

    def __init__(self, portal_url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        if portal_url:
            if not portal_url.startswith(('http://', 'https://')):
                portal_url = 'https://' + portal_url
            self.start_urls = [portal_url]
            self.allowed_domains = [urlparse(portal_url).netloc]

    def get_portal_config(self, url):
        """Get configuration based on the portal URL"""
        domain = urlparse(url).netloc.lower()
        
        for portal_key in self.portal_configs:
            if portal_key in domain:
                return self.portal_configs[portal_key]
        
        return self.portal_configs['default']

    def extract_headline_and_body(self, url):
        """Extract article content using trafilatura"""
        download = trafilatura.fetch_url(url)

        if download:
            result = trafilatura.extract(download)
            if result:
                parts = result.split('\n', 1)
                headline = parts[0].strip()
                body = parts[1].strip() if len(parts) > 1 else ""
                return headline, body
            else:
                self.logger.warning(f"Could not extract article content from {url}")
        else:
            self.logger.warning(f"Failed to fetch URL content: {url}")
        return None, None

    def parse(self, response):
        """Parse the main news portal page"""
        self.logger.info(f"Scraping news from: {response.url}")
        self.logger.info("=" * 60)
        
        # Get portal-specific configuration
        config = self.get_portal_config(response.url)
        
        # Extract headlines and links
        news_items = []
        
        # Try different selectors to find headlines with links
        for link_selector in config['link_selectors']:
            links = response.css(link_selector)
            if links:
                for link in links:
                    headline_text = link.css('::text').get()
                    if headline_text:
                        headline_text = headline_text.strip()
                    
                    if headline_text and len(headline_text) > 10:
                        href = link.css('::attr(href)').get()
                        if href:
                            full_url = urljoin(response.url, href)
                            news_items.append({
                                'headline': headline_text,
                                'url': full_url
                            })
                break
        
        # If no links found with text, try to extract from parent elements
        if not news_items:
            for link_selector in config['link_selectors']:
                links = response.css(link_selector)
                if links:
                    for link in links:
                        # Try to get text from the link or its parent
                        headline_text = link.css('::text').get()
                        if not headline_text:
                            # Try to get text from parent element
                            parent = link.xpath('..')
                            if parent:
                                headline_text = parent.css('::text').get()
                        
                        if headline_text:
                            headline_text = headline_text.strip()
                        
                        if headline_text and len(headline_text) > 10:
                            href = link.css('::attr(href)').get()
                            if href:
                                full_url = urljoin(response.url, href)
                                news_items.append({
                                    'headline': headline_text,
                                    'url': full_url
                                })
                    if news_items:
                        break
        
        # If still no links found, try to find headlines without links
        if not news_items:
            for headline_selector in config['headline_selectors']:
                headlines = response.css(headline_selector)
                if headlines:
                    for headline in headlines:
                        headline_text = headline.css('::text').get()
                        if headline_text:
                            headline_text = headline_text.strip()
                        
                        if headline_text and len(headline_text) > 10:
                            news_items.append({
                                'headline': headline_text,
                                'url': None
                            })
                    if news_items:
                        break

        if not news_items:
            self.logger.warning("No news items found. The website structure might have changed.")
            return

        self.logger.info(f"Found {len(news_items)} news items\n")

        # Process each news item
        for i, item in enumerate(news_items):
            self.logger.info(f"{i+1}. HEADLINE: {item['headline']}")
            
            news_data = NewsItem()
            news_data['headline'] = item['headline']
            news_data['url'] = item['url']
            news_data['body'] = None
            
            if item['url']:
                self.logger.info(f"   URL: {item['url']}")
                # Extract full article content
                headline, body = self.extract_headline_and_body(item['url'])
                if headline and body:
                    news_data['body'] = body
                    self.logger.info(f"   EXTRACTED HEADLINE: {headline}")
                    self.logger.info(f"   BODY: {body[:200]}...")  # Show first 200 chars
            
            self.logger.info("-" * 50)
            
            # Add respectful delay
            time.sleep(2)
            
            yield news_data

    def closed(self, reason):
        """Called when spider closes"""
        self.logger.info(f"Spider closed: {reason}")