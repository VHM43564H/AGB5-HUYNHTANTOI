import feedparser
import json
from datetime import datetime
import os

def fetch_rss(url, limit=8):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.title,
            "summary": entry.summary[:150] + "..." if 'summary' in entry else entry.description[:150] + "...",
            "link": entry.link,
            "date": entry.published if 'published' in entry else datetime.now().strftime("%d/%m/%Y"),
            "source": feed.feed.title
        })
    return items

news_data = {
    "tin_tuc": fetch_rss("https://vnexpress.net/rss/kinh-doanh.rss") + fetch_rss("https://cafef.vn/rss/kinh-doanh.rss", 4),
    "chinh_sach": fetch_rss("https://vnexpress.net/rss/phap-luat.rss") + fetch_rss("https://thuvienphapluat.vn/rss", 4)  # hoặc RSS khác nếu có
}

os.makedirs("data", exist_ok=True)
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print("✅ Đã cập nhật tin tức!")
