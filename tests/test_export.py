from openpyxl import load_workbook

from src.data_loader import load_sales_csv
from src.export import build_excel_report, filtered_csv_bytes
from src.kpis import category_profitability, compute_kpis, monthly_revenue, top_products


def test_filtered_csv_bytes(sample_csv_bytes):
    df, _ = load_sales_csv(sample_csv_bytes)
    raw = filtered_csv_bytes(df)
    assert raw.startswith(b"Order ID") or b"Order ID" in raw
    assert b"Desk" in raw


def test_excel_report_sheets(sample_csv_bytes):
    df, _ = load_sales_csv(sample_csv_bytes)
    kpis = compute_kpis(df)
    products = top_products(df)
    monthly = monthly_revenue(df)
    categories = category_profitability(df)

    payload = build_excel_report(df, kpis, products, monthly, categories)
    wb = load_workbook(filename=__import__("io").BytesIO(payload))
    assert set(wb.sheetnames) == {
        "Filtered Data",
        "KPI Summary",
        "Top Products",
        "Monthly Revenue",
        "Category Profit",
    }


def test_formula_like_product_names_are_exported_as_text(sample_rows):
    from io import BytesIO
    import pandas as pd

    sample_rows.loc[0, "Product Name"] = "=cmd|' /C calc'!A0"
    sample_rows.loc[1, "Product Name"] = "+HYPERLINK(\"https://example.com\")"
    csv_payload = sample_rows.to_csv(index=False).encode()
    df, _ = load_sales_csv(csv_payload)
    kpis = compute_kpis(df)

    csv_export = filtered_csv_bytes(df)
    csv_round_trip = pd.read_csv(BytesIO(csv_export))
    assert csv_round_trip.loc[0, "Product Name"].startswith("'")
    assert csv_round_trip.loc[0, "Product Name"].startswith("'=cmd")

    workbook_payload = build_excel_report(
        df,
        kpis,
        top_products(df),
        monthly_revenue(df),
        category_profitability(df),
    )
    workbook = load_workbook(BytesIO(workbook_payload), data_only=False)
    filtered_product = workbook["Filtered Data"]["C2"]
    top_product = workbook["Top Products"]["A2"]
    assert filtered_product.value.startswith("'")
    assert filtered_product.data_type == "s"
    assert top_product.value.startswith("'")
    assert top_product.data_type == "s"
