import streamlit as st
import pandas as pd

# Load Data
df = pd.read_excel("b2b_leads_dataset.xlsx")

# Title
st.title("📊 B2B Sales Analytics Dashboard")

# ------------------ KPI SECTION ------------------
st.subheader("Key Performance Indicators")

total_leads = len(df)
converted_leads = len(df[df['Status'] == "Converted"])
conversion_rate = (converted_leads / total_leads) * 100
avg_followup = df['Follow_Up_Time'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", total_leads)
col2.metric("Converted Leads", converted_leads)
col3.metric("Conversion Rate (%)", round(conversion_rate, 2))
col4.metric("Avg Follow-Up Time", round(avg_followup, 2))

# ------------------ FILTERS ------------------
st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect(
    "Select Region", df["Region"].unique()
)

industry_filter = st.sidebar.multiselect(
    "Select Industry", df["Industry"].unique()
)

source_filter = st.sidebar.multiselect(
    "Select Lead Source", df["Lead_Source"].unique()
)

# Apply Filters
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
conv_industry = filtered_df[filtered_df["Status"] == "Converted"]["Industry"].value_counts()
st.bar_chart(conv_industry)

st.subheader("📈 Revenue Trend")
st.line_chart(filtered_df["Revenue"])

st.subheader("📊 Lead Source Analysis")
st.bar_chart(filtered_df["Lead_Source"].value_counts())

# ------------------ INSIGHTS ------------------

st.subheader("📌 Insights")

st.write("✔ Total Leads:", total_leads)
st.write("✔ Conversion Rate:", round(conversion_rate, 2), "%")
st.write("✔ Avg Follow-Up Time:", round(avg_followup, 2), "hours")
