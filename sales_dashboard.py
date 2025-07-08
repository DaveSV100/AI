import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

load_dotenv()

def connect_to_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_DATABASE"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
    )

def load_sales():
    conn = connect_to_db()
    query = "SELECT * FROM sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("📊 Sales Summary Dashboard")

sales_df = load_sales()

st.metric("Total sales", len(sales_df))
st.metric("Total revenue", f"${sales_df['total_price'].sum():,.2f}")
st.metric("Average sale value", f"${sales_df['total_price'].mean():,.2f}")

st.subheader("🔹 Payment Methods")
st.bar_chart(sales_df["formadepago"].value_counts())

st.subheader("🏢 Sales by Branch")
st.bar_chart(sales_df["sucursal"].value_counts())

sales_df["fecha"] = pd.to_datetime(sales_df["fecha"])
daily = sales_df.groupby("fecha")["total_price"].sum()
st.subheader("📈 Revenue Over Time")
st.line_chart(daily)




