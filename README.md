# JobCompass - Market Insights Dashboard

JobCompass adalah sebuah dashboard interaktif yang dibangun menggunakan **Streamlit** dan **Plotly** untuk melakukan analisis komprehensif terkait tren lowongan kerja, peta kompensasi (gaji), dan kebutuhan keterampilan (skills) di industri saat ini.

## 📌 Fitur Utama

Dashboard ini membagi analisis ke dalam 4 bagian (Tab) utama:

1. **📊 Permintaan Pasar**: Menganalisis kategori pekerjaan apa yang paling banyak dicari oleh pasar. Dilengkapi dengan visualisasi distribusi jumlah lowongan per kategori.
2. **💰 Analisis Kompensasi (USD)**: Menampilkan sebaran dan disparitas tawaran kompensasi keuangan antar kategori pekerjaan, mencakup nilai rata-rata (Bar Chart) dan sebaran variasi/rentang gaji (Box Plot).
3. **🔑 Keterampilan Krusial (Key Skills)**: Mengekstrak dan menganalisis 10 keterampilan paling krusial yang dicari perusahaan berdasarkan data deskripsi pekerjaan dan keahlian teknis.
4. **🔍 Eksplorasi Master Data**: Tabel interaktif yang memungkinkan pengguna untuk mencari dan memfilter raw data spesifik berdasarkan _Job Title_ (Kata Kunci Jabatan).

## 📂 Struktur Direktori

```text
data_science/
│
├── dashboard/
│   └── app.py                  # Script utama aplikasi Streamlit
│
├── data/
│   ├── raw/
│   │   └── indian-job-market-dataset-2025.xlsx # Dataset mentah awal
│   └── processed/
│       ├── dataset_clean.csv   # Dataset bersih yang digunakan untuk dashboard
│       └── dataset_final.csv   # Dataset final yang disiapkan khusus untuk pemodelan AI
│
├── notebooks/
│   └── jobcompass.ipynb        # Jupyter Notebook untuk eksplorasi data, pembersihan data, dan analisis
│
├── venv/                       # Virtual Environment Python
│
├── requirements.txt            # Daftar library dan dependensi proyek
└── README.md                   # Dokumentasi proyek (file ini)
```

## 🛠️ Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Web Framework (Dashboard)**: [Streamlit](https://streamlit.io/)
- **Data Manipulasi & Analisis**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualisasi Data**: [Plotly Express](https://plotly.com/python/plotly-express/) (Dashboard), [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (Notebook)
- **Kaggle API**: `kagglehub` (Untuk ekstraksi data langsung)
- **Utility / Built-in**: `collections`, `re`, `os`

## 🚀 Cara Instalasi & Menjalankan Aplikasi

1. **Clone repositori ini** (atau pastikan Anda berada di root folder `data_science`).
2. **Buat Virtual Environment**:
   Karena folder `venv` tidak ikut dipublish ke _repository_, Anda perlu membuatnya terlebih dahulu:
   ```bash
   python -m venv venv
   ```
3. **Aktifkan Virtual Environment**:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. **Instal dependensi** dari `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
5. **Siapkan Dataset Bersih**:
   Sebelum menjalankan dashboard, Anda harus menjalankan Jupyter Notebook `notebooks/jobcompass.ipynb` terlebih dahulu guna mendapatkan dataset yang bersih.
6. **Jalankan Dashboard Streamlit**:
   Masuk ke direktori `dashboard` lalu eksekusi perintah streamlit:
   ```bash
   cd dashboard
   streamlit run app.py
   ```
7. Buka browser dan akses alamat lokal yang diberikan (biasanya `http://localhost:8501`).

## 📊 Kebutuhan Data

Dashboard ini menggunakan `dataset_clean.csv` yang berada di direktori `data/processed/`.
Pastikan file data tersebut tersedia sebelum menjalankan aplikasi. Dataset tersebut memuat kolom penting seperti:

- `category` (Kategori Pekerjaan)
- `avg_sal_dollar` (Rata-rata Gaji dalam USD)
- `key_skills`, `description`, `clean_desc`, atau `job_title` (Untuk ekstraksi kemampuan)

Selain itu, terdapat `dataset_final.csv` di direktori yang sama, yang merupakan data hasil pemrosesan akhir yang dikhususkan untuk **Pelatihan Model AI**.

Adapun data mentah aslinya (`data/raw/indian-job-market-dataset-2025.xlsx`) didapatkan bersumber dari Kaggle: [Indian Job Market Dataset 2025-2026](https://www.kaggle.com/datasets/shivamshrivastava21/indian-job-market-dataset-2025-2026).

---
