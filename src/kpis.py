import pandas as pd


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute summary KPIs from a filtered DataFrame."""
    order_count = df["Order ID"].nunique()
    total_revenue = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    product_qty = df.groupby("Product Name")["Quantity"].sum()
    product_sales = df.groupby("Product Name")["Sales"].sum()
    monthly_revenue = df.groupby("order_month")["Sales"].sum()
    category_profit = df.groupby("Category")["Profit"].sum()

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": order_count,
        "avg_order_value": total_revenue / order_count if order_count else 0.0,
        "top_product_by_quantity": product_qty.idxmax() if len(product_qty) else None,
        "top_product_quantity": product_qty.max() if len(product_qty) else 0,
        "top_product_by_sales": product_sales.idxmax() if len(product_sales) else None,
        "top_product_sales": product_sales.max() if len(product_sales) else 0.0,
        "best_month": monthly_revenue.idxmax() if len(monthly_revenue) else None,
        "best_month_revenue": monthly_revenue.max() if len(monthly_revenue) else 0.0,
        "top_category": category_profit.idxmax() if len(category_profit) else None,
        "top_category_profit": category_profit.max() if len(category_profit) else 0.0,
    }


def top_products(df: pd.DataFrame, by: str = "Quantity", n: int = 10) -> pd.DataFrame:
    """Return top N products ranked by quantity or sales."""
    metric = "Sales" if by == "Sales" else "Quantity"
    grouped = (
        df.groupby("Product Name")
        .agg(Quantity=("Quantity", "sum"), Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values(metric, ascending=False)
        .head(n)
        .reset_index()
    )
    return grouped


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly revenue totals sorted chronologically."""
    return (
        df.groupby("order_month", as_index=False)["Sales"]
        .sum()
        .rename(columns={"Sales": "Revenue"})
        .sort_values("order_month")
    )


def category_profitability(df: pd.DataFrame) -> pd.DataFrame:
    """Return profit and margin by category and sub-category."""
    grouped = (
        df.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"))
    )
    grouped["profit_margin"] = grouped.apply(
        lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0.0,
        axis=1,
    )
    return grouped.sort_values("Profit", ascending=False)


def category_margin_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return profit margin % per top-level category."""
    grouped = (
        df.groupby("Category", as_index=False)
        .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"))
    )
    grouped["profit_margin"] = grouped.apply(
        lambda row: row["Profit"] / row["Sales"] if row["Sales"] != 0 else 0.0,
        axis=1,
    )
    return grouped.sort_values("profit_margin", ascending=False)
