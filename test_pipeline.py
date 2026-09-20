from src.news import collect_news
from src.sentiment import analyze_sentiment


articles = collect_news("ChatGPT", 10)


for article in articles:

    text = article["title"] + " " + article["text"]

    sentiment = analyze_sentiment(text)

    article["sentiment"] = sentiment["label"]
    article["sentiment_score"] = sentiment["score"]


print("\n========== AI NEWS SENTIMENT ==========\n")


for article in articles:

    print("TITLE:", article["title"])
    print("SENTIMENT:", article["sentiment"])
    print("SCORE:", article["sentiment_score"])
    print("URL:", article["url"])
    print("--------------------------------------")
    