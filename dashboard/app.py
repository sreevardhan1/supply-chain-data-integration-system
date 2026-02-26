"""
Enterprise Supply Chain Dashboard
----------------------------------
• Glassmorphism UI
• Gradient Theme
• USA State Map
• Single Screen Layout
• Optimized BigQuery Usage
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px
from google.cloud import bigquery


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Enterprise Supply Chain Dashboard",
    layout="wide",
    page_icon="📊"
)

st.markdown("""
<h1 style="
    text-align:center;
    align-content: center;
    font-size:46px;
    font-weight:800;
    margin-bottom:28px;
    letter-spacing:1px;
    -webkit-background-clip: text;
    background-clip: text;
    color: white;
    display: inline-block;
">
    📊 Enterprise Supply Chain Dashboard
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<style>
* {
    transition: all 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# GLASS + GRADIENT THEME
# =====================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.block-container {
    padding-top: 2rem;    
    padding-bottom: 0rem;
    padding-left : 2.5rem;
    padding-right : 2.5rem;
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 15px;
    padding: 10px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.12);
    border-radius: 15px;
    padding: 12px;
    border: 1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="metric-container"] {
    font-size:18px !important;
}
</style>
""", unsafe_allow_html=True)

# Sub -heading CSS
st.markdown("""
<style>
.section-title {
    font-size:18px;
    font-weight:600;
    margin-bottom:6px;
    color:#d0e6ff;
    letter-spacing:0.5px;
}

.section-divider {
    height:2px;
    width:120px;
    background: linear-gradient(90deg,#00f5ff,#00ff88);
    margin-bottom:12px;
    border-radius:4px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# BIGQUERY CLIENT
# =====================================================
@st.cache_resource
def get_client():
    return bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))

client = get_client()

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data(ttl=600)
def load_sales():
    query = """
    SELECT year,
           month,
           region,
           category,
           total_sales,
           total_profit,
           total_quantity
    FROM `supply-chain-dw.supply_chain_dw.vw_sales_mart`
    """
    return client.query(query).to_dataframe()

