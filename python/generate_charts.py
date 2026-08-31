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

# Ensure order_date is datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Set dark grid style for professional charts
sns.set_theme(style="darkgrid")

# -------------------------------------------------------------
# Chart 1: Revenue by Category (Bar Chart)
# -------------------------------------------------------------
plt.figure(figsize=(8, 5))
cat_revenue = df[df['order_status'] == 'Completed'].groupby('category')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False)
ax1 = sns.barplot(data=cat_revenue, x='category', y='total_amount', hue='category', palette='magma', legend=False)
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

# -------------------------------------------------------------
# Chart 2: Order Status Breakdown (Pie Chart)
# -------------------------------------------------------------
plt.figure(figsize=(6, 6))
status_counts = df['order_status'].value_counts()
plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=['#4CAF50', '#FF5722'], startangle=140, explode=(0, 0.1))
plt.title('Order Status Breakdown (Completed vs Returned)', fontsize=14, fontweight='bold')

chart2_path = os.path.join(output_dir, 'order_status_breakdown.png')
plt.tight_layout()
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"[SUCCESS] Saved Chart 2 to {chart2_path}")

# -------------------------------------------------------------
# Chart 3: Monthly Revenue Trend (Line Chart)
# -------------------------------------------------------------
plt.figure(figsize=(9, 5))
df['year_month'] = df['order_date'].dt.to_period('M').astype(str)
monthly_trend = df[df['order_status'] == 'Completed'].groupby('year_month')['total_amount'].sum().reset_index()

ax3 = sns.lineplot(data=monthly_trend, x='year_month', y='total_amount', marker='o', color='#2196F3', linewidth=2.5)
plt.title('Monthly Sales Revenue Trend ($)', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue ($)', fontsize=12)

for x, y in zip(monthly_trend['year_month'], monthly_trend['total_amount']):
    plt.annotate(f"${y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontweight='bold')

chart3_path = os.path.join(output_dir, 'monthly_revenue_trend.png')
plt.tight_layout()
plt.savefig(chart3_path, dpi=300)
plt.close()
print(f"[SUCCESS] Saved Chart 3 to {chart3_path}")

# -------------------------------------------------------------
# Chart 4: Top 5 Customers by Spend (Horizontal Bar Chart)
# -------------------------------------------------------------
plt.figure(figsize=(8, 5))
customer_spend = df[df['order_status'] == 'Completed'].groupby('customer_name')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False).head(5)

ax4 = sns.barplot(data=customer_spend, y='customer_name', x='total_amount', hue='customer_name', palette='viridis', legend=False)
plt.title('Top 5 Spending Customers ($)', fontsize=14, fontweight='bold')
plt.ylabel('Customer Name', fontsize=12)
plt.xlabel('Total Spent ($)', fontsize=12)

for p in ax4.patches:
    width = p.get_width()
    ax4.annotate(f"${width:,.2f}", (width, p.get_y() + p.get_height() / 2.),
                 ha='left', va='center', fontsize=10, fontweight='bold', xytext=(5, 0), textcoords='offset points')

chart4_path = os.path.join(output_dir, 'top_customers.png')
plt.tight_layout()
plt.savefig(chart4_path, dpi=300)
plt.close()
print(f"[SUCCESS] Saved Chart 4 to {chart4_path}")
