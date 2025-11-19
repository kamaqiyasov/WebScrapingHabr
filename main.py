import re
from typing import Optional
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

URL = "https://habr.com"
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def find_in_text(keywords: list, text: str) -> bool:
    pattern = '|'.join(keywords)
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    return len(matches) > 0

def get_url_soup(url: str, headers: dict) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None

def parse_preview(preview: str) -> Optional[dict]:
    preview_date = preview.find("time")    
    if not preview_date or not preview_date.get('title'):
        return None
    
    article_date = datetime.strptime(preview_date['title'], "%Y-%m-%d, %H:%M")        
    preview_date = article_date + timedelta(hours=3)
    
    preview_title = preview.find("h2", {"data-test-id": "articleTitle"})
    if not preview_title:
        return None
    
    title = preview_title.get_text(strip=True)
    preview_link = preview_title.find("a")
    if not preview_link or not preview_link.get('href'):
        return None
    
    link = URL + preview_link['href']
    preview_text = preview.get_text(strip=True)

    return {'date': preview_date, 'title': title, 'link': link, 'text': preview_text}

def get_full_text(url: str, header: dict) -> str:
    soup = get_url_soup(url, header)
    if not soup:
        return ""
    article = soup.find("div", {"data-test-id": "article-body"})
    
    return article.get_text(strip=True) if article else ""

def main():
    headers = Headers(browser="chrome", os="win", headers=True)
    header = headers.generate()
    
    soup = get_url_soup(URL + '/ru/articles', header)
    if not soup:
        print("Ошибка при загрузке страницы")
        return
    
    previews = soup.find_all("article", {"data-test-id": "articles-list-item"})
    if not previews:
        return
    
    for preview in previews:
        
        preview_data = parse_preview(preview)
        if not preview_data:
            continue
        
        if find_in_text(KEYWORDS, preview_data['text']):
            print(f"{preview_data['date']} - {preview_data['title']} - {preview_data['link']}")
            continue
        
        full_text = get_full_text(preview_data['link'], header)
        if find_in_text(KEYWORDS, full_text):
            print(f"{preview_data['date']} - {preview_data['title']} - {preview_data['link']}")
        
        time.sleep(0.5)
        
if __name__ == "__main__":
    main()