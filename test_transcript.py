from youtube_transcript_api import YouTubeTranscriptApi

try:
    print("Testing video ID: nuNXiEDnM44")
    
    # Create an instance
    api = YouTubeTranscriptApi()
    
    # List available transcripts
    transcript_list = api.list('nuNXiEDnM44')
    print("Found transcripts:")
    
    transcripts = list(transcript_list)
    print(f"Number of transcripts: {len(transcripts)}")
    
    for i, transcript_info in enumerate(transcripts):
        print(f"Transcript {i}: Language={transcript_info.language_code}, Generated={transcript_info.is_generated}")
    
    # Fetch the first transcript
    transcript_data = transcripts[0].fetch()
    print(f"Success! Found transcript with {len(transcript_data)} items")
    
    # Check the structure of transcript items
    print(f"First item type: {type(transcript_data[0])}")
    print(f"First item attributes: {dir(transcript_data[0])}")
    print(f"First item: {transcript_data[0]}")
    
    # Try accessing text attribute
    if hasattr(transcript_data[0], 'text'):
        full_text = ' '.join([item.text for item in transcript_data])
    else:
        full_text = ' '.join([str(item) for item in transcript_data])
    
    print(f"Total length: {len(full_text)} characters")
    print(f"First 200 characters: {full_text[:200]}")
    
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    import traceback
    traceback.print_exc()
