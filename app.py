from flask import Flask, render_template, request, redirect, url_for
import trafilatura
import os
import requests as req
from portal import NewsPortalScraper
from checkurl import is_single_article_url, is_youtube_url
from pymongo import MongoClient
from youtube_handler import extract_video_id, get_youtube_transcript
from datetime import datetime
import traceback


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Auto-reload templates during development

# ... [keep all your existing route and function code] ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Added host and port parameters

# Database connection
client = MongoClient("mongodb://localhost:27017/")
db = client["news_database"]
articles_collection = db["articles"]
transcripts_collection = db["youtube_transcripts"]

# Initialize scraper
scraper = NewsPortalScraper()

@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', 
                         error="Internal Server Error",
                         details=traceback.format_exc()), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', 
                         error="Page Not Found"), 404

def extract_headline_and_body(url: str):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        result = trafilatura.extract(downloaded)
        if result:
            parts = result.split('\n', 1)
            headline = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""
            return headline, body
    return None, None

def summarize_text(text):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    response = req.post(api_url, headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}, json={"inputs": text})
    try:
        return response.json()[0]['summary_text']
    except:
        return "Could not generate summary"

def analyze_sentiment(text):
    api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    response = req.post(api_url, headers={"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}, json={"inputs": text})
    try:
        result = response.json()[0]
        top_sentiment = max(result, key=lambda x: x['score'])
        return f"{top_sentiment['label']} ({top_sentiment['score']*100:.2f}%)"
    except:
        return "Could not analyze sentiment"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url').strip()
        if not url:
            return render_template('error.html', error="Please enter a URL")
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        if is_youtube_url(url):
            return redirect(url_for('handle_youtube', url=url))
        elif is_single_article_url(url):
            return redirect(url_for('show_article', url=url))
        else:
            return redirect(url_for('show_portal', url=url))
    
    return render_template('index.html')

@app.route('/youtube', methods=['GET'])
def handle_youtube():
    try:
        url = request.args.get('url')
        transcript_text, error = get_youtube_transcript(url)
        
        if error:
            return render_template('error.html', error=error)
        
        return render_template('youtube.html', 
                            transcript=transcript_text,
                            video_id=extract_video_id(url))
        
    except Exception as e:
        app.logger.error(f"Youtube route error: {traceback.format_exc()}")
        return render_template('error.html',
                            error="Failed to process YouTube video",
                            details=str(e)), 500

@app.route('/article')
def show_article():
    url = request.args.get('url')

    # Clear database before storing new article
    articles_collection.delete_many({})

    headline, body = extract_headline_and_body(url)
    
    if not headline or not body:
        return render_template('error.html', error="Could not extract article content")
    
    # Save to database
    articles_collection.insert_one({
        'headline': headline,
        'url': url,
        'body': body
    })
    
    summary = summarize_text(body[:1024])
    sentiment = analyze_sentiment(body[:512])
    
    return render_template('article.html',
                         headline=headline,
                         body=body,
                         summary=summary,
                         sentiment=sentiment,
                         url=url)

@app.route('/portal')
def show_portal():
    url = request.args.get('url')
    news_items = scraper.scrape_news_portal(url)
    return render_template('portal.html', news_items=news_items, portal_url=url)

if __name__ == '__main__':
    app.run(debug=True)