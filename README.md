# Data Scraping - Content Extraction System

A comprehensive web-based application for extracting content from news portals, individual articles, and YouTube videos with advanced text processing capabilities.

## Features

- **News Portal Scraping**: Extract headlines and full articles from major news sites (BBC, CNN, Prothom Alo, Daily Star, etc.)
- **Article Extraction**: Clean text extraction from individual news article URLs
- **YouTube Transcripts**: Multi-language transcript extraction with timestamp formatting
- **Auto-Detection**: Intelligent URL analysis for streamlined processing
- **Multi-Language Support**: Bengali, English, and international language processing
- **Export Options**: JSON download and clipboard integration

## Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask REST API
- **Libraries**: BeautifulSoup, trafilatura, youtube-transcript-api
- **Architecture**: Stateless design without database dependency

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**
   ```bash
   python app.py
   ```

3. **Access Interface**
   Open `http://localhost:5000` in your browser

## Usage

- **Portal Scraping**: Enter news portal URLs to extract multiple articles
- **Single Article**: Process individual article URLs for clean content extraction
- **YouTube Videos**: Extract timestamped transcripts from video URLs
- **Quick Extract**: Paste any URL for automatic content type detection

## API Endpoints

- `POST /api/scrape-portal` - News portal scraping
- `POST /api/extract-article` - Single article extraction  
- `POST /api/extract-transcript` - YouTube transcript extraction

## Output

All extracted content can be viewed in the web interface, exported as JSON, or copied to clipboard.

---

**Note**: This system operates without database integration, providing a lightweight and easily deployable solution for content extraction needs.
