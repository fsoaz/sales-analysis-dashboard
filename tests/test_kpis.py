from src.data_loader import load_sales_csv
from src.kpis import (
    category_margin_summary,
    category_profitability,
    compute_kpis,
    monthly_revenue,
    top_products,
)


def test_compute_kpis(sample_csv_bytes):
    df, _ = load_sales_csv(sample_csv_bytes)
    kpis = compute_kpis(df)
    assert kpis["total_orders"] == 3
    assert kpis["total_revenue"] == float(df["Sales"].sum())
    assert kpis["top_product_by_sales"] == "Desk"
    assert kpis["top_category"] == "Furniture"


def test_top_products(sample_csv_bytes):
    df, _ = load_sales_csv(sample_csv_bytes)
    by_qty = top_products(df, by="Quantity", n=3)
    assert list(by_qty.columns) == ["Product Name", "Quantity", "Sales", "Profit"]
    assert by_qty.iloc[0]["Product Name"] == "Desk"


def test_monthly_and_category(sample_csv_bytes):
    df, _ = load_sales_csv(sample_csv_bytes)
    monthly = monthly_revenue(df)
    assert "Revenue" in monthly.columns
    assert len(monthly) == 3

    cat = category_profitability(df)
    assert {"Category", "Sub-Category", "Profit", "Sales", "profit_margin"} <= set(cat.columns)

    margins = category_margin_summary(df)
    assert margins.iloc[0]["Category"] in {"Furniture", "Office Supplies"}
