"""Load and clean sales CSVs for the dashboard."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import pandas as pd

NUMERIC_COLUMNS = ["Sales", "Quantity", "Discount", "Profit"]
REQUIRED_COLUMNS = [
    "Order ID",
    "Order Date",
    "Product Name",
    "Category",
    "Sales",
    "Profit",
    "Quantity",
]
OPTIONAL_FILL = {
    "Region": "All",
    "Sub-Category": "Unknown",
    "Category": "Unknown",
}


class DataValidationError(ValueError):
    """Raised when a CSV is missing required columns or cannot be parsed."""

    def __init__(self, message: str, *, missing_columns: list[str] | None = None):
        super().__init__(message)
        self.missing_columns = missing_columns or []


def _read_csv(source: str | Path | bytes | BinaryIO) -> pd.DataFrame:
    if isinstance(source, (str, Path)):
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        return pd.read_csv(path, encoding="utf-8")

    if isinstance(source, bytes):
        return pd.read_csv(BytesIO(source), encoding="utf-8")

    return pd.read_csv(source, encoding="utf-8")


def validate_columns(df: pd.DataFrame) -> list[str]:
    """Return list of missing required column names."""
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]


def load_sales_csv(source: str | Path | bytes | BinaryIO) -> tuple[pd.DataFrame, dict]:
    """Load and clean a sales CSV. Returns cleaned DataFrame and cleaning stats.

    Accepts a filesystem path, raw bytes, or a binary file-like object.
    Raises DataValidationError when required columns are missing.
    """
    try:
        df = _read_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise DataValidationError("The CSV is empty.") from exc

    missing = validate_columns(df)
    if missing:
        raise DataValidationError(
            f"Missing required columns: {', '.join(missing)}",
            missing_columns=missing,
        )

    stats = {"rows_before": len(df)}

    date_cols = [c for c in ("Order Date", "Ship Date") if c in df.columns]
    for date_col in date_cols:
        # Superstore exports use day-first dates (for example, 8/11/2016 is
        # 8 November). Preserve ISO dates' unambiguous year-first meaning
        # while parsing slash-separated values as day-first.
        values = df[date_col].astype("string").str.strip()
        iso_mask = values.str.match(r"^\d{4}[-/]", na=False)
        parsed = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
        if iso_mask.any():
            parsed.loc[iso_mask] = pd.to_datetime(
                values.loc[iso_mask], format="mixed", dayfirst=False, errors="coerce"
            )
        if (~iso_mask).any():
            parsed.loc[~iso_mask] = pd.to_datetime(
                values.loc[~iso_mask], format="mixed", dayfirst=True, errors="coerce"
            )
        df[date_col] = parsed

    df = df.drop_duplicates()
    stats["duplicates_removed"] = stats["rows_before"] - len(df)

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        elif col == "Discount":
            df[col] = 0.0

    null_mask = df[REQUIRED_COLUMNS].isna().any(axis=1)
    stats["invalid_rows_removed"] = int(null_mask.sum())
    df = df[~null_mask].copy()

    if df.empty:
        raise DataValidationError("The CSV contains no valid sales rows.")

    for col, default in OPTIONAL_FILL.items():
        if col not in df.columns:
            df[col] = default
        else:
            df[col] = df[col].fillna(default)

    df["order_month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["order_year"] = df["Order Date"].dt.year
    df["profit_margin"] = df.apply(
        lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0.0,
        axis=1,
    )

    stats["rows_after"] = len(df)
    return df, stats


def load_superstore(path: str | Path) -> tuple[pd.DataFrame, dict]:
    """Backward-compatible alias for load_sales_csv."""
    return load_sales_csv(path)
