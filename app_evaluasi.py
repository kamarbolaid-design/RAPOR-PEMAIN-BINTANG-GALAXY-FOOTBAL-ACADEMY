import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Rapor Pro - Bintang Galaxy FA", layout="wide")

# ==========================================
# 0. SISTEM KEAMANAN & LOGIN
# ==========================================
USER_DATABASE = {
    "coach": "bintang123",
    "admin": "galaxy2026",
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
    st.title("🔒 Akses Terbatas - Pro Academy Portal")
    st.subheader("Bintang Galaxy Football Academy")
    
    with st.form("form_login"):
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        tombol_login = st.form_submit_button("Masuk / Login", type="primary")
        
        if tombol_login:
            proses_login(username_input, password_input)
            if st.session_state.logged_in:
                st.rerun()

    st.caption("Hubungi Manajemen jika Anda memerlukan kredensial akses.")
    st.stop()

# ==========================================
# DASHBOARD UTAMA (SETELAH LOGIN)
# ==========================================
st.sidebar.markdown(f"**👤 Login sebagai:** {st.session_state.user_fullname}")
if st.sidebar.button("🚪 Logout / Keluar"):
    proses_logout()
    st.rerun()

# --- FUNGSI PEMBUAT PDF PRO DENGAN IDP & ROLE PROFILING ---
def buat_pdf_pro(data_bio, dict_penilaian, idp_data, periode_bulan, periode_tahun, path_logo=None, path_foto=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Header Kop Surat
    if path_logo and os.path.exists(path_logo):
        pdf.image(path_logo, x=10, y=10, w=22)
        pdf.set_xy(35, 12)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 7, "BINTANG GALAXY FOOTBALL ACADEMY", ln=True)
        pdf.set_xy(35, 19)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 5, f"EUROPEAN STANDARDIZED PLAYER REPORT & IDP | Periode: {periode_bulan} {periode_tahun}", ln=True)
        pdf.line(10, 35, 200, 35)
        pdf.ln(10)
    else:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, "BINTANG GALAXY FOOTBALL ACADEMY - PRO PLAYER REPORT", ln=True, align='C')
        pdf.line(10, 25, 200, 25)
        pdf.ln(8)
    
    y_start_bio = pdf.get_y()
    
    # A. PROFIL PEMAIN & ROLE PROFILING
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "A. PROFIL PEMAIN & MODEL MAIN (ROLE & PROFILING)", ln=True)
    pdf.set_font("Arial", '', 9)
    
    pdf.cell(35, 5, "Nama Lengkap", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, data_bio['nama'].upper(), 0, 1)
    
    pdf.cell(35, 5, "TTL / Usia", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, f"{data_bio['ttl']} ({data_bio['usia']} Tahun)", 0, 1)
    
    pdf.cell(35, 5, "Posisi / Role Spesifik", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, f"{data_bio['posisi']} - [{data_bio['role']}]", 0, 1)
    
    pdf.cell(35, 5, "Kaki Dominan", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, data_bio['kaki'], 0, 1)
    
    if path_foto and os.path.exists(path_foto):
        pdf.image(path_foto, x=160, y=y_start_bio + 6, w=28)
        
    pdf.ln(5)
    
    # B. EVALUASI TAKTIK, KOGNITIF & MENTAL MODERN
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "B. EVALUASI TAKTIK, KOGNITIF & MENTAL MODERN (Skala 1-5)", ln=True)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(140, 6, " Aspek Parameter Penilaian", border=1)
    pdf.cell(50, 6, "Nilai (1-5)", border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 9)
    for metrik, nilai in dict_penilaian.items():
        pdf.cell(140, 5.5, f" {metrik}", border=1)
        pdf.cell(50, 5.5, str(nilai), border=1, align='C', ln=True)
        
    pdf.ln(5)
    
    # C. CATATAN TERSTRUKTUR & INDIVIDUAL DEVELOPMENT PLAN (IDP)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "C. INDIVIDUAL DEVELOPMENT PLAN (IDP) & CATATAN PELATIH", ln=True)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "1. Key Strengths (Kelebihan Utama):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 4, idp_data['strengths'] if idp_data['strengths'] else "-")
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "2. Areas for Improvement (Area Prioritas Pengembangan):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 4, idp_data['improvements'] if idp_data['improvements'] else "-")
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "3. Actionable IDP (Rencana Aksi & Latihan Mandiri):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 4, idp_data['action_plan'] if idp_data['action_plan'] else "-")
    
    nama_file = "Rapor_Pro_Temp.pdf"
    pdf.output(nama_file)
    return nama_file

