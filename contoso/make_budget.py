"""Make contoso/budget.csv: the FY2026 sales budget, a Vizlake addition (not part of SQLBI's data).

Rule: for each month of FY2026 (April 2025 to March 2026), store and product category, the budget is the same month,
store and category of FY2025 (April 2024 to March 2025) in USD, plus 5%, rounded to whole dollars. USD is each sale's
Quantity x NetPrice / ExchangeRate (ExchangeRate is the order currency per USD). A store and category with no sales in a
month of FY2025 has no budget row for it. The online store (StoreKey 999999) is budgeted as one store.

Usage: python make_budget.py            (run from the repository root or anywhere; reads and writes beside this file)
"""
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
GROWTH = 0.05
FY_START = date(2025, 4, 1)          # FY2026 starts here; FY2025 is the year before it

category_of = {}
with open(HERE / "product.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        category_of[r["ProductKey"]] = int(r["CategoryKey"])

actual = defaultdict(float)
with open(HERE / "sales.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        d = date.fromisoformat(r["OrderDate"][:10])
        if date(2024, 4, 1) <= d < FY_START:
            month = date(d.year + 1, d.month, 1)          # the same month one year later, in FY2026
            usd = int(r["Quantity"]) * float(r["NetPrice"]) / float(r["ExchangeRate"])
            actual[(month, int(r["StoreKey"]), category_of[r["ProductKey"]])] += usd

with open(HERE / "budget.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\r\n")           # CRLF, like the other CSVs of this folder
    w.writerow(["Date", "StoreKey", "CategoryKey", "AmountUSD"])
    for (month, store, cat), usd in sorted(actual.items()):
        w.writerow([month.isoformat(), store, cat, round(usd * (1 + GROWTH))])
print(f"budget.csv: {len(actual)} rows, total {sum(round(v * (1 + GROWTH)) for v in actual.values()):,} USD")