# =====================================================
# LOAD GEO SALES (FOR MAP)
# =====================================================
@st.cache_data(ttl=600)
def load_geo_sales():
    query = """
    SELECT year,
           month,
           country,
           region,
           state,
           city,
           total_sales,
           total_profit,
           total_quantity
    FROM `supply-chain-dw.supply_chain_dw.vw_geo_sales`
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=600)
def load_vendor():
    query = """
    SELECT vendor_name, total_sales, avg_lead_time
    FROM `supply-chain-dw.supply_chain_dw.vw_vendor_performance`
    """
    return client.query(query).to_dataframe()

@st.cache_data(ttl=600)
def load_lead_time():
    query = """
    SELECT year,
           region,
           category,
           avg_lead_time
    FROM `supply-chain-dw.supply_chain_dw.vw_lead_time_mart`
    """
    return client.query(query).to_dataframe()

df_sales = load_sales()
df_vendor = load_vendor()
df_geo = load_geo_sales()
df_lead = load_lead_time()

# =====================================================
# FILTER BAR
# =====================================================
f1, f2, f3, f4 = st.columns(4)

with f1:
    selected_year = st.selectbox("Year", sorted(df_sales.year.unique()))

with f2:
    metric_choice = st.selectbox("Metric", ["Sales", "Profit"])

with f3:
    selected_region = st.selectbox(
        "Region",
        ["All"] + sorted(df_sales.region.unique())
    )

with f4:
    selected_category = st.selectbox(
        "Category",
        ["All"] + sorted(df_sales.category.unique())
    )

metric_column = "total_sales" if metric_choice == "Sales" else "total_profit"

# =====================================================
# FILTER DATA
# =====================================================
# For - Monthly Sales Trend
df = df_sales[df_sales.year == selected_year]

if selected_region != "All":
    df = df[df.region == selected_region]

if selected_category != "All":
    df = df[df.category == selected_category]

# FOR : Geo filtering plot(MAP)

df_geo_filtered = df_geo[df_geo.year == selected_year]

if selected_region != "All":
    df_geo_filtered = df_geo_filtered[
        df_geo_filtered.region == selected_region
    ]

geo_metric = "total_sales" if metric_choice == "Sales" else "total_profit"

df_state = (
    df_geo_filtered
    .groupby("state")[geo_metric]
    .sum()
    .reset_index()
)

# For: Lead_time_Days gauge
df_lead_filtered = df_lead[df_lead.year == selected_year]

if selected_region != "All":
    df_lead_filtered = df_lead_filtered[
        df_lead_filtered.region == selected_region
    ]

if selected_category != "All":
    df_lead_filtered = df_lead_filtered[
        df_lead_filtered.category == selected_category
    ]

# =====================================================
# KPI SECTION
# =====================================================
total_sales = df.total_sales.sum()
total_profit = df.total_profit.sum()
total_quantity = df.total_quantity.sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Sales", f"${total_sales:,.0f}")
k2.metric("Total Profit", f"${total_profit:,.0f}")
k3.metric("Quantity", f"{int(total_quantity):,}")
k4.metric("Profit Margin", f"{profit_margin:.2f}%")

# st.divider()

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# =====================================================
# CHART 1: MONTHLY TREND (YoY Comparison)
# =====================================================

import plotly.graph_objects as go

# Current Year Data
df_current = df_sales[df_sales.year == selected_year]

if selected_region != "All":
    df_current = df_current[df_current.region == selected_region]

if selected_category != "All":
    df_current = df_current[df_current.category == selected_category]

df_current["date"] = pd.to_datetime(
    df_current["year"].astype(str) + "-" +
    df_current["month"].astype(str) + "-01"
)

df_current_monthly = (
    df_current.groupby("date")[metric_column]
    .sum()
    .reset_index()
)

# Previous Year Data
previous_year = selected_year - 1
df_previous = df_sales[df_sales.year == previous_year]

if selected_region != "All":
    df_previous = df_previous[df_previous.region == selected_region]

if selected_category != "All":
    df_previous = df_previous[df_previous.category == selected_category]

df_previous["date"] = pd.to_datetime(
    df_previous["year"].astype(str) + "-" +
    df_previous["month"].astype(str) + "-01"
)

df_previous_monthly = (
    df_previous.groupby("date")[metric_column]
    .sum()
    .reset_index()
)

# Align previous year months to current year for overlay
df_previous_monthly["date"] = df_previous_monthly["date"].apply(
    lambda x: x.replace(year=selected_year)
)

# Create Figure
fig_trend = go.Figure()

# Current Year Line
fig_trend.add_trace(go.Scatter(
    x=df_current_monthly["date"],
    y=df_current_monthly[metric_column],
    mode="lines+markers",
    name=f"{selected_year}",
    line=dict(shape="spline", width=3, color="#00f5ff"),
    fill="tozeroy",
    opacity=0.5,
    hovertemplate="<b>Date:</b> %{x|%b %Y}<br><b>Value:</b> %{y:$,.0f}"
))

# Previous Year Line
fig_trend.add_trace(go.Scatter(
    x=df_previous_monthly["date"],
    y=df_previous_monthly[metric_column],
    mode="lines+markers",
    name=f"{previous_year}",
    line=dict(shape="spline", width=2, dash="dash", color="#00ff88"),
    hovertemplate="<b>Date:</b> %{x|%b %Y}<br><b>Value:</b> %{y:$,.0f}"
))

fig_trend.update_layout(
    template="plotly_dark",
    height=220,
    margin=dict(l=5, r=5, t=30, b=5),
    hovermode="x unified",
    transition_duration=600,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

# =====================================================
# CHART 2: CATEGORY DISTRIBUTION 
# =====================================================

import plotly.graph_objects as go

# Aggregate Category Data
df_cat = (
    df.groupby("category")[metric_column]
    .sum()
    .reset_index()
)

total_value = df_cat[metric_column].sum()

fig_donut = go.Figure()

fig_donut.add_trace(go.Pie(
    labels=df_cat["category"],
    values=df_cat[metric_column],
    hole=0.6,
    pull=[0.03]*len(df_cat),
    textinfo="percent",
    textfont=dict(size=13),
    hovertemplate="<b>%{label}</b><br>Value: %{value:$,.0f}<br>Share: %{percent}",
))

# Add Center Metric
fig_donut.add_annotation(
    text=f"${total_value:,.0f}",
    x=0.5, y=0.5,
    font=dict(size=18, color="white"),
    showarrow=False
)

fig_donut.update_layout(
    template="plotly_dark",
    height=220,
    margin=dict(l=5, r=5, t=30, b=5),
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="left",
        x=1.02
    ),
    transition_duration=600
)

# =====================================================
# CHART 3: USA STATE MAP
# =====================================================
us_state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Illinois": "IL", "New York": "NY", "Texas": "TX"
    # Add all states here
}

df_state["state_code"] = df_state["state"].map(us_state_abbrev)

fig_map = px.choropleth(
    df_state,
    locations="state_code",
    locationmode="USA-states",
    color=geo_metric,
    scope="usa",
    template="plotly_dark"
)

fig_map.update_layout(
    height=230,
    margin=dict(l=5,r=5,t=30,b=5),
    geo = dict(
        bgcolor = "rgba(0,0,0,0)",
        showlakes = True,
        lakecolor = 'rgb(20,20,30)'
    ),
    transition_duration = 600
)
fig_map.update_traces(
    hovertemplate="<b>State:</b> %{location}<br><b>Value:</b> %{z:$,.0f}"
)


# =====================================================
# CHART 4: REGION
# =====================================================

df_region = (
    df.groupby("region")[metric_column]
    .sum()
    .reset_index()
    .sort_values(metric_column, ascending=False)
)

fig_region = px.bar(
    df_region,
    x="region",
    y=metric_column,
    text=metric_column,
    color=metric_column,
    color_continuous_scale="Blues"
)

fig_region.update_traces(
    texttemplate="%{text:$,.0f}",
    textposition="outside",
    marker_line_color="white",
    marker_line_width=1.5
)

fig_region.update_layout(
    template="plotly_dark",
    height=230,
    margin=dict(l=5, r=5, t=30, b=5),
    showlegend=False,
    yaxis_title=metric_choice,
    xaxis_title="Region",
    transition_duration=600
)

# =====================================================
# CHART 5: VENDOR SALES
# =====================================================
fig_vendor_sales = px.bar(
    df_vendor.sort_values("total_sales", ascending=True),
    x="total_sales",
    y="vendor_name",
    orientation="h",
    template="plotly_dark",
    color="total_sales",
    color_continuous_scale="blues"
)

fig_vendor_sales.update_layout(
    height=230,
    margin=dict(l=5,r=5,t=30,b=5),
    hovermode = "y unified",
    transition_duration = 600
)

fig_vendor_sales.update_traces(opacity=0.9)


# =====================================================
# CHART 6: VENDOR LEAD TIME
# =====================================================
import plotly.graph_objects as go

avg_lead = df_lead_filtered["avg_lead_time"].mean()

fig_vendor_lead = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_lead,
    number={'suffix': " days"},
    # title={'text': "Avg Vendor Lead Time"},
    gauge={
        'axis': {'range': [0, 10]},
        'bar': {'color': "#00f5ff"},
        'steps': [
            {'range': [0, 4], 'color': "#00ff88"},
            {'range': [4, 7], 'color': "#ffcc00"},
            {'range': [7, 10], 'color': "#ff4d4d"}
        ],
        'threshold': {
            'line': {'color': "white", 'width': 4},
            'thickness': 0.75,
            'value': 5
        }
    }
))

fig_vendor_lead.update_layout(
    template="plotly_dark",
    height=220,
    margin=dict(l=5,r=5,t=30,b=5),
    # transition_duration = 800
)

# =====================================================
# ENTERPRISE 3x2 GRID (NO SCROLL)
# =====================================================
r1c1, r1c2, r1c3 = st.columns(3)
r2c1, r2c2, r2c3 = st.columns(3)

with r1c1:
    st.markdown('<div class="section-title">📈 Monthly Sales Trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with r1c2:
    st.markdown('<div class="section-title">🗂 Category Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True)

with r1c3:
    st.markdown('<div class="section-title">🗺 State-wise Sales</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True)

with r2c1:
    st.markdown('<div class="section-title">🌍 Region Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_region, use_container_width=True)

with r2c2:
    st.markdown('<div class="section-title">🏢 Vendor Sales Ranking</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_vendor_sales, use_container_width=True)

with r2c3:
    st.markdown('<div class="section-title">⏱ Average Vendor Lead Time</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_vendor_lead, use_container_width=True)