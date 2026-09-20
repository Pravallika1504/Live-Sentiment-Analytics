from src.sentiment import analyze_sentiment


texts = [
    "ChatGPT is an amazing AI tool and has improved productivity significantly.",
    "Users are disappointed with the latest ChatGPT update.",
    "OpenAI released a new AI model today."
]


for text in texts:

    result = analyze_sentiment(text)

    print("\nTEXT:", text)
    print("SENTIMENT:", result["label"])
    print("SCORE:", result["score"])
    