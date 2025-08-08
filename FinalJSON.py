import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import trafilatura
import sys
import json
import os

class NewsPortalScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common selectors for different news portals
        self.portal_configs = {
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

    def extract_headline_and_body(self, url):
        download = trafilatura.fetch_url(url)

        if download:
            result = trafilatura.extract(download)
            if result:
                parts = result.split('\n', 1)
                headline = parts[0].strip()
                body = parts[1].strip() if len(parts) > 1 else ""
                return headline, body
            else:
                print("Could not extract the article content.") 
        else:
            print("Failed to fetch the URL content.")
        return None, None
   
    def scrape_news_portal(self, portal_url):
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
        
        # Scrape Headlines and URLs
        scraped_news = []
        full_articles = []
        for i, item in enumerate(news_items):
            print(f"{i+1}. HEADLINE: {item['headline']}")
            news_data = {
                'headline': item['headline'],
                'url': item['url'],
            }  
            scraped_news.append(news_data)
            if item['url']:
                print(f"   URL: {item['url']}")
                news_content = self.extract_headline_and_body(item['url'])
                if news_content:
                        print(f"   HEADLINE: {news_content[0]}")
                        print(f"   BODY: {news_content[1]}")
                        full_articles.append({
                        "headline": news_content[0],
                        "url": item['url'],
                        "body": news_content[1]
            })
        if full_articles:
            with open("news_content.json", "w", encoding="utf-8") as f:
                json.dump(full_articles, f, ensure_ascii=False, indent=4)
                print("Full news content saved to news_content.json")


                    
            #         with open("news_content.json", "a", encoding="utf-8") as f:
            #             json.dump(
            #                 f""
            #                 news_content, f, ensure_ascii=False, indent=4)
            #         print("Scraped data saved to news_content.json")
            
                       
            #         print("Saving to:", os.path.abspath("news_content.json"))


            #         print(f"   HEADLINE: {news_content[0]}")
            #         print(f"   BODY: {news_content[1]}")
            print("-" * 50)
        time.sleep(2)  # Respectful scraping delay
        return scraped_news



def main():
    scraper = NewsPortalScraper()
  
    portal_url = input("Enter news portal URL: ").strip()
    if not portal_url.startswith(('http://', 'https://')):
        portal_url = 'https://' + portal_url
        
    try:
        news_data = scraper.scrape_news_portal(portal_url)

        # if news_data:
        #     with open("scraped_news.json", "w", encoding="utf-8") as f:
        #         json.dump(news_data, f, ensure_ascii=False, indent=4)
        #     print("Scraped data saved to scraped_news.json")
            
        #     print("Saving to:", os.path.abspath("scraped_news.json"))

        # else:
        #     print("No news articles found.")
    
        # if news_data:
        #     for item in news_data:
        #         print(f"HEADLINE: {item['headline']}")
        #         if item['url']:
        #             print(f"URL: {item['url']}")
        #             # news_content = extract_headline_and_body(item['url'])
        #             # if news_content:
        #             #     print(f"HEADLINE: {news_content[0]}")
        #             #     print(f"BODY: {news_content[1]}")
        #         print("-" * 50)
        # else:
        #     print("No news articles found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    main()