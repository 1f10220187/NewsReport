from NewsReport import app 
from flask import render_template
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI



# .envファイルを読み込む    
# .envファイルから環境変数を読み込む
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# OpenAIクライアント定義
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,)

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

    try:
        response=requests.get(url,params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    if response.status_code != 200:
        return []
    data = response.json()
    return data.get("articles", [])

############################################
#############記事要約#######################

def summarize_article(text,max_tokens=100):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "以下のニュース記事を日本語で簡潔に要約してください。"},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"APIエラー: {e}")
        return "要約に失敗しました。"

############################################

@app.route('/')
def index():
    articles = fetch_news()
    for article in articles:
        article['summary'] = summarize_article(article['content'])
        if not article['summary']:
            article['summary'] = "要約に失敗"
    return render_template('index.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)