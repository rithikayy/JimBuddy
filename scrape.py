# url for sitemap: https://thefitness.wiki/sitemap-1.xml

# pip install requests
# pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import os

os.makedirs('gym_data', exist_ok=True)

sitemap_url = 'https://thefitness.wiki/sitemap-1.xml'
r = requests.get(sitemap_url)
soup = BeautifulSoup(r.content, 'xml') # used to extract data from the html
pages = []
for loc in soup.find_all('loc'):
    pages.append(loc.get_text())


for i, page in enumerate(pages):
    r = requests.get(page)
    newsoup = BeautifulSoup(r.content, 'html.parser')
    title_tag = newsoup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else f"page_{i}"
    title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))[:50]
    filename = f'gym_data/{title}.txt'

    # Get the article content
    article = newsoup.find('article')
    content = article.get_text(separator='\n', strip=True)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Title: {title}\n")
        f.write(f"URL: {page}\n\n")
        f.write(content)
