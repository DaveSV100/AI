import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Load the dataset
    df = pd.read_csv('Data.csv')
    
    print("Rows", len(df))
    print("Columns", list(df.columns))
    print("\nNumber of first 5:\n", df.head())
    print("\nNumber of last 5:\n", df.tail())
    
    col = "SepalWidthCm"
    if col in df.columns:
        df[col].hist()
        print("\nDescription of the column:")
        df[col].describe()
        plt.title(f"Histogram of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        # plt.show()
        plt.savefig("Petals-histogram.png")
    else: 
        print(f"Column {col} not found")
        
if __name__ == "__main__":
    main()