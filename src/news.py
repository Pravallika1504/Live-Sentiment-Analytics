import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")


def collect_news(keyword, page_size=10):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "apiKey": API_KEY,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "publishedAt"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        articles.append({
            "source": "News",
            "title": article.get("title"),
            "text": article.get("description") or "",
            "created": article.get("publishedAt"),
            "url": article.get("url")
        })

    return articles
