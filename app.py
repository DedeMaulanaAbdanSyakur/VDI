
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from pymongo import MongoClient
import plotly.express as px

st.set_page_config(
    page_title="Supermarket Dashboard",
    page_icon="📊",
    layout="wide"
)

load_dotenv()
POSTGRES_URI = os.getenv("POSTGRES_URI")
MONGO_URI = os.getenv("MONGO_URI")

@st.cache_data(ttl=300)
def load_data():
    engine = create_engine(POSTGRES_URI)
    df_pg = pd.read_sql("SELECT * FROM branch_master", engine)
    engine.dispose()

    client = MongoClient(MONGO_URI)
    db = client["supermarket_db"]
    data = list(db["transactions"].find({}, {"_id": 0}))
    client.close()

    df_mongo = pd.DataFrame(data)

    return pd.merge(df_mongo, df_pg, on="Branch", how="left")


try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

if df.empty:
    st.warning("Data transaksi kosong.")
    st.stop()

# Pastikan kolom numerik
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")


st.sidebar.title("Supermarket")
st.sidebar.subheader("Filter Reports")

cities = sorted(df["City"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "Pilih Kota",
    cities,
    default=cities
)

branches = sorted(
    df[df["City"].isin(selected_cities)]["Branch"]
    .dropna().unique()
)

selected_branches = st.sidebar.multiselect(
    "Pilih Cabang",
    branches,
    default=branches
)

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.success("Database Connected")

# Filter data
filtered_df = df[
    (df["City"].isin(selected_cities)) &
    (df["Branch"].isin(selected_branches))
]


st.title("Supermarket Analytics")
st.caption("Sales performance and customer satisfaction overview.")

if filtered_df.empty:
    st.warning("Tidak ada data sesuai filter.")

else:

    # =================================
    # KPI
    # =================================

    revenue = filtered_df["Sales"].sum()
    rating = filtered_df["Rating"].mean()
    transactions = len(filtered_df)

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Revenue", f"${revenue:,.2f}")
    col2.metric("⭐ Average Rating", f"{rating:.1f}/10" if pd.notna(rating) else "N/A")
    col3.metric("🛒 Total Transactions", f"{transactions:,}")

    st.divider()

    # =================================
    # CHARTS
    # =================================

    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Revenue by City")

        revenue_city = (
            filtered_df.groupby("City")["Sales"]
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            revenue_city,
            x="City",
            y="Sales",
            color="City",
            template="plotly_dark"
        )

        st.plotly_chart(fig1, use_container_width=True)

    with chart2:
        st.subheader("Rating by Branch")

        rating_branch = (
            filtered_df.groupby("Branch")["Rating"]
            .mean()
            .reset_index()
        )

        fig2 = px.pie(
            rating_branch,
            names="Branch",
            values="Rating",
            hole=0.5,
            template="plotly_dark"
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # =================================
    # TRANSACTION TABLE
    # =================================

    st.subheader("📋 Transaction Details")

    search = st.text_input("Cari data transaksi")

    display_df = filtered_df.copy()

    if search:
        mask = display_df.astype(str).apply(
            lambda x: x.str.contains(search, case=False, na=False)
        ).any(axis=1)

        display_df = display_df[mask]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="supermarket_transactions.csv",
        mime="text/csv"
    )

# Footer
st.divider()
st.caption("Supermarket Analytics | PostgreSQL + MongoDB + Streamlit")
