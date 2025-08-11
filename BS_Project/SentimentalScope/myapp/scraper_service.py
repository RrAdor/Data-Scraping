import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import trafilatura
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from bson import ObjectId
from .mongodb_connection import mongodb

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
                for link in links[:20]:  # Limit to first 20 items
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
                    for headline in headlines[:20]:
                        headline_text = headline.get_text(strip=True)
                        if headline_text and len(headline_text) > 10:
                            news_items.append({
                                'headline': headline_text,
                                'url': None
                            })
                    break
        
        return news_items

    def extract_headline_and_body(self, url):
        """Extract headline and body from a single article URL"""
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
   
    def scrape_news_portal_headlines_only(self, portal_url):
        """Scrape only headlines from a news portal (first stage)"""
        soup = self.fetch_page(portal_url)
        if not soup:
            return []
        
        config = self.get_portal_config(portal_url)
        news_items = self.extract_headlines_and_links(soup, config, portal_url)
        
        if not news_items:
            return []
        
        # Return only headlines and URLs
        scraped_news = []
        for item in news_items:
            news_data = {
                'headline': item['headline'],
                'url': item['url'],
            }  
            scraped_news.append(news_data)
        
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
    
    def get_youtube_transcript_data(self, video_id):
        """Get structured transcript data from YouTube video"""
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)
            transcripts = list(transcript_list)
            
            if not transcripts:
                return None, "No transcripts available for this video"
            
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
            
            # Group transcript into paragraphs
            full_transcript = []
            current_paragraph = []
            last_timestamp = 0
            paragraph_count = 1
            
            for item in transcript_data:
                current_paragraph.append(item.text.strip())
                
                # Create new paragraph every 2 minutes or every 10 sentences
                if (item.start - last_timestamp > 120) or (len(current_paragraph) >= 10):
                    if current_paragraph:
                        minutes = int(item.start // 60)
                        seconds = int(item.start % 60)
                        timestamp = f"[{minutes:02d}:{seconds:02d}]"
                        
                        paragraph_text = ' '.join(current_paragraph)
                        full_transcript.append({
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
                full_transcript.append({
                    'timestamp': timestamp,
                    'paragraph': paragraph_text
                })

            return full_transcript, "Success"
            
        except Exception as e:
            return None, f"Could not extract transcript: {str(e)}"
        
    def is_single_article_url(self, url):
        """Check if URL points to a single article"""
        for char in reversed(url.strip('/')):
            if char.isdigit():
                return True
            if char in ['/', '?', '#']:
                break
        return False


class ScrapedContentService:
    def __init__(self):
        self.db = mongodb.get_database()
        self.collection = self.db['scraped_content']
    
    def save_headlines_only(self, user_id, content_type, headlines_data, source_url):
        """Save only headlines and URLs initially"""
        documents = []
        for item in headlines_data:
            doc = {
                'user_id': user_id,
                'content_type': content_type,  # 'article', 'portal', 'youtube'
                'storage_level': 'headline_only',
                'headline': item['headline'],
                'source_url': item['url'] if item['url'] else source_url,
                'original_url': source_url,  # The URL user originally entered
                'full_content': None,
                'transcript_data': None,
                'scraped_at': datetime.now(),
                'viewed_at': None,
                'analyzed': False
            }
            documents.append(doc)
        
        if documents:
            result = self.collection.insert_many(documents)
            return result.inserted_ids
        return []
    
    def update_with_full_content(self, document_id, full_content_data):
        """Update existing document with full content when viewed"""
        update_data = {
            'storage_level': 'full_content',
            'viewed_at': datetime.now()
        }
        
        if 'body' in full_content_data:
            update_data['full_content'] = full_content_data['body']
        
        if 'transcript' in full_content_data:
            update_data['transcript_data'] = full_content_data['transcript']
        
        result = self.collection.update_one(
            {'_id': ObjectId(document_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def get_user_headlines(self, user_id):
        """Get all scraped headlines for a user"""
        return list(self.collection.find(
            {'user_id': user_id},
            {'headline': 1, 'source_url': 1, 'content_type': 1, 'scraped_at': 1, 'storage_level': 1}
        ).sort('scraped_at', -1))
    
    def get_full_content(self, document_id):
        """Get full content for analysis"""
        return self.collection.find_one({'_id': ObjectId(document_id)})
    
    def clear_user_headlines(self, user_id):
        """Clear all scraped content for a user (both headline_only and full_content)"""
        result = self.collection.delete_many({'user_id': user_id})
        return result.deleted_count
