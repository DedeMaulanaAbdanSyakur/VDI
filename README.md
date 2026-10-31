# Supermarket Analytics Dashboard

Dashboard analitik interaktif yang dibangun menggunakan Streamlit untuk memvisualisasikan performa cabang supermarket. Proyek ini mengimplementasikan integrasi *multi-DBMS* yang menggabungkan data relasional dan non-relasional ke dalam satu *data pipeline*.

## 🔗 Daftar Tautan Utama
* **Live Web Application:** [https://tugasvdidede.streamlit.app/](https://tugasvdidede.streamlit.app/)
* **Repositori GitHub:** [https://github.com/DedeMaulanaAbdanSyakur/VDI](https://github.com/DedeMaulanaAbdanSyakur/VDI)
* **Sumber Data Asli (Dataset):** [Kaggle - Supermarket Sales](https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales)
* **Referensi Kode/Proyek:** [Streamlit Database Connections](https://docs.streamlit.io/knowledge-base/tutorials/databases)

## 🏗️ Ringkasan Arsitektur & Data Pipeline
1. **DBMS 1 (Relational - PostgreSQL via Supabase):** Berfungsi menyimpan data master yang terstruktur, yaitu informasi cabang (`branch_master`).
2. **DBMS 2 (Document/NoSQL - MongoDB via Atlas):** Berfungsi menyimpan log data transaksi penjualan supermarket (`transactions`).
3. **Alur Integrasi (Data Pipeline):** Aplikasi menggunakan pustaka `psycopg2` dan `pymongo` untuk menarik data dari kedua *engine* basis data tersebut. Data kemudian diubah menjadi *dataframe* Pandas dan digabungkan (*data joining*) di tingkat aplikasi menggunakan metode agregasi Pandas sebelum dirender ke antarmuka web.

## 📊 Fitur Interaktivitas
* **Filter Navigasi:** Pengguna dapat memfilter data berdasarkan Kota dan Cabang menggunakan tombol sakelar (*toggle*) di *sidebar*.
* **KPI Dinamis:** Menampilkan ringkasan metrik secara *real-time* (Total Pendapatan, Rata-rata Rating, dan Total Transaksi) berdasarkan filter yang aktif.
* **Grafik Interaktif:** Visualisasi data berbasis Plotly (grafik batang dan pai) yang mendukung fitur *hover* detail informasi.
