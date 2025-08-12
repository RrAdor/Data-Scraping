from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from urllib.parse import urlparse, quote
import subprocess
import re
import pymongo
from django.conf import settings

def get_mongo_db():
    client = pymongo.MongoClient(settings.MONGO_URI)
    return client[settings.MONGO_DB]

def get_collection_name(url):
    """Generate collection name from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '').replace('.', '_')
    return f"{domain}_articles"

class HomeView(View):
    def get(self, request):
        db = get_mongo_db()
        # Get all collections that end with '_articles'
        collections = db.list_collection_names()
        news_collections = [c for c in collections if c.endswith('_articles')]
        
        # Get recent headlines from all portals
        recent_headlines = []
        for collection in news_collections:
            headlines = list(db[collection].find(
                {'scraped_full_content': False}
            ).sort('timestamp', -1).limit(5))
            recent_headlines.extend(headlines)
        
        return render(request, 'newsapp/home.html', {
            'recent_headlines': recent_headlines,
            'portals': [c.replace('_articles', '') for c in news_collections]
        })

class ScrapePortalView(View):
    def post(self, request):
        url = request.POST.get('url', '').strip()
        if not url:
            messages.error(request, "Please provide a URL")
            return redirect('home')

        try:
            # Scrape portal headlines
            subprocess.run([
                'scrapy', 'crawl', 'news',
                '-a', f'portal_url={url}'
            ], cwd='../news_scraper')

            collection_name = get_collection_name(url)
            db = get_mongo_db()
            count = db[collection_name].count_documents({'scraped_full_content': False})
            
            messages.success(request, f"Found {count} headlines from {urlparse(url).netloc}")
            return redirect('headlines', portal=collection_name.replace('_articles', ''))
            
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('home')

class HeadlinesView(View):
    def get(self, request, portal):
        db = get_mongo_db()
        collection_name = f"{portal}_articles"
        headlines = list(db[collection_name].find(
            {'scraped_full_content': False}
        ).sort('timestamp', -1))
        
        return render(request, 'newsapp/headlines.html', {
            'headlines': headlines,
            'portal': portal
        })

class ArticleView(View):
    def get(self, request):
        article_url = request.GET.get('url')
        if not article_url:
            messages.error(request, "No article URL provided")
            return redirect('home')

        decoded_url = quote(article_url, safe='/:?=&')
        db = get_mongo_db()
        
        # Find which collection contains this article
        collections = db.list_collection_names()
        article = None
        for collection in collections:
            if collection.endswith('_articles'):
                article = db[collection].find_one({'url': decoded_url})
                if article:
                    break
        
        if not article:
            messages.error(request, "Article not found in database")
            return redirect('home')
            
        # If full content not scraped yet, trigger full content spider
        if not article.get('scraped_full_content'):
            try:
                subprocess.run([
                    'scrapy', 'crawl', 'full_content',
                    '-a', f'url={decoded_url}',
                    '-a', f'collection_name={collection}'
                ], cwd='../news_scraper')
                
                # Refresh the article data
                article = db[collection].find_one({'url': decoded_url})
                messages.success(request, "Full content retrieved")
            except Exception as e:
                messages.error(request, f"Error retrieving full content: {str(e)}")
                return redirect('headlines', portal=collection.replace('_articles', ''))
        
        return render(request, 'newsapp/article_detail.html', {
            'article': article,
            'portal': collection.replace('_articles', '')
        })