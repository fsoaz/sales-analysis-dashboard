import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.i18n import get_translator
from src.styles import BORDER, CHART_SEQUENCE, INK, MUTED, PRIMARY

FONT = "Inter, -apple-system, Segoe UI, Roboto, sans-serif"


def _style(fig: go.Figure, *, title: str = "") -> go.Figure:
    """Apply shared SaaS chart theme: clean grid, brand font, transparent bg."""
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=15, color=INK, family=FONT), x=0, xanchor="left"),
        font=dict(family=FONT, color=MUTED, size=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=12, t=44, b=8),
        colorway=CHART_SEQUENCE,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=""),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family=FONT, bordercolor=BORDER),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=BORDER, tickcolor=BORDER)
    fig.update_yaxes(showgrid=True, gridcolor=BORDER, zeroline=False, linecolor="rgba(0,0,0,0)")
    return fig


def top_products_chart(df: pd.DataFrame, by: str = "Quantity", t=None) -> go.Figure:
    """Horizontal bar chart of top products."""
    t = t or get_translator("en")
    metric = "Sales" if by == "Sales" else "Quantity"
    label = t("chart_sales_axis") if by == "Sales" else t("quantity")
    data = df.sort_values(metric, ascending=True)

    fig = px.bar(
        data,
        x=metric,
        y="Product Name",
        orientation="h",
        labels={metric: label, "Product Name": t("chart_product")},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(marker_line_width=0, hovertemplate="%{y}<br>%{x}<extra></extra>")
    _style(fig, title=t("chart_top_products_title", label=label))
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=420)
    fig.update_yaxes(showgrid=False)
    return fig


def monthly_revenue_chart(df: pd.DataFrame, t=None) -> go.Figure:
    """Line chart of monthly revenue."""
    t = t or get_translator("en")
    fig = px.area(
        df,
        x="order_month",
        y="Revenue",
        markers=True,
        labels={"order_month": t("chart_month"), "Revenue": t("chart_revenue_axis")},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(
        line=dict(width=2.5),
        fillcolor="rgba(99,102,241,0.12)",
        marker=dict(size=6),
        hovertemplate="%{x}<br>%{y:$,.0f}<extra></extra>",
    )
    _style(fig, title=t("chart_monthly_revenue_title"))
    fig.update_layout(xaxis={"tickangle": -45}, height=400)
    return fig


def category_profit_chart(df: pd.DataFrame, t=None) -> go.Figure:
    """Grouped bar chart of profit by category and sub-category."""
    t = t or get_translator("en")
    fig = px.bar(
        df,
        x="Sub-Category",
        y="Profit",
        color="Category",
        labels={
            "Profit": t("chart_profit_axis"),
            "Sub-Category": t("chart_sub_category"),
            "Category": t("category"),
        },
    )
    fig.update_traces(marker_line_width=0)
    _style(fig, title=t("chart_profit_by_category_title"))
    fig.update_xaxes(tickfont=dict(size=12, color=INK), automargin=True)
    fig.update_yaxes(title_font=dict(size=12, color=MUTED))
    fig.update_layout(
        xaxis={"tickangle": -45},
        height=440,
        barmode="relative",
        title_font=dict(size=17, color=INK, family=FONT),
        # Legend below the plot so it never overlaps the top-left title.
        legend=dict(orientation="h", yanchor="top", y=-0.32, xanchor="center", x=0.5, title=""),
    )
    return fig


def category_margin_chart(df: pd.DataFrame, t=None) -> go.Figure:
    """Bar chart of profit margin % per category."""
    t = t or get_translator("en")
    data = df.copy()
    data["margin_pct"] = data["profit_margin"] * 100

    fig = px.bar(
        data,
        x="Category",
        y="margin_pct",
        labels={"margin_pct": t("chart_margin_axis"), "Category": t("category")},
        text=data["margin_pct"].map(lambda v: f"{v:.1f}%"),
        color="margin_pct",
        color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_width=0,
        textfont=dict(family=FONT, size=13, color=INK),
    )
    _style(fig, title=t("chart_margin_title"))

    # Headroom so the outside % labels never clip (covers negative-margin bars).
    lo = min(0.0, float(data["margin_pct"].min()))
    hi = max(0.0, float(data["margin_pct"].max()))
    pad = (hi - lo) * 0.15 or 5.0
    fig.update_yaxes(range=[lo - pad, hi + pad], title_font=dict(size=12, color=MUTED))
    fig.update_xaxes(tickfont=dict(size=12, color=INK))
    fig.update_layout(
        height=380,
        coloraxis_showscale=False,
        title_font=dict(size=17, color=INK, family=FONT),
    )
    return fig
