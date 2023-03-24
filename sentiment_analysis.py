import json
from textblob import TextBlob

def calculate_sentiment_scores():
    with open('comments.json', 'r') as f:
        comments = json.load(f)

    sentiments = {}
    for subreddit in comments:
        subreddit_comments = comments[subreddit]
        polarity_scores = []
        for comment in subreddit_comments:
            blob = TextBlob(comment)
            polarity_scores.append(blob.sentiment.polarity)
        avg_polarity_score = sum(polarity_scores) / len(polarity_scores)
        sentiments[subreddit] = avg_polarity_score

    with open('sentiments.json', 'w') as f:
        json.dump(sentiments, f)

if __name__ == '__main__':
    calculate_sentiment_scores()
