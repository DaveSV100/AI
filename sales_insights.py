from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
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
    
def load_sales(conn):
    # Pull every column from the sales table
    query = "SELECT * FROM sales"
    return pd.read_sql(query, conn)

def summarize_sales(sales_data):
    # 1) Total rows & revenue
    print("🔹 Total sales records:", len(sales_data))
    print("🔹 Total revenue:", sales_data["total_price"].sum())
    
    # 2) Sales count by branch
    print("\n 🔹 Sales by branch:")
    print(sales_data["sucursal"].value_counts())
    
    # 3) Payment method distribution
    print("\n🔹 Payment methods:")
    print(sales_data["formadepago"].value_counts())
    
    # 4) Average sale value
    avg = sales_data["total_price"].mean()
    print(f"\n🔹 Average sale value: {avg:.2f}")

def plot_sales_over_time(sales_data):
    sales_data["fecha"] = pd.to_datetime(sales_data["fecha"])
    daily = sales_data.groupby("fecha")["total_price"].sum().reset_index()
    
    plt.figure()
    plt.plot(daily["fecha"], daily["total_price"])
    plt.title("Daily Revenue Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()
    
def plot_sales_by_branch(sales_data):
    counts = sales_data["sucursal"].value_counts()
    plt.figure()
    counts.plot.bar()
    plt.title("Number of Sales by Branch")
    plt.xlabel("Branch")
    plt.ylabel("Number of sales")
    plt.tight_layout()
    plt.show()
    
    
def main():
    conn = connect_to_db()
    df = load_sales(conn)
    conn.close()
    
    summarize_sales(df)
    plot_sales_over_time(df)
    plot_sales_by_branch(df)
    
    # Save a cleaned CSV of all sales for future use
    print("Saving CSV to:", os.getcwd())
    df.to_csv("all_sales.csv", index=False)
    print("\n✅ Saved data to all_sales.csv")
    
if __name__ == "__main__":
    main()