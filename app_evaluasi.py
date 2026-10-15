import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Evaluasi Bintang Galaxy", layout="centered")

# --- FUNGSI PEMBUAT PDF DENGAN LOGO, FOTO & PERIODE ---
def buat_pdf(nama, tempat_lahir, tanggal_lahir, usia, posisi, dict_nilai, catatan, rata_rata, predikat, periode_bulan, periode_tahun, path_logo=None, path_foto=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Header / Kop Surat dengan Logo & Periode
    if path_logo and os.path.exists(path_logo):
        pdf.image(path_logo, x=10, y=10, w=25)
        pdf.set_xy(40, 15)
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 8, "BINTANG GALAXY FOOTBALL ACADEMY", ln=True, align='L')
        pdf.set_xy(40, 23)
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 6, f"Rapor Evaluasi Perkembangan Pemain U17 | Periode: {periode_bulan} {periode_tahun}", ln=True, align='L')
        pdf.line(10, 40, 200, 40)
        pdf.ln(15)
    else:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "RAPOR EVALUASI PEMAIN U17", ln=True, align='C')
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "BINTANG GALAXY FOOTBALL ACADEMY", ln=True, align='C')
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 8, f"Periode: {periode_bulan} {periode_tahun}", ln=True, align='C')
        pdf.line(10, 38, 200, 38)
        pdf.ln(10)
    
    y_biodata = pdf.get_y()
    
    # A. Biodata
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "A. Biodata Peserta", ln=True)
    pdf.set_font("Arial", '', 11)
    
    pdf.cell(40, 8, "Nama Lengkap", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.cell(100, 8, nama.upper(), 0, 1)
    
    pdf.cell(40, 8, "TTL", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.cell(100, 8, f"{tempat_lahir}, {tanggal_lahir.strftime('%d %b %Y')}", 0, 1)
    
    pdf.cell(40, 8, "Usia", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.cell(100, 8, f"{usia} Tahun", 0, 1)
    
    pdf.cell(40, 8, "Posisi", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.cell(100, 8, posisi, 0, 1)
    
    # Pasang Foto Pemain
    if path_foto and os.path.exists(path_foto):
        pdf.image(path_foto, x=160, y=y_biodata + 8, w=30)
        
    pdf.ln(5)
    
    # B. Tabel Evaluasi
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"B. Hasil Evaluasi - Bulan {periode_bulan}", ln=True)
    
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(140, 10, " Aspek Penilaian", border=1)
    pdf.cell(50, 10, "Nilai (1-5)", border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 11)
    for metrik, nilai in dict_nilai.items():
        pdf.cell(140, 10, f" {metrik}", border=1)
        pdf.cell(50, 10, str(nilai), border=1, align='C', ln=True)
    
    pdf.ln(5)
    
    # C. Kesimpulan Akhir
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "C. Kesimpulan Akhir", ln=True)
    pdf.set_font("Arial", '', 11)
    
    pdf.cell(40, 8, "Nilai Rata-rata", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"{rata_rata:.2f} / 5.00", 0, 1)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(40, 8, "Predikat", 0, 0)
    pdf.cell(5, 8, ":", 0, 0)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, predikat, 0, 1)
    pdf.ln(5)
    
    # D. Catatan Pelatih
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "D. Catatan Pelatih & Fokus Latihan:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 8, catatan if catatan else "-")
    
    nama_file = "Rapor_Temp.pdf"
    pdf.output(nama_file)
    return nama_file

# --- HEADER APLIKASI ---
st.title("⚽ Rapor Evaluasi Pemain U17")
st.subheader("Bintang Galaxy Football Academy")
st.write("---")

# ==========================================
# 1. BAGIAN BIODATA & UPLOAD FOTO
# ==========================================
st.header("📝 Biodata & Foto Pemain")

col_bio1, col_bio2 = st.columns(2)

with col_bio1:
    nama_pemain = st.text_input("Nama Lengkap", placeholder="Masukkan nama pemain...")
    tempat_lahir = st.text_input("Tempat Lahir", placeholder="Contoh: Makassar")
    tanggal_lahir = st.date_input("Tanggal Lahir", value=date(2009, 1, 1), min_value=date(2000, 1, 1), max_value=date(2015, 12, 31))
    
    st.write("---")
    st.markdown("**🖼️ Pengaturan Cetak PDF**")
    file_logo = st.file_uploader("1. Unggah Logo Akademi (Opsional, untuk Kop Surat)", type=['png', 'jpg', 'jpeg'])

with col_bio2:
    posisi = st.selectbox("Posisi Bermain", ["Penyerang (Forward)", "Gelandang (Midfielder)", "Bertahan (Defender)", "Penjaga Gawang (GK)"])
    hari_ini = date.today()
    usia = hari_ini.year - tanggal_lahir.year - ((hari_ini.month, hari_ini.day) < (tanggal_lahir.month, tanggal_lahir.day))
    st.info(f"**Usia Saat Ini:** {usia} Tahun")
    
    st.write("---")
    st.markdown("**📸 Profil Pemain**")
    file_foto = st.file_uploader("2. Unggah Pas Foto Pemain (Opsional)", type=['png', 'jpg', 'jpeg'])

st.write("---")

# ==========================================
# 2. PANEL PENILAIAN & PERIODE EVALUASI
# ==========================================
st.header("📊 Input Evaluasi (Skala 1-5)")

# Pemilihan Periode Bulan & Tahun
col_periode1, col_periode2 = st.columns(2)
with col_periode1:
    bulan_evaluasi = st.selectbox("Bulan Evaluasi", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], index=9)
