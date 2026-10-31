# Supermarket Analytics Dashboard

Dashboard analitik interaktif yang dibangun menggunakan Streamlit untuk memvisualisasikan performa cabang supermarket. Proyek ini mengimplementasikan integrasi *multi-DBMS* yang menggabungkan data relasional dan non-relasional ke dalam satu *data pipeline*.

🔗 **Live Dashboard:** [https://tugasvdidede.streamlit.app/](https://tugasvdidede.streamlit.app/)

## Arsitektur Data
* **PostgreSQL (Supabase):** Menyimpan data master cabang (`branch_master`).
* **MongoDB (Atlas):** Menyimpan data transaksi supermarket (`transactions`).
* **Visualisasi (Streamlit & Plotly):** Memproses operasi *join* pada *dataframe* Pandas dan merender antarmuka web.

## Fitur Utama
* **KPI Cards:** Menampilkan *Total Revenue*, *Average Rating*, dan *Total Transactions* secara dinamis.
* **Interactive Filters:** Filter berbasis *toggle switch* untuk lokasi Kota dan spesifik Cabang.
* **Visualisasi Data:** Grafik batang (*Revenue by City*) dan grafik pai (*Rating Distribution*).
* **Data Table:** Menampilkan detail data mentah dari transaksi yang telah digabungkan dan difilter.

## Teknologi yang Digunakan
* Python 3
* Streamlit
* Plotly Express
* Pandas
* SQLAlchemy & psycopg2
* PyMongo
