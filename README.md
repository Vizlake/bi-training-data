# Vizlake — BI Training Data

Public datasets used in Vizlake's BI training and assessment programmes.

## Datasets

| Dataset | Path | Source | Description |
|---|---|---|---|
| Contoso Sales (100K) | [`contoso/`](contoso/) | Microsoft sample | A fictional global retailer's sales, customers, products, stores. Used in our Train & Hire candidate assignment. |

## Using the data in Power BI

Each CSV can be loaded directly via its raw GitHub URL — no local download needed.

In Power BI Desktop:

1. **Get Data → Web**
2. Paste the raw URL, e.g. `https://raw.githubusercontent.com/Vizlake/bi-training-data/main/contoso/Sales.csv`
3. Repeat for each table.
4. Build relationships between fact and dimension tables in the model view.

Alternatively, clone the repo and load from disk:

```bash
git clone https://github.com/Vizlake/bi-training-data.git
```

## Licensing

The Contoso sample data is provided by Microsoft for educational and demonstration use. We redistribute it here unchanged (or lightly cleaned for ease of use) under the same terms. Refer to Microsoft's original distribution for canonical licensing.

The structure, documentation, and any additions in this repository are released under the [MIT License](LICENSE).

---

Vizlake Analytics — Europe | Middle East | India · [www.vizlake.com](https://www.vizlake.com)
