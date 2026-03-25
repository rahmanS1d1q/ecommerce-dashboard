import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
sns.set(style="whitegrid")

# Load data
main_data_df = pd.read_csv("main_data.csv")

# KPI
kpi_df = main_data_df[main_data_df["type"] == "kpi"].copy()

def get_kpi(metric_name):
    return kpi_df.loc[kpi_df["metric"] == metric_name, "value"].values[0]

total_products = int(float(get_kpi("total_products")))
total_categories = int(float(get_kpi("total_categories")))
total_reviews = int(float(get_kpi("total_reviews")))
average_review_score = round(float(get_kpi("average_review_score")), 2)

# Data chart
top_categories_df = main_data_df[main_data_df["type"] == "top_category"].copy()
review_distribution_df = main_data_df[main_data_df["type"] == "review_distribution"].copy()
customer_segment_df = main_data_df[main_data_df["type"] == "customer_segment"].copy()

# Rapikan tipe data
top_categories_df["count"] = top_categories_df["count"].astype(float)
review_distribution_df["count"] = review_distribution_df["count"].astype(float)
review_distribution_df["review_score"] = review_distribution_df["review_score"].astype(int)
customer_segment_df["count"] = customer_segment_df["count"].astype(float)

# Header
st.title("Dashboard Analisis Data E-Commerce")
st.markdown(
    "Dashboard ini menampilkan distribusi kategori produk, distribusi review score, "
    "serta segmentasi pelanggan berdasarkan tingkat kepuasan."
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Products", total_products)

with col2:
    st.metric("Total Categories", total_categories)

with col3:
    st.metric("Total Reviews", total_reviews)

with col4:
    st.metric("Average Review Score", average_review_score)

st.markdown("---")

# Chart 1 - Top Categories
st.subheader("Top 10 Kategori Produk Terbanyak")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=top_categories_df,
    x="count",
    y="category",
    ax=ax
)
ax.set_title("Top 10 Kategori Produk")
ax.set_xlabel("Jumlah Produk")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# Chart 2 - Review Distribution
st.subheader("Distribusi Review Score")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=review_distribution_df,
    x="review_score",
    y="count",
    ax=ax
)
ax.set_title("Distribusi Review Score Pelanggan")
ax.set_xlabel("Review Score")
ax.set_ylabel("Jumlah Review")
st.pyplot(fig)

# Chart 3 - Customer Segment
st.subheader("Segmentasi Pelanggan Berdasarkan Kepuasan")

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(
    data=customer_segment_df,
    x="segment",
    y="count",
    ax=ax
)
ax.set_title("Distribusi Segmentasi Pelanggan")
ax.set_xlabel("Segment")
ax.set_ylabel("Jumlah Pelanggan")
st.pyplot(fig)

st.markdown("---")

st.markdown(
    """
    ### Insight Singkat
    - Kategori produk terbanyak didominasi oleh kebutuhan rumah tangga dan gaya hidup.
    - Mayoritas pelanggan memberikan review score tinggi, terutama nilai 5.
    - Sebagian besar pelanggan termasuk dalam segmen **High Satisfaction**.
    """
)