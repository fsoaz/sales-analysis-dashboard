"""Lightweight i18n for the dashboard. Supports en-US and pt-BR."""

LANGUAGES = {
    "English (US)": "en",
    "Português (BR)": "pt",
}

DEFAULT_LANG = "en"

TRANSLATIONS = {
    "en": {
        "page_title": "Sales Analysis",
        "app_title": "Superstore Sales Analysis",
        "app_caption": "KPIs, top products, monthly revenue, and category profitability",
        "brand_name": "Superstore",
        "brand_tagline": "Sales Intelligence",
        "hero_badge": "● Live data",
        "vs_prior": "vs prior period",
        "workspace": "Workspace",
        "dataset_not_found": "Dataset not found.",
        "dataset_help": (
            "Download the [Superstore Sales dataset]"
            "(https://www.kaggle.com/datasets/kyanyoga/sample-superstore-dataset) "
            "and save it as `data/superstore.csv`."
        ),
        "language": "Language",
        "filters": "Filters",
        "order_date_range": "Order date range",
        "region": "Region",
        "category": "Category",
        "data_cleaning_summary": "Data cleaning summary",
        "rows_before": "Rows before cleaning: {n:,}",
        "duplicates_removed": "Duplicates removed: {n:,}",
        "invalid_rows_removed": "Invalid rows removed: {n:,}",
        "rows_after": "Rows after cleaning: {n:,}",
        "select_region_category": "Select at least one region and one category.",
        "no_data": "No data matches the current filters.",
        "total_revenue": "Total Revenue",
        "total_profit": "Total Profit",
        "total_orders": "Total Orders",
        "avg_order_value": "Avg Order Value",
        "products_question": "Which products sell the most?",
        "rank_products_by": "Rank products by",
        "quantity": "Quantity",
        "sales": "Sales",
        "top_product": "Top Product",
        "top_product_metric": "Top product {label}",
        "label_sales": "sales",
        "label_units_sold": "units sold",
        "months_question": "Which months have the highest revenue?",
        "peak_month": "Peak Month",
        "peak_revenue": "Peak Revenue",
        "categories_question": "Which categories are the most profitable?",
        "most_profitable_category": "Most Profitable Category",
        "category_profit": "Category Profit",
        # charts
        "chart_top_products_title": "Top Products by {label}",
        "chart_sales_axis": "Sales ($)",
        "chart_product": "Product",
        "chart_monthly_revenue_title": "Monthly Revenue",
        "chart_month": "Month",
        "chart_revenue_axis": "Revenue ($)",
        "chart_profit_by_category_title": "Profit by Category and Sub-Category",
        "chart_profit_axis": "Profit ($)",
        "chart_sub_category": "Sub-Category",
        "chart_margin_title": "Profit Margin by Category",
        "chart_margin_axis": "Margin (%)",
    },
    "pt": {
        "page_title": "Análise de Vendas",
        "app_title": "Análise de Vendas Superstore",
        "app_caption": "KPIs, produtos mais vendidos, receita mensal e lucratividade por categoria",
        "brand_name": "Superstore",
        "brand_tagline": "Inteligência de Vendas",
        "hero_badge": "● Dados ao vivo",
        "vs_prior": "vs período anterior",
        "workspace": "Espaço de trabalho",
        "dataset_not_found": "Conjunto de dados não encontrado.",
        "dataset_help": (
            "Baixe o [conjunto de dados Superstore Sales]"
            "(https://www.kaggle.com/datasets/kyanyoga/sample-superstore-dataset) "
            "e salve como `data/superstore.csv`."
        ),
        "language": "Idioma",
        "filters": "Filtros",
        "order_date_range": "Período do pedido",
        "region": "Região",
        "category": "Categoria",
        "data_cleaning_summary": "Resumo da limpeza de dados",
        "rows_before": "Linhas antes da limpeza: {n:,}",
        "duplicates_removed": "Duplicatas removidas: {n:,}",
        "invalid_rows_removed": "Linhas inválidas removidas: {n:,}",
        "rows_after": "Linhas após a limpeza: {n:,}",
        "select_region_category": "Selecione ao menos uma região e uma categoria.",
        "no_data": "Nenhum dado corresponde aos filtros atuais.",
        "total_revenue": "Receita Total",
        "total_profit": "Lucro Total",
        "total_orders": "Total de Pedidos",
        "avg_order_value": "Ticket Médio",
        "products_question": "Quais produtos mais vendem?",
        "rank_products_by": "Ordenar produtos por",
        "quantity": "Quantidade",
        "sales": "Vendas",
        "top_product": "Produto Top",
        "top_product_metric": "{label} do produto top",
        "label_sales": "vendas",
        "label_units_sold": "unidades vendidas",
        "months_question": "Quais meses têm a maior receita?",
        "peak_month": "Mês de Pico",
        "peak_revenue": "Receita de Pico",
        "categories_question": "Quais categorias são mais lucrativas?",
        "most_profitable_category": "Categoria Mais Lucrativa",
        "category_profit": "Lucro da Categoria",
        # charts
        "chart_top_products_title": "Produtos Mais Vendidos por {label}",
        "chart_sales_axis": "Vendas (R$)",
        "chart_product": "Produto",
        "chart_monthly_revenue_title": "Receita Mensal",
        "chart_month": "Mês",
        "chart_revenue_axis": "Receita (R$)",
        "chart_profit_by_category_title": "Lucro por Categoria e Subcategoria",
        "chart_profit_axis": "Lucro (R$)",
        "chart_sub_category": "Subcategoria",
        "chart_margin_title": "Margem de Lucro por Categoria",
        "chart_margin_axis": "Margem (%)",
    },
}


def get_translator(lang: str):
    """Return a t(key, **kwargs) function for the given language code."""
    table = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
    fallback = TRANSLATIONS[DEFAULT_LANG]

    def t(key: str, **kwargs) -> str:
        text = table.get(key, fallback.get(key, key))
        return text.format(**kwargs) if kwargs else text

    return t
