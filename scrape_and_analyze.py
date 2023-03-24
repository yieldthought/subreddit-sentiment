import json
import requests
from textblob import TextBlob

def collect_comments_from_subreddits():
    with open('subreddits.txt', 'r') as f:
        subreddits = [line.strip() for line in f.readlines()]

    num_comments = 10
    comments = {}
    for subreddit in subreddits:
        url = f'https://www.reddit.com/r/{subreddit}/comments.json?limit={num_comments}'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)

        comments[subreddit] = []
        for comment in data['data']['children']:
            comments[subreddit].append(comment['data']['body'])
    
    return comments

def calculate_sentiment_scores(comments):
    sentiments = {}
    for subreddit in comments:
        subreddit_comments = comments[subreddit]
        polarity_scores = []
        for comment in subreddit_comments:
            blob = TextBlob(comment)
            polarity_scores.append(blob.sentiment.polarity)
        avg_polarity_score = sum(polarity_scores) / len(polarity_scores)
        sentiments[subreddit] = avg_polarity_score

    return sentiments

if __name__ == '__main__':
    comments = collect_comments_from_subreddits()
    sentiment_scores = calculate_sentiment_scores(comments)

    with open('sentiments.json', 'w') as f:
        json.dump(sentiment_scores, f)
