import re
import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
#print(soup.prettify())

#Extracting the Headlines
headlines = soup.find_all('h2')

# Print information about the headlines and their children
print(f"Number of a elements found: {len(headlines)}")
