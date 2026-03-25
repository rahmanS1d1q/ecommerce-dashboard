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
df = pd.read_csv(data_path)

# Pisahkan data
kpi_df = df[df["type"] == "kpi"]
top_category_df = df[df["type"] == "top_category"]
review_df = df[df["type"] == "review_distribution"]
segment_df = df[df["type"] == "customer_segment"]

# ======================
# SIDEBAR FILTER (WAJIB)
# ======================
st.sidebar.header("Filter")

selected_scores = st.sidebar.multiselect(
    "Pilih Review Score",
    options=sorted(review_df["review_score"].dropna().unique()),
    default=sorted(review_df["review_score"].dropna().unique())
)

# Filter review
filtered_review_df = review_df[review_df["review_score"].isin(selected_scores)]

# Recalculate segment berdasarkan filter
def categorize(score):
    if score >= 4:
        return "High Satisfaction"
    elif score == 3:
        return "Medium Satisfaction"
    else:
        return "Low Satisfaction"

expanded = []
for _, row in filtered_review_df.iterrows():
    score = int(row["review_score"])
    count = int(row["count"])
    expanded.extend([score] * count)

temp_df = pd.DataFrame({"review_score": expanded})
temp_df["segment"] = temp_df["review_score"].apply(categorize)

segment_filtered = temp_df["segment"].value_counts().reset_index()
segment_filtered.columns = ["segment", "count"]

# KPI dari filter
total_reviews = len(temp_df)
avg_score = round(temp_df["review_score"].mean(), 2) if total_reviews > 0 else 0

# ======================
# MAIN
# ======================
st.title("Dashboard Analisis Data E-Commerce")

# KPI
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Review (Filtered)", total_reviews)

with col2:
    st.metric("Average Review Score", avg_score)

st.markdown("---")

# ======================
# CHART 1: CATEGORY
# ======================
st.subheader("Top 10 Kategori Produk")

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=top_category_df,
    x="count",
    y="category",
    ax=ax
)
st.pyplot(fig)

# ======================
# CHART 2: REVIEW
# ======================
st.subheader("Distribusi Review Score (Filtered)")

fig, ax = plt.subplots()
sns.barplot(
    data=filtered_review_df,
    x="review_score",
    y="count",
    ax=ax
)
st.pyplot(fig)

# ======================
# CHART 3: SEGMENT
# ======================
st.subheader("Segmentasi Pelanggan (Filtered)")

fig, ax = plt.subplots()
sns.barplot(
    data=segment_filtered,
    x="segment",
    y="count",
    ax=ax
)
st.pyplot(fig)

# ======================
# INSIGHT DINAMIS
# ======================
st.markdown("---")
st.subheader("Insight Berdasarkan Filter")

st.write(f"Filter aktif: {selected_scores}")
st.write(f"Total review setelah filter: {total_reviews}")
st.write(f"Rata-rata score: {avg_score}")

if avg_score >= 4:
    st.success("Mayoritas pelanggan puas")
elif avg_score >= 3:
    st.info("Kepuasan sedang")
else:
    st.error("Banyak pelanggan tidak puas")
