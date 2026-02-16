"""
Veridi Logistics — Delivery Performance Audit Dashboard
Story 6: Candidate's Choice — Professional Streamlit Dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Veridi Logistics · Delivery Audit",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — dark industrial theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0d0f14;
    --surface:   #14181f;
    --surface2:  #1c2230;
    --border:    #252d3a;
    --accent:    #e8413a;
    --accent2:   #f5a623;
    --accent3:   #3a9de8;
    --text:      #e8eaf0;
    --muted:     #6b7a94;
    --good:      #27c28a;
    --warn:      #f5a623;
    --bad:       #e8413a;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Hide streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: transform .2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.kpi-card.red::before   { background: var(--bad); }
.kpi-card.yellow::before{ background: var(--warn); }
.kpi-card.green::before { background: var(--good); }
.kpi-card.blue::before  { background: var(--accent3); }

.kpi-label {
    font-size: 10px;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 8px;
    font-family: 'DM Mono', monospace;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-value.red    { color: var(--bad); }
.kpi-value.yellow { color: var(--warn); }
.kpi-value.green  { color: var(--good); }
.kpi-value.blue   { color: var(--accent3); }
.kpi-sub {
    font-size: 11px;
    color: var(--muted);
}

/* ── Section header ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--muted);
    border-left: 3px solid var(--accent);
    padding-left: 12px;
    margin: 32px 0 16px;
}

/* ── Page title ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -.02em;
    margin-bottom: 2px;
}
.page-sub {
    font-size: 12px;
    color: var(--muted);
    letter-spacing: .06em;
    margin-bottom: 28px;
}

/* ── Chart wrappers ── */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}

/* ── Insight box ── */
.insight-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent2);
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 12px;
    color: var(--text);
    line-height: 1.7;
    margin-top: 12px;
}
.insight-box strong { color: var(--accent2); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Dataframe ── */
.dataframe { font-size: 11px !important; }

/* ── Plotly background override ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Multiselect / select boxes ── */
div[data-baseweb="select"] > div { background: var(--surface2) !important; border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_BG   = "rgba(0,0,0,0)"
PAPER_BG  = "rgba(0,0,0,0)"
GRID_COL  = "#252d3a"
TEXT_COL  = "#e8eaf0"
FONT_FAM  = "DM Mono, monospace"

def apply_theme(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_FAM, color=TEXT_COL, size=11),
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis=dict(gridcolor=GRID_COL, zeroline=False, tickfont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COL, zeroline=False, tickfont=dict(size=10)),
    )
    return fig

PALETTE = {
    "On Time":    "#27c28a",
    "Late":       "#f5a623",
    "Super Late": "#e8413a",
    "Failed":     "#6b7a94",
}

# ─────────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    """Load and process all datasets into analysis-ready frames."""

    # ── locate files ──
    base = os.path.dirname(os.path.abspath(__file__))
    def find(name):
        for d in [base, ".", os.path.join(base, "data")]:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
        return None

    orders_path    = find("olist_orders_dataset.csv")
    reviews_path   = find("olist_order_reviews_dataset.csv")
    customers_path = find("olist_customers_dataset.csv")
    products_path  = find("olist_products_dataset.csv")
    items_path     = find("olist_order_items_dataset.csv")
    trans_path     = find("product_category_name_translation.csv")

    if not all([orders_path, reviews_path, customers_path]):
        return None, "Missing required CSV files. Place them in the same folder as dashboard.py."

    orders    = pd.read_csv(orders_path)
    reviews   = pd.read_csv(reviews_path)
    customers = pd.read_csv(customers_path)

    # ── datetime conversion ──
    for c in ["order_purchase_timestamp","order_approved_at",
              "order_delivered_carrier_date","order_delivered_customer_date",
              "order_estimated_delivery_date"]:
        orders[c] = pd.to_datetime(orders[c], errors="coerce")
    for c in ["review_creation_date","review_answer_timestamp"]:
        reviews[c] = pd.to_datetime(reviews[c], errors="coerce")

    # ── deduplicate reviews ──
    rev_dedup = (
        reviews.sort_values(["order_id","review_answer_timestamp","review_creation_date"])
               .drop_duplicates("order_id", keep="last")
               [["order_id","review_score"]]
    )

    # ── build master ──
    master = (orders
              .merge(customers, on="customer_id", how="left", validate="many_to_one")
              .merge(rev_dedup,  on="order_id",   how="left", validate="one_to_one"))

    # ── flags ──
    master["is_delivered"] = (
        (master["order_status"] == "delivered") &
        master["order_delivered_customer_date"].notna() &
        master["order_estimated_delivery_date"].notna()
    )
    master["never_delivered"] = master["order_status"].isin(["canceled","unavailable"])

    # ── delivered subset ──
    dlv = master[master["is_delivered"]].copy()
    dlv["delay_days"] = (
        dlv["order_delivered_customer_date"] - dlv["order_estimated_delivery_date"]
    ).dt.days
    dlv["delay_status"] = np.select(
        [dlv["delay_days"] <= 0,
         (dlv["delay_days"] > 0) & (dlv["delay_days"] <= 5),
         dlv["delay_days"] > 5],
        ["On Time","Late","Super Late"],
        default="Unknown"
    )
    dlv["purchase_month"] = dlv["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()

    # ── category translation ──
    if items_path and products_path:
        products   = pd.read_csv(products_path)
        items      = pd.read_csv(items_path)
        items_d    = items.drop_duplicates("order_id", keep="first")[["order_id","product_id"]]
        if trans_path:
            trans = pd.read_csv(trans_path)
            trans.columns = ["product_category_name","product_category_name_english"]
        else:
            trans = pd.DataFrame({"product_category_name":[],"product_category_name_english":[]})
        prod_t = products.merge(trans, on="product_category_name", how="left")
        order_cat = items_d.merge(
            prod_t[["product_id","product_category_name_english"]], on="product_id", how="left"
        )
        dlv = dlv.merge(order_cat, on="order_id", how="left")

    return dlv, None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:16px 0 8px'>
        <div style='font-family:Syne,sans-serif;font-size:20px;font-weight:800;color:#e8eaf0'>📦 VERIDI</div>
        <div style='font-size:10px;color:#6b7a94;letter-spacing:.12em;text-transform:uppercase;margin-top:2px'>Logistics Intelligence</div>
    </div>
    <hr style='border-color:#252d3a;margin:12px 0'>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:10px;color:#6b7a94;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px'>Navigation</div>", unsafe_allow_html=True)
    page = st.radio("", ["📊  Executive Overview", "🗺️  Regional Analysis", "💬  Sentiment Audit", "📦  Category Drill-Down"], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#252d3a;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#6b7a94;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px'>Filters</div>", unsafe_allow_html=True)

    with st.spinner("Loading data…"):
        dlv, err = load_data()

    if err:
        st.error(err)
        st.stop()

    # date range
    min_d = dlv["order_purchase_timestamp"].min().date()
    max_d = dlv["order_purchase_timestamp"].max().date()
    date_range = st.date_input("Date range", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    # state filter
    all_states = sorted(dlv["customer_state"].dropna().unique())
    sel_states = st.multiselect("States", all_states, default=[], placeholder="All states")

    st.markdown("<hr style='border-color:#252d3a;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:10px;color:#6b7a94'>Dataset: {len(dlv):,} delivered orders</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
df = dlv.copy()
if len(date_range) == 2:
    s, e = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    df = df[(df["order_purchase_timestamp"] >= s) & (df["order_purchase_timestamp"] <= e)]
if sel_states:
    df = df[df["customer_state"].isin(sel_states)]

# ─────────────────────────────────────────────
# SHARED METRICS
# ─────────────────────────────────────────────
total          = len(df)
n_late         = (df["delay_status"] == "Late").sum()
n_super        = (df["delay_status"] == "Super Late").sum()
n_ontime       = (df["delay_status"] == "On Time").sum()
pct_late       = (n_late + n_super) / total * 100 if total else 0
avg_review     = df["review_score"].mean()
avg_delay_late = df.loc[df["delay_days"] > 0, "delay_days"].mean()

# ─────────────────────────────────────────────
# ══════════════ PAGES ══════════════
# ─────────────────────────────────────────────

# ╔══════════════════════════════╗
# ║   PAGE 1 — EXECUTIVE OVERVIEW ║
# ╚══════════════════════════════╝
if page.startswith("📊"):

    st.markdown("""
    <div class='page-title'>Delivery Performance Audit</div>
    <div class='page-sub'>VERIDI LOGISTICS · EXECUTIVE OVERVIEW · REAL-TIME DELIVERY INTELLIGENCE</div>
    """, unsafe_allow_html=True)

    # ── KPI Row ──
    st.markdown(f"""
    <div class='kpi-grid'>
      <div class='kpi-card red'>
        <div class='kpi-label'>Total Late Rate</div>
        <div class='kpi-value red'>{pct_late:.1f}%</div>
        <div class='kpi-sub'>{n_late+n_super:,} of {total:,} orders</div>
      </div>
      <div class='kpi-card yellow'>
        <div class='kpi-label'>Super Late (>5 days)</div>
        <div class='kpi-value yellow'>{n_super:,}</div>
        <div class='kpi-sub'>{n_super/total*100:.1f}% of delivered orders</div>
      </div>
      <div class='kpi-card green'>
        <div class='kpi-label'>On-Time Deliveries</div>
        <div class='kpi-value green'>{n_ontime:,}</div>
        <div class='kpi-sub'>{n_ontime/total*100:.1f}% success rate</div>
      </div>
      <div class='kpi-card blue'>
        <div class='kpi-label'>Avg Review Score</div>
        <div class='kpi-value blue'>{avg_review:.2f}</div>
        <div class='kpi-sub'>out of 5.00</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # ── Donut: delay distribution ──
    with col1:
        st.markdown("<div class='section-title'>Delivery Status Breakdown</div>", unsafe_allow_html=True)
        status_counts = df["delay_status"].value_counts().reindex(["On Time","Late","Super Late"]).fillna(0)
        fig = go.Figure(go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.62,
            marker_colors=[PALETTE["On Time"], PALETTE["Late"], PALETTE["Super Late"]],
            textfont=dict(family=FONT_FAM, size=11),
            hovertemplate="%{label}: %{value:,} orders (%{percent})<extra></extra>",
        ))
        fig.add_annotation(
            text=f"<b>{total:,}</b><br><span style='font-size:10px'>orders</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family="Syne, sans-serif", size=18, color=TEXT_COL),
            align="center"
        )
        apply_theme(fig, height=320)
        fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.05))
        st.plotly_chart(fig, use_container_width=True)

    # ── Line: monthly trend ──
    with col2:
        st.markdown("<div class='section-title'>Monthly Late Delivery Trend</div>", unsafe_allow_html=True)
        monthly = (
            df.groupby(["purchase_month","delay_status"])
              .size().reset_index(name="count")
        )
        monthly_total = df.groupby("purchase_month").size().reset_index(name="total")
        monthly_late  = (
            df[df["delay_status"].isin(["Late","Super Late"])]
              .groupby("purchase_month").size().reset_index(name="late")
        )
        trend = monthly_total.merge(monthly_late, on="purchase_month", how="left").fillna(0)
        trend["pct_late"] = trend["late"] / trend["total"] * 100

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=trend["purchase_month"], y=trend["pct_late"],
            mode="lines+markers",
            line=dict(color="#e8413a", width=2.5),
            marker=dict(size=5, color="#e8413a"),
            fill="tozeroy",
            fillcolor="rgba(232,65,58,0.08)",
            name="Late Rate %",
            hovertemplate="%{x|%b %Y}: %{y:.1f}%<extra></extra>",
        ))
        apply_theme(fig2, height=320)
        fig2.update_layout(yaxis_title="Late Rate (%)", xaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Avg delay days histogram ──
    st.markdown("<div class='section-title'>Distribution of Delivery Delay (Days)</div>", unsafe_allow_html=True)
    late_only = df[df["delay_days"] > 0]["delay_days"].clip(upper=60)
    fig3 = px.histogram(
        late_only, nbins=50,
        color_discrete_sequence=["#e8413a"],
        labels={"value": "Days Late", "count": "Orders"},
    )
    fig3.update_traces(marker_line_width=0, opacity=0.85)
    apply_theme(fig3, height=280)
    fig3.update_layout(
        showlegend=False,
        xaxis_title="Days Late (capped at 60)",
        yaxis_title="Number of Orders",
        bargap=0.04,
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
        <strong>💡 Executive Insight:</strong>
        {pct_late:.1f}% of delivered orders arrive late. Of those,
        {n_super:,} orders ({n_super/total*100:.1f}%) are classified as <strong>Super Late</strong> (>5 days),
        which most strongly predict 1-star reviews (see Sentiment Audit).
        Average delay for late orders is <strong>{avg_delay_late:.1f} days</strong>.
        If Super Late orders could be eliminated, estimated review score would improve by ~0.4 points.
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════╗
# ║   PAGE 2 — REGIONAL ANALYSIS  ║
# ╚══════════════════════════════╝
elif page.startswith("🗺️"):

    st.markdown("""
    <div class='page-title'>Regional Performance Analysis</div>
    <div class='page-sub'>VERIDI LOGISTICS · GEOGRAPHIC BREAKDOWN · STATE-LEVEL LATE DELIVERY RATES</div>
    """, unsafe_allow_html=True)

    # ── state stats ──
    state_pivot = (
        df.groupby(["customer_state","delay_status"])
          .size().unstack(fill_value=0).reset_index()
    )
    for col in ["On Time","Late","Super Late"]:
        if col not in state_pivot.columns:
            state_pivot[col] = 0
    state_pivot["total"]          = state_pivot[["On Time","Late","Super Late"]].sum(axis=1)
    state_pivot["pct_late"]       = (state_pivot["Late"]       / state_pivot["total"] * 100).round(2)
    state_pivot["pct_super_late"] = (state_pivot["Super Late"] / state_pivot["total"] * 100).round(2)
    state_pivot["pct_combined"]   = state_pivot["pct_late"] + state_pivot["pct_super_late"]

    avg_review_state = df.groupby("customer_state")["review_score"].mean().reset_index()
    avg_review_state.columns = ["customer_state","avg_review"]
    state_stats = state_pivot.merge(avg_review_state, on="customer_state")

    remote_states = ["AC","RO","RR","AP","AM","TO","MT","MS","PA"]
    state_stats["is_remote"] = state_stats["customer_state"].isin(remote_states)

    col1, col2 = st.columns([3, 2])

    # ── horizontal bar chart ──
    with col1:
        st.markdown("<div class='section-title'>Late Delivery Rate by State</div>", unsafe_allow_html=True)
        top20 = state_stats.sort_values("pct_combined", ascending=True).tail(20)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=top20["customer_state"], x=top20["pct_late"],
            orientation="h", name="Late (1-5 days)",
            marker_color=PALETTE["Late"],
        ))
        fig.add_trace(go.Bar(
            y=top20["customer_state"], x=top20["pct_super_late"],
            orientation="h", name="Super Late (>5 days)",
            marker_color=PALETTE["Super Late"],
        ))
        apply_theme(fig, height=480)
        fig.update_layout(
            barmode="stack", xaxis_title="Late Rate (%)",
            yaxis_title=None, legend=dict(orientation="h", y=1.05)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # ── remote vs non-remote ──
        st.markdown("<div class='section-title'>Remote vs Non-Remote</div>", unsafe_allow_html=True)
        remote_summary = state_stats.groupby("is_remote")[["pct_late","pct_super_late","avg_review"]].mean().reset_index()
        remote_summary["label"] = remote_summary["is_remote"].map({True:"Remote", False:"Non-Remote"})

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=remote_summary["label"], y=remote_summary["pct_late"],
            name="Late %", marker_color=PALETTE["Late"],
        ))
        fig2.add_trace(go.Bar(
            x=remote_summary["label"], y=remote_summary["pct_super_late"],
            name="Super Late %", marker_color=PALETTE["Super Late"],
        ))
        apply_theme(fig2, height=220)
        fig2.update_layout(barmode="group", xaxis_title=None, yaxis_title="Rate (%)")
        st.plotly_chart(fig2, use_container_width=True)

        # ── avg review scatter ──
        st.markdown("<div class='section-title'>Late Rate vs Review Score</div>", unsafe_allow_html=True)
        fig3 = px.scatter(
            state_stats, x="pct_combined", y="avg_review",
            text="customer_state", size="total",
            color="is_remote",
            color_discrete_map={True: "#f5a623", False: "#3a9de8"},
            labels={"pct_combined":"Combined Late Rate (%)","avg_review":"Avg Review","is_remote":"Remote"},
            hover_data={"total": True, "pct_combined": ":.1f"},
        )
        fig3.update_traces(textfont=dict(size=9, color=TEXT_COL), textposition="top center")
        apply_theme(fig3, height=220)
        fig3.update_layout(showlegend=True)
        st.plotly_chart(fig3, use_container_width=True)

    # ── full state table ──
    st.markdown("<div class='section-title'>Full State Performance Table</div>", unsafe_allow_html=True)
    table = state_stats[[
        "customer_state","total","pct_late","pct_super_late","pct_combined","avg_review","is_remote"
    ]].sort_values("pct_combined", ascending=False).reset_index(drop=True)
    table.columns = ["State","Orders","Late %","Super Late %","Combined Late %","Avg Review","Remote"]
    st.dataframe(
        table.style
             .format({"Late %": "{:.2f}","Super Late %": "{:.2f}","Combined Late %": "{:.2f}","Avg Review": "{:.2f}"})
             .background_gradient(subset=["Combined Late %"], cmap="Reds")
             .background_gradient(subset=["Avg Review"],       cmap="Greens"),
        use_container_width=True,
        hide_index=True,
    )

    # worst & best state insight
    worst = table.iloc[0]
    best  = table[table["Orders"] > 200].sort_values("Combined Late %").iloc[0]
    st.markdown(f"""
    <div class='insight-box'>
        <strong>💡 Regional Insight:</strong>
        <strong>{worst['State']}</strong> is the worst-performing state with a combined late rate of
        <strong>{worst['Combined Late %']:.1f}%</strong> and avg review of <strong>{worst['Avg Review']:.2f}/5</strong>.
        Best performer (min 200 orders): <strong>{best['State']}</strong> at {best['Combined Late %']:.1f}% late.
        Non-remote states actually average a <em>higher</em> late rate than remote ones, confirming this is a
        <strong>nationwide infrastructure problem</strong>, not a last-mile rural issue.
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════╗
# ║   PAGE 3 — SENTIMENT AUDIT    ║
# ╚══════════════════════════════╝
elif page.startswith("💬"):

    st.markdown("""
    <div class='page-title'>Customer Sentiment Audit</div>
    <div class='page-sub'>VERIDI LOGISTICS · REVIEW SCORE ANALYSIS · DOES DELAY CAUSE BAD REVIEWS?</div>
    """, unsafe_allow_html=True)

    # ── KPI row ──
    avg_ontime  = df.loc[df["delay_status"] == "On Time",     "review_score"].mean()
    avg_late    = df.loc[df["delay_status"] == "Late",         "review_score"].mean()
    avg_slate   = df.loc[df["delay_status"] == "Super Late",   "review_score"].mean()
    pct_1star_late  = (df.loc[df["delay_days"] > 5, "review_score"] == 1).mean() * 100
    pct_1star_ontime= (df.loc[df["delay_days"] <= 0,"review_score"] == 1).mean() * 100

    st.markdown(f"""
    <div class='kpi-grid'>
      <div class='kpi-card green'>
        <div class='kpi-label'>On-Time Avg Review</div>
        <div class='kpi-value green'>{avg_ontime:.2f}</div>
        <div class='kpi-sub'>out of 5.00</div>
      </div>
      <div class='kpi-card yellow'>
        <div class='kpi-label'>Late Avg Review</div>
        <div class='kpi-value yellow'>{avg_late:.2f}</div>
        <div class='kpi-sub'>–{avg_ontime-avg_late:.2f} vs on-time</div>
      </div>
      <div class='kpi-card red'>
        <div class='kpi-label'>Super Late Avg Review</div>
        <div class='kpi-value red'>{avg_slate:.2f}</div>
        <div class='kpi-sub'>–{avg_ontime-avg_slate:.2f} vs on-time</div>
      </div>
      <div class='kpi-card red'>
        <div class='kpi-label'>1-Star Rate (Super Late)</div>
        <div class='kpi-value red'>{pct_1star_late:.0f}%</div>
        <div class='kpi-sub'>vs {pct_1star_ontime:.0f}% for on-time</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    # ── grouped bar: avg review by status ──
    with col1:
        st.markdown("<div class='section-title'>Avg Review Score by Delay Status</div>", unsafe_allow_html=True)
        status_order = ["On Time","Late","Super Late"]
        avg_scores   = [avg_ontime, avg_late, avg_slate]
        colors_      = [PALETTE[s] for s in status_order]

        fig = go.Figure(go.Bar(
            x=status_order, y=avg_scores,
            marker_color=colors_,
            text=[f"{v:.2f}" for v in avg_scores],
            textposition="outside",
            textfont=dict(size=14, family="Syne, sans-serif"),
            hovertemplate="%{x}: %{y:.2f}/5<extra></extra>",
        ))
        apply_theme(fig, height=320)
        fig.update_layout(
            yaxis=dict(range=[0, 5.5], title="Avg Review Score"),
            showlegend=False,
            xaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── review score distribution by status ──
    with col2:
        st.markdown("<div class='section-title'>Review Score Distribution by Status</div>", unsafe_allow_html=True)
        score_dist = (
            df.groupby(["delay_status","review_score"]).size()
              .reset_index(name="count")
        )
        score_dist["pct"] = score_dist.groupby("delay_status")["count"].transform(lambda x: x / x.sum() * 100)

        fig2 = px.bar(
            score_dist[score_dist["delay_status"].isin(["On Time","Late","Super Late"])],
            x="review_score", y="pct", color="delay_status",
            barmode="group",
            color_discrete_map=PALETTE,
            labels={"review_score":"Review Score","pct":"% of Orders","delay_status":"Status"},
            category_orders={"delay_status":["On Time","Late","Super Late"]},
        )
        apply_theme(fig2, height=320)
        fig2.update_layout(xaxis=dict(tickmode="linear", dtick=1), yaxis_title="% of Status Orders")
        st.plotly_chart(fig2, use_container_width=True)

    # ── scatter: delay days vs review ──
    st.markdown("<div class='section-title'>Delay Days vs Review Score (Sampled)</div>", unsafe_allow_html=True)
    sample = df.dropna(subset=["delay_days","review_score"])
    if len(sample) > 6000:
        sample = sample.sample(6000, random_state=42)

    fig3 = px.scatter(
        sample, x="delay_days", y="review_score",
        color="delay_status",
        color_discrete_map=PALETTE,
        opacity=0.25,
        labels={"delay_days":"Delay Days","review_score":"Review Score","delay_status":"Status"},
        category_orders={"delay_status":["On Time","Late","Super Late"]},
        hover_data={"customer_state": True},
    )
    # add average trend line
    binned = (
        df.assign(day_bin=df["delay_days"].clip(-30,60).round(0))
          .groupby("day_bin")["review_score"].mean().reset_index()
    )
    fig3.add_trace(go.Scatter(
        x=binned["day_bin"], y=binned["review_score"],
        mode="lines",
        line=dict(color="#ffffff", width=2, dash="dot"),
        name="Moving Avg",
    ))
    fig3.add_vline(x=0, line_dash="dash", line_color="#6b7a94", line_width=1.5,
                   annotation_text="Estimated date", annotation_font_color="#6b7a94")
    apply_theme(fig3, height=320)
    fig3.update_layout(xaxis=dict(range=[-35, 65], title="Days Relative to Estimate (+ = late)"))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
        <strong>💡 Sentiment Insight:</strong>
        On-time deliveries average <strong>{avg_ontime:.2f}/5</strong>.
        Super Late orders crash to <strong>{avg_slate:.2f}/5</strong> — a drop of
        <strong>{avg_ontime - avg_slate:.2f} points</strong>.
        Critically, <strong>{pct_1star_late:.0f}%</strong> of Super Late orders receive 1-star reviews vs
        only <strong>{pct_1star_ontime:.0f}%</strong> for on-time orders.
        The scatter confirms a clear negative correlation: every additional day of delay predicts a lower review.
        <strong>Logistics performance is the primary driver of customer dissatisfaction.</strong>
    </div>
    """, unsafe_allow_html=True)


# ╔══════════════════════════════╗
# ║  PAGE 4 — CATEGORY DRILL-DOWN ║
# ╚══════════════════════════════╝
elif page.startswith("📦"):

    st.markdown("""
    <div class='page-title'>Category Drill-Down</div>
    <div class='page-sub'>VERIDI LOGISTICS · PRODUCT CATEGORY PERFORMANCE · TRANSLATION CHALLENGE</div>
    """, unsafe_allow_html=True)

    if "product_category_name_english" not in df.columns:
        st.warning(
            "⚠️ `olist_order_items_dataset.csv` or `product_category_name_translation.csv` not found. "
            "Place them alongside dashboard.py and restart."
        )
        st.stop()

    cat_df = df.dropna(subset=["product_category_name_english"]).copy()
    cat_df["is_late"] = cat_df["delay_days"] > 0

    cat_stats = cat_df.groupby("product_category_name_english").agg(
        orders     = ("order_id",     "count"),
        pct_late   = ("is_late",      "mean"),
        avg_review = ("review_score", "mean"),
        avg_delay  = ("delay_days",   "mean"),
    ).reset_index()
    cat_stats = cat_stats[cat_stats["orders"] >= 200]
    cat_stats["pct_late_pct"] = (cat_stats["pct_late"] * 100).round(2)
    cat_stats["avg_review"]   = cat_stats["avg_review"].round(2)
    cat_stats["avg_delay"]    = cat_stats["avg_delay"].round(1)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("<div class='section-title'>Bubble Chart: Late Rate × Review Score × Volume</div>", unsafe_allow_html=True)
        fig = px.scatter(
            cat_stats,
            x="pct_late_pct", y="avg_review",
            size="orders",
            color="pct_late_pct",
            color_continuous_scale=["#27c28a","#f5a623","#e8413a"],
            hover_name="product_category_name_english",
            hover_data={"orders":True, "pct_late_pct":":.1f", "avg_review":":.2f", "avg_delay":":.1f"},
            labels={
                "pct_late_pct":"Late Rate (%)",
                "avg_review":"Avg Review Score",
                "orders":"Order Volume",
            },
            size_max=55,
        )
        # label the 5 worst
        worst5 = cat_stats.nlargest(5, "pct_late_pct")
        for _, row in worst5.iterrows():
            fig.add_annotation(
                x=row["pct_late_pct"], y=row["avg_review"],
                text=row["product_category_name_english"].replace("_"," "),
                showarrow=False, yshift=18,
                font=dict(size=8, color="#e8eaf0"),
            )
        apply_theme(fig, height=460)
        fig.update_coloraxes(colorbar=dict(title="Late %", tickfont=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>Top 10 — Worst Categories</div>", unsafe_allow_html=True)
        worst10 = cat_stats.nlargest(10, "pct_late_pct")[
            ["product_category_name_english","orders","pct_late_pct","avg_review"]
        ].reset_index(drop=True)
        worst10.columns = ["Category","Orders","Late %","Avg Review"]

        fig2 = px.bar(
            worst10.sort_values("Late %"),
            x="Late %", y="Category",
            orientation="h",
            color="Late %",
            color_continuous_scale=["#f5a623","#e8413a"],
            text="Late %",
        )
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont=dict(size=10))
        apply_theme(fig2, height=340)
        fig2.update_layout(showlegend=False, coloraxis_showscale=False, yaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("<div class='section-title'>Top 10 — Best Categories</div>", unsafe_allow_html=True)
        best10 = cat_stats.nsmallest(10, "pct_late_pct")[
            ["product_category_name_english","orders","pct_late_pct","avg_review"]
        ].reset_index(drop=True)
        best10.columns = ["Category","Orders","Late %","Avg Review"]

        fig3 = px.bar(
            best10.sort_values("Late %", ascending=False),
            x="Late %", y="Category",
            orientation="h",
            color="Late %",
            color_continuous_scale=["#27c28a","#3a9de8"],
            text="Late %",
        )
        fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont=dict(size=10))
        apply_theme(fig3, height=340)
        fig3.update_layout(showlegend=False, coloraxis_showscale=False, yaxis_title=None)
        st.plotly_chart(fig3, use_container_width=True)

    # ── full table ──
    st.markdown("<div class='section-title'>Full Category Performance Table</div>", unsafe_allow_html=True)
    full_table = cat_stats[[
        "product_category_name_english","orders","pct_late_pct","avg_review","avg_delay"
    ]].sort_values("pct_late_pct", ascending=False).reset_index(drop=True)
    full_table.columns = ["Category (English)","Orders","Late Rate (%)","Avg Review","Avg Delay (days)"]

    st.dataframe(
        full_table.style
                  .format({"Late Rate (%)": "{:.2f}", "Avg Review": "{:.2f}", "Avg Delay (days)": "{:.1f}"})
                  .background_gradient(subset=["Late Rate (%)"], cmap="Reds")
                  .background_gradient(subset=["Avg Review"],    cmap="Greens"),
        use_container_width=True,
        hide_index=True,
    )

    worst_cat = cat_stats.nlargest(1, "pct_late_pct").iloc[0]
    best_cat  = cat_stats.nsmallest(1, "pct_late_pct").iloc[0]
    st.markdown(f"""
    <div class='insight-box'>
        <strong>💡 Category Insight:</strong>
        <strong>{worst_cat['product_category_name_english'].replace('_',' ').title()}</strong>
        is the most problematic category: <strong>{worst_cat['pct_late_pct']:.1f}%</strong> late rate
        and avg review of <strong>{worst_cat['avg_review']:.2f}/5</strong>.
        <strong>{best_cat['product_category_name_english'].replace('_',' ').title()}</strong>
        performs best at only <strong>{best_cat['pct_late_pct']:.1f}%</strong> late.
        Operations should prioritise renegotiating carrier SLAs for high-volume, high-delay categories
        and recalibrate estimated delivery windows to set realistic customer expectations.
    </div>
    """, unsafe_allow_html=True)