# --- JUDUL APLIKASI ---
st.title("⚽ Rapor Evaluasi Pro - Bintang Galaxy FA")
st.subheader("Standardized European Academy Player Report & IDP")
st.write("---")

# ==========================================
# 1. BIODATA & MODEL MAIN (ROLE & PROFILING)
# ==========================================
st.header("📝 1. Detail Posisi Spesifik & Model Main (Role & Profiling)")

col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    nama_pemain = st.text_input("Nama Lengkap Pemain", placeholder="Contoh: Adnan Putra")
    tempat_lahir = st.text_input("Tempat Lahir", placeholder="Contoh: Bekasi")
    tanggal_lahir = st.date_input("Tanggal Lahir", value=date(2009, 1, 1))

with col_b2:
    posisi_utama = st.selectbox("Kategori Posisi", ["Penyerang (Forward)", "Gelandang (Midfielder)", "Bertahan (Defender)", "Penjaga Gawang (GK)"])
    role_spesifik = st.text_input("Peran Spesifik (Role)", placeholder="Contoh: Ball Playing Defender / Wing-Back / Deep Lying Playmaker")
    kaki_dominan = st.selectbox("Dominasi Kaki (Preferred Foot)", ["Kanan (Right)", "Kiri (Left)", "Kedua Kaki (Both Feet)"])

with col_b3:
    bulan_eval = st.selectbox("Bulan Evaluasi", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], index=9)
    tahun_eval = st.selectbox("Tahun Evaluasi", [2025, 2026, 2027], index=1)

hari_ini = date.today()
usia_pemain = hari_ini.year - tanggal_lahir.year - ((hari_ini.month, hari_ini.day) < (tanggal_lahir.month, tanggal_lahir.day))

col_up1, col_up2 = st.columns(2)
with col_up1:
    file_logo = st.file_uploader("Upload Logo Bintang Galaxy FA (Opsional)", type=['png', 'jpg', 'jpeg'])
with col_up2:
    file_foto = st.file_uploader("Upload Pas Foto Pemain (Opsional)", type=['png', 'jpg', 'jpeg'])

st.write("---")

# ==========================================
# 2. EVALUASI TAKTIK, KOGNITIF & MENTAL MODERN
# ==========================================
st.header("🧠 2. Evaluasi Taktik, Kognitif & Mental Modern (Skala 1-5)")

tab_tak, tab_psik = st.tabs(["🧩 Aspek Taktik & Kognitif Detail", "🔥 Evaluasi Psikologis & Mental Modern"])

dict_penilaian = {}

with tab_tak:
    st.subheader("Aspek Taktik & Kognitif")
    dict_penilaian["Scanning Rate / Orientasi Lapangan (Pengamatan sebelum terima bola)"] = st.slider("Scanning Rate / Orientasi Lapangan", 1, 5, 3)
    dict_penilaian["Body Shape & Body Language (Postur menyambut bola & kepemimpinan)"] = st.slider("Body Shape & Body Language", 1, 5, 3)
    dict_penilaian["1v1 Defending Mechanics (Jockeying, Delaying, Tackle/Interception)"] = st.slider("1v1 Defending Mechanics", 1, 5, 3)
    dict_penilaian["Rest Defense & Defensive Line Control (Kerapatan & koordinasi offside)"] = st.slider("Rest Defense & Defensive Line Control", 1, 5, 3)

