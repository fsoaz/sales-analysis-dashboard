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
from src.kpis import (
    category_margin_summary,
    category_profitability,
    compute_kpis,
    monthly_revenue,
    top_products,
)

DATA_PATH = Path(__file__).parent / "data" / "superstore.csv"


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


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


def main() -> None:
    st.set_page_config(
        page_title="Sales Analysis",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Superstore Sales Analysis")
    st.caption("KPIs, top products, monthly revenue, and category profitability")

    if not DATA_PATH.exists():
        st.error("Dataset not found.")
        st.markdown(
            """
            Download the [Superstore Sales dataset](https://www.kaggle.com/datasets/kyanyoga/sample-superstore-dataset)
            and save it as `data/superstore.csv`.
            """
        )
        st.stop()

    df, stats = get_data(str(DATA_PATH))

    with st.sidebar:
        st.header("Filters")
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        date_range = st.date_input(
            "Order date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )
        if not isinstance(date_range, tuple) or len(date_range) != 2:
            date_range = (min_date, max_date)

        regions = st.multiselect(
            "Region",
            options=sorted(df["Region"].unique()),
            default=sorted(df["Region"].unique()),
        )
        categories = st.multiselect(
            "Category",
            options=sorted(df["Category"].unique()),
            default=sorted(df["Category"].unique()),
        )

        with st.expander("Data cleaning summary"):
            st.write(f"Rows before cleaning: {stats['rows_before']:,}")
            st.write(f"Duplicates removed: {stats['duplicates_removed']:,}")
            st.write(f"Invalid rows removed: {stats['invalid_rows_removed']:,}")
            st.write(f"Rows after cleaning: {stats['rows_after']:,}")

    if not regions or not categories:
        st.warning("Select at least one region and one category.")
        st.stop()

    filtered = apply_filters(df, date_range, regions, categories)

    if filtered.empty:
        st.warning("No data matches the current filters.")
        st.stop()

    kpis = compute_kpis(filtered)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", format_currency(kpis["total_revenue"]))
    col2.metric("Total Profit", format_currency(kpis["total_profit"]))
    col3.metric("Total Orders", f"{kpis['total_orders']:,}")
    col4.metric("Avg Order Value", format_currency(kpis["avg_order_value"]))

    st.divider()

    st.subheader("Which products sell the most?")
    rank_by = st.radio(
        "Rank products by",
        options=["Quantity", "Sales"],
        horizontal=True,
        key="product_rank",
    )
    products_df = top_products(filtered, by=rank_by)
    prod_col1, prod_col2 = st.columns([2, 1])
    with prod_col1:
        st.plotly_chart(top_products_chart(products_df, by=rank_by), use_container_width=True)
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
        label = "sales" if rank_by == "Sales" else "units sold"
        st.metric("Top Product", top_name or "—")
        st.metric(f"Top product {label}", f"{top_value:,.0f}" if rank_by == "Quantity" else format_currency(top_value))
        st.dataframe(
            products_df.style.format({"Sales": "${:,.2f}", "Profit": "${:,.2f}"}),
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    st.subheader("Which months have the highest revenue?")
    monthly_df = monthly_revenue(filtered)
    month_col1, month_col2 = st.columns([3, 1])
    with month_col1:
        st.plotly_chart(monthly_revenue_chart(monthly_df), use_container_width=True)
    with month_col2:
        st.metric("Peak Month", kpis["best_month"] or "—")
        st.metric("Peak Revenue", format_currency(kpis["best_month_revenue"]))

    st.divider()

    st.subheader("Which categories are the most profitable?")
    cat_profit_df = category_profitability(filtered)
    cat_margin_df = category_margin_summary(filtered)
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        st.plotly_chart(category_profit_chart(cat_profit_df), use_container_width=True)
    with cat_col2:
        st.metric("Most Profitable Category", kpis["top_category"] or "—")
        st.metric("Category Profit", format_currency(kpis["top_category_profit"]))
        st.plotly_chart(category_margin_chart(cat_margin_df), use_container_width=True)


if __name__ == "__main__":
    main()
