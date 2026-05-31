from vnstock import stock_historical_data
import json
import os
from datetime import datetime, timedelta

# Lấy dữ liệu 3 tháng gần nhất cho VN-Index hoặc cổ phiếu bạn quan tâm
symbol = "VNINDEX"   # hoặc "VNM", "HPG", "FPT"...
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

df = stock_historical_data(symbol=symbol, start_date=start_date, end_date=end_date)

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

print("✅ Đã cập nhật biểu đồ nến!")
