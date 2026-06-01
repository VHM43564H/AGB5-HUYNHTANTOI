import feedparser
import json
from datetime import datetime, timezone
import os

def clean_text(text, max_len=160):
    """Strip HTML/tags and truncate cleanly."""
    if not text:
        return ""
    # remove tags
    import re
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > max_len:
        text = text[:max_len].rsplit(' ', 1)[0] + "..."
    return text

def fetch_rss(url, limit=8):
    feed = feedparser.parse(url)
    items = []
    feed_title = getattr(feed.feed, 'title', 'RSS Feed')
    for entry in feed.entries[:limit]:
        pub = getattr(entry, 'published', None) or getattr(entry, 'updated', None)
        if not pub:
            pub = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0700")
        summary_raw = getattr(entry, 'summary', None) or getattr(entry, 'description', '') or ''
        items.append({
            "title": getattr(entry, 'title', 'Không tiêu đề'),
            "summary": clean_text(summary_raw, 180),
            "link": getattr(entry, 'link', '#'),
            "date": pub,
            "source": feed_title
        })
    return items

# ==================== NGUỒN DỮ LIỆU ====================
# Tin tức kinh tế: Kinh doanh
tin_tuc_sources = [
    ("https://vnexpress.net/rss/kinh-doanh.rss", 8),
    ("https://tuoitre.vn/rss/kinh-doanh.rss", 5),
]

# Chính sách & Luật: Thời sự (nhiều nghị định, chính sách, quyết định của CP/ các Bộ) + một ít pháp luật
chinh_sach_sources = [
    ("https://vnexpress.net/rss/thoi-su.rss", 7),
    ("https://tuoitre.vn/rss/thoi-su.rss", 5),
    ("https://vnexpress.net/rss/phap-luat.rss", 3),  # ít để tránh tin hình sự
]

def collect_from_sources(sources):
    all_items = []
    for url, lim in sources:
        try:
            all_items.extend(fetch_rss(url, lim))
        except Exception as e:
            print(f"  [WARN] Lỗi fetch {url}: {e}")
    # dedup by link
    seen = set()
    unique = []
    for it in all_items:
        if it["link"] not in seen:
            seen.add(it["link"])
            unique.append(it)
    return unique[:12]  # cap total

news_data = {
    "tin_tuc": collect_from_sources(tin_tuc_sources),
    "chinh_sach": collect_from_sources(chinh_sach_sources),
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "meta": {
        "tin_tuc_sources": ["VnExpress Kinh doanh", "Tuổi Trẻ Kinh doanh"],
        "chinh_sach_sources": ["VnExpress Thời sự", "Tuổi Trẻ Thời sự", "VnExpress Pháp luật (một phần)"]
    }
}

os.makedirs("data", exist_ok=True)
with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=2)

print("[OK] Da cap nhat data/news.json (tin tuc + chinh sach luat)")
print("   last_updated:", news_data['last_updated'])
print("   tin_tuc:", len(news_data['tin_tuc']), "items")
print("   chinh_sach:", len(news_data['chinh_sach']), "items")
