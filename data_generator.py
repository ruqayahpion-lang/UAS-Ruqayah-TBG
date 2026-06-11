import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("⏳ Memulai pembuatan data simulasi tapping kartu mahasiswa...")

# Pengaturan dasar sesuai soal UAS
gedung_list = ['Fakultas Sains dan Teknologi', 'Perpustakaan', 'Auditorium']
waktu_mulai = datetime(2026, 6, 11, 9, 0, 0) # Simulasi dimulai jam 09:00 WITA

data_rows = []

# Mensimulasikan data selama 100 menit
for menit in range(100):
    waktu_sekarang = waktu_mulai + timedelta(minutes=menit)
    
    for gedung in gedung_list:
        # Generate jumlah mahasiswa acak antara 20 - 300 sesuai ketentuan soal
        attendance_count = int(np.random.randint(20, 301))
        
        data_rows.append({
            'timestamp': waktu_sekarang.strftime('%Y-%m-%d %H:%M:%S'),
            'building': gedung,
            'attendance_count': attendance_count
        })

# Simpan ke bentuk CSV sementara untuk dibaca oleh Spark
df = pd.DataFrame(data_rows)
os.makedirs('raw_data', exist_ok=True)
df.to_csv('raw_data/attendance_raw.csv', index=False)

print("✅ Sukses! Berhasil men-generate 300 baris data tapping di 'raw_data/attendance_raw.csv'.")

