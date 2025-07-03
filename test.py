import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_db():
    return psycopg2.connect(
        host="YOUR_DB_HOST",
        port="YOUR_DB_PORT",
        database="defaultdb",
        user="YOUR_DB_USER",
        password="YOUR_DB_PASS"
    )

def load_sales(conn):
    # Pull every column from the sales table
    query = "SELECT * FROM sales"
    return pd.read_sql(query, conn)

def summarize_sales(df):
    # 1) Total rows & revenue
    print("🔹 Total sales records:", len(df))
    print("🔹 Total revenue:", df["total_price"].sum())

    # 2) Sales count by branch
    print("\n🔹 Sales by branch:")
    print(df["sucursal"].value_counts())

    # 3) Payment method distribution
    print("\n🔹 Payment methods:")
    print(df["formadepago"].value_counts())

    # 4) Average sale value
    avg = df["total_price"].mean()
    print(f"\n🔹 Average sale value: {avg:.2f}")

def plot_sales_over_time(df):
    # Ensure fecha is a datetime
    df["fecha"] = pd.to_datetime(df["fecha"])
    daily = df.groupby("fecha")["total_price"].sum().reset_index()
    
    plt.figure()
    plt.plot(daily["fecha"], daily["total_price"])
    plt.title("Daily Revenue Over Time")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()

def plot_sales_by_branch(df):
    counts = df["sucursal"].value_counts()
    plt.figure()
    counts.plot.bar()
    plt.title("Number of Sales by Branch")
    plt.xlabel("Branch")
    plt.ylabel("Number of Sales")
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
    df.to_csv("all_sales.csv", index=False)
    print("\n✅ Saved full sales data to ‘all_sales.csv’")

if __name__ == "__main__":
    main()
