import pandas as pd

# Prompt the user for the URL of the CSV file
csv_url = input("Enter the URL of the CSV file: ")

# Prompt the user for the output file name
output_file = input("Enter the name of the output Parquet file (without extension): ")

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_url)

# Convert the DataFrame to Parquet format
df.to_parquet(f"{output_file}.parquet", index=False)

print("CSV file converted to Parquet successfully!")
