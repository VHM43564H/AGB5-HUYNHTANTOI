#!/usr/bin/env python3
"""
Fetch Vietnam Macroeconomic indicators from World Bank API
Data source: World Bank Open Data (https://data.worldbank.org)
"""

import requests
import json
import os
from datetime import datetime, timezone

# World Bank API base
WB_BASE = "https://api.worldbank.org/v2"

# Vietnam indicators (annual)
INDICATORS = {
    "gdp_growth": {
        "code": "NY.GDP.MKTP.KD.ZG",
        "name": "GDP growth (annual %)",
        "unit": "%"
    },
    "gdp_current_usd": {
        "code": "NY.GDP.MKTP.CD",
        "name": "GDP (current US$)",
        "unit": "USD"
    },
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.CD",
        "name": "GDP per capita (current US$)",
        "unit": "USD"
    },
    "cpi_inflation": {
        "code": "FP.CPI.TOTL.ZG",
        "name": "Inflation, consumer prices (annual %)",
        "unit": "%"
    },
    "unemployment": {
        "code": "SL.UEM.TOTL.ZS",
        "name": "Unemployment, total (% of total labor force)",
        "unit": "%"
    },
    "fdi_net_inflows": {
        "code": "BX.KLT.DINV.CD.WD",
        "name": "Foreign direct investment, net inflows (BoP, current US$)",
        "unit": "USD"
    },
    "exports_goods_services": {
        "code": "NE.EXP.GNFS.CD",
        "name": "Exports of goods and services (current US$)",
        "unit": "USD"
    },
    "imports_goods_services": {
        "code": "NE.IMP.GNFS.CD",
        "name": "Imports of goods and services (current US$)",
        "unit": "USD"
    }
}


def fetch_worldbank(indicator_code, country="VN", per_page=60):
    """Fetch indicator data for a country. Returns list of {year, value} sorted ascending by year."""
    url = f"{WB_BASE}/country/{country}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "per_page": per_page,
        "date": "1995:2030"
    }
    try:
        resp = requests.get(url, params=params, timeout=45)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list) or len(data) < 2:
            return []
        records = []
        for item in data[1]:
            if item.get("value") is not None:
                records.append({
                    "year": item["date"],
                    "value": float(item["value"])
                })
        records.sort(key=lambda x: int(x["year"]))
        return records
    except Exception as e:
        print(f"WARNING: Error fetching {indicator_code}: {e}")
        return []


def format_value(val, unit):
    """Format large USD numbers nicely for display."""
    if unit != "USD":
        return round(val, 2)
    if val >= 1_000_000_000_000:
        return round(val / 1_000_000_000_000, 2)  # trillions
    if val >= 1_000_000_000:
        return round(val / 1_000_000_000, 2)     # billions
    return round(val, 0)


def main():
    print("Dang tai du lieu Kinh te Vi mo Viet Nam tu World Bank...")
    
    macro_data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "source": "World Bank Open Data",
        "country": "Vietnam (VN)",
        "indicators": {},
        "latest": {}
    }
    
    for key, meta in INDICATORS.items():
        print(f"   -> {meta['name']} ...")
        series = fetch_worldbank(meta["code"])
        macro_data["indicators"][key] = series
        
        if series:
            latest = series[-1]
            macro_data["latest"][key] = {
                "year": latest["year"],
                "value": latest["value"],
                "formatted": format_value(latest["value"], meta["unit"])
            }
        else:
            macro_data["latest"][key] = None
        
        print(f"      OK {len(series)} nam du lieu")
    
    # Derived: Trade balance (exports - imports) for convenience
    exp = macro_data["indicators"].get("exports_goods_services", [])
    imp = macro_data["indicators"].get("imports_goods_services", [])
    if exp and imp:
        trade_balance = []
        exp_map = {e["year"]: e["value"] for e in exp}
        for i in imp:
            if i["year"] in exp_map:
                tb = exp_map[i["year"]] - i["value"]
                trade_balance.append({"year": i["year"], "value": tb})
        macro_data["indicators"]["trade_balance"] = trade_balance
    
    # Write output
    os.makedirs("data", exist_ok=True)
    out_path = "data/macro.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(macro_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nDa cap nhat thanh cong: {out_path}")
    print(f"   Thoi gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Print latest snapshot
    print("\nSnapshot gan nhat:")
    for k, v in macro_data["latest"].items():
        if v:
            print(f"   {k}: {v['value']:.2f} ({v['year']})")


if __name__ == "__main__":
    main()