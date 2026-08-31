import pandas as pd
import sqlite3
import os

# Define file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, 'data', 'raw_sales.csv')
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')

print("Loading Raw Sales Data...")
df = pd.read_csv(csv_path)

# Calculate Total Sale Amount
df['total_amount'] = df['quantity'] * df['unit_price']
df['order_date'] = pd.to_datetime(df['order_date'])

print("\n--- Sales Summary ---")
print(f"Total Transactions: {len(df)}")
print(f"Total Revenue: ${df['total_amount'].sum():,.2f}")
print("\n--- Revenue by Category ---")
category_summary = df.groupby('category')['total_amount'].sum().reset_index()
print(category_summary)

# Save into SQLite Database
conn = sqlite3.connect(db_path)
df.to_sql('sales', conn, if_exists='replace', index=False)
conn.close()

print(f"\n[SUCCESS] Data successfully processed and exported to SQLite Database: {db_path}")
