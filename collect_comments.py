import requests
from bs4 import BeautifulSoup
import json

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

with open('comments.json', 'w') as f:
    json.dump(comments, f)
