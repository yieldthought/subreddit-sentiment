import json
from flask import Flask, render_template, request
from scrape_and_analyze import collect_comments_from_subreddits, calculate_sentiment_scores

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    with open('sentiments.json', 'r') as f:
        sentiment_scores = json.load(f)

    return render_template('index.html', sentiment_scores=sentiment_scores)

@app.route('/update', methods=['POST'])
def update_sentiments():
    comments = collect_comments_from_subreddits()
    updated_sentiment_scores = calculate_sentiment_scores(comments)

    with open('sentiments.json', 'w') as f:
        json.dump(updated_sentiment_scores, f)

    return json.dumps(updated_sentiment_scores)

if __name__ == '__main__':
    app.run(debug=True)
