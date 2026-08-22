import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ChainSight AI",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# DESIGN TOKENS
# --------------------------------------------------
# Palette — cool navy-ink base with a two-accent system:
#   cyan  = instrumentation / primary reads (the "sight")
#   amber = attention / things that need a human
# Type   — IBM Plex Mono for every number (this is a product about
#           reading instruments), Inter for everything you read as prose.

BG        = "#0A0E16"
PANEL     = "#121826"
PANEL_HI  = "#161E2E"
BORDER    = "#232C3D"
TEXT      = "#EAF0F7"
MUTED     = "#8592A6"
CYAN      = "#31D6C8"
CYAN_DIM  = "rgba(49,214,200,0.14)"
AMBER     = "#F5A623"
AMBER_DIM = "rgba(245,166,35,0.14)"
POS       = "#3ED598"
NEG       = "#F0654F"

CHART_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono, monospace", color=MUTED, size=12),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=BORDER, tickcolor=BORDER),
        yaxis=dict(showgrid=True, gridcolor=BORDER, zeroline=False),
        margin=dict(l=10, r=10, t=10, b=10),
        hoverlabel=dict(bgcolor=PANEL_HI, bordercolor=BORDER, font=dict(family="IBM Plex Mono, monospace", color=TEXT)),
    )
)

# --------------------------------------------------
# GLOBAL STYLE
# --------------------------------------------------

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(1100px 500px at 15% -10%, rgba(49,214,200,0.07), transparent 60%),
        radial-gradient(900px 500px at 100% 0%, rgba(245,166,35,0.05), transparent 55%),
        {BG};
}}

section[data-testid="stSidebar"] {{
    background-color: {PANEL};
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] .stRadio label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13.5px;
    color: {MUTED};
    padding: 7px 10px;
    border-radius: 8px;
    transition: all 0.15s ease;
    width: 100%;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background: {PANEL_HI};
    color: {TEXT};
}}
section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {{
    border-color: {CYAN} !important;
}}

h1, h2, h3 {{ color: {TEXT}; letter-spacing: -0.01em; }}
p, span, li {{ color: {MUTED}; }}

hr {{ border-color: {BORDER} !important; }}

.stButton > button {{
    width: 100%;
    border-radius: 8px;
    background: {CYAN};
    color: #06181A;
    font-weight: 600;
    border: none;
}}
.stButton > button:hover {{
    background: #4ee3d5;
    color: #06181A;
}}

/* ---- eyebrow label ---- */
.eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.16em;
    color: {CYAN};
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.eyebrow::before {{
    content: "";
    width: 14px;
    height: 1px;
    background: {CYAN};
    display: inline-block;
}}

/* ---- hero ---- */
.hero {{
    padding: 34px 36px 30px 36px;
    border: 1px solid {BORDER};
    border-radius: 16px;
    background: linear-gradient(160deg, {PANEL} 0%, {PANEL_HI} 100%);
    position: relative;
    overflow: hidden;
    margin-bottom: 8px;
}}
.hero-title {{
    font-size: 40px;
    font-weight: 700;
    color: {TEXT};
    margin: 0;
    line-height: 1.1;
}}
.hero-title span {{ color: {CYAN}; }}
.hero-sub {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px;
    color: {MUTED};
    margin-top: 10px;
}}
.scan {{
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, {CYAN}, transparent);
    animation: sweep 3.2s ease-in-out infinite;
}}
@keyframes sweep {{
    0%   {{ transform: translateX(-100%); opacity: 0; }}
    15%  {{ opacity: 1; }}
    50%  {{ transform: translateX(100%); opacity: 1; }}
    65%  {{ opacity: 0; }}
    100% {{ transform: translateX(100%); opacity: 0; }}
}}

/* ---- metric card ---- */
.mcard {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-left: 3px solid {CYAN};
    border-radius: 12px;
    padding: 16px 18px;
    transition: transform 0.15s ease, border-color 0.15s ease;
    height: 100%;
}}
.mcard:hover {{
    transform: translateY(-2px);
    border-color: {CYAN};
}}
.mcard.amber {{ border-left-color: {AMBER}; }}
.mcard-label {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {MUTED};
}}
.mcard-value {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 26px;
    font-weight: 600;
    color: {TEXT};
    margin-top: 6px;
}}
.mcard-delta {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12.5px;
    font-weight: 600;
    margin-top: 6px;
}}

