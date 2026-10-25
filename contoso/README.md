# Contoso (100K) — Sample Dataset

A 100K-customer-scale Contoso retail dataset, ready to load directly into Power BI. Generated using SQLBI's [Contoso Data Generator V2](https://www.sqlbi.com/tools/contoso-data-generator/) and sourced from their [ready-to-use data release](https://github.com/sql-bi/Contoso-Data-Generator-V2-data/releases/tag/ready-to-use-data).

Contoso is a fictional global retailer selling consumer electronics, home appliances, and accessories across multiple regions, currencies, and channels.

## Files

| File | Rows | Description |
|---|---|---|
| `sales.csv` | 223,974 | Order line items with order header info and currency, in a single flattened table. |
| `orders.csv` | 93,470 | Order headers — one row per order, with customer, store, and dates. |
| `orderrows.csv` | 223,974 | Order line items — products, quantities, and prices, keyed to `orders.csv`. |
| `customer.csv` | 104,990 | Customer profiles with demographics, address, and geo coordinates. |
| `product.csv` | 2,517 | Product catalogue with category, subcategory, brand, manufacturer, cost and price. |
| `store.csv` | 74 | Stores with country, state, size, open/close dates, and status. |
| `date.csv` | 4,018 | Calendar table covering the full data range. |
| `currencyexchange.csv` | 100,450 | Daily exchange rates by currency pair. |
| `budget.csv` | 8,430 | FY2026 sales budget (April 2025 to March 2026) by month, store and product subcategory, in USD. A Vizlake addition, made by `make_budget.py`. |

`sales.csv` and (`orders.csv` + `orderrows.csv`) contain the same underlying transactions in different shapes — a denormalized form and a normalized form.

## Schema

### sales
`OrderKey`, `LineNumber`, `OrderDate`, `DeliveryDate`, `CustomerKey`, `StoreKey`, `ProductKey`, `Quantity`, `UnitPrice`, `NetPrice`, `UnitCost`, `CurrencyCode`, `ExchangeRate`

### orders
`OrderKey`, `CustomerKey`, `StoreKey`, `OrderDate`, `DeliveryDate`, `CurrencyCode`

### orderrows
`OrderKey`, `LineNumber`, `ProductKey`, `Quantity`, `UnitPrice`, `NetPrice`, `UnitCost`

### customer
`CustomerKey`, `GeoAreaKey`, `StartDT`, `EndDT`, `Continent`, `Gender`, `Title`, `GivenName`, `MiddleInitial`, `Surname`, `StreetAddress`, `City`, `State`, `StateFull`, `ZipCode`, `Country`, `CountryFull`, `Birthday`, `Age`, `Occupation`, `Company`, `Vehicle`, `Latitude`, `Longitude`

### product
`ProductKey`, `ProductCode`, `ProductName`, `Manufacturer`, `Brand`, `Color`, `WeightUnit`, `Weight`, `Cost`, `Price`, `CategoryKey`, `CategoryName`, `SubCategoryKey`, `SubCategoryName`

### store
`StoreKey`, `StoreCode`, `GeoAreaKey`, `CountryCode`, `CountryName`, `Channel`, `State`, `OpenDate`, `CloseDate`, `Description`, `SquareMeters`, `Status`

### date
`Date`, `DateKey`, `Year`, `YearQuarter`, `YearQuarterNumber`, `Quarter`, `YearMonth`, `YearMonthShort`, `YearMonthNumber`, `Month`, `MonthShort`, `MonthNumber`, `DayofWeek`, `DayofWeekShort`, `DayofWeekNumber`, `WorkingDay`, `WorkingDayNumber`

### currencyexchange
`Date`, `FromCurrency`, `ToCurrency`, `Exchange`

### budget
`Date` (first day of the month), `StoreKey`, `CategoryKey`, `SubCategoryKey` (as in `product.csv`), `AmountUSD`

## Loading into Power BI

**Get Data → Web** and paste the raw URL for each file you need:

```text
https://raw.githubusercontent.com/Vizlake/bi-training-data/main/contoso/<filename>.csv
```

For example:
```text
https://raw.githubusercontent.com/Vizlake/bi-training-data/main/contoso/sales.csv
```

## Vizlake additions

Everything else in this folder is SQLBI's `csv-100k` release byte for byte (checked 2026-10-25). Two things are ours:

- `store.csv` has a `Channel` column: `Online` for the one virtual store (`StoreKey` 999999), `In-store` for the other 73.
  No other value in the file changed.
- `budget.csv` is a sales budget for the fiscal year April 2025 to March 2026 ($29,346,434, level with FY2025), so reports
  can compare actuals with a plan. It is set as a retailer would have set it at the end of March 2025, from FY2025 only:
  each month, store and subcategory of FY2025 in USD (Quantity x NetPrice / ExchangeRate), times a category target and a
  market target, rounded to whole dollars. A store and subcategory with no sales in that month of FY2025 has no row; the
  online store is one market. The targets were checked against FY2026's actual sales so that reports show a realistic mix
  of hits and misses: it is a plan, not a forecast. Rebuild it with `python make_budget.py`.

  | Category | Target | Evidence at March 2025 (last quarter vs a year earlier) |
  |---|---|---|
  | Cameras and camcorders | +15% | the one sizeable category growing: +11%, SLR cameras +17% |
  | Audio | +10% | +2%, headphones +20% |
  | Games and Toys | +8% | +5% |
  | Cell phones | 0% | -17%, smartphones steadier |
  | Computers | -2% | -23%, slowing; the largest category |
  | Home Appliances | -3% | -20% |
  | Music, Movies and Audio Books | -5% | -15%, physical media |
  | TV and Video | -15% | -25%, the steepest fall in every window |

  | Market | Target | Evidence |
  |---|---|---|
  | Online | -5% | -24%: the decline slows |
  | Stores: the recovery plan | +10% | in-store sales fell 11% in the last quarter against 21% over the half year |
  | Italy | +30% | +66% in the last quarter |
  | Germany | +20% | +16% |
  | United Kingdom, Canada | +12% | +4%, +3% |
  | United States, France | +10% | the plan; France +5% over the half year |
  | Netherlands, Australia | +8% | -24%, -21% |

## Source & licensing

Data generated by SQLBI's [Contoso Data Generator V2](https://www.sqlbi.com/tools/contoso-data-generator/) and downloaded from the [`sql-bi/Contoso-Data-Generator-V2-data`](https://github.com/sql-bi/Contoso-Data-Generator-V2-data) repository (release: `ready-to-use-data`).

The generator and its outputs are published by SQLBI for educational and demonstration use. Refer to the upstream repository for canonical licensing.
