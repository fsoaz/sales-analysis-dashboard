"""SaaS-style design system: palette, global CSS, and reusable UI components.

All components render through ``st.html`` (not ``st.markdown``). ``st.html`` skips
Markdown parsing, so indentation and blank lines can never be misread as a code
block — the failure mode that previously broke the KPI grid. Dynamic text is
escaped via ``esc`` to keep the markup well-formed and injection-safe.
"""

import html as _html

import streamlit as st


def esc(value: object) -> str:
    """HTML-escape any value before interpolating it into markup."""
    return _html.escape(str(value), quote=True)

# Brand palette ------------------------------------------------------------
PRIMARY = "#6366F1"      # indigo
PRIMARY_DARK = "#4F46E5"
ACCENT = "#06B6D4"       # cyan
SUCCESS = "#10B981"
DANGER = "#EF4444"
WARNING = "#F59E0B"
INK = "#0F172A"
MUTED = "#64748B"
SURFACE = "#FFFFFF"
CANVAS = "#F8FAFC"
BORDER = "#E2E8F0"

# Ordered palette for categorical charts
CHART_SEQUENCE = ["#6366F1", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]

FONT_STACK = (
    "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
)


def inject_css() -> None:
    """Inject global stylesheet. Call once, right after set_page_config."""
    st.html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
        :root {{
            --primary: {PRIMARY};
            --primary-dark: {PRIMARY_DARK};
            --accent: {ACCENT};
            --ink: {INK};
            --muted: {MUTED};
            --surface: {SURFACE};
            --canvas: {CANVAS};
            --border: {BORDER};
        }}

        html, body, [class*="css"], .stMarkdown, .stMetric {{
            font-family: {FONT_STACK};
        }}

        .stApp {{
            background:
                radial-gradient(1200px 600px at 100% -10%, rgba(99,102,241,0.08), transparent 60%),
                radial-gradient(900px 500px at -10% 0%, rgba(6,182,212,0.06), transparent 55%),
                {CANVAS};
        }}

        /* Tighten default top padding */
        .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px; }}

        /* Hide Streamlit chrome for a product feel */
        #MainMenu, footer, header {{ visibility: hidden; }}

        /* Hero -------------------------------------------------------- */
        .hero {{
            background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 55%, {ACCENT} 130%);
            border-radius: 20px;
            padding: 28px 32px;
            color: #fff;
            box-shadow: 0 20px 45px -20px rgba(79,70,229,0.55);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}
        .hero h1 {{ font-size: 1.7rem; font-weight: 800; margin: 0; letter-spacing: -0.02em; color:#fff; }}
        .hero p {{ margin: 6px 0 0; opacity: 0.9; font-size: 0.95rem; }}
        .hero-badge {{
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.28);
            padding: 8px 14px; border-radius: 999px;
            font-size: 0.8rem; font-weight: 600; white-space: nowrap;
            backdrop-filter: blur(6px);
        }}

        /* KPI cards --------------------------------------------------- */
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 18px 0 4px; }}
        @media (max-width: 900px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        .kpi-card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 18px 18px 16px;
            box-shadow: 0 1px 2px rgba(15,23,42,0.04), 0 8px 24px -16px rgba(15,23,42,0.18);
            transition: transform .15s ease, box-shadow .15s ease;
            position: relative; overflow: hidden;
        }}
        .kpi-card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 30px -12px rgba(15,23,42,0.25); }}
        .kpi-card::before {{
            content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
            background: linear-gradient(180deg, var(--primary), var(--accent));
        }}
        .kpi-top {{ display: flex; align-items: center; justify-content: space-between; }}
        .kpi-label {{ color: {MUTED}; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
        .kpi-icon {{
            width: 38px; height: 38px; border-radius: 11px;
            display: flex; align-items: center; justify-content: center; font-size: 1.05rem;
            background: rgba(99,102,241,0.10); color: {PRIMARY_DARK};
        }}
        .kpi-value {{ font-size: 1.8rem; font-weight: 800; color: {INK}; margin-top: 10px; letter-spacing: -0.02em; }}
        .kpi-delta {{ font-size: 0.82rem; font-weight: 600; margin-top: 4px; display: inline-flex; align-items: center; gap: 4px; }}
        .kpi-delta.up {{ color: {SUCCESS}; }}
        .kpi-delta.down {{ color: {DANGER}; }}
        .kpi-delta.flat {{ color: {MUTED}; }}

        /* Section headers --------------------------------------------- */
        .section-head {{ display: flex; align-items: center; gap: 10px; margin: 6px 0 2px; }}
        .section-head .dot {{ width: 10px; height: 10px; border-radius: 3px; background: linear-gradient(135deg, var(--primary), var(--accent)); }}
        .section-head h3 {{ margin: 0; font-size: 1.15rem; font-weight: 700; color: {INK}; letter-spacing: -0.01em; }}

        /* Bordered containers as cards */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {SURFACE}; border-radius: 16px; border: 1px solid {BORDER} !important;
            box-shadow: 0 8px 24px -18px rgba(15,23,42,0.18);
        }}

        /* Sidebar ----------------------------------------------------- */
        section[data-testid="stSidebar"] {{
            background: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        .brand {{ display: flex; align-items: center; gap: 11px; padding: 4px 2px 14px; }}
        .brand-logo {{
            width: 38px; height: 38px; border-radius: 11px; flex: none;
            background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
            display: flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 800; font-size: 1.1rem;
            box-shadow: 0 8px 20px -8px rgba(99,102,241,0.7);
        }}
        .brand-name {{ font-weight: 800; font-size: 1.05rem; color: {INK}; line-height: 1.1; }}
        .brand-sub {{ font-size: 0.72rem; color: {MUTED}; font-weight: 500; }}

        /* Inputs */
        .stMultiSelect [data-baseweb="tag"] {{ background: {PRIMARY}; }}
        .stRadio [role="radiogroup"] {{ gap: 6px; }}

        /* Metric tweaks for any native st.metric still used */
        div[data-testid="stMetric"] {{
            background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 14px;
            padding: 14px 16px; box-shadow: 0 6px 18px -16px rgba(15,23,42,0.2);
        }}

        .divider-soft {{ height: 1px; background: {BORDER}; border: 0; margin: 22px 0; }}
        </style>
        """
    )


def hero(title: str, subtitle: str, badge: str) -> None:
    st.html(
        f'<div class="hero">'
        f'<div><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div>'
        f'<div class="hero-badge">{esc(badge)}</div>'
        f'</div>'
    )


def brand(name: str, tagline: str) -> None:
    st.html(
        f'<div class="brand">'
        f'<div class="brand-logo">◆</div>'
        f'<div><div class="brand-name">{esc(name)}</div>'
        f'<div class="brand-sub">{esc(tagline)}</div></div>'
        f'</div>'
    )


def section(title: str) -> None:
    st.html(
        f'<div class="section-head"><span class="dot"></span><h3>{esc(title)}</h3></div>'
    )


def divider() -> None:
    st.html('<hr class="divider-soft">')


def kpi_cards(cards: list[dict]) -> None:
    """Render a responsive grid of KPI cards.

    Each card dict: {label, value, icon, delta (optional str), trend ('up'|'down'|'flat')}.
    """
    parts = ['<div class="kpi-grid">']
    arrows = {"up": "▲", "down": "▼", "flat": "■"}
    for c in cards:
        delta_html = ""
        if c.get("delta"):
            trend = c.get("trend", "flat")
            trend_class = trend if trend in arrows else "flat"
            delta_html = (
                f'<div class="kpi-delta {trend_class}">'
                f'{arrows.get(trend_class, "")} {esc(c["delta"])}</div>'
            )
        parts.append(
            f'<div class="kpi-card">'
            f'<div class="kpi-top">'
            f'<span class="kpi-label">{esc(c["label"])}</span>'
            f'<span class="kpi-icon">{esc(c["icon"])}</span>'
            f'</div>'
            f'<div class="kpi-value">{esc(c["value"])}</div>'
            f'{delta_html}'
            f'</div>'
        )
    parts.append("</div>")
    st.html("".join(parts))
