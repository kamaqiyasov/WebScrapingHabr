import re
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

URL = "https://habr.com"
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def find_in_text(keywords: list, text: str) -> bool:
    pattern = '|'.join(keywords)
    matches = re.findall(pattern, text, re.IGNORECASE)
    
    return len(matches) > 0

def main():
    headers = Headers(browser="chrome", os="win", headers=True)
    header = headers.generate()
    response = requests.get(URL + '/ru/articles', headers=header)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    previews = soup.find_all("article", {"data-test-id": "articles-list-item"})
    for preview in previews:
        preview_date = preview.find("time").get('title')        
        article_date = datetime.strptime(preview_date, "%Y-%m-%d, %H:%M")        
        article_date_msk = article_date + timedelta(hours=3)
        preview_title = preview.find("h2", {"data-test-id": "articleTitle"})
        preview_href = preview_title.find("a")['href']
        preview_link = URL + preview_href
        preview_text = preview.get_text()
        if not find_in_text(KEYWORDS, preview_text):
            response_preview = requests.get(preview_link, headers=header)
            if response_preview.status_code != 200:
                print(f"Ошибка: {response.status_code}")
            
            article_soup = BeautifulSoup(response_preview.text, 'html.parser')
            article = article_soup.find("div", {"data-test-id": "article-body"})
            article_text = article.get_text()
            if find_in_text(KEYWORDS, article_text):
                print(f"{article_date_msk} - {preview_title.text} - {preview_link}")
        else:
            print(f"{article_date_msk} - {preview_title.text} - {preview_link}")
            
if __name__ == "__main__":
    main()