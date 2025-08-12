from django.views import View
from django.shortcuts import render, redirect
from urllib.parse import urlparse, quote
import subprocess
import re
import pymongo

def get_mongo_db():
    client = pymongo.MongoClient(settings.MONGO_URI)
    return client[settings.MONGO_DB]

def is_youtube_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    return re.match(youtube_regex, url)

class HomeView(View):
    def get(self, request):
        db = get_mongo_db()
        # Show recent headlines from ALL portals (optional)
        recent_headlines = list(db.articles.find(
            {'type': 'article'}).sort('scraped_at', -1).limit(10))
        return render(request, 'newsapp/home.html', {
            'recent_headlines': recent_headlines
        })

class ScrapePortalView(View):
    def post(self, request):
        url = request.POST.get('url', '').strip()
        if not url:
            messages.error(request, "Please provide a URL")
            return redirect('home')

        try:
            portal = urlparse(url).netloc.replace('.', '_')  # bbc.com → bbc_com
            
            if is_youtube_url(url):
                subprocess.run([
                    'scrapy', 'crawl', 'news',
                    '-a', f'article_url={url}'
                ], cwd='../news_scraper')
                messages.success(request, "Video transcript scraped!")
                return redirect('home')

            # Scrape portal headlines
            subprocess.run([
                'scrapy', 'crawl', 'news',
                '-a', f'portal_url={url}'
            ], cwd='../news_scraper')

            # Count headlines in PORTAL-SPECIFIC collection
            db = get_mongo_db()
            count = db[f"{portal}_headlines"].count_documents({})
            messages.success(request, f"Found {count} headlines from {urlparse(url).netloc}")
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
        
        return redirect('headlines', portal=portal)

class HeadlinesView(View):
    def get(self, request, portal):
        db = get_mongo_db()
        headlines = list(db[f"{portal}_headlines"].find().sort('scraped_at', -1))
        return render(request, 'newsapp/headlines.html', {
            'headlines': headlines,
            'portal': portal
        })

class ArticleView(View):
    def get(self, request):
        article_url = request.GET.get('url')
        decoded_url = quote(article_url, safe='/:?=&')
        
        db = get_mongo_db()
        if not db.articles.find_one({'url': decoded_url}):
            subprocess.run([
                'scrapy', 'crawl', 'news',
                '-a', f'article_url={decoded_url}'
            ], cwd='../news_scraper')

        article = db.articles.find_one({'url': decoded_url})
        if not article:
            messages.error(request, "Article not found")
            return redirect('home')
            
        template = 'video_detail.html' if article['type'] == 'video' else 'article_detail.html'
        return render(request, f'newsapp/{template}', {'article': article})