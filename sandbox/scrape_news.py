import trafilatura
import sys
import io

# Ensure proper UTF-8 output for Bangla and other non-Latin scripts
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_headline_and_body(url: str):
    """
    Fetch and extract main article text using trafilatura.
    Splits the result into headline and body (based on first newline).
    Returns a tuple (headline, body), or (None, None) if failed.
    """
    downloaded = trafilatura.fetch_url(url)

    if downloaded:
        result = trafilatura.extract(downloaded)
        
        if result:
            parts = result.split('\n', 1)
            headline = parts[0].strip()
            body = parts[1].strip() if len(parts) > 1 else ""
            return headline, body
        else:
            print("⚠️ Could not extract the article content.")
    else:
        print("⚠️ Failed to fetch the URL content.")
    
    return None, None

# Main script usage
if __name__ == "__main__":
    url = input("Enter the URL of the news article: ").strip()
    headline, body = extract_headline_and_body(url)

    if headline and body:
        print("\nHeadline:\n", headline)
        print("\nArticle Body:\n", body)
