import trafilatura
import sys
import io

# Ensure terminal stdout supports UTF-8 (important for Bangla display)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Your target URL
url = input("Enter url: ")  # Use a Bangla URL if testing Bangla

# Fetch and extract the article
downloaded = trafilatura.fetch_url(url)

if downloaded:
    result = trafilatura.extract(downloaded)
    if result:
        print(result)
    else:
        print("⚠️ Failed to extract main content.")
else:
    print("⚠️ Failed to download page.")
