"""SalesPulse design system: palette, global CSS, and reusable UI components.

All components render through ``st.html`` (not ``st.markdown``). ``st.html`` skips
Markdown parsing, so indentation and blank lines can never be misread as a code
block. Dynamic text is escaped via ``esc`` to keep the markup well-formed and
injection-safe.
"""

import html as _html

import streamlit as st


def esc(value: object) -> str:
    """HTML-escape any value before interpolating it into markup."""
    return _html.escape(str(value), quote=True)


# Brand palette — deep slate + teal (B2B, not indigo SaaS default)
PRIMARY = "#0F766E"  # teal-700
PRIMARY_DARK = "#115E59"  # teal-800
ACCENT = "#0369A1"  # sky-700; readable against white and in the hero gradient
SUCCESS = "#047857"  # emerald-700; WCAG AA on white
DANGER = "#DC2626"
WARNING = "#B45309"  # amber-700; WCAG AA on white
INK = "#0B1220"
MUTED = "#5B6B7C"
SURFACE = "#FFFFFF"
CANVAS = "#F3F6F8"
BORDER = "#D8E0E7"

CHART_SEQUENCE = ["#0F766E", "#0369A1", "#047857", "#B45309", "#DC2626", "#334155", "#64748B"]

FONT_STACK = (
    "'DM Sans', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
)
DISPLAY_STACK = (
    "'Source Serif 4', Georgia, 'Times New Roman', serif"
)


def inject_css() -> None:
    """Inject global stylesheet. Call once, right after set_page_config."""
    st.html(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
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
                radial-gradient(1100px 520px at 100% -8%, rgba(14,165,233,0.07), transparent 58%),
                radial-gradient(900px 480px at -8% 4%, rgba(15,118,110,0.08), transparent 55%),
                {CANVAS};
        }}

        .block-container {{ padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px; }}

        #MainMenu, footer, header {{ visibility: hidden; }}

        .hero {{
            background: linear-gradient(135deg, {PRIMARY_DARK} 0%, {PRIMARY} 58%, {ACCENT} 140%);
            border-radius: 18px;
            padding: 28px 32px;
            color: #fff;
            box-shadow: 0 18px 40px -22px rgba(15,118,110,0.55);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }}
        .hero h1 {{
            font-family: {DISPLAY_STACK};
            font-size: 1.75rem; font-weight: 700; margin: 0;
            letter-spacing: -0.02em; color:#fff;
        }}
        .hero p {{ margin: 6px 0 0; opacity: 0.92; font-size: 0.95rem; }}
        .hero-badge {{
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.28);
            padding: 8px 14px; border-radius: 8px;
            font-size: 0.8rem; font-weight: 600; white-space: nowrap;
        }}

        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 18px 0 4px; }}
        @media (max-width: 900px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 520px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}
        .kpi-card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 14px;
            padding: 18px 18px 16px;
            box-shadow: 0 1px 2px rgba(11,18,32,0.04), 0 8px 24px -16px rgba(11,18,32,0.16);
            transition: transform .15s ease, box-shadow .15s ease;
            position: relative; overflow: hidden;
        }}
        .kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 28px -14px rgba(11,18,32,0.22); }}
        .kpi-card::before {{
            content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
            background: linear-gradient(180deg, var(--primary), var(--accent));
        }}
        .kpi-top {{ display: flex; align-items: center; justify-content: space-between; }}
        .kpi-label {{ color: {MUTED}; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }}
        .kpi-icon {{
            width: 36px; height: 36px; border-radius: 9px;
            display: flex; align-items: center; justify-content: center;
            font-size: 0.72rem; font-weight: 700; letter-spacing: 0.02em;
            background: rgba(15,118,110,0.10); color: {PRIMARY_DARK};
        }}
        .kpi-value {{ font-size: 1.75rem; font-weight: 700; color: {INK}; margin-top: 10px; letter-spacing: -0.02em; }}
        .kpi-delta {{ font-size: 0.82rem; font-weight: 600; margin-top: 4px; display: inline-flex; align-items: center; gap: 4px; }}
        .kpi-delta.up {{ color: {SUCCESS}; }}
        .kpi-delta.down {{ color: {DANGER}; }}
        .kpi-delta.flat {{ color: {MUTED}; }}

        .section-head {{ display: flex; align-items: center; gap: 10px; margin: 6px 0 2px; }}
        .section-head .dot {{ width: 10px; height: 10px; border-radius: 3px; background: linear-gradient(135deg, var(--primary), var(--accent)); }}
        .section-head h3 {{
            margin: 0; font-size: 1.15rem; font-weight: 700; color: {INK};
            letter-spacing: -0.01em; font-family: {DISPLAY_STACK};
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {SURFACE}; border-radius: 14px; border: 1px solid {BORDER} !important;
            box-shadow: 0 8px 24px -18px rgba(11,18,32,0.16);
        }}

        section[data-testid="stSidebar"] {{
            background: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        .brand {{ display: flex; align-items: center; gap: 11px; padding: 4px 2px 14px; }}
        .brand-logo {{
            width: 38px; height: 38px; border-radius: 10px; flex: none;
            background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
            display: flex; align-items: center; justify-content: center;
            color: #fff; font-weight: 700; font-size: 0.95rem;
            box-shadow: 0 8px 18px -10px rgba(15,118,110,0.65);
            font-family: {FONT_STACK};
        }}
        .brand-name {{ font-weight: 700; font-size: 1.05rem; color: {INK}; line-height: 1.1; }}
        .brand-sub {{ font-size: 0.72rem; color: {MUTED}; font-weight: 500; }}

        .stMultiSelect [data-baseweb="tag"] {{ background: {PRIMARY}; }}
        .stRadio [role="radiogroup"] {{ gap: 6px; }}

        div[data-testid="stMetric"] {{
            background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px;
            padding: 14px 16px; box-shadow: 0 6px 18px -16px rgba(11,18,32,0.18);
        }}

        .divider-soft {{ height: 1px; background: {BORDER}; border: 0; margin: 22px 0; }}
        .empty-state {{
            border: 1px dashed {BORDER}; border-radius: 12px; padding: 28px 20px;
            text-align: center; color: {MUTED}; background: rgba(255,255,255,0.6);
            margin: 12px 0;
        }}
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
        f'<div class="brand-logo">SP</div>'
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


def empty_state(message: str) -> None:
    st.html(f'<div class="empty-state">{esc(message)}</div>')


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