/* ---- nav card (overview explore tiles) ---- */
.navcard {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 18px 18px 16px 18px;
    height: 100%;
    transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}}
.navcard:hover {{
    transform: translateY(-2px);
    border-color: {CYAN};
    background: {PANEL_HI};
}}
.navcard-icon {{ font-size: 20px; }}
.navcard-title {{
    color: {TEXT};
    font-weight: 600;
    font-size: 15px;
    margin-top: 8px;
}}
.navcard-desc {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 4px;
    line-height: 1.4;
}}

/* ---- status pill ---- */
.pill {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: {POS};
    background: rgba(62,213,152,0.10);
    border: 1px solid rgba(62,213,152,0.30);
    padding: 5px 11px;
    border-radius: 999px;
}}
.pill-dot {{
    width: 6px; height: 6px; border-radius: 50%;
    background: {POS};
    box-shadow: 0 0 0 3px rgba(62,213,152,0.18);
}}

/* ---- progress ---- */
.progress-track {{
    background: {PANEL_HI};
    border: 1px solid {BORDER};
    border-radius: 999px;
    height: 10px;
    width: 100%;
    overflow: hidden;
}}
.progress-fill {{
    background: linear-gradient(90deg, {CYAN}, {POS});
    height: 100%;
    border-radius: 999px;
}}

/* ---- section divider (chain motif) ---- */
.chain-divider {{
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 22px 0 18px 0;
    color: {BORDER};
    font-size: 11px;
}}
.chain-divider::before, .chain-divider::after {{
    content: "";
    flex: 1;
    height: 1px;
    background: {BORDER};
}}

