## Smart Campus Attendance Analytics

## 🏛️ Arsitektur & Pipeline Sistem
Sistem ini dirancang menggunakan arsitektur modern berkinerja tinggi dengan alur kerja (*pipeline*) sebagai berikut:
1. **Data Generation:** Simulasi deret waktu (*time-series*) aktivitas *tapping* kartu mahasiswa selama 100 menit dengan interval acak (20–300 mahasiswa per entri) pada 3 lokasi target.
2. **Spark Analytics (PySpark):** Mesin pemrosesan terdistribusi yang melakukan agregasi, transformasi jendela (*windowing*), dan penyiapan fitur AI menggunakan DataFrame API.
3. **Parquet Storage:** Penyimpanan berbasis kolom (*columnar storage*) berkinerja tinggi yang diwajibkan menggunakan **Absolute Path** sistem operasi.
4. **AI Prediction:** Pemodelan prediktif cerdas berbasis waktu menggunakan algoritma **Linear Regression** dari pustaka *Scikit-Learn*.
5. **Interactive Dashboard:** Visualisasi data berbasis web menggunakan **Streamlit** dan grafik interaktif **Plotly** untuk memproyeksikan kepadatan kampus secara dinamis.


---

## 🛠️ Komponen Teknologi & Framework
* **Bahasa Pemrograman:** Python 3
* **Environment:** Linux Server / WSL (Windows Subsystem for Linux)
* **Data Processing:** Apache Spark (PySpark DataFrame API)
* **Penyimpanan Utama:** Apache Parquet Format *(Zero CSV Output untuk data matang)*
* **Kecerdasan Buatan (AI):** Scikit-Learn (Linear Regression Model)
* **Penyimpanan Model AI:** Pickle Serialization (`.pkl`)
* **Visualisasi & Dashboard:** Streamlit & Plotly Express

---

## 📂 Struktur Direktori Proyek (Absolute Path)
Seluruh komponen kode diwajibkan berjalan pada jalur absolut (*Absolute Path*) sistem lokal: `/home/qeyy/UAS_Ruqayah_TBG/`


/home/qeyy/UAS_Ruqayah_TBG/
├── .gitignore            
├── data_generator.py     
├── spark_analytics.py     
├── train_model.py         
├── app.py                 
├── raw_data/             
│   └── attendance_raw.csv
├── model/               
│   └── linear_reg_model.pkl
└── output/               
    ├── attendance_total/  
    ├── attendance_time/   
    └── ml_attendance/     


## 📸  Tampilan Dashboard Utama Streamlit & Grafik Plotly
Tampilan Dashboard Utama Streamlit & Grafik Plotly

Antarmuka web interaktif yang menampilkan penyesuaian filter gedung di bagian sidebar dan visualisasi grafik tren garis dinamis dari data Parquet.
<img width="1517" height="502" alt="Cuplikan layar 2026-06-11 101428" src="https://github.com/user-attachments/assets/9cf45fee-0b6a-44f2-a2a2-c81427f19878" />
<img width="1499" height="727" alt="Cuplikan layar 2026-06-11 101420" src="https://github.com/user-attachments/assets/56855d2a-ad51-4d82-998e-d192ea272758" />
<img width="1517" height="502" alt="Cuplikan layar 2026-06-11 101428" src="https://github.com/user-attachments/assets/5aaf072e-53cf-4fcd-b3cf-f78d5fa7e800" />

---

* [x] **Spark Berhasil Dijalankan:** Menggunakan SparkSession lokal terdistribusi.
* [x] **File Parquet Berhasil Dibuat:** Penyimpanan murni berbasis folder Parquet terkompresi.
* [x] **Dashboard Streamlit Berjalan:** Berhasil di-host lokal pada port `8501`.
* [x] **Grafik Plotly Tampil:** Menggunakan visualisasi interaktif berkualitas tinggi (*Line Chart*).
* [x] **Prediksi AI Berjalan:** Implementasi fungsi Scikit-Learn matematika garis lurus secara presisi.
* [x] **Filter Sidebar Berfungsi:** Dropdown navigasi gedung langsung merubah data visual secara real-time.
* [x] **Wajib Menggunakan Absolute Path:** Seluruh skrip menggunakan alamat mutlak `/home/qeyy/UAS_Ruqayah_TBG/`.
"""

# 🖥️ Smart Campus Attendance Analytics - Big Data Pipeline

Proyek ini merupakan implementasi **End-to-End Big Data Pipeline** yang dibangun untuk memenuhi tugas **Ujian Akhir Semester (UAS) Genap 20252** pada mata kuliah **Teknologi Big Data (PTI23048)**. Sistem ini mensimulasikan, memproses, menganalisis, dan memprediksi tingkat kepadatan mahasiswa di berbagai gedung kampus berdasarkan data *tapping* kartu identitas secara *real-time*.

---

## 👤 Profil Mahasiswa
* **Nama:** Ruqayah
* **Kelas:** TI23A
* **Program Studi:** Teknologi Informasi
* **Dosen Pengampu:** Muhayat, M.IT
* **Instansi:** Universitas Islam Negeri (UIN)
