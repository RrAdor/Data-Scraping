import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

class NewsPortalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common selectors for different news portals
        self.portal_configs = {
            # 'bbc.com': {
            #     'headline_selectors': [
            #         'h2[data-testid="card-headline"]',
            #         'h3[data-testid="card-headline"]',https://www.bbc.com/
            #         'h2',
            #         'h3.gs-c-promo-heading__title'
            #     ],
            #     'link_selectors': [
            #         'a[data-testid="internal-link"]',
            #         'h2[data-testid="card-headline"] a',
            #         'h3[data-testid="card-headline"] a'
            #     ],
            #     'article_content_selectors': [
            #         '[data-component="text-block"] p',
            #         'div[data-component="text-block"]',
            #         '.story-body p',
            #         'article p'
            #     ]
            # },
            # 'prothomalo.com': {
            #     'headline_selectors': [
            #         'h1.headline',
            #         'h2.headline',
            #         'h3.story_title',
            #         '.title a',
            #         'h2',
            #         'h3'
            #     ],
            #     'link_selectors': [
            #         '.title a',
            #         '.story_title a',
            #         'h2 a',
            #         'h3 a'
            #     ],
            #     'article_content_selectors': [
            #         '.story_content p',
            #         '.news_content p',
            #         'article p',
            #         '.content p'
            #     ]
            # },
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
    
    def get_portal_config(self, url):
        """Get configuration based on the portal URL"""
        domain = urlparse(url).netloc.lower()
        
        for portal_key in self.portal_configs:
            if portal_key in domain:
                return self.portal_configs[portal_key]
        
        return self.portal_configs['default']
    
    def fetch_page(self, url):
        """Fetch webpage content"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_headlines_and_links(self, soup, config, base_url):
        """Extract headlines and their corresponding links"""
        news_items = []
        
        # Try different selectors to find headlines with links
        for link_selector in config['link_selectors']:
            links = soup.select(link_selector)
            if links:
                for link in links:  # Limit to first 20 items
                    headline_text = link.get_text(strip=True)
                    if headline_text and len(headline_text) > 10:  # Filter out short/empty text
                        href = link.get('href')
                        if href:
                            full_url = urljoin(base_url, href)
                            news_items.append({
                                'headline': headline_text,
                                'url': full_url
                            })
                break  
        
        # If no links found, try to find headlines without links
        if not news_items:
            for headline_selector in config['headline_selectors']:
                headlines = soup.select(headline_selector)
                if headlines:
                    for headline in headlines:
                        headline_text = headline.get_text(strip=True)
                        if headline_text and len(headline_text) > 10:
                            news_items.append({
                                'headline': headline_text,
                                'url': None
                            })
                    break
        
        return news_items
    
    def scrape_article_content(self, article_url, config):
        """Scrape the full article content from article URL"""
        if not article_url:
            return "Article URL not available"
        
        soup = self.fetch_page(article_url)
        if not soup:
            return "Could not fetch article content"
        
        # Try different selectors to find article content
        content_paragraphs = []
        
        for selector in config['article_content_selectors']:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 20:  # Filter out short paragraphs
                        content_paragraphs.append(text)
                break
        
        if content_paragraphs:
            return '\n\n'.join(content_paragraphs)  
        else:
            return "Article content not found or not accessible"
    
    def scrape_news_portal(self, portal_url, include_full_articles=True):
        """Main method to scrape news from a portal"""
        print(f"Scraping news from: {portal_url}")
        print("=" * 60)
        
        # Get the main page
        soup = self.fetch_page(portal_url)
        if not soup:
            return []
        
        # Get portal-specific configuration
        config = self.get_portal_config(portal_url)
        
        # Extract headlines and links
        news_items = self.extract_headlines_and_links(soup, config, portal_url)
        
        if not news_items:
            print("No news items found. The website structure might have changed.")
            return []
        
        print(f"Found {len(news_items)} news items\n")
        
        # Scrape full articles if requested
        scraped_news = []
        for i, item in enumerate(news_items):
            print(f"{i+1}. HEADLINE: {item['headline']}")
            
            article_content = ""
            if include_full_articles and item['url']:
                print("   Fetching full article...")
                article_content = self.scrape_article_content(item['url'], config)
                time.sleep(1)  
            
            news_data = {
                'headline': item['headline'],
                'url': item['url'],
                'content': article_content
            }
            
            scraped_news.append(news_data)
            
            if include_full_articles:
                print(f"   CONTENT: {article_content}...")
            if item['url']:
                print(f"   URL: {item['url']}")
            print("-" * 50)
        
        return scraped_news

def main():
    scraper = NewsPortalScraper()
    
    while True:
        print("\n" + "="*60)
        print("NEWS PORTAL SCRAPER")
        print("="*60)
        
        portal_url = input("Enter news portal URL (or 'quit' to exit): ").strip()
        
        if portal_url.lower() == 'quit':
            break
        
        if not portal_url.startswith(('http://', 'https://')):
            portal_url = 'https://' + portal_url
        
        # Ask if user wants full articles
        full_articles = input("Do you want to scrape full articles? (y/n, default=y): ").strip().lower()
        include_full_articles = full_articles != 'n'
        
        print(f"\nStarting scraping...")
        
        try:
            news_data = scraper.scrape_news_portal(portal_url, include_full_articles)
            
            if news_data:
                print(f"\n Successfully scraped {len(news_data)} news items!")
                
                # Ask if user wants to save to file
                save_file = input("\nSave results to file? (y/n): ").strip().lower()
                if save_file == 'y':
                    filename = f"news_{urlparse(portal_url).netloc}_{int(time.time())}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"News scraped from: {portal_url}\n")
                        f.write(f"Scraped on: {time.ctime()}\n")
                        f.write("="*60 + "\n\n")
                        
                        for i, item in enumerate(news_data):
                            f.write(f"{i+1}. HEADLINE: {item['headline']}\n")
                            if item['url']:
                                f.write(f"   URL: {item['url']}\n")
                            if item['content']:
                                f.write(f"   CONTENT:\n   {item['content']}\n")
                            f.write("-"*50 + "\n\n")
                    
                    print(f"Results saved to: {filename}")
            else:
                print("No news items could be scraped.")
                
        except Exception as e:
            print(f"Error occurred: {e}")
        
        print("\n" + "="*60)

if __name__ == "__main__":
    main()