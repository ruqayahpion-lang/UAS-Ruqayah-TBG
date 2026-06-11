import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
import os

print("🤖 Memulai Inisialisasi Model Machine Learning...")

# 1. Membaca data Parquet hasil olahan Spark menggunakan Pandas
path_ml_data = "output/ml_attendance"

if not os.path.exists(path_ml_data):
    print("❌ Error: Folder 'output/ml_attendance' tidak ditemukan!")
    print("💡 Pastikan Anda sudah menjalankan 'spark-submit spark_analytics.py' di Tahap 1.")
    exit()

# Pandas dapat membaca folder parquet secara langsung
df = pd.read_parquet(path_ml_data)
print("📋 Berhasil memuat dataset training dari Parquet.")

# 2. Menyiapkan Fitur (X) dan Target (y) sesuai soal
# Prediksi: attendance_count berdasarkan hour
X = df[['hour']]            # Fitur (Variabel Independen)
y = df['attendance_count']  # Target (Variabel Dependen)

print(f"📊 Menghitung regresi untuk {len(df)} baris data...")

# 3. Inisialisasi dan Pelatihan Model Linear Regression
model = LinearRegression()
model.fit(X, y)

print("✅ Model AI Linear Regression berhasil dilatih!")
print(f"📈 Formula Linear: Korelasi Kemiringan (Slope) = {model.coef_[0]:.4f}, Intersep = {model.intercept_:.4f}")

# 4. Menyimpan Model AI ke dalam file (.pkl) agar bisa dipakai di Dashboard Streamlit
os.makedirs('model', exist_ok=True)
model_filename = 'model/linear_reg_model.pkl'

with open(model_filename, 'wb') as file:
    pickle.dump(model, file)

print(f"💾 Sukses! Model AI disimpan dengan aman di folder: '{model_filename}'")
