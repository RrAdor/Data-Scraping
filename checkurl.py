def is_single_article_url(url: str) -> bool:
    """
    Checks if the given URL points to a single news article.
    Returns True if it's a single article, False if it's a portal page.
    """
    for char in reversed(url.strip('/')):
        if char.isdigit():
            return True  # Found a digit → likely a single article
        if char in ['/', '?', '#']:
            break  # Reached end of last slug before finding a digit
    return False  # No digit found → portal page

url = input("Enter url: ")


result = "📰 Article" if is_single_article_url(url) else "📚 Portal"
print(f"{url} → {result}")
