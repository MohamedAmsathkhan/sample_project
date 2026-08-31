import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .metric-card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load Data from SQLite Database
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['order_date'] = pd.to_datetime(df['order_date'])
    return df

df = load_data()

# Header
st.title("📊 E-Commerce Sales & Customer Insights")
st.markdown("### Interactive Data Analytics Dashboard & SQL Insights")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
category_filter = st.sidebar.multiselect(
    "Select Product Category:",
    options=df['category'].unique(),
    default=df['category'].unique()
)

status_filter = st.sidebar.multiselect(
    "Select Order Status:",
    options=df['order_status'].unique(),
    default=df['order_status'].unique()
)

# Apply Filters
filtered_df = df[
    (df['category'].isin(category_filter)) &
    (df['order_status'].isin(status_filter))
]

# KPI Metrics
total_revenue = filtered_df[filtered_df['order_status'] == 'Completed']['total_amount'].sum()
total_orders = len(filtered_df)
completed_orders = len(filtered_df[filtered_df['order_status'] == 'Completed'])
aov = total_revenue / completed_orders if completed_orders > 0 else 0
return_rate = (len(filtered_df[filtered_df['order_status'] == 'Returned']) / total_orders * 100) if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="💰 Total Revenue", value=f"${total_revenue:,.2f}")
with col2:
    st.metric(label="📦 Total Orders", value=f"{total_orders}")
with col3:
    st.metric(label="🛒 Avg Order Value (AOV)", value=f"${aov:,.2f}")
with col4:
    st.metric(label="🔄 Return Rate", value=f"{return_rate:.1f}%")

st.markdown("---")

# Tabs for Dashboard, SQL Explorer, and Raw Data
tab1, tab2, tab3 = st.tabs(["📈 Executive Dashboard", "🛢️ SQL Query Runner", "📁 Data Table"])

with tab1:
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.subheader("Total Revenue by Category")
        cat_rev = filtered_df[filtered_df['order_status'] == 'Completed'].groupby('category')['total_amount'].sum().reset_index()
        fig_bar = px.bar(
            cat_rev, x='category', y='total_amount',
            text_auto='$.2s', color='category',
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={'total_amount': 'Revenue ($)', 'category': 'Category'}
        )
        fig_bar.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_bar, use_container_width=True)

    with row1_col2:
        st.subheader("Order Status Distribution")
        status_cnt = filtered_df['order_status'].value_counts().reset_index()
        status_cnt.columns = ['order_status', 'count']
        fig_pie = px.pie(
            status_cnt, names='order_status', values='count',
            hole=0.4, color_discrete_sequence=['#10B981', '#EF4444']
        )
        fig_pie.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.subheader("Monthly Sales Revenue Trend")
        df_trend = filtered_df[filtered_df['order_status'] == 'Completed'].copy()
        df_trend['year_month'] = df_trend['order_date'].dt.to_period('M').astype(str)
        monthly_df = df_trend.groupby('year_month')['total_amount'].sum().reset_index()
        
        fig_line = px.line(
            monthly_df, x='year_month', y='total_amount',
            markers=True, line_shape='spline',
            labels={'total_amount': 'Revenue ($)', 'year_month': 'Month'}
        )
        fig_line.update_traces(line_color='#3B82F6', line_width=3)
        fig_line.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_line, use_container_width=True)

    with row2_col2:
        st.subheader("Top 5 Customers by Spend")
        top_cust = filtered_df[filtered_df['order_status'] == 'Completed'].groupby('customer_name')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=True).tail(5)
        fig_cust = px.bar(
            top_cust, y='customer_name', x='total_amount',
            orientation='h', text_auto='$.2s', color_discrete_sequence=['#8B5CF6']
        )
        fig_cust.update_layout(template="plotly_dark", height=400)
        st.plotly_chart(fig_cust, use_container_width=True)

with tab2:
    st.subheader("🛢️ Live SQL Analytical Queries")
    st.markdown("Run custom SQL queries on `ecommerce.db` database:")
    
    default_query = """SELECT 
    category,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM sales
WHERE order_status = 'Completed'
GROUP BY category
ORDER BY total_revenue DESC;"""

    query = st.text_area("SQL Query Input:", value=default_query, height=150)
    
    if st.button("▶ Run SQL Query"):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'data', 'ecommerce.db')
            conn = sqlite3.connect(db_path)
            res = pd.read_sql_query(query, conn)
            conn.close()
            st.success("Query Executed Successfully!")
            st.dataframe(res, use_container_width=True)
        except Exception as e:
            st.error(f"SQL Error: {e}")

with tab3:
    st.subheader("📁 Processed Sales Dataset")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name="filtered_ecommerce_sales.csv",
        mime="text/csv"
    )