with tab_psik:
    st.subheader("Evaluasi Psikologis & Mental Modern")
    dict_penilaian["Resiliensi & Mentalitas Bertanding (Respon saat tertinggal/salah)"] = st.slider("Resiliensi & Mentalitas Bertanding", 1, 5, 3)
    dict_penilaian["Emotional Regulation (Kontrol emosi vs tekanan/wasit)"] = st.slider("Emotional Regulation", 1, 5, 3)
    dict_penilaian["Coachability (Kecepatan merespon instruksi pelatih)"] = st.slider("Coachability", 1, 5, 3)

st.write("---")

# ==========================================
# 3. CATATAN PELATIH TERSTRUKTUR (IDP)
# ==========================================
st.header("🎯 3. Catatan Pelatih Terstruktur (Individual Development Plan)")

key_strengths = st.text_area("Kelebihan Utama (Key Strengths - 2 s/d 3 Poin Utama)", 
                              placeholder="- Kualitas scanning rate tinggi sebelum menerima bola.\n- Postur body shape selalu terbuka saat memulai build-up.")

areas_improvement = st.text_area("Area Prioritas Pengembangan (Areas for Improvement - 2 Poin Mendasar)", 
                                 placeholder="- Timing jockeying saat situasi 1v1 defensive.\n- Pengendalian emosi ketika mendapat tekanan intens dari lawan.")

actionable_idp = st.text_area("Rencana Aksi & Latihan Mandiri (Actionable IDP)", 
                              placeholder="- Drill latihan wall-passing dengan kontrol footwork kaki kiri 2x seminggu.\n- Sesi analisis video posisi 1v1 defending 15 menit sebelum latihan.")

st.write("---")

# ==========================================
# PROSES GENERATE RAPOR PRO
# ==========================================
if st.button("🚀 Generate Rapor Standar Pro (PDF)", type="primary"):
    if not nama_pemain:
        st.error("⚠️ Silakan isi Nama Lengkap Pemain terlebih dahulu di bagian Profil!")
    else:
        st.success(f"✅ Rapor Pro untuk **{nama_pemain.upper()}** berhasil diproses.")
        
        data_bio = {
            'nama': nama_pemain,
            'ttl': f"{tempat_lahir}, {tanggal_lahir.strftime('%d %b %Y')}",
            'usia': usia_pemain,
            'posisi': posisi_utama,
            'role': role_spesifik if role_spesifik else "Standard Role",
            'kaki': kaki_dominan
        }
        
        idp_data = {
            'strengths': key_strengths,
            'improvements': areas_improvement,
            'action_plan': actionable_idp
        }
        
        # Penanganan Upload Foto & Logo (PNG / JPG)
        path_logo_temp = None
        path_foto_temp = None
        
        if file_logo:
            ext_logo = file_logo.name.split(".")[-1]
            path_logo_temp = f"temp_logo.{ext_logo}"
            with open(path_logo_temp, "wb") as f: f.write(file_logo.getbuffer())

        if file_foto:
            ext_foto = file_foto.name.split(".")[-1]
            path_foto_temp = f"temp_foto.{ext_foto}"
            with open(path_foto_temp, "wb") as f: f.write(file_foto.getbuffer())

        # Buat File PDF Pro
        file_pdf_pro = buat_pdf_pro(data_bio, dict_penilaian, idp_data, bulan_eval, tahun_eval, path_logo_temp, path_foto_temp)
        
        with open(file_pdf_pro, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            
        st.download_button(
            label=f"📥 Unduh Rapor Pro ({bulan_eval} {tahun_eval}) PDF",
            data=PDFbyte,
            file_name=f"Rapor_Pro_{nama_pemain.replace(' ', '_')}_{bulan_eval}_{tahun_eval}.pdf",
            mime="application/pdf"
        )
        
        # Membersihkan file sementara
        os.remove(file_pdf_pro)
        if path_logo_temp and os.path.exists(path_logo_temp): os.remove(path_logo_temp)
        if path_foto_temp and os.path.exists(path_foto_temp): os.remove(path_foto_temp)
