from transformers import pipeline

classifier = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

def predict_sentiment(text):
    result = classifier(text)[0]

    stars = int(result["label"][0])

    sentiment = "POSITIVE" if stars >= 4 else "NEGATIVE"

    return {
        "label": sentiment,
        "score": result["score"]
    }