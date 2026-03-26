import streamlit as st
import pandas as pd

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("b2b_leads_dataset.xlsx", engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

df = load_data()

# Stop if data not loaded
if df is None:
    st.stop()

# ------------------ TITLE ------------------
st.title("📊 B2B Sales Analytics Dashboard")

# ------------------ KPIs ------------------
total_leads = len(df)
converted_leads = df[df['Status'] == "Converted"].shape[0]
conversion_rate = (converted_leads / total_leads) * 100
avg_followup = df['Follow_Up_Time'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", total_leads)
col2.metric("Converted Leads", converted_leads)
col3.metric("Conversion Rate (%)", round(conversion_rate, 2))
col4.metric("Avg Follow-Up Time", round(avg_followup, 2))

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect("Region", df["Region"].unique())
industry_filter = st.sidebar.multiselect("Industry", df["Industry"].unique())
source_filter = st.sidebar.multiselect("Lead Source", df["Lead_Source"].unique())

# Apply filters
filtered_df = df.copy()

if region_filter:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]

if industry_filter:
    filtered_df = filtered_df[filtered_df["Industry"].isin(industry_filter)]

if source_filter:
    filtered_df = filtered_df[filtered_df["Lead_Source"].isin(source_filter)]

# ------------------ CHARTS ------------------

st.subheader("📊 Leads by Region")
st.bar_chart(filtered_df["Region"].value_counts())

st.subheader("📊 Conversion by Industry")
conversion_data = filtered_df[filtered_df["Status"] == "Converted"]
st.bar_chart(conversion_data["Industry"].value_counts())

st.subheader("📈 Revenue Trend")
st.line_chart(filtered_df["Revenue"])

st.subheader("📊 Lead Source Analysis")
st.bar_chart(filtered_df["Lead_Source"].value_counts())

# ------------------ INSIGHTS ------------------

st.subheader("📌 Insights")

st.write(f"Total Leads: {total_leads}")
st.write(f"Converted Leads: {converted_leads}")
st.write(f"Conversion Rate: {round(conversion_rate, 2)}%")
st.write(f"Average Follow-Up Time: {round(avg_followup, 2)} hours")
