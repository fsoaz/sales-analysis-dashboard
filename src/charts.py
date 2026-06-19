import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def top_products_chart(df: pd.DataFrame, by: str = "Quantity") -> go.Figure:
    """Horizontal bar chart of top products."""
    metric = "Sales" if by == "Sales" else "Quantity"
    label = "Sales ($)" if by == "Sales" else "Quantity"
    data = df.sort_values(metric, ascending=True)

    fig = px.bar(
        data,
        x=metric,
        y="Product Name",
        orientation="h",
        title=f"Top Products by {label}",
        labels={metric: label, "Product Name": "Product"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420)
    return fig


def monthly_revenue_chart(df: pd.DataFrame) -> go.Figure:
    """Line chart of monthly revenue."""
    fig = px.line(
        df,
        x="order_month",
        y="Revenue",
        markers=True,
        title="Monthly Revenue",
        labels={"order_month": "Month", "Revenue": "Revenue ($)"},
    )
    fig.update_layout(xaxis={"tickangle": -45}, height=400)
    return fig


def category_profit_chart(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart of profit by category and sub-category."""
    fig = px.bar(
        df,
        x="Sub-Category",
        y="Profit",
        color="Category",
        title="Profit by Category and Sub-Category",
        labels={"Profit": "Profit ($)", "Sub-Category": "Sub-Category"},
    )
    fig.update_layout(xaxis={"tickangle": -45}, height=420)
    return fig


def category_margin_chart(df: pd.DataFrame) -> go.Figure:
    """Bar chart of profit margin % per category."""
    data = df.copy()
    data["margin_pct"] = data["profit_margin"] * 100

    fig = px.bar(
        data,
        x="Category",
        y="margin_pct",
        title="Profit Margin by Category",
        labels={"margin_pct": "Margin (%)", "Category": "Category"},
        text=data["margin_pct"].map(lambda v: f"{v:.1f}%"),
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(height=380)
    return fig
