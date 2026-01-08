# 🚗 Sistem Deteksi Kecelakaan

Aplikasi web untuk mendeteksi kecelakaan lalu lintas menggunakan model YOLO v11n dengan antarmuka interaktif berbasis Streamlit.

## ✨ Fitur Utama

- 🖼️ **Deteksi Gambar**: Upload dan analisis gambar kecelakaan
- 🎥 **Deteksi Video**: Proses video untuk deteksi real-time
- 📸 **Screenshot Otomatis**: Simpan hasil deteksi secara otomatis
- 📜 **History**: Lihat dan kelola semua hasil deteksi yang tersimpan
- ⚙️ **Konfigurasi Fleksibel**: Sesuaikan confidence, IOU threshold, dan ukuran gambar

## 🚀 Instalasi

1. **Clone atau download repository**

   ```bash
   cd "DETEKSI KECELAKAAN"
   ```

2. **Buat virtual environment (opsional)**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Pastikan file model tersedia**
   - File `best.pt` harus ada di direktori root

## 🎯 Cara Menggunakan

1. **Jalankan aplikasi**

   ```bash
   streamlit run app.py
   ```

2. **Buka browser** ke `http://localhost:8501`

3. **Pilih Mode**:

   - **Gambar**: Upload file JPG/PNG untuk deteksi
   - **Video**: Upload file MP4/AVI/MOV untuk deteksi

4. **Atur Konfigurasi** (sidebar):

   - Confidence Level (0.0 - 1.0)
   - Remove Duplicates (IOU threshold)
   - Image Size (320 - 1024)

5. **Lihat History**: Klik tombol "Lihat History Deteksi" untuk melihat semua screenshot tersimpan

## 📂 Struktur File

```
DETEKSI KECELAKAAN/
├── app.py                  # Aplikasi utama
├── best.pt                 # Model YOLO
├── requirements.txt        # Dependencies
├── detection_history/      # Folder screenshot (auto-generated)
└── README.md              # File ini
```

## 🛠️ Teknologi

- **Streamlit**: Framework web app
- **YOLO v11n**: Model deteksi objek
- **OpenCV**: Pemrosesan video/gambar
- **PyTorch**: Deep learning framework

## 📝 Catatan

- Screenshot gambar tersimpan sebagai `img_YYYYMMDD_HHMMSS.jpg`
- Screenshot video tersimpan setiap 30 frame deteksi sebagai `vid_YYYYMMDD_HHMMSS_frameXXX.jpg`
- Semua screenshot disimpan di folder `detection_history/`

---

**Powered by YOLO | Deteksi Kecelakaan Berbasis AI**
