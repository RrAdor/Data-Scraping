// Global state to store all extracted content
let extractedContent = {
    articles: [],
    transcripts: [],
    totalWords: 0
};

// Navigation functions
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section, .hero-section').forEach(section => {
        section.classList.remove('active-section');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active-section');
    
    // Update nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`[href="#${sectionId}"]`).classList.add('active');
    
    // Update URL
    window.location.hash = sectionId;
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            showSection(sectionId);
        });
    });
    
    // Handle browser back/forward
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash.substring(1);
        if (hash) {
            showSection(hash);
        }
    });
    
    // Show initial section based on URL
    const initialHash = window.location.hash.substring(1);
    if (initialHash) {
        showSection(initialHash);
    }
    
    updateStats();
});

// Quick extract function with API integration
async function quickExtract() {
    const url = document.getElementById('quickUrl').value.trim();
    if (!url) {
        alert('Please enter a URL');
        return;
    }
    
    showLoading('Analyzing URL...', 'Determining the best extraction method for your content');
    
    try {
        // Call API to analyze URL type
        const response = await fetch(`${API_BASE_URL}/api/analyze-url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const analysis = await response.json();
        
        if (analysis.error) {
            throw new Error(analysis.error);
        }
        
        hideLoading();
        
        // Navigate to appropriate section and populate URL
        if (analysis.type === 'youtube') {
            showSection('youtube');
            document.getElementById('youtubeUrl').value = url;
            extractYouTubeTranscript();
        } else if (analysis.type === 'portal') {
            showSection('portal');
            document.getElementById('portalUrl').value = url;
            scrapePortal();
        } else {
            showSection('single');
            document.getElementById('singleUrl').value = url;
            extractSingleArticle();
        }
    } catch (error) {
        hideLoading();
        alert('Error processing URL: ' + error.message);
    }
}

// Portal scraping function
async function scrapePortal() {
    const url = document.getElementById('portalUrl').value.trim();
    const maxArticles = document.getElementById('maxArticles').value;
    const extractFullContent = document.getElementById('extractFullContent').checked;
    
    if (!url) {
        alert('Please enter a news portal URL');
        return;
    }
    
    showLoading('Scraping News Portal...', `Extracting headlines and content from ${getDomainName(url)}`);
    
    try {
        // Simulate API call to Python scraper
        const response = await simulatePortalScraping(url, maxArticles, extractFullContent);
        
        hideLoading();
        displayPortalResults(response.articles);
        
        // Add to global state
        extractedContent.articles.push(...response.articles);
        updateStats();
        
    } catch (error) {
        hideLoading();
        alert('Error scraping portal: ' + error.message);
    }
}

// Single article extraction
async function extractSingleArticle() {
    const url = document.getElementById('singleUrl').value.trim();
    
    if (!url) {
        alert('Please enter an article URL');
        return;
    }
    
    showLoading('Extracting Article...', 'Processing content with advanced text extraction algorithms');
    
    try {
        // Simulate API call to Python scraper
        const response = await simulateSingleArticleExtraction(url);
        
        hideLoading();
        displaySingleArticle(response);
        
        // Add to global state
        extractedContent.articles.push(response);
        updateStats();
        
    } catch (error) {
        hideLoading();
        alert('Error extracting article: ' + error.message);
    }
}

// YouTube transcript extraction
async function extractYouTubeTranscript() {
    const url = document.getElementById('youtubeUrl').value.trim();
    const language = document.getElementById('transcriptLang').value;
    const includeTimestamps = document.getElementById('includeTimestamps').checked;
    
    if (!url) {
        alert('Please enter a YouTube URL');
        return;
    }
    
    const videoId = extractYouTubeVideoId(url);
    if (!videoId) {
        alert('Invalid YouTube URL');
        return;
    }
    
    showLoading('Extracting Transcript...', 'Getting video transcript with timestamps and formatting');
    
    try {
        // Simulate API call to Python scraper
        const response = await simulateYouTubeTranscriptExtraction(videoId, language, includeTimestamps);
        
        hideLoading();
        displayYouTubeTranscript(response);
        
        // Add to global state
        extractedContent.transcripts.push(response);
        updateStats();
        
    } catch (error) {
        hideLoading();
        alert('Error extracting transcript: ' + error.message);
    }
}

// Display functions
function displayPortalResults(articles) {
    const container = document.getElementById('portalArticlesList');
    const resultsContainer = document.getElementById('portalResults');
    
    if (articles.length === 0) {
        container.innerHTML = '<div class="no-results"><i class="fas fa-exclamation-circle"></i><h3>No articles found</h3><p>The portal might have changed its structure or be temporarily unavailable</p></div>';
        resultsContainer.style.display = 'block';
        return;
    }
    
    container.innerHTML = articles.map(article => `
        <div class="article-card" onclick="showArticleModal('${article.id}')">
            <div class="article-header">
                <div class="article-title">${article.headline}</div>
            </div>
            <a href="${article.url}" target="_blank" class="article-url" onclick="event.stopPropagation()">${article.url}</a>
            ${article.body ? `<div class="article-content">${article.body}</div>` : '<div class="article-content text-muted">Full content not extracted</div>'}
            <div class="article-actions">
                <button class="btn-secondary btn-small" onclick="event.stopPropagation(); copyToClipboard('${article.id}', 'article')">
                    <i class="fas fa-copy"></i> Copy
                </button>
                <button class="btn-secondary btn-small" onclick="event.stopPropagation(); downloadArticle('${article.id}')">
                    <i class="fas fa-download"></i> Download
                </button>
            </div>
        </div>
    `).join('');
    
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function displaySingleArticle(article) {
    const container = document.getElementById('singleArticleContent');
    const resultsContainer = document.getElementById('singleResults');
    
    container.innerHTML = `
        <div class="single-article">
            <div class="single-article-header">
                <h1 class="single-article-title">${article.headline}</h1>
                <div class="single-article-meta">
                    <span><i class="fas fa-link"></i> <a href="${article.url}" target="_blank">Original Article</a></span>
                    <span><i class="fas fa-clock"></i> Extracted: ${new Date().toLocaleString()}</span>
                </div>
            </div>
            <div class="single-article-body">
                ${article.body.split('\n').map(paragraph => `<p>${paragraph}</p>`).join('')}
            </div>
        </div>
    `;
    
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayYouTubeTranscript(transcript) {
    const container = document.getElementById('youtubeTranscriptContent');
    const resultsContainer = document.getElementById('youtubeResults');
    
    container.innerHTML = `
        <div class="transcript-content">
            <div class="single-article-header">
                <h1 class="single-article-title">Video Transcript</h1>
                <div class="single-article-meta">
                    <span><i class="fab fa-youtube"></i> Video ID: ${transcript.videoId}</span>
                    <span><i class="fas fa-language"></i> Language: ${transcript.language}</span>
                    <span><i class="fas fa-clock"></i> Extracted: ${new Date().toLocaleString()}</span>
                </div>
            </div>
            ${transcript.paragraphs.map(para => `
                <div class="transcript-paragraph">
                    <div class="transcript-timestamp">${para.timestamp}</div>
                    <div class="transcript-text">${para.text}</div>
                </div>
            `).join('')}
        </div>
    `;
    
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// API functions that connect to your Python backend
async function simulatePortalScraping(url, maxArticles, extractFullContent) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/scrape-portal`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                maxArticles: maxArticles,
                extractFullContent: extractFullContent
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        return data;
    } catch (error) {
        console.error('Portal scraping error:', error);
        throw error;
    }
}

async function simulateSingleArticleExtraction(url) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/extract-article`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        return data;
    } catch (error) {
        console.error('Article extraction error:', error);
        throw error;
    }
}

async function simulateYouTubeTranscriptExtraction(videoId, language, includeTimestamps) {
    try {
        // Reconstruct URL from video ID
        const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
        
        const response = await fetch(`${API_BASE_URL}/api/extract-transcript`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: videoUrl,
                language: language
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        return data;
    } catch (error) {
        console.error('Transcript extraction error:', error);
        throw error;
    }
}

// Utility functions
function isPortalUrl(url) {
    const portalIndicators = ['/news', '/politics', '/world', '/business', '/technology'];
    const domain = getDomainName(url).toLowerCase();
    
    // Check if it's a known news domain
    const newsDomains = ['bbc.com', 'cnn.com', 'prothomalo.com', 'thedailystar.net', 'news24bd.tv'];
    if (newsDomains.some(d => domain.includes(d))) {
        return true;
    }
    
    // Check if URL contains portal indicators
    return portalIndicators.some(indicator => url.includes(indicator)) || 
           !url.match(/\/\d+/) && // No article IDs
           !url.includes('/article/') && 
           !url.includes('/story/');
}

function getDomainName(url) {
    try {
        return new URL(url).hostname;
    } catch {
        return url;
    }
}

function extractYouTubeVideoId(url) {
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
        /youtube\.com\/v\/([a-zA-Z0-9_-]{11})/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) return match[1];
    }
    return null;
}

function generateId() {
    return 'item_' + Math.random().toString(36).substr(2, 9);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Modal functions
function showLoading(title, subtitle) {
    document.getElementById('loadingText').textContent = title;
    document.getElementById('loadingSubtext').textContent = subtitle;
    document.getElementById('loadingModal').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingModal').style.display = 'none';
}

function closeModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

// Click outside modal to close
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        closeModal();
    }
});

// Export functions
function exportPortalResults() {
    const portalArticles = extractedContent.articles.filter(article => !article.videoId);
    downloadJSON(portalArticles, 'portal_articles.json');
}

function exportSingleResult() {
    const singleArticle = extractedContent.articles[extractedContent.articles.length - 1];
    downloadJSON([singleArticle], 'single_article.json');
}

function exportYouTubeResult() {
    const transcript = extractedContent.transcripts[extractedContent.transcripts.length - 1];
    downloadJSON([transcript], 'youtube_transcript.json');
}

function exportAllResults() {
    downloadJSON(extractedContent, 'all_extracted_content.json');
}

function downloadJSON(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Statistics update
function updateStats() {
    document.getElementById('totalArticles').textContent = extractedContent.articles.length;
    document.getElementById('totalTranscripts').textContent = extractedContent.transcripts.length;
    
    // Calculate total words
    let totalWords = 0;
    extractedContent.articles.forEach(article => {
        if (article.body) {
            totalWords += article.body.split(/\s+/).length;
        }
    });
    extractedContent.transcripts.forEach(transcript => {
        transcript.paragraphs.forEach(para => {
            totalWords += para.text.split(/\s+/).length;
        });
    });
    
    extractedContent.totalWords = totalWords;
    document.getElementById('totalWords').textContent = totalWords.toLocaleString();
    
    // Update results overview
    updateResultsOverview();
}

function updateResultsOverview() {
    const container = document.getElementById('allResultsContainer');
    
    if (extractedContent.articles.length === 0 && extractedContent.transcripts.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <i class="fas fa-inbox"></i>
                <h3>No content extracted yet</h3>
                <p>Start by extracting content from news portals, articles, or YouTube videos</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    if (extractedContent.articles.length > 0) {
        html += `
            <div class="results-section">
                <h3><i class="fas fa-newspaper"></i> Extracted Articles (${extractedContent.articles.length})</h3>
                <div class="articles-grid">
                    ${extractedContent.articles.map(article => `
                        <div class="article-card">
                            <div class="article-title">${article.headline}</div>
                            <a href="${article.url}" target="_blank" class="article-url">${article.url}</a>
                            ${article.body ? `<div class="article-content">${article.body}</div>` : '<div class="article-content text-muted">Headline only</div>'}
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    if (extractedContent.transcripts.length > 0) {
        html += `
            <div class="results-section">
                <h3><i class="fab fa-youtube"></i> Video Transcripts (${extractedContent.transcripts.length})</h3>
                <div class="articles-grid">
                    ${extractedContent.transcripts.map(transcript => `
                        <div class="article-card">
                            <div class="article-title">Video Transcript (${transcript.videoId})</div>
                            <div class="article-content">Language: ${transcript.language} • ${transcript.paragraphs.length} paragraphs</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    container.innerHTML = html;
}

// Copy to clipboard function
async function copyToClipboard(itemId, type) {
    let content = '';
    
    if (type === 'article') {
        const article = extractedContent.articles.find(a => a.id === itemId);
        if (article) {
            content = `${article.headline}\n\n${article.body || 'No content available'}\n\nSource: ${article.url}`;
        }
    }
    
    try {
        await navigator.clipboard.writeText(content);
        // Show temporary success message
        showTemporaryMessage('Content copied to clipboard!');
    } catch (err) {
        alert('Failed to copy to clipboard');
    }
}

function showTemporaryMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.textContent = message;
    messageEl.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        z-index: 3000;
        font-weight: 600;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(messageEl);
    
    setTimeout(() => {
        messageEl.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => document.body.removeChild(messageEl), 300);
    }, 2000);
}
