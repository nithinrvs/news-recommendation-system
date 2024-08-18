from pygooglenews import GoogleNews
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

gn = GoogleNews()

topics = ['WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SCIENCE', 'SPORTS', 'HEALTH']
news_data = []

for topic in topics:
    news = gn.topic_headlines(topic, proxies=None, scraping_bee=None)
    for entry in news['entries']:
        news_data.append({
            'title': entry['title'],
            'link': entry['link'],
            'description': entry.get('description', ''),
            'pubDate': entry['pubDate'],
            'topic': topic
        })

news_df = pd.DataFrame(news_data)
excel_file_path = 'news_data.csv'
news_df.to_csv(excel_file_path, index=False)


