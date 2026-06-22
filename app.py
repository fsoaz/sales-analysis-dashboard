from pathlib import Path

import pandas as pd
import streamlit as st

from src.charts import (
    category_margin_chart,
    category_profit_chart,
    monthly_revenue_chart,
    top_products_chart,
)
from src.data_loader import load_superstore
from src.i18n import DEFAULT_LANG, LANGUAGES, get_translator
from src.kpis import (
    category_margin_summary,
    category_profitability,
    compute_kpis,
    monthly_revenue,
    top_products,
)
from src import styles

DATA_PATH = Path(__file__).parent / "data" / "superstore.csv"


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def format_compact(value: float) -> str:
    """Compact currency for KPI cards: $1.2M, -$34.5K. Sign before the $."""
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    for unit, div in (("M", 1e6), ("K", 1e3)):
        if magnitude >= div:
            return f"{sign}${magnitude / div:,.1f}{unit}"
    return f"{sign}${magnitude:,.0f}"


@st.cache_data
def get_data(path: str) -> tuple[pd.DataFrame, dict]:
    return load_superstore(path)


def apply_filters(
    df: pd.DataFrame,
    date_range: tuple,
    regions: list[str],
    categories: list[str],
) -> pd.DataFrame:
    mask = (
        (df["Order Date"] >= pd.Timestamp(date_range[0]))
        & (df["Order Date"] <= pd.Timestamp(date_range[1]))
        & (df["Region"].isin(regions))
        & (df["Category"].isin(categories))
    )
    return df[mask]


def period_deltas(df: pd.DataFrame) -> dict:
    """Compare the second half of the selected date range against the first half.

    Returns percent change per metric, or None when there's no comparable prior period.
    """
    if df.empty:
        return {}
    start = df["Order Date"].min()
    end = df["Order Date"].max()
    midpoint = start + (end - start) / 2
    prior = df[df["Order Date"] < midpoint]
    recent = df[df["Order Date"] >= midpoint]
    if prior.empty or recent.empty:
        return {}

    def pct(curr: float, prev: float):
        if prev == 0:
            return None
        return (curr - prev) / prev * 100

    def block(d: pd.DataFrame) -> dict:
        orders = d["Order ID"].nunique()
        revenue = d["Sales"].sum()
        return {
            "revenue": revenue,
            "profit": d["Profit"].sum(),
            "orders": orders,
            "aov": revenue / orders if orders else 0.0,
        }

    p, r = block(prior), block(recent)
    return {k: pct(r[k], p[k]) for k in p}


def delta_card(label: str, value: str, icon: str, change, t) -> dict:
    """Build a KPI card dict with a formatted period-over-period delta."""
    card = {"label": label, "value": value, "icon": icon}
    if change is not None:
        trend = "up" if change > 0.05 else "down" if change < -0.05 else "flat"
        card["delta"] = f"{abs(change):.1f}% {t('vs_prior')}"
        card["trend"] = trend
    return card


def main() -> None:
    st.set_page_config(
        page_title="Sales Analysis | Análise de Vendas",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    styles.inject_css()

    lang_label = st.sidebar.selectbox("🌐 Language / Idioma", options=list(LANGUAGES.keys()))
    lang = LANGUAGES.get(lang_label, DEFAULT_LANG)
    t = get_translator(lang)

    styles.hero(t("app_title"), t("app_caption"), t("hero_badge"))

    if not DATA_PATH.exists():
        st.error(t("dataset_not_found"))
        st.markdown(t("dataset_help"))
        st.stop()

    df, stats = get_data(str(DATA_PATH))

    with st.sidebar:
        styles.brand(t("brand_name"), t("brand_tagline"))
        st.caption(t("workspace").upper())
        st.header(t("filters"))
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        date_range = st.date_input(
            t("order_date_range"),
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            date_range = (min_date, max_date)

        regions = st.multiselect(
            t("region"),
            options=sorted(df["Region"].unique()),
            default=sorted(df["Region"].unique()),
        )
        categories = st.multiselect(
            t("category"),
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique()),
        )

        with st.expander(t("data_cleaning_summary")):
            st.write(t("rows_before", n=stats["rows_before"]))
            st.write(t("duplicates_removed", n=stats["duplicates_removed"]))
            st.write(t("invalid_rows_removed", n=stats["invalid_rows_removed"]))
            st.write(t("rows_after", n=stats["rows_after"]))

    if not regions or not categories:
        st.warning(t("select_region_category"))
        st.stop()

    filtered = apply_filters(df, date_range, regions, categories)

    if filtered.empty:
        st.warning(t("no_data"))
        st.stop()

    kpis = compute_kpis(filtered)
    deltas = period_deltas(filtered)

    styles.kpi_cards([
        delta_card(t("total_revenue"), format_compact(kpis["total_revenue"]), "💰", deltas.get("revenue"), t),
        delta_card(t("total_profit"), format_compact(kpis["total_profit"]), "📈", deltas.get("profit"), t),
        delta_card(t("total_orders"), f"{kpis['total_orders']:,}", "🧾", deltas.get("orders"), t),
        delta_card(t("avg_order_value"), format_currency(kpis["avg_order_value"]), "🛒", deltas.get("aov"), t),
    ])

    styles.divider()

    with st.container(border=True):
        styles.section(t("products_question"))
        rank_options = {"Quantity": t("quantity"), "Sales": t("sales")}
        rank_by = st.radio(
            t("rank_products_by"),
            options=["Quantity", "Sales"],
            format_func=lambda v: rank_options[v],
            horizontal=True,
            key="product_rank",
        )
        products_df = top_products(filtered, by=rank_by)
        prod_col1, prod_col2 = st.columns([2, 1])
        with prod_col1:
            st.plotly_chart(top_products_chart(products_df, by=rank_by, t=t), width="stretch")
        with prod_col2:
            top_name = (
                kpis["top_product_by_sales"]
                if rank_by == "Sales"
                else kpis["top_product_by_quantity"]
            )
            top_value = (
                kpis["top_product_sales"]
                if rank_by == "Sales"
                else kpis["top_product_quantity"]
            )
            label = t("label_sales") if rank_by == "Sales" else t("label_units_sold")
            st.metric(t("top_product"), top_name or "—")
            st.metric(
                t("top_product_metric", label=label),
                f"{top_value:,.0f}" if rank_by == "Quantity" else format_currency(top_value),
            )
            st.dataframe(
                products_df.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}"}),
                width="stretch",
                hide_index=True,
            )

    styles.divider()

    with st.container(border=True):
        styles.section(t("months_question"))
        monthly_df = monthly_revenue(filtered)
        month_col1, month_col2 = st.columns([3, 1])
        with month_col1:
            st.plotly_chart(monthly_revenue_chart(monthly_df, t=t), width="stretch")
        with month_col2:
            st.metric(t("peak_month"), kpis["best_month"] or "—")
            st.metric(t("peak_revenue"), format_currency(kpis["best_month_revenue"]))

    styles.divider()

    with st.container(border=True):
        styles.section(t("categories_question"))
        cat_profit_df = category_profitability(filtered)
        cat_margin_df = category_margin_summary(filtered)
        cat_col1, cat_col2 = st.columns(2)
        with cat_col1:
            st.plotly_chart(category_profit_chart(cat_profit_df, t=t), width="stretch")
        with cat_col2:
            st.metric(t("most_profitable_category"), kpis["top_category"] or "—")
            st.metric(t("category_profit"), format_currency(kpis["top_category_profit"]))
            st.plotly_chart(category_margin_chart(cat_margin_df, t=t), width="stretch")


if __name__ == "__main__":
    main()
