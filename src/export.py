"""Build CSV and Excel exports from filtered dashboard data."""

from __future__ import annotations

from io import BytesIO

import pandas as pd


FORMULA_PREFIXES = ("=", "+", "-", "@")


def _neutralize_formula(value: object) -> object:
    """Keep spreadsheet formula-like text as text in CSV and Excel exports."""
    if isinstance(value, str) and value.lstrip().startswith(FORMULA_PREFIXES):
        return f"'{value}"
    return value


def _safe_export_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy with formula-like strings escaped without changing numbers."""
    safe = df.copy()
    for column in safe.columns:
        if pd.api.types.is_object_dtype(safe[column]) or pd.api.types.is_string_dtype(
            safe[column]
        ):
            safe[column] = safe[column].map(_neutralize_formula)
    return safe


def filtered_csv_bytes(df: pd.DataFrame) -> bytes:
    """Serialize the filtered detail table as UTF-8 CSV bytes."""
    buffer = BytesIO()
    _safe_export_frame(df).to_csv(buffer, index=False)
    return buffer.getvalue()


def build_excel_report(
    filtered: pd.DataFrame,
    kpis: dict,
    products_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    category_df: pd.DataFrame,
) -> bytes:
    """Build a multi-sheet Excel workbook for client download."""
    buffer = BytesIO()
    kpi_rows = [
        {"Metric": "Total Revenue", "Value": kpis.get("total_revenue")},
        {"Metric": "Total Profit", "Value": kpis.get("total_profit")},
        {"Metric": "Total Orders", "Value": kpis.get("total_orders")},
        {"Metric": "Avg Order Value", "Value": kpis.get("avg_order_value")},
        {"Metric": "Top Product (Sales)", "Value": kpis.get("top_product_by_sales")},
        {"Metric": "Top Category", "Value": kpis.get("top_category")},
        {"Metric": "Peak Month", "Value": kpis.get("best_month")},
    ]
    kpi_df = pd.DataFrame(kpi_rows)

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        _safe_export_frame(filtered).to_excel(writer, sheet_name="Filtered Data", index=False)
        _safe_export_frame(kpi_df).to_excel(writer, sheet_name="KPI Summary", index=False)
        _safe_export_frame(products_df).to_excel(writer, sheet_name="Top Products", index=False)
        _safe_export_frame(monthly_df).to_excel(writer, sheet_name="Monthly Revenue", index=False)
        _safe_export_frame(category_df).to_excel(writer, sheet_name="Category Profit", index=False)

    return buffer.getvalue()