</style>
""", unsafe_allow_html=True)


def eyebrow(text):
    st.markdown(f'<div class="eyebrow">{text}</div>', unsafe_allow_html=True)


def metric_card(label, value, delta=None, accent="cyan"):
    delta_html = ""
    if delta:
        positive = delta.strip().startswith("+")
        color = POS if positive else NEG
        arrow = "▲" if positive else "▼"
        delta_html = f'<div class="mcard-delta" style="color:{color};">{arrow} {delta}</div>'
    cls = "mcard amber" if accent == "amber" else "mcard"
    st.markdown(f"""
    <div class="{cls}">
        <div class="mcard-label">{label}</div>
        <div class="mcard-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def nav_card(icon, title, desc):
    st.markdown(f"""
    <div class="navcard">
        <div class="navcard-icon">{icon}</div>
        <div class="navcard-title">{title}</div>
        <div class="navcard-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def chain_divider(label=""):
    st.markdown(f'<div class="chain-divider">{label}</div>', unsafe_allow_html=True)


def line_fig(y_values, color=CYAN, name="", fill=True):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=y_values,
        mode="lines+markers",
        line=dict(color=color, width=2.5, shape="spline"),
        marker=dict(size=5, color=color, line=dict(width=1, color=BG)),
        fill="tozeroy" if fill else None,
        fillcolor=color.replace(")", ",0.12)").replace("rgb", "rgba") if color.startswith("rgb") else None,
        name=name,
        hovertemplate="%{y:,.0f}<extra></extra>",
    ))
    if fill and color == CYAN:
        fig.data[0].fillcolor = "rgba(49,214,200,0.12)"
    fig.update_layout(template=CHART_TEMPLATE, height=260, showlegend=False)
    return fig


def bar_fig(y_values, color=CYAN, name=""):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=y_values,
        marker=dict(color=color, line=dict(width=0)),
        name=name,
        hovertemplate="%{y:,.0f}<extra></extra>",
    ))
    fig.update_traces(marker_cornerradius=6)
    fig.update_layout(template=CHART_TEMPLATE, height=260, showlegend=False, bargap=0.35)
    return fig


def multi_bar_fig(series: dict):
    fig = go.Figure()
    colors = [CYAN, AMBER, "#7C8CF8"]
    for i, (name, values) in enumerate(series.items()):
        fig.add_trace(go.Bar(y=values, name=name, marker=dict(color=colors[i % len(colors)])))
    fig.update_traces(marker_cornerradius=6)
    fig.update_layout(
        template=CHART_TEMPLATE, height=280, barmode="group",
        legend=dict(orientation="h", y=1.15, font=dict(family="IBM Plex Mono, monospace", color=MUTED)),
    )
    return fig


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
        <span style="font-size:26px;">🔗</span>
        <span style="font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;color:{TEXT};">ChainSight<span style="color:{CYAN};">AI</span></span>
    </div>
    <div style="color:{MUTED};font-size:12.5px;margin-bottom:14px;">E-Commerce Intelligence</div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="eyebrow">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        "Go to",
        [
            "🏠 Overview",
            "📊 Executive Dashboard",
            "👥 Customer Analytics",
            "💰 Sales Analytics",
            "🚚 Supply Chain",
            "⭐ Review Analytics",
            "📦 Product Analytics",
            "🤖 AI Business Analyst",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown('<div class="eyebrow">System Status</div>', unsafe_allow_html=True)
    st.markdown('<div class="pill"><span class="pill-dot"></span>Operational</div>', unsafe_allow_html=True)


# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------

if page == "🏠 Overview":

    st.markdown(f"""
    <div class="hero">
        <div class="scan"></div>
        <div class="hero-title">🔗 ChainSight <span>AI</span></div>
        <div class="hero-sub">AI-POWERED E-COMMERCE SUPPLY CHAIN INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    eyebrow("Business Health")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Revenue", "$2.84M", "+18.4%")
    with col2:
        metric_card("Orders", "48.3K", "+12.8%")
    with col3:
        metric_card("Customers", "18.6K", "+9.7%")
    with col4:
        metric_card("On-Time Delivery", "94.6%", "+4.2%")

    chain_divider("EXPLORE")

    col1, col2, col3 = st.columns(3)
    with col1:
        nav_card("📊", "Executive Dashboard", "Monitor overall performance, revenue and orders.")
    with col2:
        nav_card("👥", "Customer Analytics", "Understand customer behavior, growth and retention.")
    with col3:
        nav_card("💰", "Sales Analytics", "Analyze sales, revenue, categories and trends.")

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        nav_card("🚚", "Supply Chain", "Monitor deliveries, logistics and fulfillment.")
    with col2:
        nav_card("⭐", "Review Analytics", "Understand ratings, reviews and customer feedback.")
    with col3:
        nav_card("📦", "Product Analytics", "Explore product performance and categories.")

    chain_divider("ASK CHAINSIGHT")

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"""
        <div class="navcard" style="border-left:3px solid {CYAN};">
            <div class="navcard-title">🤖 AI Business Analyst</div>
            <div class="navcard-desc">Ask questions about your business data using natural language.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.write("")
        if st.button("Open Analyst →"):
            st.info("Select '🤖 AI Business Analyst' from the sidebar.")


# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

elif page == "📊 Executive Dashboard":

    eyebrow("Overview")
    st.title("📊 Executive Dashboard")
    st.write("High-level overview of your e-commerce business.")

    chain_divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("Revenue", "$2.84M", "+18.4%")
    with col2: metric_card("Orders", "48,291", "+12.8%")
    with col3: metric_card("Customers", "18,642", "+9.7%")
    with col4: metric_card("Profit Margin", "24.8%", "+3.4%")

    st.write("")
    eyebrow("Performance")
    st.plotly_chart(
        line_fig([180000, 210000, 225000, 245000, 270000, 290000, 310000], name="Revenue"),
        use_container_width=True,
    )


# --------------------------------------------------
# CUSTOMER ANALYTICS
# --------------------------------------------------

elif page == "👥 Customer Analytics":

    eyebrow("People")
    st.title("👥 Customer Analytics")
    st.write("Understand your customers and their purchasing behavior.")

    chain_divider()

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("Total Customers", "18,642")
    with col2: metric_card("New Customers", "3,421", "+11.2%")
    with col3: metric_card("Retention", "72.4%", "+5.1%", accent="amber")

    st.write("")
    eyebrow("Customer Growth")
    st.plotly_chart(
        line_fig([11000, 12500, 13200, 14500, 15800, 17100, 18642], name="Customers"),
        use_container_width=True,
    )


# --------------------------------------------------
# SALES ANALYTICS
# --------------------------------------------------

elif page == "💰 Sales Analytics":

    eyebrow("Revenue")
    st.title("💰 Sales Analytics")
    st.write("Analyze revenue and sales performance.")

    chain_divider()

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("Revenue", "$2.84M", "+18.4%")
    with col2: metric_card("Average Order", "$58.82", "+4.8%")
    with col3: metric_card("Orders", "48,291", "+12.8%")

    st.write("")
    eyebrow("Revenue Trend")
    st.plotly_chart(
        bar_fig([180000, 220000, 250000, 270000, 290000, 315000, 350000], name="Revenue"),
        use_container_width=True,
    )


# --------------------------------------------------
# SUPPLY CHAIN
# --------------------------------------------------

elif page == "🚚 Supply Chain":

    eyebrow("Logistics")
    st.title("🚚 Supply Chain")
    st.write("Monitor deliveries, fulfillment and logistics.")

    chain_divider()

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("On-Time Delivery", "94.6%", "+4.2%")
    with col2: metric_card("Orders in Transit", "1,284")
    with col3: metric_card("Delayed Orders", "87", "-14.2%", accent="amber")

    st.write("")
    eyebrow("Delivery Performance")
    st.markdown(f"""
    <div class="progress-track"><div class="progress-fill" style="width:94.6%;"></div></div>
    <div style="font-family:'IBM Plex Mono',monospace;color:{MUTED};font-size:13px;margin-top:8px;">
        94.6% of orders are currently delivered on time.
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# REVIEW ANALYTICS
# --------------------------------------------------

elif page == "⭐ Review Analytics":

    eyebrow("Feedback")
    st.title("⭐ Review Analytics")
    st.write("Understand customer feedback and product ratings.")

    chain_divider()

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("Average Rating", "4.42 / 5")
    with col2: metric_card("Total Reviews", "32,841")
    with col3: metric_card("Positive Reviews", "87.4%", "+2.1%")

    st.write("")
    eyebrow("Rating Distribution (1★–5★)")
    st.plotly_chart(
        bar_fig([2, 4, 7, 18, 69], color=AMBER, name="Rating"),
        use_container_width=True,
    )


# --------------------------------------------------
# PRODUCT ANALYTICS
# --------------------------------------------------

elif page == "📦 Product Analytics":

    eyebrow("Catalog")
    st.title("📦 Product Analytics")
    st.write("Analyze products, categories and inventory performance.")

    chain_divider()

    col1, col2, col3 = st.columns(3)
    with col1: metric_card("Products", "4,821")
    with col2: metric_card("Top Category", "Electronics")
    with col3: metric_card("Best Seller", "Product A")

    st.write("")
    eyebrow("Category Performance")
    st.plotly_chart(
        multi_bar_fig({
            "Electronics": [120, 145, 180, 210, 250],
            "Home": [90, 110, 125, 140, 160],
            "Fashion": [80, 95, 115, 130, 150],
        }),
        use_container_width=True,
    )


# --------------------------------------------------
# AI BUSINESS ANALYST
# --------------------------------------------------

elif page == "🤖 AI Business Analyst":

    eyebrow("Ask ChainSight")
    st.title("🤖 AI Business Analyst")
    st.write("Ask questions about your e-commerce business.")

    chain_divider()

    question = st.text_input(
        "Ask a question",
        placeholder="Example: Which products generated the most revenue?",
        label_visibility="collapsed",
    )

    if st.button("Analyze"):
        if question:
            st.success(f"Question received: {question}")
            st.info("Your existing AI / SQL backend can be connected here to generate the actual business answer.")
        else:
            st.warning("Please enter a question first.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

chain_divider()

st.markdown(f"""
<div style="text-align:center;font-family:'IBM Plex Mono',monospace;color:{MUTED};font-size:12px;padding-bottom:10px;">
    ChainSight AI · E-Commerce Intelligence Platform
</div>
""", unsafe_allow_html=True)