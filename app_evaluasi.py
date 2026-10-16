import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Evaluasi Bintang Galaxy", layout="centered")

# ==========================================
# 0. SISTEM KEAMANAN & LOGIN
# ==========================================
USER_DATABASE = {
    "coach": "bintang123",       # Username: coach | Password: bintang123
    "admin": "galaxy2026",       # Username: admin | Password: galaxy2026
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_fullname" not in st.session_state:
    st.session_state.user_fullname = ""

def proses_login(username, password):
    if username in USER_DATABASE and USER_DATABASE[username] == password:
        st.session_state.logged_in = True
        st.session_state.user_fullname = username.upper()
        st.success("✅ Login berhasil!")
    else:
        st.error("❌ Username atau Password salah!")

def proses_logout():
    st.session_state.logged_in = False
    st.session_state.user_fullname = ""

if not st.session_state.logged_in:
    st.title("🔒 Akses Terbatas")
    st.subheader("Bintang Galaxy Football Academy")
    st.write("Silakan login menggunakan akun pelatih untuk mengakses Sistem Evaluasi Rapor.")
    with st.form("form_login"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        tombol_login = st.form_submit_button("Masuk / Login", type="primary")
        if tombol_login:
            proses_login(username_input, password_input)
    if st.session_state.logged_in:
        st.rerun()
    st.caption("Hubungi tim IT / Manajemen jika Anda lupa kata sandi.")
    st.stop()

# Sidebar Logout
st.sidebar.markdown(f"**👤 Login sebagai:** {st.session_state.user_fullname}")
if st.sidebar.button("🚪 Logout / Keluar"):
    proses_logout()
    st.rerun()

# ==========================================
# FUNGSI PEMBUAT PDF DENGAN DETAIL DITAMBAHKAN
# ==========================================
def buat_pdf(nama, tempat_lahir, tanggal_lahir, usia, posisi_kategori, peran_spesifik, kaki_dominan, dict_nilai, kelebihan, area_pengembangan, rencana_aksi, rata_rata, predikat, periode_bulan, periode_tahun, path_logo=None, path_foto=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Header / Kop Surat
    if path_logo and os.path.exists(path_logo):
        pdf.image(path_logo, x=10, y=10, w=25)
        pdf.set_xy(40, 15)
        pdf.set_font("Arial", 'B', 18)
        pdf.cell(0, 8, "BINTANG GALAXY FOOTBALL ACADEMY", ln=True, align='L')
        pdf.set_xy(40, 23)
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 6, f"Rapor Evaluasi Perkembangan Pemain  | Periode: {periode_bulan} {periode_tahun}", ln=True, align='L')
        pdf.line(10, 40, 200, 40)
        pdf.ln(15)
    else:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "RAPOR EVALUASI PEMAIN", ln=True, align='C')
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "BINTANG GALAXY FOOTBALL ACADEMY", ln=True, align='C')
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 8, f"Periode: {periode_bulan} {periode_tahun}", ln=True, align='C')
        pdf.line(10, 38, 200, 38)
        pdf.ln(10)
        
    y_biodata = pdf.get_y()
    
    # A. Biodata Peserta
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "A. Biodata & Profil Pemain", ln=True)
    pdf.set_font("Arial", '', 10)
    
    pdf.cell(40, 6, "Nama Lengkap", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.cell(100, 6, nama.upper(), 0, 1)
    
    pdf.cell(40, 6, "TTL / Usia", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.cell(100, 6, f"{tempat_lahir}, {tanggal_lahir.strftime('%d %b %Y')} ({usia} Tahun)", 0, 1)
    
    pdf.cell(40, 6, "Kategori Posisi", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.cell(100, 6, posisi_kategori, 0, 1)

    pdf.cell(40, 6, "Peran Spesifik (Role)", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.cell(100, 6, peran_spesifik if peran_spesifik else "-", 0, 1)

    pdf.cell(40, 6, "Kaki Dominan", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.cell(100, 6, kaki_dominan, 0, 1)

    if path_foto and os.path.exists(path_foto):
        pdf.image(path_foto, x=160, y=y_biodata + 8, w=30)
    
    pdf.ln(4)
    
    # B. Hasil Evaluasi
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"B. Hasil Evaluasi - Bulan {periode_bulan}", ln=True)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(140, 7, " Aspek Penilaian", border=1)
    pdf.cell(50, 7, "Nilai (1-5)", border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 9)
    for metrik, nilai in dict_nilai.items():
        pdf.cell(140, 5, f" {metrik}", border=1)
        pdf.cell(50, 5, str(nilai), border=1, align='C', ln=True)
    pdf.ln(4)
    
    # C. Kesimpulan Akhir
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "C. Kesimpulan Akhir", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(40, 6, "Nilai Rata-rata", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, f"{rata_rata:.2f} / 5.00", 0, 1)
    
    pdf.set_font("Arial", '', 10)
    pdf.cell(40, 6, "Predikat", 0, 0)
    pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, predikat, 0, 1)
    pdf.ln(4)
    
    # D. Catatan Pelatih Terstruktur
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "D. Catatan Pelatih & Development Plan", ln=True)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, "1. Kelebihan Utama (Key Strengths):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 5, kelebihan if kelebihan else "-")
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, "2. Area Prioritas Pengembangan (Areas for Improvement):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 5, area_pengembangan if area_pengembangan else "-")
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, "3. Rencana Aksi & Latihan Mandiri (Actionable IDP):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 5, rencana_aksi if rencana_aksi else "-")

    nama_file = "Rapor_Temp.pdf"
    pdf.output(nama_file)
    return nama_file

# ==========================================
# TAMPILAN UTAMA APLIKASI
# ==========================================
st.title("⚽ Rapor Evaluasi Pemain ")
st.subheader("Bintang Galaxy Football Academy")
st.write("---")

# 1. BIODATA & PROFILING PEMAIN
st.header("📝 Biodata & Profiling Pemain")
col_bio1, col_bio2 = st.columns(2)

with col_bio1:
    nama_pemain = st.text_input("Nama Lengkap", placeholder="Masukkan nama pemain...")
    tempat_lahir = st.text_input("Tempat Lahir", placeholder="Contoh: Makassar")
    tanggal_lahir = st.date_input("Tanggal Lahir", value=date(2009, 1, 1), min_value=date(2000, 1, 1), max_value=date(2015, 12, 31))
    posisi_kategori = st.selectbox("Kategori Posisi", ["Penyerang (Forward)", "Gelandang (Midfielder)", "Bertahan (Defender)", "Penjaga Gawang (GK)"])
    
with col_bio2:
    peran_spesifik = st.text_input("Peran Spesifik (Role)", placeholder="Contoh: Central Back - Ball Playing Defender / Wing-back")
    kaki_dominan = st.selectbox("Dominasi Kaki (Preferred Foot)", ["Kanan", "Kiri", "Kedua Kaki (Ambidextrous)"])
    
    hari_ini = date.today()
    usia = hari_ini.year - tanggal_lahir.year - ((hari_ini.month, hari_ini.day) < (tanggal_lahir.month, tanggal_lahir.day))
    st.info(f"**Usia Saat Ini:** {usia} Tahun")

st.write("---")
col_img1, col_img2 = st.columns(2)
with col_img1:
    file_logo = st.file_uploader("Unggah Logo Akademi (Opsional)", type=['png', 'jpg', 'jpeg'])
with col_img2:
    file_foto = st.file_uploader("Unggah Pas Foto Pemain (Opsional)", type=['png', 'jpg', 'jpeg'])

st.write("---")

# 2. INPUT EVALUASI (PENILAIAN)
st.header("📊 Input Evaluasi (Skala 1-5)")
col_periode1, col_periode2 = st.columns(2)
with col_periode1:
    bulan_evaluasi = st.selectbox("Bulan Evaluasi", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], index=9)
with col_periode2:
    tahun_evaluasi = st.selectbox("Tahun Evaluasi", [2025, 2026, 2027, 2028], index=1)

st.write("---")
nilai_baru = {}

# 1. Physical Attributes
st.markdown("### 1. Physical Attributes")
nilai_baru["Physical - Speed"] = st.slider("Speed", 1, 5, 3)
nilai_baru["Physical - Strength"] = st.slider("Strength", 1, 5, 3)
nilai_baru["Physical - Quickness"] = st.slider("Quickness", 1, 5, 3)
nilai_baru["Physical - Endurance"] = st.slider("Endurance", 1, 5, 3)
nilai_baru["Physical - Work Rate"] = st.slider("Work Rate", 1, 5, 3)

# 2. Technical Attributes
st.markdown("### 2. Technical Attributes")
nilai_baru["Technical - Juggling"] = st.slider("Juggling", 1, 5, 3)
nilai_baru["Technical - Control / First Touch"] = st.slider("Control / First Touch", 1, 5, 3)
nilai_baru["Technical - Passing"] = st.slider("Passing", 1, 5, 3)
nilai_baru["Technical - Dribbling"] = st.slider("Dribbling", 1, 5, 3)
nilai_baru["Technical - Shooting / Finishing"] = st.slider("Shooting / Finishing", 1, 5, 3)
nilai_baru["Technical - Long Ball / Direct Ball"] = st.slider("Long Ball / Direct Ball", 1, 5, 3)
nilai_baru["Technical - Heading"] = st.slider("Heading", 1, 5, 3)
nilai_baru["Technical - Shielding"] = st.slider("Shielding", 1, 5, 3)
nilai_baru["Technical - Tackling"] = st.slider("Tackling", 1, 5, 3)
nilai_baru["Technical - Play Under Pressure"] = st.slider("Play Under Pressure", 1, 5, 3)
nilai_baru["Technical - Speed of Play"] = st.slider("Speed of Play", 1, 5, 3)

# 3. Tactical Attributes
st.markdown("### 3. Tactical Attributes")
nilai_baru["Tactical - 1 v 1 Attacking"] = st.slider("1 v 1 Attacking", 1, 5, 3)
nilai_baru["Tactical - 1 v 1 Defending"] = st.slider("1 v 1 Defending", 1, 5, 3)
nilai_baru["Tactical - Group Attacking"] = st.slider("Group Attacking", 1, 5, 3)
nilai_baru["Tactical - Group Defending"] = st.slider("Group Defending", 1, 5, 3)
nilai_baru["Tactical - Movement off Ball"] = st.slider("Movement off Ball", 1, 5, 3)
nilai_baru["Tactical - Creativity"] = st.slider("Creativity", 1, 5, 3)
nilai_baru["Tactical - Game Awareness"] = st.slider("Game Awareness", 1, 5, 3)
nilai_baru["Tactical - Communication"] = st.slider("Communication", 1, 5, 3)

# 4. Psychological Attributes
st.markdown("### 4. Psychological Attributes")
nilai_baru["Psychological - Attitude"] = st.slider("Attitude", 1, 5, 3)
nilai_baru["Psychological - Teamwork"] = st.slider("Teamwork", 1, 5, 3)
nilai_baru["Psychological - Concentration / Commitment"] = st.slider("Concentration / Commitment", 1, 5, 3)
nilai_baru["Psychological - Anticipation"] = st.slider("Anticipation", 1, 5, 3)
nilai_baru["Psychological - Sportsmanship"] = st.slider("Sportsmanship", 1, 5, 3)
nilai_baru["Psychological - Confidence"] = st.slider("Confidence", 1, 5, 3)
nilai_baru["Psychological - Attendance"] = st.slider("Attendance", 1, 5, 3)

st.write("---")

# 3. CATATAN PELATIH TERSTRUKTUR
st.header("📝 Catatan Pelatih Terstruktur (IDP)")
kelebihan = st.text_area("1. Kelebihan Utama (Key Strengths)", placeholder="Sebutkan 2-3 poin aspek unggulan pemain yang wajib dipertahankan...")
area_pengembangan = st.text_area("2. Area Prioritas Pengembangan (Areas for Improvement)", placeholder="Sebutkan 2 poin kelemahan mendasar yang perlu diperbaiki...")
rencana_aksi = st.text_area("3. Rencana Aksi & Latihan Mandiri (Actionable IDP)", placeholder="Program drill latihan spesifik untuk bulan berikutnya (misal: latihan dribbling di ruang sempit 2x seminggu)...")

# 4. PROSES & GENERATE PDF
if st.button("Simpan & Lihat Rapor", type="primary"):
    if not nama_pemain:
        st.error("⚠️ Silakan isi Nama Pemain terlebih dahulu di bagian Biodata!")
    else:
        st.write("---")
        st.header(f"📋 Laporan Perkembangan Pemain - {bulan_evaluasi} {tahun_evaluasi}")
        st.success(f"**Data atas nama {nama_pemain.upper()} berhasil diproses.**")
        
        total_skor = sum(nilai_baru.values())
        rata_rata = total_skor / len(nilai_baru)
        
        if rata_rata >= 4.5:
            predikat = "SANGAT BAIK (Pemain Menonjol)"
        elif rata_rata >= 3.5:
            predikat = "BAIK (Berkembang Sesuai Ekspektasi)"
        elif rata_rata >= 2.5:
            predikat = "CUKUP (Butuh Peningkatan Konsisten)"
        else:
            predikat = "KURANG (Butuh Perhatian Khusus)"

        col_kesimpulan1, col_kesimpulan2 = st.columns(2)
        col_kesimpulan1.metric(label="🌟 Nilai Rata-Rata Akhir", value=f"{rata_rata:.2f} / 5.00")
        col_kesimpulan2.metric(label="🎯 Predikat", value=predikat.split(" (")[0], delta=predikat.split("(")[1].replace(")", ""), delta_color="off")

        df_rapor = pd.DataFrame([{"Aspek Penilaian": k, "Nilai (1-5)": v} for k, v in nilai_baru.items()])
        st.table(df_rapor)

        # Penanganan Upload Logo & Foto
        if file_logo:
            ext_logo = file_logo.name.split(".")[-1]
            path_logo_temp = f"temp_logo.{ext_logo}"
            with open(path_logo_temp, "wb") as f:
                f.write(file_logo.getbuffer())
        else:
            path_logo_temp = None

        if file_foto:
            ext_foto = file_foto.name.split(".")[-1]
            path_foto_temp = f"temp_foto.{ext_foto}"
            with open(path_foto_temp, "wb") as f:
                f.write(file_foto.getbuffer())
        else:
            path_foto_temp = None

        # Generate PDF File
        file_pdf = buat_pdf(
            nama_pemain, tempat_lahir, tanggal_lahir, usia, posisi_kategori, 
            peran_spesifik, kaki_dominan, nilai_baru, kelebihan, area_pengembangan, 
            rencana_aksi, rata_rata, predikat, bulan_evaluasi, tahun_evaluasi, 
            path_logo_temp, path_foto_temp
        )

        with open(file_pdf, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            st.download_button(
                label=f"📥 Unduh Rapor ({bulan_evaluasi} {tahun_evaluasi}) PDF",
                data=PDFbyte,
                file_name=f"Rapor_{nama_pemain.replace(' ', '_')}_{bulan_evaluasi}_{tahun_evaluasi}.pdf",
                mime="application/pdf",
            )

        # Cleanup Temporary Files
        os.remove(file_pdf)
        if path_logo_temp and os.path.exists(path_logo_temp):
            os.remove(path_logo_temp)
        if path_foto_temp and os.path.exists(path_foto_temp):
            os.remove(path_foto_temp)
