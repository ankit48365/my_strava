import feedparser
from google.cloud import bigquery
import urllib.parse

def fetch_google_news(request):
    # 1. Configuration
    topic = "Google Cloud"
    encoded_topic = urllib.parse.quote(topic)
    # The "when:1d" ensures we only get news from the last 24 hours
    rss_url = f"https://news.google.com/rss/search?q={encoded_topic}+when:1d&hl=en-US&gl=US&ceid=US:en"
    
    # 2. Parse the RSS Feed
    feed = feedparser.parse(rss_url)
    client = bigquery.Client()
    table_id = "your_project.your_dataset.news_tracker"
    
    rows_to_insert = []
    for entry in feed.entries:
        rows_to_insert.append({
            "topic": topic,
            "title": entry.title,
            "url": entry.link,
            "published_date": entry.published  # feedparser handles the string conversion
        })

    # 3. Save to BigQuery
    if rows_to_insert:
        errors = client.insert_rows_json(table_id, rows_to_insert)
        if not errors:
            # TRIGGER YOUR JOBS HERE
            # e.g., call_another_function(rows_to_insert)
            return f"Success: Inserted {len(rows_to_insert)} articles.", 200
    
    return "No new articles found.", 200