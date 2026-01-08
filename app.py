import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
from PIL import Image
import os
from datetime import datetime
import glob

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Deteksi Kecelakaan",
    page_icon="🚗",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.stButton>button {
    width: 100%;
    background-color: #FF4B4B;
    color: white;
    border-radius: 8px;
    padding: 0.5rem;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #FF6B6B;
}
h1 {
    color: #FF4B4B;
    text-align: center;
    padding-bottom: 1rem;
    border-bottom: 3px solid #FF4B4B;
    margin-bottom: 2rem;
}
.upload-text {
    text-align: center;
    color: #666;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚗 Sistem Deteksi Kecelakaan")
st.markdown("""
<div style='text-align: center; color: #666; margin-bottom: 2rem;'>
    Deteksi kecelakaan lalu lintas menggunakan model YOLO V12n
</div>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# =========================
# SETUP FOLDER UNTUK SCREENSHOT
# =========================
SCREENSHOT_FOLDER = "detection_history"
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

# =========================
# SIDEBAR - KONFIGURASI MODEL
# =========================
with st.sidebar:
    # Mode Selection di Sidebar
    st.markdown("## 📂 Select Mode")
    mode = st.radio(
        "",
        ["🖼️ Gambar", "🎥 Video"],
        horizontal=False
    )
    
    st.markdown("---")
    
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    # Confidence Threshold
    st.markdown("### 🎯 Confidence Level")
    confidence = st.slider(
        "Seberapa yakin deteksi?",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.05,
        help="Nilai tinggi = lebih yakin, tapi bisa melewatkan objek"
    )
    
    # IOU Threshold
    st.markdown("### 📐 Remove Duplicates")
    iou_threshold = st.slider(
        "Hindari deteksi ganda",
        min_value=0.0,
        max_value=1.0,
        value=0.45,
        step=0.05,
        help="Nilai tinggi = lebih banyak box ditampilkan"
    )
    
    # Image Size
    st.markdown("### 📏 Image Size")
    img_size = st.select_slider(
        "Resolusi pemrosesan",
        options=[320, 416, 512, 640, 768, 896, 1024],
        value=640,
        help="Besar = lebih detail tapi lambat | Kecil = cepat tapi kurang akurat"
    )
    
    st.markdown("---")
    
    # History Section di paling bawah
    st.markdown("## 📜 History")
    if st.button("📜 Lihat History Deteksi", use_container_width=True):
        st.session_state.show_history = True
    
    # Info jumlah screenshot
    screenshots = glob.glob(os.path.join(SCREENSHOT_FOLDER, "*.jpg"))
    st.caption(f"Total tersimpan: {len(screenshots)} gambar")

# Inisialisasi session state untuk history
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# ==================================================
# TAMPILAN HISTORY (jika tombol diklik)
# ==================================================
if st.session_state.show_history:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 📜 History Deteksi")
    with col2:
        if st.button("✖️ Tutup History", use_container_width=True):
            st.session_state.show_history = False
            st.rerun()
    
    st.markdown("---")
    
    # Ambil semua file screenshot
    screenshots = sorted(glob.glob(os.path.join(SCREENSHOT_FOLDER, "*.jpg")), reverse=True)
    
    if len(screenshots) > 0:
        st.info(f"Total screenshot tersimpan: **{len(screenshots)}** gambar")
        
        # Tombol hapus semua
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Hapus Semua History", use_container_width=True):
                for img_path in screenshots:
                    os.remove(img_path)
                st.success("✅ Semua history telah dihapus!")
                st.rerun()
        
        st.markdown("---")
        
        # Tampilkan dalam grid 3 kolom
        cols = st.columns(3)
        for idx, img_path in enumerate(screenshots):
            with cols[idx % 3]:
                img = Image.open(img_path)
                filename = os.path.basename(img_path)
                
                # Ekstrak info dari filename
                if filename.startswith("img_"):
                    source_type = "🖼️ Gambar"
                elif filename.startswith("vid_"):
                    source_type = "🎥 Video"
                else:
                    source_type = "📷"
                
                # Parse timestamp dari filename
                try:
                    time_str = filename.split("_")[1]
                    formatted_time = f"{time_str[0:4]}-{time_str[4:6]}-{time_str[6:8]} {time_str[9:11]}:{time_str[11:13]}:{time_str[13:15]}"
                except:
                    formatted_time = "Unknown"
                
                st.image(img, caption=f"{source_type}\n{formatted_time}", use_container_width=True)
                
                # Tombol hapus individual
                if st.button(f"🗑️ Hapus", key=f"del_{idx}", use_container_width=True):
                    os.remove(img_path)
                    st.rerun()
    else:
        st.warning("📭 Belum ada history deteksi. Silakan lakukan deteksi terlebih dahulu.")

# ==================================================
# MODE DETEKSI (Gambar atau Video)
# ==================================================
else:
    st.markdown("---")

    # ==================================================
    # MODE GAMBAR
    # ==================================================
    if "Gambar" in mode:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📤 Upload Gambar")
            uploaded_img = st.file_uploader(
                "Pilih gambar (JPG, PNG, JPEG)",
                type=["jpg", "jpeg", "png"]
            )

        with col2:
            st.markdown("#### 📊 Hasil Deteksi")

            if uploaded_img:
                with st.spinner("🔍 Menganalisis gambar..."):
                    image = Image.open(uploaded_img)
                    results = model(
                        image,
                        conf=confidence,
                        iou=iou_threshold,
                        imgsz=img_size
                    )

                    annotated = results[0].plot()
                    st.image(
                        annotated,
                        caption="Hasil Deteksi",
                        width=600
                    )

                    jumlah_objek = len(results[0].boxes)
                    
                    # Simpan screenshot jika ada deteksi
                    if jumlah_objek > 0:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"img_{timestamp}.jpg")
                        cv2.imwrite(screenshot_path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
                        st.success(f"✅ Deteksi selesai — {jumlah_objek} objek terdeteksi | 📸 Screenshot tersimpan!")
                    else:
                        st.success(f"✅ Deteksi selesai — {jumlah_objek} objek terdeteksi")

                    # Detail deteksi
                    if jumlah_objek > 0:
                        st.markdown("##### 🔎 Detail Deteksi")
                        for box in results[0].boxes:
                            cls_id = int(box.cls[0])
                            conf = float(box.conf[0])
                            st.write(
                                f"- **{model.names[cls_id]}** | Confidence: `{conf:.2f}`"
                            )
            else:
                st.info("👈 Silakan upload gambar untuk memulai")

    # ==================================================
    # MODE VIDEO
    # ==================================================
    if "Video" in mode:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📤 Upload Video")
            uploaded_vid = st.file_uploader(
                "Pilih video (MP4, AVI, MOV)",
                type=["mp4", "avi", "mov"]
            )

        with col2:
            st.markdown("#### 🎞️ Hasil Deteksi")

            if uploaded_vid:
                with st.spinner("🔍 Memproses video..."):
                    tfile = tempfile.NamedTemporaryFile(delete=False)
                    tfile.write(uploaded_vid.read())

                    cap = cv2.VideoCapture(tfile.name)
                    stframe = st.empty()

                    frame_count = 0
                    accident_frame = 0
                    saved_screenshots = 0

                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break

                        frame_count += 1

                        # Inference dengan konfigurasi yang dipilih
                        results = model(
                            frame,
                            stream=True,
                            conf=confidence,
                            iou=iou_threshold,
                            imgsz=img_size
                        )

                        for r in results:
                            if len(r.boxes) > 0:
                                accident_frame += 1
                                
                                # Simpan screenshot setiap 30 frame yang terdeteksi (untuk menghindari terlalu banyak)
                                if accident_frame % 30 == 0:
                                    annotated = r.plot()
                                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                    screenshot_path = os.path.join(SCREENSHOT_FOLDER, f"vid_{timestamp}_frame{frame_count}.jpg")
                                    cv2.imwrite(screenshot_path, annotated)
                                    saved_screenshots += 1
                            
                            annotated = r.plot()
                            stframe.image(
                                annotated,
                                channels="BGR",
                                width=900
                            )

                    cap.release()

                    st.success(
                        f"✅ Video selesai diproses\n\n"
                        f"• Total Frame: **{frame_count}**\n"
                        f"• Frame terdeteksi objek: **{accident_frame}**\n"
                        f"• Screenshot tersimpan: **{saved_screenshots}** 📸"
                    )
            else:
                st.info("👈 Silakan upload video untuk memulai")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #999; padding: 1rem;'>
    <small>Powered by YOLO | Deteksi Kecelakaan</small>
</div>
""", unsafe_allow_html=True)
