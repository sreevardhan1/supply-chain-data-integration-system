import streamlit as st
from google.cloud import bigquery
import pandas as pd
import os
# Enhancing UI Theme using plotly
import plotly.express as px

# ----------------------------------------
# Page Config
# ----------------------------------------
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Supply Chain Data Integration Dashboard")
st.markdown("Real-time analytics powered by BigQuery")

st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight:600;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# BigQuery Client
# ----------------------------------------
client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))

# ----------------------------------------
# Data Loading Functions
# ----------------------------------------
@st.cache_data
def load_sales_summary():
    query = """
    SELECT *
    FROM `supply-chain-dw.supply_chain_dw.vw_sales_summary`
    ORDER BY year, month
    """
    return client.query(query).to_dataframe()

@st.cache_data
def load_category_data():
    query = """
    SELECT *
    FROM `supply-chain-dw.supply_chain_dw.vw_product_performance`
    """
    return client.query(query).to_dataframe()

@st.cache_data
def load_region_data():
    query = """
    SELECT *
    FROM `supply-chain-dw.supply_chain_dw.vw_region_sales`
    """
    return client.query(query).to_dataframe()

@st.cache_data
def load_lead_time():
    query = """
    SELECT *
    FROM `supply-chain-dw.supply_chain_dw.vw_lead_time_analysis`
    """
    return client.query(query).to_dataframe()

@st.cache_data
def load_top_products(selected_year):

    query = """
    SELECT
        p.product_name,
        SUM(f.sales) AS total_sales,
        SUM(f.profit) AS total_profit
    FROM `supply-chain-dw.supply_chain_dw.fact_orders` f
    JOIN `supply-chain-dw.supply_chain_dw.dim_product` p
        ON f.product_key = p.product_key
    JOIN `supply-chain-dw.supply_chain_dw.dim_date` d
        ON f.date_key = d.date_key
    WHERE d.year = @year
    GROUP BY p.product_name
    ORDER BY total_sales DESC
    LIMIT 5
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("year", "INT64", selected_year)
        ]
    )

    return client.query(query, job_config=job_config).to_dataframe()


@st.cache_data
def load_state_sales(selected_year):
    query = f"""
    SELECT *
    FROM `supply-chain-dw.supply_chain_dw.vw_state_sales`
    WHERE year = {selected_year}
    """
    return client.query(query).to_dataframe()


# ----------------------------------------
# Load Data
# ----------------------------------------
with st.spinner("Loading Data..."):
    df_sales = load_sales_summary()
    df_category = load_category_data()
    df_region = load_region_data()
    df_lead = load_lead_time()


# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filters")

years = sorted(df_sales["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)
selected_year = int(selected_year)      # json to python int

df_filtered = df_sales[df_sales["year"] == selected_year]

# Top-Products of selected year
df_top_products = load_top_products(selected_year)


df_state = load_state_sales(selected_year)

# ----------------------------------------
# KPI SECTION
# ----------------------------------------

# KPI values
total_sales = df_filtered["total_sales"].sum()
total_profit = df_filtered["total_profit"].sum()
total_quantity = df_filtered["total_quantity"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

# -----------------------------
# Year-over-Year Growth
# -----------------------------
previous_year = selected_year - 1

df_prev = df_sales[df_sales["year"] == previous_year]

current_sales = df_filtered["total_sales"].sum()
previous_sales = df_prev["total_sales"].sum()

if previous_sales > 0:
    yoy_growth = ((current_sales - previous_sales) / previous_sales) * 100
else:
    yoy_growth = 0


# ----------------------
# Summary Card
# ----------------------
st.success(
    f"In {selected_year},\n"
    f"total sales reached ${total_sales:,.0f}\n"
    f"with a profit margin of {profit_margin:.2f}%. \n"
    f"Year-over-year growth stands at {yoy_growth:.2f}%."
)

# -------------------
# KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("📦 Total Quantity", f"{int(total_quantity):,}")
col4.metric("📊 Profit Margin", f"{profit_margin:.2f}%")
col5.metric( "📅 YoY Growth", f"{yoy_growth:.2f}%", delta=f"{yoy_growth:.2f}%", delta_color="normal")

st.divider()


# ----------------------------------------
# Monthly Sales Trend
# ----------------------------------------
st.subheader("📈 Monthly Sales Trend")

df_filtered = df_filtered.copy()
df_filtered.loc[:, "date"] = pd.to_datetime(
    df_filtered["year"].astype(str) + "-" +
    df_filtered["month"].astype(str) + "-01"
)

df_filtered = df_filtered.sort_values("date")

# st.line_chart(df_filtered.set_index("date")["total_sales"])

# plotly
fig = px.line(
    df_filtered,
    x="date",
    y="total_sales",
    markers=True,
    title=f"Monthly Sales Trend - {selected_year}",
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Sales",
    template="plotly_dark"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# ----------------------------------------
# Category & Region Layout
# ----------------------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Sales by Category")
    st.bar_chart(df_category.set_index("category")["total_sales"])

with colB:
    st.subheader("🌍 Regional Sales")
    st.bar_chart(df_region.set_index("region")["total_sales"])

st.divider()

# ----------------------------------------
# Lead Time Section
# ----------------------------------------
# sorting Data
df_lead_sorted = df_lead.sort_values("avg_lead_time", ascending=False)

st.subheader("⏳ Average Lead Time by Category")
# st.bar_chart(df_lead.set_index("category")["avg_lead_time"])
fig_lead = px.bar(
    df_lead_sorted,
    x="category",
    y="avg_lead_time",
    color="avg_lead_time",
    color_continuous_scale= ["#161B22", "#00BFA6"],
    title="Average Delivery Lead Time by Product Category",
    text_auto=".2f"
)

fig_lead.update_layout(
    xaxis_title="Category",
    yaxis_title="Average Lead Time (Days)",
    template="plotly_dark"
    # coloraxis_showscale = False
)

st.plotly_chart(fig_lead, width="stretch")

# -- Interpretation
slowest_category = df_lead_sorted.iloc[0]["category"]

st.info(f"⚠️ {slowest_category} has the highest average delivery delay. Consider supply chain optimization.")


st.divider()
# ----------------------------------
# Bar Chart of Top Products
# ----------------------------------
st.subheader("🏆 Top 5 Products by Sales")

fig_top = px.bar(
    df_top_products,
    x="total_sales",
    y="product_name",
    orientation="h",
    title=f"Top 5 Products - {selected_year}",
    template="plotly_dark"
)

fig_top.update_layout(
    xaxis_title="Total Sales",
    yaxis_title="Product",
)

st.plotly_chart(fig_top, width="stretch")



us_state_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY"
}

st.divider()
# ------------------------------------
# Sate-wise sales plot
# -----------------------------------

st.subheader("🗺️ Sales by State")

df_state = load_state_sales(selected_year)

if not df_state.empty:

    df_state["state_code"] = df_state["state"].map(us_state_abbrev)

    fig_map = px.choropleth(
        df_state,
        locations="state_code",
        locationmode="USA-states",
        color="total_sales",
        scope="usa",
        color_continuous_scale="Blues",
        title=f"State-wise Sales - {selected_year}"
    )

    fig_map.update_layout(template="plotly_dark")

    st.plotly_chart(fig_map, width="stretch")

else:
    st.warning("No state-level data available for selected year.")

# print(df_state[df_state["state_code"].isnull()])

# markdown string
st.markdown("---")
st.caption("Built using BigQuery + Streamlit | Supply Chain Data Integration Project")
