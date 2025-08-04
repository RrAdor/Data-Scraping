from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    scraped_data = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Force UTF-8 encoding for Bangla and other Unicode text
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract headlines and paragraphs
            headlines = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
            scraped_data = ''
            if headlines:
                scraped_data += '<b>Headlines:</b><br>' + '<br>'.join(headlines) + '<br><br>'
            if paragraphs:
                scraped_data += '<b>Paragraphs:</b><br>' + '<br><br>'.join(paragraphs)
            if not scraped_data:
                scraped_data = 'No main content found.'
        except Exception as e:
            error = str(e)
    return render_template('index.html', scraped_data=scraped_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
