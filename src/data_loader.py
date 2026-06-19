from pathlib import Path

import pandas as pd

NUMERIC_COLUMNS = ["Sales", "Quantity", "Discount", "Profit"]
REQUIRED_COLUMNS = ["Order ID", "Order Date", "Product Name", "Category", "Sales", "Profit", "Quantity"]


def load_superstore(path: str | Path) -> tuple[pd.DataFrame, dict]:
    """Load and clean Superstore CSV. Returns cleaned DataFrame and cleaning stats."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, encoding="utf-8")

    stats = {"rows_before": len(df)}

    for date_col in ["Order Date", "Ship Date"]:
        df[date_col] = pd.to_datetime(df[date_col], format="mixed", dayfirst=False)

    df = df.drop_duplicates()
    stats["duplicates_removed"] = stats["rows_before"] - len(df)

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    null_mask = (
        df["Product Name"].isna()
        | df["Sales"].isna()
        | df[NUMERIC_COLUMNS].isna().any(axis=1)
    )
    stats["invalid_rows_removed"] = int(null_mask.sum())
    df = df[~null_mask].copy()

    for col in ["Category", "Region", "Sub-Category"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    df["order_month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["order_year"] = df["Order Date"].dt.year
    df["profit_margin"] = df.apply(
        lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0.0,
        axis=1,
    )

    stats["rows_after"] = len(df)
    return df, stats
