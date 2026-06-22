# Superstore Sales Analysis Dashboard

An interactive [Streamlit](https://streamlit.io/) dashboard for exploring Superstore sales data — KPIs, top products, monthly revenue trends, and category profitability, all filterable by date, region, and category.

Built with Python, pandas, and Plotly.

## Features

- **KPIs** — total revenue, profit, orders, and average order value, recomputed live as filters change
- **Top products** — ranked by quantity or sales, with a chart plus a detailed sales/profit table
- **Monthly revenue** — trend chart with the peak month and revenue highlighted
- **Category profitability** — profit and margin broken down by category and sub-category
- **Filters** — order date range, region, and category (sidebar)
- **Data cleaning summary** — rows removed for duplicates and invalid values, shown in the sidebar

## Requirements

- Python 3.10+ (type hints use 3.10+ syntax)
- Dependencies pinned in `requirements.txt`: pandas, streamlit, plotly

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

The download is typically named `Sample - Superstore.csv` — rename it to `superstore.csv`. The app shows an in-page message with this link if the file is missing.

## Run

```bash
streamlit run app.py
```

The dashboard opens at `http://localhost:8501`.

## Project structure

```
app.py                 # Streamlit UI: layout, filters, charts
src/data_loader.py     # CSV loading, cleaning, and cleaning stats
src/kpis.py            # KPI and aggregation logic (revenue, top products, etc.)
src/charts.py          # Plotly chart builders
data/superstore.csv    # Dataset (not committed — download separately)
requirements.txt
```
