import json
from flask import Flask, render_template, request
import scrape_and_analyze as sa

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment_data = {}

    if request.method == 'POST':
        # Run the data collection and sentiment analysis scripts
        #comments = sa.collect_comments_from_subreddits()
        #sentiment_data = sa.calculate_sentiment_scores(comments)
        pass

    # Load the sentiment scores from the sentiments.json file
    with open('sentiments.json', 'r') as f:
        sentiment_data = json.load(f)

    return render_template('index.html', sentiment_data=sentiment_data)

@app.route('/update', methods=['POST'])
def update_sentiments():
    # Run the data collection and sentiment analysis scripts
    comments = sa.collect_comments_from_subreddits()
    sentiment_data = sa.calculate_sentiment_scores(comments)

    return json.dumps(sentiment_data)

if __name__ == '__main__':
    app.run(debug=True)

