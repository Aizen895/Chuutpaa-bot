# utils.py (Web Scraping)
import requests
from bs4 import BeautifulSoup
import logging

def get_anime_news():
    url = "https://www.animenewsnetwork.com/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        news_items = soup.find_all("div", class_="news")
        news_list = []
        for item in news_items[:5]:
            title = item.h3.a.text if item.h3 and item.h3.a else "No Title"
            link = "https://www.animenewsnetwork.com" + item.h3.a["href"] if item.h3 and item.h3.a and item.h3.a.has_attr("href") else "#"
            news_list.append({"title": title, "link": link})
        return news_list
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return []
