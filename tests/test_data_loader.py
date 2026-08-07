from pathlib import Path

import pytest

from src.data_loader import DataValidationError, load_sales_csv, validate_columns


def test_load_sample_csv_bytes(sample_csv_bytes):
    df, stats = load_sales_csv(sample_csv_bytes)
    assert len(df) == 5
    assert stats["rows_before"] == 5
    assert stats["rows_after"] == 5
    assert "order_month" in df.columns
    assert "profit_margin" in df.columns


def test_day_first_dates_are_not_silently_swapped():
    from io import BytesIO
    import pandas as pd

    rows = pd.DataFrame(
        {
            "Order ID": ["D1", "D2", "D3"],
            "Order Date": ["8/11/2016", "16/1/2016", "2016-01-08"],
            "Product Name": ["A", "B", "C"],
            "Category": ["Office Supplies"] * 3,
            "Sales": [1, 2, 3],
            "Profit": [1, 1, 1],
            "Quantity": [1, 1, 1],
        }
    )
    buffer = BytesIO()
    rows.to_csv(buffer, index=False)

    df, _ = load_sales_csv(buffer.getvalue())

    assert df["Order Date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2016-11-08",
        "2016-01-16",
        "2016-01-08",
    ]


def test_empty_or_all_invalid_csv_is_a_validation_error():
    from io import BytesIO

    with pytest.raises(DataValidationError, match="empty"):
        load_sales_csv(b"")

    invalid = BytesIO(
        b"Order ID,Order Date,Product Name,Category,Sales,Profit,Quantity\n"
        b"A1,not-a-date,,Office Supplies,nope,nope,nope\n"
    )
    with pytest.raises(DataValidationError, match="no valid sales rows"):
        load_sales_csv(invalid.getvalue())


def test_load_without_optional_region(minimal_csv_bytes):
    df, stats = load_sales_csv(minimal_csv_bytes)
    assert stats["rows_after"] == 2
    assert (df["Region"] == "All").all()
    assert (df["Sub-Category"] == "Unknown").all()


def test_missing_required_columns(sample_rows):
    bad = sample_rows.drop(columns=["Sales", "Profit"])
    missing = validate_columns(bad)
    assert "Sales" in missing
    assert "Profit" in missing
    with pytest.raises(DataValidationError) as exc:
        from io import BytesIO

        buf = BytesIO()
        bad.to_csv(buf, index=False)
        load_sales_csv(buf.getvalue())
    assert "Sales" in exc.value.missing_columns


def test_bundled_sample_file():
    path = Path(__file__).resolve().parents[1] / "data" / "sample_superstore.csv"
    assert path.exists()
    df, stats = load_sales_csv(path)
    assert stats["rows_after"] > 0
    assert {"Order ID", "Order Date", "Sales", "Profit", "Region"} <= set(df.columns)
