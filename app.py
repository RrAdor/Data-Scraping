from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import json
import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import trafilatura
from youtube_transcript_api import YouTubeTranscriptApi
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Import your existing scraper class
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
                print("Could not extract the article content.") 
        else:
            print("Failed to fetch the URL content.")
        return None, None
   
    def scrape_news_portal_api(self, portal_url, max_articles=20, extract_full_content=True):
        """API version of portal scraping"""
        print(f"Scraping news from: {portal_url}")
        
        # Get the main page
        soup = self.fetch_page(portal_url)
        if not soup:
            return {"error": "Failed to fetch the portal page", "articles": []}
        
        # Get portal-specific configuration
        config = self.get_portal_config(portal_url)
        
        # Extract headlines and links
        news_items = self.extract_headlines_and_links(soup, config, portal_url)
        
        if not news_items:
            return {"error": "No news items found", "articles": []}
        
        # Limit articles if specified
        if max_articles != "all":
            news_items = news_items[:int(max_articles)]
        
        scraped_articles = []
        for i, item in enumerate(news_items):
            article_data = {
                'id': str(uuid.uuid4()),
                'headline': item['headline'],
                'url': item['url'],
                'body': None,
                'extracted_at': datetime.now().isoformat()
            }
            
            if extract_full_content and item['url']:
                headline, body = self.extract_headline_and_body(item['url'])
                if headline and body:
                    article_data['headline'] = headline
                    article_data['body'] = body
            
            scraped_articles.append(article_data)
            time.sleep(1)  # Respectful scraping delay
        
        return {"articles": scraped_articles, "total": len(scraped_articles)}
    
    def extract_single_article_api(self, url):
        """API version of single article extraction"""
        headline, body = self.extract_headline_and_body(url)
        
        if headline or body:
            return {
                'id': str(uuid.uuid4()),
                'headline': headline or "Could not extract headline",
                'url': url,
                'body': body or "Could not extract body content",
                'extracted_at': datetime.now().isoformat()
            }
        else:
            return {"error": "Could not extract article content"}
    
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
    
    def get_youtube_transcript_api(self, video_url, preferred_lang='auto'):
        """API version of YouTube transcript extraction"""
        try:
            video_id = self.extract_video_id(video_url)
            if not video_id:
                return {"error": "Invalid YouTube URL"}
            
            # Create API instance
            api = YouTubeTranscriptApi()
            
            # List available transcripts
            transcript_list = api.list(video_id)
            transcripts = list(transcript_list)
            
            if not transcripts:
                return {"error": "No transcripts available for this video"}
            
            # Try to find transcript in preferred order
            preferred_languages = ['bn', 'bn-BD', 'en', 'en-US', 'en-GB'] if preferred_lang == 'auto' else [preferred_lang, 'en']
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
            
            # Group transcript into paragraphs (every 10 sentences or 2 minutes)
            paragraphs = []
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
                        paragraphs.append({
                            'timestamp': timestamp,
                            'text': paragraph_text
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
                paragraphs.append({
                    'timestamp': timestamp,
                    'text': paragraph_text
                })

            return {
                'videoId': video_id,
                'language': selected_transcript.language_code,
                'isGenerated': selected_transcript.is_generated,
                'paragraphs': paragraphs,
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Could not extract transcript: {str(e)}"}

# Initialize scraper
scraper = NewsPortalScraper()

@app.route('/')
def home():
    """Serve the main web interface"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        return jsonify({
            "message": "News & Video Content Extractor API",
            "note": "Web interface (index.html) not found. Please make sure index.html is in the same directory.",
            "endpoints": {
                "/api/scrape-portal": "POST - Scrape news portal",
                "/api/extract-article": "POST - Extract single article",
                "/api/extract-transcript": "POST - Extract YouTube transcript"
            }
        })

@app.route('/style.css')
def serve_css():
    """Serve the CSS file"""
    return send_from_directory('.', 'style.css', mimetype='text/css')

@app.route('/app.js')
def serve_js():
    """Serve the JavaScript file"""
    return send_from_directory('.', 'app.js', mimetype='application/javascript')

@app.route('/api')
def api_info():
    return jsonify({
        "message": "News & Video Content Extractor API",
        "endpoints": {
            "/api/scrape-portal": "POST - Scrape news portal",
            "/api/extract-article": "POST - Extract single article",
            "/api/extract-transcript": "POST - Extract YouTube transcript"
        }
    })

@app.route('/api/scrape-portal', methods=['POST'])
def scrape_portal():
    try:
        data = request.json
        url = data.get('url', '').strip()
        max_articles = data.get('maxArticles', 20)
        extract_full_content = data.get('extractFullContent', True)
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        result = scraper.scrape_news_portal_api(url, max_articles, extract_full_content)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract-article', methods=['POST'])
def extract_article():
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        result = scraper.extract_single_article_api(url)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract-transcript', methods=['POST'])
def extract_transcript():
    try:
        data = request.json
        url = data.get('url', '').strip()
        language = data.get('language', 'auto')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        result = scraper.get_youtube_transcript_api(url, language)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze URL to determine the type of content"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Check if it's YouTube
        if 'youtube.com' in url or 'youtu.be' in url:
            return jsonify({"type": "youtube", "message": "YouTube video detected"})
        
        # Check if it's a single article (contains digits in URL path)
        if re.search(r'\/\d+', url) or '/article/' in url or '/story/' in url:
            return jsonify({"type": "single", "message": "Single article detected"})
        
        # Default to portal
        return jsonify({"type": "portal", "message": "News portal detected"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
