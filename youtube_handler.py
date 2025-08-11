import re
from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
from datetime import datetime

def extract_video_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_youtube_transcript(url):
    """Get raw transcript text from YouTube video"""
    try:
        # Initialize MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["news_database"]
        transcripts_collection = db["youtube_transcripts"]
        
        video_id = extract_video_id(url)
        if not video_id:
            return None, "Invalid YouTube URL"
        
        # Check if transcript exists in database
        existing = transcripts_collection.find_one({"video_id": video_id})
        if existing:
            return existing['transcript_text'], None
        
        # Get transcript from YouTube
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcripts = list(transcript_list)
        
        if not transcripts:
            return None, "No transcripts available for this video"
        
        # Try preferred languages (Bangla first, then English)
        preferred_languages = ['bn', 'bn-BD', 'en', 'en-US', 'en-GB']
        selected_transcript = None
        
        for lang_code in preferred_languages:
            for transcript_info in transcripts:
                if transcript_info.language_code == lang_code:
                    selected_transcript = transcript_info
                    break
            if selected_transcript:
                break
        
        # Fallback to first available transcript
        if selected_transcript is None:
            selected_transcript = transcripts[0]
        
        # Fetch and join transcript text
        transcript_data = selected_transcript.fetch()
        transcript_text = " ".join([entry['text'] for entry in transcript_data])
        
        # Store in database
        transcripts_collection.insert_one({
            "video_id": video_id,
            "url": url,
            "language": selected_transcript.language_code,
            "is_generated": selected_transcript.is_generated,
            "transcript_text": transcript_text,
            "timestamp": datetime.now()
        })
        
        return transcript_text, None
        
    except Exception as e:
        return None, f"Could not extract transcript: {str(e)}"