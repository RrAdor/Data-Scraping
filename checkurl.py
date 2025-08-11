import re

def is_youtube_url(url: str) -> bool:
    """Check if the URL is a YouTube video URL"""
    patterns = [
        r'(https?://)?(www\.)?youtube\.com/watch\?v=',
        r'(https?://)?(www\.)?youtu\.be/',
        r'(https?://)?(www\.)?youtube\.com/embed/'
    ]
    return any(re.search(pattern, url.lower()) for pattern in patterns)

def is_single_article_url(url: str) -> bool:
    """
    Checks if the given URL points to a single news article.
    Returns True if it's a single article, False if it's a portal page.
    """
    if is_youtube_url(url):
        return True
    
    for char in reversed(url.strip('/')):
        if char.isdigit():
            return True  # Found a digit → likely a single article
        if char in ['/', '?', '#']:
            break  # Reached end of last slug before finding a digit
    return False  # No digit found → portal page

# url = input("Enter url: ")


# result = "📰 Article" if is_single_article_url(url) else "📚 Portal"
# print(f"{url} → {result}")
