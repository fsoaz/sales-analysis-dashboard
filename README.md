# Superstore Sales Analysis Dashboard

A sleek, SaaS-style [Streamlit](https://streamlit.io/) dashboard for exploring Superstore sales data — KPIs, top products, monthly revenue trends, and category profitability, all filterable by date, region, and category. Fully bilingual (English / Português-BR).

Built with Python, pandas, and Plotly.

## Features

- **KPIs** — total revenue, profit, orders, and average order value as branded cards with **period-over-period deltas** (second half of the selected range vs. the first), recomputed live as filters change
- **Top products** — ranked by quantity or sales, with a chart plus a detailed sales/profit table
- **Monthly revenue** — area trend chart with the peak month and revenue highlighted
- **Category profitability** — profit and margin broken down by category and sub-category
- **Filters** — order date range, region, and category (sidebar)
- **Data cleaning summary** — rows removed for duplicates and invalid values, shown in the sidebar
- **Multilanguage** — switch between English (US) and Português (BR) from the sidebar; all UI text and chart labels translated
- **SaaS-style UI** — custom design system: branded sidebar, gradient hero header, hover-lift KPI cards, themed Plotly charts, custom theme via `.streamlit/config.toml`

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
app.py                 # Streamlit UI: layout, filters, KPI cards, charts
src/data_loader.py     # CSV loading, cleaning, and cleaning stats
src/kpis.py            # KPI and aggregation logic (revenue, top products, etc.)
src/charts.py          # Plotly chart builders + shared `_style` theme
src/styles.py          # Design system: palette, global CSS, hero/brand/KPI components
src/i18n.py            # Translations (en / pt-BR) and translator helper
.streamlit/config.toml # Streamlit theme (brand colors, font)
.gitignore             # Ignores __pycache__, .venv, the dataset, secrets
data/superstore.csv    # Dataset (not committed — download separately)
requirements.txt
```

## Internationalization

UI strings live in `src/i18n.py` under `TRANSLATIONS` (`en`, `pt`). Add a language by extending `LANGUAGES` and adding a matching key block. `get_translator(lang)` returns `t(key, **kwargs)`, which falls back to English for any missing key.

## Design system (`src/styles.py`)

- **Brand palette** — single source of color constants, also consumed by `src/charts.py` for themed charts.
- **`inject_css()`** — global stylesheet (fonts, hero, KPI cards, sidebar). Call once after `st.set_page_config`.
- **Components** — `hero()`, `brand()`, `section()`, `divider()`, `kpi_cards()`.
- **Rendering** — all components render through `st.html`, not `st.markdown(unsafe_allow_html=True)`. `st.html` skips Markdown parsing, so indentation / blank lines can't be misread as a code block. Dynamic text is escaped via `esc()`.

## Charts (`src/charts.py`)

Every figure passes through `_style()` for a consistent SaaS look — brand colorway, `Inter` font, transparent background, clean grid. The profit-by-category chart places its legend below the plot so it never overlaps the title in narrow (embedded) layouts.
