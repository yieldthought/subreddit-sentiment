import json
from json.decoder import JSONDecodeError
import time
import datetime
import requests

from textblob import TextBlob


def collect_comments_from_subreddits():
    with open('subreddits.txt', 'r') as f:
        subreddits = [line.strip() for line in f.readlines()]

    num_comments = 10
    comments = {}
    delay_between_requests = 1  # In seconds
    max_retries = 8

    for subreddit in subreddits:
        comments[subreddit] = {}
        for i in range(1, 13):
            print(f"{subreddit} {i}/12")
            current_time = int(time.time())
            month_delta = datetime.timedelta(days=30*i)
            end_time = datetime.datetime.fromtimestamp(current_time - (i - 1) * month_delta.total_seconds())
            start_time = datetime.datetime.fromtimestamp(current_time - i * month_delta.total_seconds())

            retries = 0
            while retries < max_retries:
                url = f'https://api.pushshift.io/reddit/search/comment/?subreddit={subreddit}&size={num_comments}&after={start_time.timestamp()}&before={end_time.timestamp()}'
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers)

                if response.status_code == 429:
                    retries += 1
                    delay = delay_between_requests * 2 ** retries
                    time.sleep(delay)
                    print(f"Rate limit reached for subreddit '{subreddit}' and month {i}. Retrying after {delay} seconds.")
                    continue
                break

            if retries >= max_retries:
                print(f"Max retries reached for subreddit '{subreddit}' and month {i}. Skipping this month.")
                continue

            try:
                data = response.json()
            except JSONDecodeError as e:
                print(f"Error decoding JSON data for subreddit '{subreddit}' and month {i}: {e}")
                print(f"URL: {url}")
                print(f"Status code: {response.status_code}")
                print(f"JSON response: {response.text}")
                print("Skipping this month.")
                continue

            month_name = start_time.strftime("%B %Y")
            comments[subreddit][month_name] = []
            for comment in data['data']:
                comments[subreddit][month_name].append(comment['body'])

            time.sleep(delay_between_requests)

    return comments



def calculate_sentiment_scores(comments):
    sentiments = {}
    for subreddit in comments:
        sentiments[subreddit] = {}
        for month in comments[subreddit]:
            subreddit_comments = comments[subreddit][month]
            polarity_scores = []
            for comment in subreddit_comments:
                blob = TextBlob(comment)
                polarity_scores.append(blob.sentiment.polarity)
            avg_polarity_score = sum(polarity_scores) / len(polarity_scores)
            sentiments[subreddit][month] = avg_polarity_score

    return sentiments


if __name__ == '__main__':
    comments = collect_comments_from_subreddits()
    sentiment_scores = calculate_sentiment_scores(comments)

    with open('sentiments.json', 'w') as f:
        json.dump(sentiment_scores, f)
