"""Lightweight i18n for the dashboard. Supports en-US and pt-BR."""

LANGUAGES = {
    "English (US)": "en",
    "Português (BR)": "pt",
}

DEFAULT_LANG = "en"

CURRENCY_SYMBOL = {
    "en": "$",
    "pt": "R$",
}

TRANSLATIONS = {
    "en": {
        "page_title": "SalesPulse",
        "app_title": "SalesPulse Analytics",
        "app_caption": "KPIs, top products, monthly revenue, and category profitability",
        "brand_name": "SalesPulse",
        "brand_tagline": "Sales Intelligence",
        "hero_badge_sample": "Sample data",
        "hero_badge_upload": "Your upload",
        "vs_prior": "vs prior period",
        "workspace": "Workspace",
        "dataset_not_found": "Sample dataset not found.",
        "dataset_help": (
            "Place `data/sample_superstore.csv` in the project, or upload your own CSV "
            "from the sidebar."
        ),
        "language": "Language / Idioma",
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
        "loading_data": "Loading data…",
        "empty_chart": "No rows to chart for the current filters.",
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
        # data source
        "data_source": "Data source",
        "source_sample": "Sample dataset",
        "source_upload": "Upload CSV",
        "upload_csv": "Upload sales CSV",
        "upload_help": (
            "Required columns: Order ID, Order Date, Product Name, Category, "
            "Sales, Profit, Quantity. Region and Sub-Category are optional."
        ),
        "upload_missing": "Upload a CSV to continue.",
        "validation_error": "Could not load this file: {detail}",
        "missing_columns": "Missing required columns: {cols}",
        # auth
        "login_title": "Sign in to SalesPulse",
        "login_caption": "Enter the workspace password to open the dashboard.",
        "login_badge": "Secure access",
        "password": "Password",
        "sign_in": "Sign in",
        "sign_out": "Sign out",
        "auth_invalid": "Incorrect password.",
        "auth_locked": "Too many failed attempts. Try again in {seconds} seconds.",
        "auth_secrets_missing": "App password is not configured.",
        "auth_secrets_help": (
            "Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` "
            "and set `app_password`, or add the secret in Streamlit Community Cloud."
        ),
        # export
        "export": "Export",
        "download_csv": "Download filtered CSV",
        "download_excel": "Download Excel report",
        # charts
        "chart_top_products_title": "Top Products by {label}",
        "chart_sales_axis": "Sales ({symbol})",
        "chart_product": "Product",
        "chart_monthly_revenue_title": "Monthly Revenue",
        "chart_month": "Month",
        "chart_revenue_axis": "Revenue ({symbol})",
        "chart_profit_by_category_title": "Profit by Category and Sub-Category",
        "chart_profit_axis": "Profit ({symbol})",
        "chart_sub_category": "Sub-Category",
        "chart_margin_title": "Profit Margin by Category",
        "chart_margin_axis": "Margin (%)",
    },
    "pt": {
        "page_title": "SalesPulse",
        "app_title": "SalesPulse Analytics",
        "app_caption": "KPIs, produtos mais vendidos, receita mensal e lucratividade por categoria",
        "brand_name": "SalesPulse",
        "brand_tagline": "Inteligência de Vendas",
        "hero_badge_sample": "Dados de exemplo",
        "hero_badge_upload": "Seu arquivo",
        "vs_prior": "vs período anterior",
        "workspace": "Espaço de trabalho",
        "dataset_not_found": "Conjunto de dados de exemplo não encontrado.",
        "dataset_help": (
            "Coloque `data/sample_superstore.csv` no projeto, ou envie seu próprio "
            "CSV pela barra lateral."
        ),
        "language": "Language / Idioma",
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
        "loading_data": "Carregando dados…",
        "empty_chart": "Nenhuma linha para o gráfico com os filtros atuais.",
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
        # data source
        "data_source": "Fonte de dados",
        "source_sample": "Conjunto de exemplo",
        "source_upload": "Enviar CSV",
        "upload_csv": "Enviar CSV de vendas",
        "upload_help": (
            "Colunas obrigatórias: Order ID, Order Date, Product Name, Category, "
            "Sales, Profit, Quantity. Region e Sub-Category são opcionais."
        ),
        "upload_missing": "Envie um CSV para continuar.",
        "validation_error": "Não foi possível carregar este arquivo: {detail}",
        "missing_columns": "Colunas obrigatórias ausentes: {cols}",
        # auth
        "login_title": "Entrar no SalesPulse",
        "login_caption": "Digite a senha do espaço de trabalho para abrir o painel.",
        "login_badge": "Acesso seguro",
        "password": "Senha",
        "sign_in": "Entrar",
        "sign_out": "Sair",
        "auth_invalid": "Senha incorreta.",
        "auth_locked": "Muitas tentativas inválidas. Tente novamente em {seconds} segundos.",
        "auth_secrets_missing": "A senha do app não está configurada.",
        "auth_secrets_help": (
            "Copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml` "
            "e defina `app_password`, ou adicione o segredo no Streamlit Community Cloud."
        ),
        # export
        "export": "Exportar",
        "download_csv": "Baixar CSV filtrado",
        "download_excel": "Baixar relatório Excel",
        # charts
        "chart_top_products_title": "Produtos Mais Vendidos por {label}",
        "chart_sales_axis": "Vendas ({symbol})",
        "chart_product": "Produto",
        "chart_monthly_revenue_title": "Receita Mensal",
        "chart_month": "Mês",
        "chart_revenue_axis": "Receita ({symbol})",
        "chart_profit_by_category_title": "Lucro por Categoria e Subcategoria",
        "chart_profit_axis": "Lucro ({symbol})",
        "chart_sub_category": "Subcategoria",
        "chart_margin_title": "Margem de Lucro por Categoria",
        "chart_margin_axis": "Margem (%)",
    },
}


def currency_symbol(lang: str) -> str:
    return CURRENCY_SYMBOL.get(lang, CURRENCY_SYMBOL[DEFAULT_LANG])


def get_translator(lang: str):
    """Return a t(key, **kwargs) function for the given language code."""
    table = TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANG])
    fallback = TRANSLATIONS[DEFAULT_LANG]

    def t(key: str, **kwargs) -> str:
        text = table.get(key, fallback.get(key, key))
        return text.format(**kwargs) if kwargs else text

    return t
