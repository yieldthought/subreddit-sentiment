import json
from flask import Flask, render_template, request
import collect_comments
import sentiment_analysis

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Run the data collection and sentiment analysis scripts
        collect_comments.collect_comments_from_subreddits()
        sentiment_analysis.calculate_sentiment_scores()

    # Load the sentiment scores from the sentiments.json file
    with open('sentiments.json', 'r') as f:
        sentiment_scores = json.load(f)

    return render_template('index.html', sentiment_scores=sentiment_scores)

@app.route('/update', methods=['POST'])
def update_sentiments():
    # Run the data collection and sentiment analysis scripts
    collect_comments.collect_comments_from_subreddits()
    sentiment_analysis.calculate_sentiment_scores()

    # Load the updated sentiment scores from the sentiments.json file
    with open('sentiments.json', 'r') as f:
        updated_sentiment_scores = json.load(f)

    return json.dumps(updated_sentiment_scores)

if __name__ == '__main__':
    app.run(debug=True)
