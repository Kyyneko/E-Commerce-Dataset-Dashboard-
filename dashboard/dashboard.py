import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Headers */
    h1 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-align: center;
    }
    
    h2, h3 {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stMetric"] label {
        color: #a0a0a0 !important;
        font-size: 14px !important;
    }
    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    
    /* Info box styling */
    .info-box {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .chart-description {
        background: rgba(255, 255, 255, 0.05);
        border-left: 3px solid #00d4ff;
        padding: 12px 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        color: #b0b0b0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: #00d4ff; margin: 0;'>E-Commerce</h2>
        <p style='color: #888; font-size: 14px;'>Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("<p style='color: #00d4ff; font-weight: 600;'>Filter Tanggal</p>", unsafe_allow_html=True)
    min_date = df['order_purchase_timestamp'].min().date()
    max_date = df['order_purchase_timestamp'].max().date()
    
    start_date = st.date_input("Dari", min_date, min_value=min_date, max_value=max_date)
    end_date = st.date_input("Sampai", max_date, min_value=min_date, max_value=max_date)
    
    st.markdown("---")
    
    st.markdown("<p style='color: #00d4ff; font-weight: 600;'>Dataset Info</p>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: rgba(0,212,255,0.1); padding: 15px; border-radius: 10px; border-left: 3px solid #00d4ff;'>
        <p style='margin: 0; color: #ccc; font-size: 13px;'>Total Records</p>
        <p style='margin: 0; color: #fff; font-size: 20px; font-weight: 600;'>{len(df):,}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Keterangan Singkatan
    st.markdown("<p style='color: #00d4ff; font-weight: 600;'>Keterangan Singkatan</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; font-size: 12px;'>
        <p style='margin: 0 0 8px 0; color: #ccc;'><strong style='color: #10b981;'>R$</strong> = Real Brasil (Mata Uang Brazil)</p>
        <p style='margin: 0 0 8px 0; color: #ccc;'><strong style='color: #f59e0b;'>RFM</strong> = Recency, Frequency, Monetary</p>
        <p style='margin: 0 0 8px 0; color: #ccc;'><strong style='color: #8b5cf6;'>Avg</strong> = Average (Rata-rata)</p>
        <p style='margin: 0; color: #ccc;'><strong style='color: #3b82f6;'>SP, RJ, MG</strong> = Kode Negara Bagian Brazil</p>
    </div>
    """, unsafe_allow_html=True)

# Filter data
filtered_df = df[
    (df['order_purchase_timestamp'].dt.date >= start_date) &
    (df['order_purchase_timestamp'].dt.date <= end_date)
]

# Header
st.markdown("""
<div style='text-align: center; padding: 20px 0 40px 0;'>
    <h1 style='font-size: 42px; background: linear-gradient(90deg, #00d4ff, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px;'>E-Commerce Dashboard</h1>
    <p style='color: #888; font-size: 16px;'>Analisis Data Penjualan Olist Brazil</p>
</div>
""", unsafe_allow_html=True)

# Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_orders = filtered_df['order_id'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    total_revenue = filtered_df['price'].sum()
    st.metric("Total Revenue", f"R$ {total_revenue:,.0f}")

with col3:
    avg_order_value = filtered_df.groupby('order_id')['price'].sum().mean()
    st.metric("Avg Order Value", f"R$ {avg_order_value:,.0f}")

with col4:
    total_customers = filtered_df['customer_unique_id'].nunique()
    st.metric("Total Customers", f"{total_customers:,}")

st.markdown("<br>", unsafe_allow_html=True)

# Chart styling function
def style_chart(fig, ax, title):
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#1a1a2e')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#444')
    ax.spines['left'].set_color('#444')
    ax.tick_params(colors='#aaa')
    ax.xaxis.label.set_color('#aaa')
    ax.yaxis.label.set_color('#aaa')
    ax.set_title(title, color='white', fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.15, color='white', linestyle='--')

# ============================================
# Row 1: Monthly Orders Trend
# ============================================
st.markdown("### Trend Penjualan Bulanan")

monthly_orders = filtered_df.groupby(
    filtered_df['order_purchase_timestamp'].dt.to_period('M')
).agg({
    'order_id': 'nunique',
    'price': 'sum'
}).reset_index()

monthly_orders.columns = ['month', 'total_orders', 'total_revenue']
monthly_orders['month'] = monthly_orders['month'].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
style_chart(fig, ax, '')

# Gradient effect with fill
ax.fill_between(range(len(monthly_orders)), monthly_orders['total_orders'], alpha=0.3, color='#00d4ff')
ax.plot(
    range(len(monthly_orders)),
    monthly_orders['total_orders'],
    marker='o',
    linewidth=3,
    color='#00d4ff',
    markersize=8,
    markerfacecolor='#1a1a2e',
    markeredgewidth=2,
    markeredgecolor='#00d4ff'
)

ax.set_xticks(range(len(monthly_orders)))
ax.set_xticklabels(monthly_orders['month'], rotation=45, ha='right')
ax.set_xlabel('Bulan', fontsize=11)
ax.set_ylabel('Jumlah Order', fontsize=11)

plt.tight_layout()
st.pyplot(fig)

# Penjelasan Chart 1
st.markdown("""
<div class='chart-description'>
    <strong>Penjelasan:</strong> Grafik ini menunjukkan perkembangan jumlah pesanan (order) per bulan. 
    Sumbu X menampilkan periode bulan, sedangkan sumbu Y menunjukkan total order unik. 
    Tren naik mengindikasikan pertumbuhan bisnis, sedangkan tren turun perlu dianalisis lebih lanjut.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# Row 2: Best and Worst Products
# ============================================
st.markdown("### Performa Kategori Produk")

col1, col2 = st.columns(2)

category_sales = filtered_df.groupby('product_category_name_english').agg({
    'order_id': 'count'
}).reset_index()
category_sales.columns = ['category', 'total_sold']
category_sales = category_sales.sort_values('total_sold', ascending=False)

# Best Products
with col1:
    st.markdown("<p style='color: #10b981; font-weight: 600; text-align: center;'>Top 5 Terlaris</p>", unsafe_allow_html=True)
    
    top_5 = category_sales.head(5)
    
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    style_chart(fig1, ax1, '')
    
    colors = ['#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5']
    bars = ax1.barh(top_5['category'], top_5['total_sold'], color=colors, height=0.6)
    
    for bar in bars:
        width = bar.get_width()
        ax1.annotate(f'{int(width):,}',
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontweight='bold', fontsize=10, color='white')
    
    ax1.set_xlabel('Jumlah Terjual', fontsize=11)
    ax1.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig1)

# Worst Products
with col2:
    st.markdown("<p style='color: #ef4444; font-weight: 600; text-align: center;'>Bottom 5 Kurang Laris</p>", unsafe_allow_html=True)
    
    bottom_5 = category_sales.tail(5)
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    style_chart(fig2, ax2, '')
    
    colors = ['#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626']
    bars = ax2.barh(bottom_5['category'], bottom_5['total_sold'], color=colors, height=0.6)
    
    for bar in bars:
        width = bar.get_width()
        ax2.annotate(f'{int(width):,}',
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha='left', va='center', fontweight='bold', fontsize=10, color='white')
    
    ax2.set_xlabel('Jumlah Terjual', fontsize=11)
    ax2.invert_yaxis()
    plt.tight_layout()
    st.pyplot(fig2)

# Penjelasan Chart 2
st.markdown("""
<div class='chart-description'>
    <strong>Penjelasan:</strong> Perbandingan kategori produk berdasarkan jumlah penjualan.
    <strong style='color: #10b981;'>Top 5</strong> menampilkan kategori dengan penjualan tertinggi yang menjadi andalan bisnis.
    <strong style='color: #ef4444;'>Bottom 5</strong> menampilkan kategori dengan penjualan terendah yang perlu strategi pemasaran khusus atau evaluasi stok.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# Row 3: Customer Demographics
# ============================================
st.markdown("### Demografi Pelanggan per Negara Bagian")

customer_by_state = filtered_df.groupby('customer_state').agg({
    'customer_unique_id': 'nunique'
}).reset_index()
customer_by_state.columns = ['state', 'customer_count']
customer_by_state = customer_by_state.sort_values('customer_count', ascending=False)

fig3, ax3 = plt.subplots(figsize=(14, 5))
style_chart(fig3, ax3, '')

top_10_states = customer_by_state.head(10)

# Create gradient colors
colors = plt.cm.plasma(np.linspace(0.2, 0.8, 10))

bars = ax3.bar(top_10_states['state'], top_10_states['customer_count'], color=colors, width=0.7)
ax3.set_xlabel('Negara Bagian', fontsize=11)
ax3.set_ylabel('Jumlah Pelanggan', fontsize=11)

for bar in bars:
    height = bar.get_height()
    ax3.annotate(f'{int(height):,}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')

plt.tight_layout()
st.pyplot(fig3)

# Penjelasan Chart 3
st.markdown("""
<div class='chart-description'>
    <strong>Penjelasan:</strong> Distribusi pelanggan berdasarkan negara bagian di Brazil. 
    Kode negara bagian menggunakan singkatan resmi Brazil: <strong>SP</strong> = São Paulo, <strong>RJ</strong> = Rio de Janeiro, 
    <strong>MG</strong> = Minas Gerais, <strong>RS</strong> = Rio Grande do Sul, <strong>PR</strong> = Paraná, dll.
    Data ini berguna untuk menentukan strategi distribusi dan pemasaran regional.
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# Row 4: RFM Analysis
# ============================================
st.markdown("### Segmentasi Pelanggan (RFM Analysis)")

# Penjelasan RFM di atas chart
st.markdown("""
<div class='chart-description'>
    <strong>Apa itu RFM?</strong> RFM adalah metode segmentasi pelanggan berdasarkan 3 metrik:<br>
    • <strong style='color: #00d4ff;'>Recency (R)</strong> - Seberapa baru pelanggan melakukan pembelian terakhir<br>
    • <strong style='color: #00d4ff;'>Frequency (F)</strong> - Seberapa sering pelanggan melakukan pembelian<br>
    • <strong style='color: #00d4ff;'>Monetary (M)</strong> - Berapa total uang yang dibelanjakan pelanggan
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

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
    'Best Customers': '#10b981',
    'Loyal Customers': '#3b82f6',
    'Recent Customers': '#8b5cf6',
    'Frequent Customers': '#f59e0b',
    'Big Spenders': '#f97316',
    'Regular Customers': '#6b7280',
    'Lost Customers': '#ef4444'
}

segment_counts = rfm_df['segment'].value_counts()

with col1:
    fig4, ax4 = plt.subplots(figsize=(10, 5))
    style_chart(fig4, ax4, '')
    
    colors = [segment_colors.get(seg, '#6b7280') for seg in segment_counts.index]
    bars = ax4.bar(segment_counts.index, segment_counts.values, color=colors, width=0.7)
    ax4.set_xlabel('Segment', fontsize=11)
    ax4.set_ylabel('Jumlah Pelanggan', fontsize=11)
    ax4.tick_params(axis='x', rotation=30)
    
    for bar in bars:
        height = bar.get_height()
        ax4.annotate(f'{int(height):,}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')
    
    plt.tight_layout()
    st.pyplot(fig4)

with col2:
    st.markdown("<p style='color: #00d4ff; font-weight: 600;'>Ringkasan Segment</p>", unsafe_allow_html=True)
    
    for segment in segment_counts.index[:5]:
        count = segment_counts[segment]
        percentage = (count / segment_counts.sum()) * 100
        color = segment_colors.get(segment, '#6b7280')
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.05); padding: 12px 15px; border-radius: 10px; margin-bottom: 8px; border-left: 4px solid {color};'>
            <p style='margin: 0; color: #aaa; font-size: 12px;'>{segment}</p>
            <p style='margin: 0; color: white; font-size: 18px; font-weight: 600;'>{count:,} <span style='color: #888; font-size: 12px;'>({percentage:.1f}%)</span></p>
        </div>
        """, unsafe_allow_html=True)

# Penjelasan Segment
st.markdown("""
<div class='chart-description'>
    <strong>Penjelasan Segment:</strong><br>
    • <strong style='color: #10b981;'>Best Customers</strong> - Pelanggan terbaik: baru belanja, sering, dan banyak belanja<br>
    • <strong style='color: #3b82f6;'>Loyal Customers</strong> - Pelanggan setia: aktif dan cukup sering belanja<br>
    • <strong style='color: #8b5cf6;'>Recent Customers</strong> - Pelanggan baru: baru saja melakukan pembelian<br>
    • <strong style='color: #f59e0b;'>Frequent Customers</strong> - Pelanggan yang sering belanja tapi sudah lama tidak aktif<br>
    • <strong style='color: #f97316;'>Big Spenders</strong> - Pelanggan dengan nilai belanja tinggi<br>
    • <strong style='color: #6b7280;'>Regular Customers</strong> - Pelanggan biasa dengan aktivitas standar<br>
    • <strong style='color: #ef4444;'>Lost Customers</strong> - Pelanggan yang sudah lama tidak aktif (perlu re-engagement)
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p style='margin: 0; font-size: 14px;'>E-Commerce Dashboard | Olist Brazilian E-Commerce Dataset</p>
    <p style='margin: 5px 0 0 0; font-size: 12px;'>Created with Streamlit</p>
</div>
""", unsafe_allow_html=True)
