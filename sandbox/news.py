import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def scrape_news_article(url, title_selector='h1'):
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    title_element = soup.find(title_selector)
    print(title_element )
    title = title_element.get_text(strip=True) if title_element else "Title not found"

    content = "Content not found"
    common_selectors = [
            '[data-component="text-block"]',
            'div[data-component="text-block"] p',
            'article div p',
            'main article p',
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            'story-element story-element-text',
            '.content',
            'main p',
            'news-item-0',
            'article__content',
            'text-block'   
        ]
        
    for selector in common_selectors:
            content_elements = soup.select(selector)
            print(content_elements)
            if content_elements:
                if selector.endswith(' p'):
                    content = "\n".join([p.get_text(strip=True) for p in content_elements])
                    print(f"Content found using selector: {selector}")
                else:
                    paragraphs = content_elements[0].find_all('p')
                    if paragraphs:
                        content = "\n".join([p.get_text(strip=True) for p in paragraphs])
                        print(f"Content found using selector: {selector}")  
                    else:
                        content = content_elements[0].get_text(strip=True)
                        print(f"Content found using selector: {selector}")
                break

    return {"title": title, "content": content}

article_url = input("Enter the news article URL: ")
article_data = scrape_news_article(article_url,title_selector='h1')

if article_data:
    print(f"Title: {article_data['title']}")
    print(f"\nContent:\n{article_data['content']}")
    print("--------------------------------")