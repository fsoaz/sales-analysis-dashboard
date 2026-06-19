# Superstore Sales Analysis Dashboard

Interactive Streamlit dashboard for analyzing Superstore sales data — top products, monthly revenue, and category profitability.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Dataset

Download the [Superstore Sales dataset](https://www.kaggle.com/datasets/kyanyoga/sample-superstore-dataset) and place the CSV at:

```
data/superstore.csv
```

The file is typically named `Sample - Superstore.csv` — rename it to `superstore.csv` when saving.

## Run

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

## Features

- **KPIs:** Total revenue, profit, orders, and average order value
- **Top products:** Ranked by quantity or sales
- **Monthly revenue:** Trend chart with peak month highlighted
- **Category profitability:** Profit and margin by category and sub-category
- **Filters:** Date range, region, and category
