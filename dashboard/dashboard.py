import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# Sidebar - Date Filter
st.sidebar.header("Filter Data")
min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

start_date = st.sidebar.date_input("Tanggal Mulai", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date, min_value=min_date, max_value=max_date)

# Filter data berdasarkan tanggal
filtered_df = df[
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
]

# Header
st.title("🛒 E-Commerce Dashboard")
st.markdown("Dashboard analisis data E-Commerce Olist Brazil")
st.markdown("---")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    total_revenue = filtered_df['price'].sum()
    st.metric("Total Revenue", f"R$ {total_revenue:,.2f}")

with col3:
    avg_order_value = filtered_df.groupby('order_id')['price'].sum().mean()
    st.metric("Avg Order Value", f"R$ {avg_order_value:,.2f}")

with col4:
    total_customers = filtered_df['customer_unique_id'].nunique()
    st.metric("Total Customers", f"{total_customers:,}")

st.markdown("---")

# Row 1: Monthly Orders Trend
st.subheader("📈 Trend Penjualan Bulanan")

monthly_orders = filtered_df.groupby(
    filtered_df['order_purchase_timestamp'].dt.to_period('M')
).agg({
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

monthly_orders.columns = ['month', 'total_orders', 'total_revenue']
monthly_orders['month'] = monthly_orders['month'].astype(str)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(
    monthly_orders['month'],
    monthly_orders['total_orders'],
    marker='o',
    linewidth=2,
    color='#3498db'
)
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Order')
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)
plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# Row 2: Best and Worst Products
st.subheader("🏆 Kategori Produk Terlaris & Kurang Laris")

col1, col2 = st.columns(2)

# Best Products
with col1:
    st.markdown("**Top 5 Kategori Terlaris**")
    
    category_sales = filtered_df.groupby('product_category_name_english').agg({
        'order_id': 'count'
    }).reset_index()
    category_sales.columns = ['category', 'total_sold']
    category_sales = category_sales.sort_values('total_sold', ascending=False)
    
    top_5 = category_sales.head(5)
    
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    colors = ['#2ecc71', '#27ae60', '#1abc9c', '#16a085', '#3498db']
    ax1.barh(top_5['category'], top_5['total_sold'], color=colors)
    ax1.set_xlabel('Jumlah Terjual')
    ax1.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig1)

# Worst Products
with col2:
    st.markdown("**Bottom 5 Kategori Kurang Laris**")
    
    bottom_5 = category_sales.tail(5)
    
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    colors = ['#e74c3c', '#c0392b', '#e67e22', '#d35400', '#f39c12']
    ax2.barh(bottom_5['category'], bottom_5['total_sold'], color=colors)
    ax2.set_xlabel('Jumlah Terjual')
    ax2.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig2)

st.markdown("---")

# Row 3: Customer Demographics
st.subheader("🗺️ Demografi Pelanggan")

customer_by_state = filtered_df.groupby('customer_state').agg({
    'customer_unique_id': 'nunique'
}).reset_index()
customer_by_state.columns = ['state', 'customer_count']
customer_by_state = customer_by_state.sort_values('customer_count', ascending=False)

fig3, ax3 = plt.subplots(figsize=(12, 4))
colors = plt.cm.Blues([0.9 - (i * 0.06) for i in range(10)])

top_10_states = customer_by_state.head(10)
bars = ax3.bar(top_10_states['state'], top_10_states['customer_count'], color=colors)
ax3.set_xlabel('Negara Bagian')
ax3.set_ylabel('Jumlah Pelanggan')

for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{int(height):,}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
st.pyplot(fig3)

st.markdown("---")

# Row 4: RFM Analysis
st.subheader("👥 Segmentasi Pelanggan (RFM Analysis)")

# Calculate RFM
reference_date = filtered_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

rfm_df = filtered_df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': 'max',
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

rfm_df.columns = ['customer_id', 'last_purchase', 'frequency', 'monetary']
rfm_df['recency'] = (reference_date - rfm_df['last_purchase']).dt.days

# RFM Scoring
rfm_df['r_score'] = pd.qcut(rfm_df['recency'], q=4, labels=[4, 3, 2, 1], duplicates='drop')
rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], q=4, labels=[1, 2, 3, 4], duplicates='drop')

# Segmentation
def rfm_segment(row):
    r = int(row['r_score'])
    f = int(row['f_score'])
    m = int(row['m_score'])
    
    if r >= 3 and f >= 3 and m >= 3:
        return 'Best Customers'
    elif r >= 3 and f >= 2:
        return 'Loyal Customers'
    elif r >= 3:
        return 'Recent Customers'
    elif f >= 3:
        return 'Frequent Customers'
    elif m >= 3:
        return 'Big Spenders'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost Customers'
    else:
        return 'Regular Customers'

rfm_df['segment'] = rfm_df.apply(rfm_segment, axis=1)

segment_colors = {
    'Best Customers': '#2ecc71',
    'Loyal Customers': '#3498db',
    'Recent Customers': '#9b59b6',
    'Frequent Customers': '#f1c40f',
    'Big Spenders': '#e67e22',
    'Regular Customers': '#95a5a6',
    'Lost Customers': '#e74c3c'
}

segment_counts = rfm_df['segment'].value_counts()

fig4, ax4 = plt.subplots(figsize=(12, 4))
colors = [segment_colors.get(seg, '#95a5a6') for seg in segment_counts.index]
bars = ax4.bar(segment_counts.index, segment_counts.values, color=colors)
ax4.set_xlabel('Segment')
ax4.set_ylabel('Jumlah Pelanggan')
ax4.tick_params(axis='x', rotation=45)

for bar in bars:
    height = bar.get_height()
    ax4.annotate(f'{int(height):,}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
st.pyplot(fig4)

# RFM Summary Table
st.markdown("**Statistik RFM per Segment:**")
rfm_summary = rfm_df.groupby('segment').agg({
    'recency': 'mean',
    'frequency': 'mean',
    'monetary': 'mean',
    'customer_id': 'count'
}).reset_index()
rfm_summary.columns = ['Segment', 'Avg Recency (days)', 'Avg Frequency', 'Avg Monetary (R$)', 'Customer Count']
rfm_summary = rfm_summary.round(2)
st.dataframe(rfm_summary, use_container_width=True)

# Footer
st.markdown("---")
st.caption("© 2024 E-Commerce Dashboard | Data: Olist Brazilian E-Commerce Dataset")
