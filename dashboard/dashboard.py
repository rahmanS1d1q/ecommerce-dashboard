import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
sns.set(style="whitegrid")

# Load data
base_dir = os.path.dirname(__file__)
data_path = os.path.join(base_dir, "main_data.csv")
main_data_df = pd.read_csv(data_path)

# Pisahkan data berdasarkan tipe
kpi_df = main_data_df[main_data_df["type"] == "kpi"].copy()
top_categories_df = main_data_df[main_data_df["type"] == "top_category"].copy()
review_distribution_df = main_data_df[main_data_df["type"] == "review_distribution"].copy()
customer_segment_df = main_data_df[main_data_df["type"] == "customer_segment"].copy()

# Rapikan tipe data
top_categories_df["count"] = pd.to_numeric(top_categories_df["count"], errors="coerce")
review_distribution_df["count"] = pd.to_numeric(review_distribution_df["count"], errors="coerce")
review_distribution_df["review_score"] = pd.to_numeric(
    review_distribution_df["review_score"], errors="coerce"
)
customer_segment_df["count"] = pd.to_numeric(customer_segment_df["count"], errors="coerce")

# Hapus NaN jika ada
top_categories_df = top_categories_df.dropna(subset=["category", "count"])
review_distribution_df = review_distribution_df.dropna(subset=["review_score", "count"])
customer_segment_df = customer_segment_df.dropna(subset=["segment", "count"])

review_distribution_df["review_score"] = review_distribution_df["review_score"].astype(int)

# Helper KPI
def get_kpi(metric_name: str, default_value=0):
    result = kpi_df.loc[kpi_df["metric"] == metric_name, "value"]
    if result.empty:
        return default_value
    return result.values[0]

total_products = int(float(get_kpi("total_products", 0)))
total_categories = int(float(get_kpi("total_categories", 0)))
total_reviews = int(float(get_kpi("total_reviews", 0)))
average_review_score = round(float(get_kpi("average_review_score", 0)), 2)

# Sidebar Interaktif
st.sidebar.header("Filter Dashboard")

category_options = ["All"] + sorted(top_categories_df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "Pilih kategori produk",
    options=category_options,
    index=0
)

segment_options = customer_segment_df["segment"].dropna().unique().tolist()
selected_segments = st.sidebar.multiselect(
    "Pilih segmen pelanggan",
    options=segment_options,
    default=segment_options
)

# Filter kategori
if selected_category != "All":
    filtered_categories_df = top_categories_df[top_categories_df["category"] == selected_category]
else:
    filtered_categories_df = top_categories_df.copy()

# Filter segment
filtered_segment_df = customer_segment_df[
    customer_segment_df["segment"].isin(selected_segments)
].copy()

# Main page
st.title("Dashboard Analisis Data E-Commerce")
st.markdown(
    "Dashboard ini menampilkan distribusi kategori produk, distribusi review score, "
    "dan segmentasi pelanggan berdasarkan tingkat kepuasan."
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
    data=filtered_categories_df,
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
    data=filtered_segment_df,
    x="segment",
    y="count",
    ax=ax
)
ax.set_title("Distribusi Segmentasi Pelanggan")
ax.set_xlabel("Segment")
ax.set_ylabel("Jumlah Pelanggan")
st.pyplot(fig)

st.markdown("---")

# Insight singkat dinamis
if selected_category == "All":
    category_text = "seluruh kategori produk"
else:
    category_text = f"kategori **{selected_category}**"

if len(selected_segments) == len(segment_options):
    segment_text = "semua segmen pelanggan"
elif len(selected_segments) == 0:
    segment_text = "tidak ada segmen yang dipilih"
else:
    segment_text = ", ".join(selected_segments)

st.markdown("### Insight Singkat")
st.write(
    f"- Grafik kategori saat ini menampilkan data untuk {category_text}."
)
st.write(
    "- Mayoritas pelanggan memberikan review score tinggi, terutama nilai 5."
)
st.write(
    f"- Grafik segmentasi saat ini menampilkan: **{segment_text}**."
)
