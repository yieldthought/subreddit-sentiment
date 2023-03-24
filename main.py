from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('sentiments.json', 'r') as f:
        sentiments = json.load(f)
    return render_template('index.html', sentiments=sentiments)

if __name__ == '__main__':
    app.run(debug=True)
