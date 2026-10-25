"""Make contoso/budget.csv: the FY2026 sales budget, a Vizlake addition (not part of SQLBI's data).

FY2026 runs from April 2025 to March 2026. The budget is set as a retailer would have set it at the end of March 2025,
from FY2025's results and trends only: each month, store and product subcategory of FY2025 in USD, times a category
target and a market target (below), rounded to whole dollars. USD is each sale's Quantity x NetPrice / ExchangeRate
(ExchangeRate is the order currency per USD). A store and subcategory with no sales in a month of FY2025 has no row.
The online store (StoreKey 999999) is budgeted as one market. The targets were then checked against FY2026's actual
sales so that reports show a realistic mix of hits and misses; the budget is a plan, not a forecast.

Usage: python make_budget.py            (reads and writes beside this file)
"""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Category targets: the evidence at March 2025 is FY2025's last quarter against the same quarter a year earlier.
CATEGORY = {
    "Computers": -0.02,                      # the largest category, -23% in Q4 but slowing: near flat
    "Cell phones": 0.00,                     # -17% in Q4, smartphones steadier: hold
    "Home Appliances": -0.03,                # -20% in Q4
    "TV and Video": -0.15,                   # -25% in Q4, the steepest fall in every window: managed decline
    "Music, Movies and Audio Books": -0.05,  # -15% in Q4, physical media
    "Cameras and camcorders": 0.15,          # the one sizeable category growing: +11% in Q4, SLR cameras +17%
    "Audio": 0.10,                           # +2% in Q4, headphones +20%
    "Games and Toys": 0.08,                  # +5% in Q4
}
# Market targets: online is expected to fall more slowly; stores get a recovery plan (+10%: in-store sales fell 11% in Q4
# against 21% over the half year), adjusted by each country's own last quarter.
MARKET = {
    "Online": -0.12,                         # -24% in Q4: the decline halves
    "United States": 0.10,                   # the largest store estate: the recovery plan
    "Germany": 0.20,                         # +16% in Q4
    "United Kingdom": 0.12,                  # +4% in Q4
    "Canada": 0.12,                          # +3% in Q4
    "France": 0.10,                          # +5% over the half year, -17% in Q4
    "Netherlands": 0.08,                     # -24% in Q4
    "Australia": 0.08,                       # -21% in Q4
    "Italy": 0.30,                           # +66% in Q4, +32% over the half year
}
FY2025 = (date(2024, 4, 1), date(2025, 3, 31))

product = {}
with open(HERE / "product.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        product[r["ProductKey"]] = (int(r["CategoryKey"]), int(r["SubCategoryKey"]), r["CategoryName"])
market = {}
with open(HERE / "store.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        market[int(r["StoreKey"])] = r["CountryName"]          # the online store's CountryName is "Online"

actual = defaultdict(float)
with open(HERE / "sales.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        d = date.fromisoformat(r["OrderDate"][:10])
        if FY2025[0] <= d <= FY2025[1]:
            cat_key, sub_key, cat_name = product[r["ProductKey"]]
            month = date(d.year + 1, d.month, 1)               # the same month one year later, in FY2026
            usd = int(r["Quantity"]) * float(r["NetPrice"]) / float(r["ExchangeRate"])
            actual[(month, int(r["StoreKey"]), cat_key, sub_key, cat_name)] += usd

rows = [(month, store, cat_key, sub_key, round(usd * (1 + CATEGORY[cat_name]) * (1 + MARKET[market[store]])))
        for (month, store, cat_key, sub_key, cat_name), usd in actual.items()]
with open(HERE / "budget.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\r\n")                   # CRLF, like the other CSVs of this folder
    w.writerow(["Date", "StoreKey", "CategoryKey", "SubCategoryKey", "AmountUSD"])
    for month, store, cat_key, sub_key, amount in sorted(rows):
        w.writerow([month.isoformat(), store, cat_key, sub_key, amount])
print(f"budget.csv: {len(rows)} rows, total {sum(r[4] for r in rows):,} USD")
