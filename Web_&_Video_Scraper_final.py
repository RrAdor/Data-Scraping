import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import trafilatura
from youtube_transcript_api import YouTubeTranscriptApi
import json

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
        full_article = []
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
                    full_article.append({
                        'headline': news_content[0],
                        'url': item['url'],
                        'body': news_content[1]
                    })
                    if full_article:
                        with open('news_articles.json', 'w', encoding='utf-8') as f:
                            json.dump(full_article, f, ensure_ascii=False, indent=4)
                            print("News articles saved to 'news_articles.json'")
                print("-" * 50)
        time.sleep(2)  # Respectful scraping delay
        return scraped_news
    
    def extract_video_id(self, url):
        """Extract YouTube video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_youtube_transcript(self, video_id):
        """Get transcript from YouTube video"""
        try:
            # Create API instance
            api = YouTubeTranscriptApi()
            
            # List available transcripts
            transcript_list = api.list(video_id)
            transcripts = list(transcript_list)
            
            if not transcripts:
                return "No transcripts available for this video"
            
            # Try to find transcript in preferred order: Bangla, English, then any
            preferred_languages = ['bn', 'bn-BD', 'en', 'en-US', 'en-GB']
            selected_transcript = None
            
            for lang_code in preferred_languages:
                for transcript_info in transcripts:
                    if transcript_info.language_code == lang_code:
                        selected_transcript = transcript_info
                        break
                if selected_transcript:
                    break
            
            # If no preferred language found, use the first available
            if selected_transcript is None:
                selected_transcript = transcripts[0]
            
            # Fetch the transcript data
            transcript_data = selected_transcript.fetch()
            
            # Create structured text output for terminal
            print(f"\n{'='*60}")
            print(f"YOUTUBE VIDEO TRANSCRIPT")
            print(f"{'='*60}")
            print(f"Language: {selected_transcript.language_code}")
            print(f"Type: {'Auto-generated' if selected_transcript.is_generated else 'Manual'}")
            print(f"{'='*60}\n")
            
            # Group transcript into paragraphs (every 10 sentences or 2 minutes)
            full_article = []
            current_paragraph = []
            last_timestamp = 0
            paragraph_count = 1
            
            for item in transcript_data:
                current_paragraph.append(item.text.strip())
                
                # Create new paragraph every 2 minutes or every 10 sentences
                if (item.start - last_timestamp > 120) or (len(current_paragraph) >= 10):
                    if current_paragraph:
                        # Format timestamp
                        minutes = int(item.start // 60)
                        seconds = int(item.start % 60)
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        
                        paragraph_text = ' '.join(current_paragraph)
                        print(f"{timestamp} - Paragraph {paragraph_count}:")
                        print(f"{paragraph_text}\n")
                        print("-" * 60)
                        full_article.append({
                            'timestamp': timestamp,
                            'paragraph': paragraph_text
                        })
                        
                        current_paragraph = []
                        last_timestamp = item.start
                        paragraph_count += 1
            
            # Add remaining text as final paragraph
            if current_paragraph:
                final_item = transcript_data[-1]
                minutes = int(final_item.start // 60)
                seconds = int(final_item.start % 60)
                timestamp = f"[{minutes:02d}:{seconds:02d}]"
                paragraph_text = ' '.join(current_paragraph)
                print(f"{timestamp} - Paragraph {paragraph_count}:")
                print(f"{paragraph_text}\n")
                print("-" * 60)
                full_article.append({
                    'timestamp': timestamp,
                    'paragraph': paragraph_text
                })

            # Save the transcript to a JSON file
                if full_article:
                    with open('youtube_transcript.json', 'w', encoding='utf-8') as f:
                        json.dump(full_article, f, ensure_ascii=False, indent=4)
                        print("Transcript saved to 'youtube_transcript.json'")
            return "Transcript extracted successfully"
            
        except Exception as e:
            return f"Could not extract transcript: {str(e)}"
        
    def is_single_article_url(self,url) -> bool:
        """
        Checks if the given URL points to a single news article.
        Returns True if it's a single article, False if it's a portal page.
        """
        for char in reversed(url.strip('/')):
            if char.isdigit():
                return True  # Found a digit → likely a single article
            if char in ['/', '?', '#']:
                break  # Reached end of last slug before finding a digit
        return False  # No digit found → portal page


def main():
    scraper = NewsPortalScraper()
  
    portal_url = input("Enter news portal URL: ").strip()
    if not portal_url.startswith(('http://', 'https://')):
        portal_url = 'https://' + portal_url

    video_id = scraper.extract_video_id(portal_url)
    is_single_article = scraper.is_single_article_url(portal_url)
        
    try:
        if video_id:
            print(f"Extracting transcript for YouTube video ID: {video_id}")
            transcript_result = scraper.get_youtube_transcript(video_id)
            if transcript_result != "Transcript extracted successfully":
                print(f"Error: {transcript_result}")
        elif is_single_article:
            content = scraper.extract_headline_and_body(portal_url)
            if content:
                print(f"HEADLINE: {content[0]}")
                print(f"BODY: {content[1]}")
            else:
                print("Could not extract the article content.")
        else:
            scraper.scrape_news_portal(portal_url)

    except Exception as e:
        print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    main()
    