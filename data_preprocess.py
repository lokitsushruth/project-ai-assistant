import pandas as pd
import os

def preprocess_csv_files():
    """
    Preprocess CSV files to improve data quality before indexing
    """
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            
            # Basic cleaning
            df = df.dropna(how='all')  # Remove completely empty rows
            df = df.fillna('')  # Fill other NaN values with empty string
            
            # Save cleaned version
            df.to_csv(file, index=False)
            print(f"Processed {file}")
            
        except Exception as e:
            print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    preprocess_csv_files()
