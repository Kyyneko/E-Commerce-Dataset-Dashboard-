# E-Commerce Data Analysis Dashboard

Dashboard analisis data E-Commerce menggunakan dataset Olist Brazil.

## Cara Menjalankan Dashboard

### Setup Environment

1. Buat virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka di browser pada `http://localhost:8501`

## Struktur Proyek

```
submission/
├── dashboard/
│   ├── main_data.csv      # Data untuk dashboard
│   └── dashboard.py       # Streamlit dashboard
├── data/
│   └── *.csv              # Dataset original
├── notebook.ipynb         # Jupyter Notebook analisis
├── README.md              # Dokumentasi
├── requirements.txt       # Dependencies
└── url.txt                # Link deploy (opsional)
```

## Pertanyaan Bisnis

1. Bagaimana performa penjualan dan revenue dalam beberapa bulan terakhir?
2. Produk apa yang paling banyak dan paling sedikit terjual?
3. Bagaimana demografi pelanggan berdasarkan lokasi?
4. Bagaimana segmentasi pelanggan berdasarkan analisis RFM?

## Fitur Dashboard

- 📊 **Metrics**: Total Orders, Revenue, Avg Order Value, Total Customers
- 📈 **Sales Trend**: Visualisasi trend penjualan bulanan
- 🏆 **Product Categories**: Top 5 dan Bottom 5 kategori produk
- 🗺️ **Demographics**: Distribusi pelanggan per negara bagian
- 👥 **RFM Analysis**: Segmentasi pelanggan berdasarkan Recency, Frequency, Monetary
