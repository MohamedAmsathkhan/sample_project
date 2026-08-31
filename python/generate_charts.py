import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Define file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
output_dir = os.path.join(base_dir, 'data')

print("Loading data from SQLite Database...")
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

# Set dark grid style for professional charts
sns.set_theme(style="darkgrid")

# Chart 1: Revenue by Category (Bar Chart)
plt.figure(figsize=(8, 5))
cat_revenue = df.groupby('category')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False)
ax1 = sns.barplot(data=cat_revenue, x='category', y='total_amount', palette='magma')
plt.title('Total Revenue by Product Category ($)', fontsize=14, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Total Revenue ($)', fontsize=12)

for p in ax1.patches:
    ax1.annotate(f"${p.get_height():,.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                 ha='center', va='bottom', fontsize=10, fontweight='bold', xytext=(0, 5), textcoords='offset points')

chart1_path = os.path.join(output_dir, 'revenue_by_category.png')
plt.tight_layout()
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"[SUCCESS] Saved Chart 1 to {chart1_path}")

# Chart 2: Order Status Breakdown (Pie Chart)
plt.figure(figsize=(6, 6))
status_counts = df['order_status'].value_counts()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'], startangle=140, explode=(0, 0.1))
plt.title('Order Status Breakdown (Completed vs Returned)', fontsize=14, fontweight='bold')

chart2_path = os.path.join(output_dir, 'order_status_breakdown.png')
plt.tight_layout()
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"[SUCCESS] Saved Chart 2 to {chart2_path}")
