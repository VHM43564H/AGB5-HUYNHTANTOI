from vnstock import Quote
import json
import os
from datetime import datetime, timedelta

# ================== CẤU HÌNH ==================
symbol = "VNINDEX"          # Bạn có thể đổi thành "VN30", "HPG", "FPT",...
days_back = 120             # Lấy dữ liệu ~4 tháng (đủ để vẽ biểu đồ đẹp)
interval = "1D"             # 1D = daily (có thể dùng "1h", "15m"...)
# =============================================

end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

print(f"Đang lấy dữ liệu {symbol} (source KBS)...")

# === API MỚI (khuyến nghị chính thức) ===
quote = Quote(symbol=symbol, source="KBS")   # KBS là nguồn ổn định nhất hiện nay

df = quote.history(
    start=start_date,
    end=end_date,
    interval=interval
)

print(f"✅ Lấy thành công {len(df)} phiên giao dịch!")

# Chuyển sang định dạng JSON cho Lightweight Charts
candles = []
for _, row in df.iterrows():
    candles.append({
        "time": row['time'].strftime("%Y-%m-%d") if hasattr(row['time'], 'strftime') else str(row['time']),
        "open": float(row['open']),
        "high": float(row['high']),
        "low": float(row['low']),
        "close": float(row['close'])
    })

# Lưu file
os.makedirs("data", exist_ok=True)
with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump({"candles": candles}, f, ensure_ascii=False, indent=2)

print("✅ Đã cập nhật biểu đồ nến thành công! File: data/stocks.json")