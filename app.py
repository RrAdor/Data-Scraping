from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = Flask(__name__)

def extract_video_id(url):
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

def get_youtube_transcript(video_id):
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
        
        # Structure the text with timestamps and paragraphs
        structured_text = f'<div style="background: #2c3e50; color: white; padding: 12px; border-radius: 6px; margin-bottom: 15px;">'
        structured_text += f"<b>Language:</b> {selected_transcript.language_code} | "
        structured_text += f"<b>Type:</b> {'Auto-generated' if selected_transcript.is_generated else 'Manual'}</div>"
        
        # Group transcript into paragraphs (every 10 sentences or 2 minutes)
        current_paragraph = []
        paragraphs = []
        last_timestamp = 0
        
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
                    paragraph_html = f'<div style="margin: 15px 0; padding: 15px; background: #ffffff; border: 2px solid #e3f2fd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
                    paragraph_html += f'<div style="color: #1976d2; font-weight: bold; margin-bottom: 8px; font-size: 0.9em;">{timestamp}</div>'
                    paragraph_html += f'<div style="color: #212121; line-height: 1.6; font-size: 1em;">{paragraph_text}</div></div>'
                    paragraphs.append(paragraph_html)
                    current_paragraph = []
                    last_timestamp = item.start
        
        # Add remaining text as final paragraph
        if current_paragraph:
            final_item = transcript_data[-1]
            minutes = int(final_item.start // 60)
            seconds = int(final_item.start % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            paragraph_text = ' '.join(current_paragraph)
            paragraph_html = f'<div style="margin: 15px 0; padding: 15px; background: #ffffff; border: 2px solid #e3f2fd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
            paragraph_html += f'<div style="color: #1976d2; font-weight: bold; margin-bottom: 8px; font-size: 0.9em;">{timestamp}</div>'
            paragraph_html += f'<div style="color: #212121; line-height: 1.6; font-size: 1em;">{paragraph_text}</div></div>'
            paragraphs.append(paragraph_html)
        
        # Join paragraphs
        structured_text += ''.join(paragraphs)
        
        return structured_text
        
    except Exception as e:
        return f"Could not extract transcript: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    scraped_data = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            # Check if it's a YouTube URL
            video_id = extract_video_id(url)
            
            if video_id:
                # Handle YouTube video transcript extraction
                transcript = get_youtube_transcript(video_id)
                if transcript.startswith("Could not extract"):
                    error = transcript
                else:
                    scraped_data = f'<div style="padding: 20px; background: #e8f5e8; border-radius: 10px; border: 2px solid #4caf50; margin: 10px 0;">'
                    scraped_data += f'<div style="background: #4caf50; color: white; padding: 12px; border-radius: 6px; margin-bottom: 15px; font-size: 1.2em; font-weight: bold; text-align: center;">YouTube Video Transcript</div>'
                    scraped_data += f'<div style="background: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd; line-height: 1.6; color: #212121;">{transcript}</div>'
                    scraped_data += f'</div>'
            else:
                # Handle regular web scraping
                response = requests.get(url)
                response.raise_for_status()
                # Force UTF-8 encoding for Bangla and other Unicode text
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for embedded videos on the page
                video_elements = soup.find_all(['iframe', 'video', 'embed'])
                youtube_videos = []
                
                for element in video_elements:
                    src = element.get('src', '')
                    if 'youtube.com' in src or 'youtu.be' in src:
                        vid_id = extract_video_id(src)
                        if vid_id:
                            youtube_videos.append(vid_id)
                
                # Extract headlines and paragraphs with better structure
                headlines = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3']) if h.get_text(strip=True)]
                paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True) and len(p.get_text(strip=True)) > 30]
                
                scraped_data = ''
                
                if headlines:
                    scraped_data += '<div style="margin-bottom: 25px;"><b style="color: #ffffff; background: #2196f3; padding: 8px 12px; border-radius: 6px; font-size: 1.1em;">📰 Headlines</b><br><br>'
                    for i, headline in enumerate(headlines[:10], 1):  # Limit to top 10 headlines
                        scraped_data += f'<div style="margin: 10px 0; padding: 12px; background: #ffffff; border-left: 4px solid #2196f3; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
                        scraped_data += f'<span style="color: #1976d2; font-weight: bold; margin-right: 8px;">{i}.</span>'
                        scraped_data += f'<span style="color: #212121; font-size: 1em; line-height: 1.5;">{headline}</span></div>'
                    scraped_data += '</div>'
                
                if paragraphs:
                    scraped_data += '<div style="margin-bottom: 25px;"><b style="color: #ffffff; background: #4caf50; padding: 8px 12px; border-radius: 6px; font-size: 1.1em;">📄 Main Content</b><br><br>'
                    for i, paragraph in enumerate(paragraphs[:15], 1):  # Limit to 15 paragraphs
                        # Truncate very long paragraphs
                        display_text = paragraph if len(paragraph) <= 300 else paragraph[:300] + "..."
                        scraped_data += f'<div style="margin: 12px 0; padding: 15px; background: #ffffff; border: 1px solid #ddd; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
                        scraped_data += f'<div style="color: #4caf50; font-weight: bold; margin-bottom: 8px; font-size: 0.9em;">¶ Paragraph {i}</div>'
                        scraped_data += f'<div style="color: #212121; line-height: 1.6; font-size: 1em;">{display_text}</div></div>'
                    scraped_data += '</div>'
                
                # Add YouTube video transcripts if found
                if youtube_videos:
                    scraped_data += '<div style="margin-top: 25px;"><b style="color: #ffffff; background: #f44336; padding: 8px 12px; border-radius: 6px; font-size: 1.1em;">🎥 YouTube Videos Found</b><br><br>'
                    for i, vid_id in enumerate(youtube_videos[:3], 1):  # Limit to first 3 videos
                        transcript = get_youtube_transcript(vid_id)
                        if not transcript.startswith("Could not extract"):
                            # Truncate transcript for preview
                            preview = transcript[:800] + "..." if len(transcript) > 800 else transcript
                            scraped_data += f'<div style="margin: 15px 0; padding: 15px; background: #ffffff; border: 2px solid #f44336; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
                            scraped_data += f'<div style="color: #f44336; font-weight: bold; margin-bottom: 10px; font-size: 1em;">📹 Video {i} Transcript</div>'
                            scraped_data += f'<div style="color: #212121; line-height: 1.6; font-size: 1em;">{preview}</div></div>'
                        else:
                            scraped_data += f'<div style="margin: 10px 0; padding: 12px; background: #fff3e0; border: 1px solid #ff9800; border-radius: 6px; color: #e65100;">'
                            scraped_data += f'<b>📹 Video {i}:</b> {transcript}</div>'
                    scraped_data += '</div>'
                
                if not scraped_data:
                    scraped_data = '<div style="padding: 20px; background: #fff8e1; border: 2px solid #ffc107; border-radius: 8px; color: #795548; text-align: center;">'
                    scraped_data += '<div style="font-size: 1.2em; margin-bottom: 8px;">⚠️ <b>No Content Found</b></div>'
                    scraped_data += '<div>No main content could be extracted from this page.</div></div>'
                    
        except Exception as e:
            error = str(e)
    return render_template('index.html', scraped_data=scraped_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