with col_periode2:
    tahun_evaluasi = st.selectbox("Tahun Evaluasi", [2025, 2026, 2027, 2028], index=1)

st.write("---")
nilai_baru = {}

st.markdown("### 1. Aspek Teknik (Technical Skills)")
nilai_baru["Passing (Akurasi umpan)"] = st.slider("Passing", 1, 5, 3)
nilai_baru["First Touch (Kontrol bola)"] = st.slider("First Touch", 1, 5, 3)
nilai_baru["Dribbling (Melewati lawan)"] = st.slider("Dribbling", 1, 5, 3)
nilai_baru["Shooting / Finishing"] = st.slider("Shooting / Finishing", 1, 5, 3)
nilai_baru["Heading (Teknik sundulan)"] = st.slider("Heading", 1, 5, 3)

st.markdown("### 2. Aspek Taktik (Tactical Understanding)")
nilai_baru["Pengambilan Keputusan"] = st.slider("Pengambilan Keputusan", 1, 5, 3)
nilai_baru["Kesadaran Ruang"] = st.slider("Kesadaran Ruang", 1, 5, 3)
nilai_baru["Transisi (Positif/Negatif)"] = st.slider("Transisi", 1, 5, 3)

st.markdown("### 3. Aspek Fisik (Physical Condition)")
nilai_baru["Kecepatan (Sprint)"] = st.slider("Kecepatan", 1, 5, 3)
nilai_baru["Stamina (Daya tahan)"] = st.slider("Stamina", 1, 5, 3)
nilai_baru["Kekuatan (Duel bola)"] = st.slider("Kekuatan", 1, 5, 3)
nilai_baru["Agility (Kelincahan)"] = st.slider("Agility", 1, 5, 3)

st.markdown("### 4. Aspek Mental & Sikap (Mental & Attitude)")
nilai_baru["Kedisiplinan"] = st.slider("Kedisiplinan", 1, 5, 3)
nilai_baru["Kerja Keras"] = st.slider("Kerja Keras", 1, 5, 3)
nilai_baru["Komunikasi"] = st.slider("Komunikasi", 1, 5, 3)

st.write("---")
catatan_pelatih = st.text_area("Catatan Pelatih & Fokus Latihan Berikutnya", placeholder="Tuliskan evaluasi kualitatif di sini...")

# ==========================================
# 3. PROSES & GENERATE PDF
# ==========================================
if st.button("Simpan & Lihat Rapor", type="primary"):
    if not nama_pemain:
        st.error("⚠️ Silakan isi Nama Pemain terlebih dahulu di bagian Biodata!")
    else:
        st.write("---")
        st.header(f"📋 Laporan Perkembangan Pemain - {bulan_evaluasi} {tahun_evaluasi}")
        st.success(f"**Data atas nama {nama_pemain.upper()} berhasil diproses.**")
        
        # Kalkulasi Kesimpulan
        total_skor = sum(nilai_baru.values())
        rata_rata = total_skor / len(nilai_baru)
        if rata_rata >= 4.5: predikat = "SANGAT BAIK (Pemain Menonjol)"
        elif rata_rata >= 3.5: predikat = "BAIK (Berkembang Sesuai Ekspektasi)"
        elif rata_rata >= 2.5: predikat = "CUKUP (Butuh Peningkatan Konsisten)"
        else: predikat = "KURANG (Butuh Perhatian Khusus)"
            
        col_kesimpulan1, col_kesimpulan2 = st.columns(2)
        col_kesimpulan1.metric(label="🌟 Nilai Rata-Rata Akhir", value=f"{rata_rata:.2f} / 5.00")
        col_kesimpulan2.metric(label="🎯 Predikat", value=predikat.split(" (")[0], delta=predikat.split("(")[1].replace(")", ""), delta_color="off")
        
        df_rapor = pd.DataFrame([{"Aspek Penilaian": k, "Nilai (1-5)": v} for k, v in nilai_baru.items()])
        st.table(df_rapor)

        path_logo_temp = "temp_logo.jpg" if file_logo else None
        path_foto_temp = "temp_foto.jpg" if file_foto else None
        
        if file_logo:
            with open(path_logo_temp, "wb") as f: f.write(file_logo.getbuffer())
        if file_foto:
            with open(path_foto_temp, "wb") as f: f.write(file_foto.getbuffer())

        # Proses PDF
        file_pdf = buat_pdf(nama_pemain, tempat_lahir, tanggal_lahir, usia, posisi, nilai_baru, catatan_pelatih, rata_rata, predikat, bulan_evaluasi, tahun_evaluasi, path_logo_temp, path_foto_temp)
        
        # Tombol Download PDF
        with open(file_pdf, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            
        st.download_button(
            label=f"📥 Unduh Rapor ({bulan_evaluasi} {tahun_evaluasi}) PDF",
            data=PDFbyte,
            file_name=f"Rapor_{nama_pemain.replace(' ', '_')}_{bulan_evaluasi}_{tahun_evaluasi}.pdf",
            mime="application/pdf",
        )
        
        # Membersihkan file sementara setelah PDF siap
        os.remove(file_pdf)
        if path_logo_temp and os.path.exists(path_logo_temp): os.remove(path_logo_temp)
        if path_foto_temp and os.path.exists(path_foto_temp): os.remove(path_foto_temp)