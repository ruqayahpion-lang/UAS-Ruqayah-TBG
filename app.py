import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import os

# Konfigurasi halaman utama dashboard
st.set_page_config(page_title="Smart Campus Attendance Analytics", layout="wide")
st.title("🏫 Smart Campus Attendance Analytics Dashboard")
st.markdown("---")

# Papan Informasi Profil Pengembang di Sidebar (Sesuai Standar UIN)
st.sidebar.header("👤 Profil Mahasiswa")
st.sidebar.info("**Nama:** Ruqayah\n\n**Kelas:** TI23A\n\n**Project:** UAS Teknologi Big Data")

# Jalur data Parquet dan Model AI
path_total = "output/attendance_total"
path_time = "output/attendance_time"
path_model = "model/linear_reg_model.pkl"

# Cek ketersediaan file data sebelum dimuat
if not (os.path.exists(path_total) and os.path.exists(path_time) and os.path.exists(path_model)):
    st.error("❌ Data output Parquet atau Model AI tidak ditemukan!")
    st.info("💡 Pastikan Anda telah menjalankan Tahap 1 (`spark-submit spark_analytics.py`) dan Tahap 2 (`python3 train_model.py`) terlebih dahulu.")
    st.stop()

# 1. Membaca Data Parquet menggunakan Pandas
df_total = pd.read_parquet(path_total)
df_time = pd.read_parquet(path_time)

# 2. Sidebar Filter Pilihan Gedung (Wajib sesuai soal)
st.sidebar.header("🎯 Filter Navigasi")
gedung_pilihan = st.sidebar.selectbox(
    "Pilih Gedung Kampus:",
    options=df_time['building'].unique()
)

# Memfilter data tren kehadiran berdasarkan gedung yang dipilih user
df_time_filtered = df_time[df_time['building'] == list(df_total['building'].unique())[0]] # Default fallback secure data
df_time_real_filter = df_time[df_time['building'] == gedung_pilihan]

# 3. Menampilkan KPI Total Mahasiswa (Wajib sesuai soal)
st.subheader("📊 Key Performance Indicator (KPI)")
col1, col2 = st.columns(2)

with col1:
    # Mengambil total keseluruhan mahasiswa di gedung yang dipilih
    total_mhs_gedung = df_total[df_total['building'] == gedung_pilihan]['total_attendance'].values[0]
    st.metric(label=f"Total Akumulasi Kehadiran di {gedung_pilihan}", value=f"{total_mhs_gedung:,} Mahasiswa")

with col2:
    # KPI Pembanding: Rata-rata per jendela tapping
    avg_mhs_gedung = int(df_time_real_filter['attendance_per_20min'].mean())
    st.metric(label="Rata-rata Kepadatan per 20 Menit", value=f"{avg_mhs_gedung} Mahasiswa")

st.markdown("---")

# 4. Grafik Tren Kehadiran Interaktif menggunakan Plotly (Wajib sesuai soal)
st.subheader(f"📈 Tren Kehadiran Mahasiswa per 20 Menit ({gedung_pilihan})")
fig_trend = px.line(
    df_time_real_filter, 
    x='start_time', 
    y='attendance_per_20min',
    labels={'start_time': 'Waktu Operasional', 'attendance_per_20min': 'Jumlah Mahasiswa (Tapping)'},
    markers=True,
    template="plotly_dark"
)
fig_trend.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")

# 5. Integrasi Prediksi Kepadatan Kampus dengan AI Linear Regression (Wajib sesuai soal)
st.subheader("🤖 AI Real-Time Density Prediction (Linear Regression)")

# Memuat model AI yang sudah dilatih pada Tahap 2
with open(path_model, 'rb') as file:
    model_ai = pickle.load(file)

st.write("Gunakan slider di bawah ini untuk memprediksi jam sibuk kepadatan kampus berdasarkan kecerdasan buatan Model Linear Regression:")

# Input interaktif untuk jam kuliah
input_jam = st.slider("Atur Jam Perkuliahan Kampus (Format 24 Jam):", min_value=0, max_value=23, value=10)

# Melakukan prediksi menggunakan model AI Scikit-Learn
prediksi_hasil = model_ai.predict([[input_jam]])[0]
prediksi_bersih = max(0, int(prediksi_hasil)) # Menghindari nilai prediksi minus yang tidak logis

# Menampilkan hasil prediksi ke User Interface
col_pred1, col_pred2 = st.columns([1, 2])
with col_pred1:
    st.markdown(f"### ⏱️ Jam Ditargetkan: **{input_jam:02d}:00**")
    st.metric(label="Prediksi Jumlah Kehadiran", value=f"± {prediksi_bersih} Mahasiswa")

with col_pred2:
    # Analisis Jam Sibuk Kampus otomatis (Sesuai output soal yang diminta)
    st.markdown("### 📋 Analisis Jam Sibuk & Rekomendasi:")
    if prediksi_bersih > 200:
        st.error(f"🚨 **STATUS JAM SIBUK EKSTREM!** Jam {input_jam:02d}:00 diprediksi akan menjadi puncak kepadatan mahasiswa. Disarankan untuk membagi jadwal kelas kuliah tatap muka atau menambah kapasitas sirkulasi udara gedung.")
    elif prediksi_bersih >= 100:
        st.warning(f"⚠️ **STATUS KEPADATAN SEDANG.** Jam {input_jam:02d}:00 area gedung terpantau cukup ramai namun sirkulasi masuknya arus mahasiswa masih dalam batas normal.")
    else:
        st.success(f"✅ **STATUS KAMPUS LENGANG.** Jam {input_jam:02d}:00 diprediksi sebagai waktu terbaik untuk melakukan kunjungan atau belajar mandiri di perpustakaan karena minim kerumunan.")
