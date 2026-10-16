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
    for met
