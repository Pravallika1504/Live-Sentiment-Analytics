from src.news import collect_news


articles = collect_news("ChatGPT", 10)


print("\n========== NEWS ARTICLES ==========\n")


for article in articles:

    print("TITLE:", article["title"])
    print("SOURCE:", article["source"])
    print("DATE:", article["created"])
    print("URL:", article["url"])
    print("-----------------------------------")