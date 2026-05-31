from vnstock import Quote
import json
import os
from datetime import datetime, timedelta

symbols = ["VNINDEX", "VN30", "HPG", "VCB", "FPT", "VNM", "GAS", "VHM", "BID", "CTG", "TCB", "MSN", "MWG", "POW", "SAB", "ACB", "MBB", "VRE", "GVR"]

days_back = 120
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")

os.makedirs("data", exist_ok=True)

data_all = {}

for symbol in symbols:
    print(f"Đang lấy dữ liệu {symbol}...")
    try:
        quote = Quote(symbol=symbol, source="KBS")
        df = quote.history(start=start_date, end=end_date, interval="1D")
        
        candles = []
        for _, row in df.iterrows():
            candles.append({
                "time": row['time'].strftime("%Y-%m-%d"),
                "open": float(row['open']),
                "high": float(row['high']),
                "low": float(row['low']),
                "close": float(row['close'])
            })
        
        data_all[symbol] = {"candles": candles}
        print(f"✅ {symbol} - {len(candles)} nến")
    except Exception as e:
        print(f"❌ Lỗi {symbol}: {e}")

with open("data/stocks.json", "w", encoding="utf-8") as f:
    json.dump(data_all, f, ensure_ascii=False, indent=2)

print("✅ Hoàn tất tất cả mã VN30!")