from NewsReport import app 
from flask import render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


#############News取得#######################

def fetch_news(query="ChatGPT", max_results=3):
    url="https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_results,
        "apiKey": NEWS_API_KEY
    }

    response=requests.get(url,params=params)
    if response.status_code != 200:
        return []
    data = response.json()
    print(data)
    return data.get("articles", [])

############################################

@app.route('/')
def index():
    articles = fetch_news()
    print(articles)
    return render_template('index.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)