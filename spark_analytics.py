from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, to_timestamp, window, hour
import shutil
import os

print("🚀 Memulai Spark Analytics Engine...")

# Inisialisasi Spark Session
spark = SparkSession.builder \
    .appName("SmartCampusAttendanceAnalytics") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# 1. Membaca data mentah dari hasil generator
df_raw = spark.read.csv("raw_data/attendance_raw.csv", header=True, inferSchema=True)
df_raw = df_raw.withColumn("timestamp", to_timestamp(col("timestamp")))

print("📋 Data mentah berhasil dimuat ke Spark DataFrame. Memulai transformasi...")

# --- TRANSFORMASI 1: Total mahasiswa per gedung ---
df_total = df_raw.groupBy("building") \
    .agg(sum("attendance_count").alias("total_attendance"))

# --- TRANSFORMASI 2: Tren kehadiran per 20 menit ---
df_time = df_raw.groupBy(
    window(col("timestamp"), "20 minutes").alias("waktu_jendela"),
    col("building")
).agg(sum("attendance_count").alias("attendance_per_20min")) \
 .select(
     col("waktu_jendela.start").cast("string").alias("start_time"),
     col("waktu_jendela.end").cast("string").alias("end_time"),
     col("building"),
     col("attendance_per_20min")
 ).orderBy("start_time", "building")

# --- TRANSFORMASI 3: Dataset AI berbasis jam ---
df_ml = df_raw.withColumn("hour", hour(col("timestamp"))) \
    .select("building", "hour", "attendance_count")

# --- PENYIMPANAN FORMAT PARQUET ---
print("💾 Menyimpan hasil analisis ke format Parquet...")

# Fungsi pembersih folder agar tidak error bertabrakan saat dijalankan ulang
def save_clean_parquet(df, path):
    if os.path.exists(path):
        shutil.rmtree(path)
    df.write.mode("overwrite").parquet(path)

save_clean_parquet(df_total, "output/attendance_total")
save_clean_parquet(df_time, "output/attendance_time")
save_clean_parquet(df_ml, "output/ml_attendance")

print("✅ SEMUA PROSES SPARK SELESAI!")
print("📂 Folder Parquet yang berhasil dibuat:")
print("   -> output/attendance_total")
print("   -> output/attendance_time")
print("   -> output/ml_attendance")

spark.stop()
