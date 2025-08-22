import streamlit as st
import pandas as pd

st.title("🛒 Retail Sales Dashboard")

# Load data
df = pd.read_csv("data/retail_sales.csv", sep="\t")

# Show raw data
st.subheader("Raw Data Preview")
st.dataframe(df.head())

# Revenue trend
st.subheader("Revenue Over Time")
revenue_time = df.groupby("date")["revenue"].sum().reset_index()
st.line_chart(revenue_time, x="date", y="revenue")

# Top categories
st.subheader("Top Categories by Revenue")
cat_rev = df.groupby("category")["revenue"].sum().reset_index().sort_values(by="revenue", ascending=False)
st.bar_chart(cat_rev, x="category", y="revenue")
