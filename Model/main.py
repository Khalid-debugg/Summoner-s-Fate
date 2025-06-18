from data_generator import generate_data
import pandas as pd
import os

if __name__ == "__main__":
    generate_data()

def load_all_data():
    csv_dir = os.path.join(os.path.dirname(__file__), "CSVs")
    csv_files = sorted([f for f in os.listdir(csv_dir) if f.endswith(".csv")])
    
    dfs = []
    for file in csv_files:
        df = pd.read_csv(os.path.join(csv_dir, file))
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)