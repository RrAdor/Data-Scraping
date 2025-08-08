import trafilatura
import requests

url = input("Enter url: ")
response = requests.get(url)

# Extract main content
downloaded = trafilatura.fetch_url(url)
result = trafilatura.extract(downloaded, include_comments=False, include_tables=False)

print(result)
