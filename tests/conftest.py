"""Fixtures shared across tests."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import pytest


@pytest.fixture
def sample_rows() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Order ID": ["A1", "A1", "B2", "C3", "C3"],
            "Order Date": ["2023-01-15", "2023-01-15", "2023-02-10", "2023-03-05", "2023-03-05"],
            "Product Name": ["Desk", "Chair", "Desk", "Lamp", "Chair"],
            "Category": ["Furniture", "Furniture", "Furniture", "Office Supplies", "Furniture"],
            "Sub-Category": ["Tables", "Chairs", "Tables", "Lighting", "Chairs"],
            "Region": ["West", "West", "East", "South", "East"],
            "Sales": [200.0, 100.0, 250.0, 50.0, 80.0],
            "Profit": [40.0, 20.0, 50.0, 10.0, 15.0],
            "Quantity": [2, 1, 2, 1, 1],
            "Discount": [0.0, 0.1, 0.0, 0.0, 0.0],
        }
    )


@pytest.fixture
def sample_csv_bytes(sample_rows: pd.DataFrame) -> bytes:
    buffer = BytesIO()
    sample_rows.to_csv(buffer, index=False)
    return buffer.getvalue()


@pytest.fixture
def minimal_csv_bytes() -> bytes:
    """Required columns only — no Region / Sub-Category."""
    df = pd.DataFrame(
        {
            "Order ID": ["X1", "X2"],
            "Order Date": ["2024-01-01", "2024-02-01"],
            "Product Name": ["Pen", "Paper"],
            "Category": ["Office Supplies", "Office Supplies"],
            "Sales": [10.0, 20.0],
            "Profit": [2.0, 5.0],
            "Quantity": [1, 2],
        }
    )
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()
