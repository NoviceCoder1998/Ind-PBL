import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load and clean dataset
def load_data():
    df = pd.read_csv("Ind PBL.csv")
    columns_to_clean = [
        'Number of Customers', 'Revenue', 'Marketing Spend', 'Operational Cost',
        'Regulatory Compliance Cost', 'Non Interest Income', 'GDP Billion USD',
        'Total Cost', 'Profit', 'Profit Margin'
    ]
    for col in columns_to_clean:
        if col == 'Profit Margin':
            df[col] = df[col].str.replace('%', '', regex=False).astype(float)
        else:
            df[col] = df[col].str.replace(',', '', regex=False).astype(float)
    df.columns = df.columns.str.replace(' ', '_').str.replace('%', 'Percent').str.lower()
    return df

# Page config
st.set_page_config(page_title="Bank Profit Insights Dashboard", layout="wide")
st.title("🏦 Bank Profit Insights Dashboard")
st.markdown("This dashboard provides comprehensive macro and micro analysis of bank profits for executives and stakeholders.")

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
countries = st.sidebar.multiselect("Select Countries", options=df.country.unique(), default=df.country.unique())
products = st.sidebar.multiselect("Select Products", options=df.product.unique(), default=df.product.unique())
branches = st.sidebar.multiselect("Select Branches", options=df.branch.unique(), default=df.branch.unique())

# Filter dataset
df_filtered = df[
    (df.country.isin(countries)) &
    (df.product.isin(products)) &
    (df.branch.isin(branches))
]

# Overview KPIs
st.subheader("🔹 Overview KPIs")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Profit", f"${df_filtered.profit.sum():,.2f}")
col2.metric("Average Profit Margin", f"{df_filtered.profit_margin.mean():.2f}%")
col3.metric("Total Revenue", f"${df_filtered.revenue.sum():,.2f}")
col4.metric("Total Customers", f"{int(df_filtered.number_of_customers.sum()):,}")

# Visual Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Country Insights", "Product Performance", "Cost & Profit Analysis", "Risk & Quality", "Economic Factors"])

with tab1:
    st.markdown("### 📍 Profit Distribution by Country")
    st.markdown("This chart shows total profit generated from each country after applying filters.")
    fig1 = px.bar(df_filtered.groupby("country", as_index=False).agg({"profit": "sum"}),
                  x="country", y="profit", color="country",
                  labels={'profit': 'Total Profit', 'country': 'Country'}, title="Profit by Country")
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 📍 Revenue vs Profit by Country")
    st.markdown("This scatter plot compares total revenue and profit across different countries.")
    country_group = df_filtered.groupby("country", as_index=False).agg({"revenue": "sum", "profit": "sum"})
    fig2 = px.scatter(country_group, x="revenue", y="profit", color="country",
                      size="profit", title="Revenue vs Profit by Country")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📍 Profit Margin Distribution by Country")
    st.markdown("This box plot visualizes the variation in profit margins across countries.")
    fig3 = px.box(df_filtered, x="country", y="profit_margin", color="country",
                  title="Profit Margin Distribution by Country")
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.markdown("### 📦 Product-Wise Profit")
    st.markdown("This bar chart shows the average profit per product.")
    fig4 = px.bar(df_filtered.groupby("product", as_index=False).agg({"profit": "mean"}),
                  x="product", y="profit", color="product", title="Average Profit by Product")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### 📦 Product-Wise Customer Count")
    st.markdown("Number of customers per product helps understand product popularity.")
    fig5 = px.pie(df_filtered, names="product", values="number_of_customers", title="Customer Count by Product")
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### 📦 Profit Margin by Product")
    fig6 = px.violin(df_filtered, x="product", y="profit_margin", color="product", box=True,
                     title="Profit Margin Spread by Product")
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.markdown("### 💸 Operational Cost vs Profit")
    st.markdown("This scatter plot explores the relationship between operational costs and profit.")
    fig7 = px.scatter(df_filtered, x="operational_cost", y="profit", color="country",
                      title="Operational Cost vs Profit")
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("### 💸 Total Cost vs Profit")
    fig8 = px.scatter(df_filtered, x="total_cost", y="profit", color="product",
                      title="Total Cost vs Profit by Product")
    st.plotly_chart(fig8, use_container_width=True)

    st.markdown("### 💸 Marketing Spend vs Revenue")
    fig9 = px.scatter(df_filtered, x="marketing_spend", y="revenue", color="product",
                      title="Marketing Spend vs Revenue")
    st.plotly_chart(fig9, use_container_width=True)

with tab4:
    st.markdown("### ⚠️ Credit Risk vs Profit")
    st.markdown("Higher credit risk generally leads to lower profits. This chart explores that.")
    fig10 = px.scatter(df_filtered, x="credit_risk_score", y="profit", color="country",
                       title="Credit Risk Score vs Profit")
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown("### ⚠️ Loan Quality Score vs Profit Margin")
    fig11 = px.scatter(df_filtered, x="loan_quality_score", y="profit_margin", color="product",
                       title="Loan Quality vs Profit Margin")
    st.plotly_chart(fig11, use_container_width=True)

    st.markdown("### ⚠️ Credit Risk Distribution")
    fig12 = px.histogram(df_filtered, x="credit_risk_score", nbins=30, title="Distribution of Credit Risk Scores")
    st.plotly_chart(fig12, use_container_width=True)

with tab5:
    st.markdown("### 🌍 GDP vs Profit")
    st.markdown("GDP of countries compared against the total profit they contribute.")
    fig13 = px.scatter(df_filtered, x="gdp_billion_usd", y="profit", color="country",
                       title="GDP vs Profit")
    st.plotly_chart(fig13, use_container_width=True)

    st.markdown("### 🌍 Inflation vs Profit Margin")
    fig14 = px.scatter(df_filtered, x="inflation_percent", y="profit_margin", color="country",
                       title="Inflation vs Profit Margin")
    st.plotly_chart(fig14, use_container_width=True)

    st.markdown("### 🌍 Interest Rate vs Revenue")
    fig15 = px.scatter(df_filtered, x="interest_rate_percent", y="revenue", color="country",
                       title="Interest Rate vs Revenue")
    st.plotly_chart(fig15, use_container_width=True)
if 'product' in df.columns:
    products = st.sidebar.multiselect("Select Products", options=df['product'].unique(), default=df['product'].unique())
else:
    st.sidebar.warning("⚠️ 'Product' column not found in the data.")
