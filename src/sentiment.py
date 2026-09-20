from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):

    if not text:
        return {
            "label": "Neutral",
            "score": 0.0
        }

    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"

    elif compound <= -0.05:
        label = "Negative"

    else:
        label = "Neutral"

    return {
        "label": label,
        "score": compound
    }