from vnstock import Vnstock
import json
import os
from datetime import datetime, timedelta

print("Đang lấy dữ liệu VNINDEX từ VNDIRECT...")

# Khởi tạo Vnstock
stock = Vnstock().stock(symbol="VNINDEX", source="VND")

# Lấy dữ liệu 180 ngày gần nhất (có thể thay đổi)
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")

df = stock.quote.history(start_date=start_date, end_date=end_date)

# Chuyển sang định dạng JSON cho Lightweight Charts
candles = []
for _, row in df.iterrows():
    candles.append({
        "time": row['time'].strftime("%Y-%m-%d"),
        "open": float(row['open']),
        "high": float(row['high']),
        "low": float(row['low']),
        "close": float(row['close'])
    })

os.makedirs("data", exist_ok=True)
with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump({"candles": candles}, f, ensure_ascii=False, indent=2)

print(f"✅ Đã cập nhật {len(candles)} nến cho tab Phân Tích Thị Trường!")
print("File data/stocks.json đã được tạo.")