import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF
import os

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Evaluasi Pro - Bintang Galaxy FA", layout="wide")

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

# --- FUNGSI PEMBUAT PDF PRO ACADEMY ---
def buat_pdf_pro(data_bio, data_fisik_obj, dict_nilai, data_match, idp_data, periode_bulan, periode_tahun, path_logo=None, path_foto=None):
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
        pdf.cell(0, 5, f"PLAYER DEVELOPMENT REPORT & IDP | Periode: {periode_bulan} {periode_tahun}", ln=True)
        pdf.line(10, 35, 200, 35)
        pdf.ln(10)
    else:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, "BINTANG GALAXY FOOTBALL ACADEMY - PRO PLAYER REPORT", ln=True, align='C')
        pdf.line(10, 25, 200, 25)
        pdf.ln(8)
    
    y_start_bio = pdf.get_y()
    
    # A. BIODATA & BIOMETRIK
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "A. PROFIL PEMAIN & BIOMETRIK", ln=True)
    pdf.set_font("Arial", '', 9)
    
    pdf.cell(32, 5, "Nama Lengkap", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, data_bio['nama'].upper(), 0, 1)
    
    pdf.cell(32, 5, "TTL / Usia", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, f"{data_bio['ttl']} ({data_bio['usia']} Thn)", 0, 1)
    
    pdf.cell(32, 5, "Posisi / Role", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, f"{data_bio['posisi']} - [{data_bio['role']}]", 0, 1)
    
    pdf.cell(32, 5, "Kaki Dominan", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, data_bio['kaki'], 0, 1)
    
    pdf.cell(32, 5, "TB / BB / PHV", 0, 0)
    pdf.cell(3, 5, ":", 0, 0)
    pdf.cell(80, 5, f"{data_bio['tb']} cm / {data_bio['bb']} kg / Status: {data_bio['phv']}", 0, 1)
    
    if path_foto and os.path.exists(path_foto):
        pdf.image(path_foto, x=160, y=y_start_bio + 6, w=28)
        
    pdf.ln(4)
    
    # B. DATA FISIK KUANTITATIF (TES OBJEKTIF)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "B. TES FISIK OBJEKTIF (QUANTITATIVE METRICS)", ln=True)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(62, 6, " Parameter Tes", border=1)
    pdf.cell(40, 6, "Hasil Tes", border=1, align='C')
    pdf.cell(88, 6, "Standar Kategori / Acuan", border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 9)
    for k, v in data_fisik_obj.items():
        pdf.cell(62, 6, f" {k}", border=1)
        pdf.cell(40, 6, str(v['hasil']), border=1, align='C')
        pdf.cell(88, 6, str(v['target']), border=1, align='C', ln=True)
        
    pdf.ln(4)
    
    # C. EVALUASI TEKNIK, TAKTIK/KOGNITIF, MENTAL
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "C. EVALUASI KUALITATIF & TAKTIK KOGNITIF (Skala 1-5)", ln=True)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(140, 6, " Aspek Penilaian", border=1)
    pdf.cell(50, 6, "Nilai", border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 9)
    for metrik, nilai in dict_nilai.items():
        pdf.cell(140, 5, f" {metrik}", border=1)
        pdf.cell(50, 5, str(nilai), border=1, align='C', ln=True)
        
    pdf.ln(4)
    
    # D. STATISTIK PERTANDINGAN & VIDEO ANALYSIS
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "D. ANALISIS PERTANDINGAN & METRIKS STATISTIK", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.cell(60, 5, f"Akurasi Passing: {data_match['pass_acc']}%", 0, 0)
    pdf.cell(60, 5, f"Aerial Duels Won: {data_match['aerial']}%", 0, 0)
    pdf.cell(70, 5, f"Interceptions / Game: {data_match['intercept']}", 0, 1)
    if data_match['video_link']:
        pdf.cell(0, 5, f"Link Video Match Highlight: {data_match['video_link']}", 0, 1)
    pdf.ln(4)
    
    # E. INDIVIDUAL DEVELOPMENT PLAN (IDP)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 6, "E. INDIVIDUAL DEVELOPMENT PLAN (IDP)", ln=True)
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "1. Key Strengths (Kelebihan Utama):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 4, idp_data['strengths'] if idp_data['strengths'] else "-")
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "2. Priority Areas for Improvement (Area Pengembangan):", ln=True)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 4, idp_data['improvements'] if idp_data['improvements'] else "-")
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(0, 5, "3. Actionable IDP (Rencana Latihan Mandiri):", ln=True)
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
# 1. BIODATA, ROLE & BIOMETRIK
# ==========================================
st.header("📝 1. Profil Pemain & Biometrik")
col_b1, col_b2, col_b3 = st.columns(3)

with col_b1:
    nama_pemain = st.text_input("Nama Lengkap Pemain", placeholder="Contoh: Adnan Putra")
    tempat_lahir = st.text_input("Tempat Lahir", placeholder="Contoh: Bekasi")
    tanggal_lahir = st.date_input("Tanggal Lahir", value=date(2009, 1, 1))

with col_b2:
    posisi_utama = st.selectbox("Posisi Utama", ["Forward", "Midfielder", "Defender", "Goalkeeper"])
    role_spesifik = st.text_input("Role Spesifik (Model Main)", placeholder="Contoh: Ball Playing Defender / Box-to-Box")
    kaki_dominan = st.selectbox("Kaki Dominan", ["Kanan (Right)", "Kiri (Left)", "Kedua Kaki (Both)"])

with col_b3:
    tinggi_badan = st.number_input("Tinggi Badan (cm)", value=168)
    berat_badan = st.number_input("Berat Badan (kg)", value=58)
    status_phv = st.selectbox("Status PHV (Maturitas Biologis)", ["Pre-PHV (Belum Spurt)", "Mid-PHV (Fase Tumbuh Pesat)", "Post-PHV (Matang)"])

hari_ini = date.today()
usia_pemain = hari_ini.year - tanggal_lahir.year - ((hari_ini.month, hari_ini.day) < (tanggal_lahir.month, tanggal_lahir.day))

col_up1, col_up2 = st.columns(2)
with col_up1:
    file_logo = st.file_uploader("Upload Logo Akademi (Opsional)", type=['png', 'jpg', 'jpeg'])
with col_up2:
    file_foto = st.file_uploader("Upload Pas Foto Pemain (Opsional)", type=['png', 'jpg', 'jpeg'])

st.write("---")

# ==========================================
# 2. DATA FISIK KUANTITATIF (TES OBJEKTIF)
# ==========================================
st.header("🏃 2. Data Tes Fisik Kuantitatif (Objektif)")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    sprint_10m = st.text_input("Sprint 10m Test (Detik)", value="1.85s")
    sprint_30m = st.text_input("Sprint 30m Test (Detik)", value="4.30s")
with col_f2:
    yoyo_test = st.text_input("Yo-Yo IR1 / Bleep Test", value="Level 16.2 (VO2Max ~48)")
    illinois_test = st.text_input("Illinois Agility Test (Detik)", value="15.80s")
with col_f3:
    vertical_jump = st.text_input("Vertical Jump (cm)", value="48 cm")

st.write("---")

# ==========================================
# 3. PENILAIAN TEKNIK, TAKTIK KOGNITIF & MENTAL
# ==========================================
st.header("📊 3. Evaluasi Taktik, Kognitif & Mental (Skala 1-5)")

tab_tek, tab_tak, tab_men = st.tabs(["⚽ Teknik & Skill", "🧠 Taktik & Kognitif Modern", "🔥 Mental & Psikologis"])

dict_penilaian = {}

with tab_tek:
    dict_penilaian["Passing (Akurasi Umpan Pendek/Panjang)"] = st.slider("Passing", 1, 5, 3)
    dict_penilaian["First Touch (Under Pressure)"] = st.slider("First Touch", 1, 5, 3)
    dict_penilaian["Dribbling & Ball Control"] = st.slider("Dribbling", 1, 5, 3)
    dict_penilaian["Shooting & Finishing"] = st.slider("Shooting", 1, 5, 3)

with tab_tak:
    dict_penilaian["Scanning Rate (Orientasi Lapangan Sebelum Menerima Bola)"] = st.slider("Scanning Rate", 1, 5, 3)
    dict_penilaian["Body Shape & Orientation (Postur Menyambut Bola)"] = st.slider("Body Shape", 1, 5, 3)
    dict_penilaian["1v1 Defending Mechanics (Jockeying, Delaying, Tackle)"] = st.slider("1v1 Defending", 1, 5, 3)
    dict_penilaian["Rest Defense & Kerapatan Line Pertahanan"] = st.slider("Rest Defense", 1, 5, 3)
    dict_penilaian["Decision Making (Passing vs Dribbling)"] = st.slider("Decision Making", 1, 5, 3)

with tab_men:
    dict_penilaian["Resiliensi (Respon Pasca Kesalahan / Tertinggal)"] = st.slider("Resiliensi", 1, 5, 3)
    dict_penilaian["Emotional Regulation (Kontrol Emosi vs Tekanan/Wasit)"] = st.slider("Emotional Regulation", 1, 5, 3)
    dict_penilaian["Coachability (Kecepatan Memahami Instruksi)"] = st.slider("Coachability", 1, 5, 3)
    dict_penilaian["Work Rate & Daya Juang"] = st.slider("Work Rate", 1, 5, 3)

st.write("---")

# ==========================================
# 4. STATISTIK MATCH & VIDEO ANALYSIS
# ==========================================
st.header("📹 4. Statistik Pertandingan & Video Analysis")
col_m1, col_m2 = st.columns(2)

with col_m1:
    pass_accuracy = st.number_input("Akurasi Passing Match (%)", value=78)
    aerial_won = st.number_input("Aerial Duels Won (%)", value=65)
    interceptions_game = st.number_input("Interceptions Per Game", value=4)

with col_m2:
    video_url = st.text_input("Link Video Highlight Performance (YouTube/Veo/Drive)", placeholder="https://...")
    bulan_eval = st.selectbox("Bulan Evaluasi", ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], index=9)
    tahun_eval = st.selectbox("Tahun Evaluasi", [2025, 2026, 2027], index=1)

st.write("---")

# ==========================================
# 5. INDIVIDUAL DEVELOPMENT PLAN (IDP)
# ==========================================
st.header("🎯 5. Individual Development Plan (IDP)")

key_strengths = st.text_area("Kelebihan Utama (Key Strengths - 2 s/d 3 Poin Utama)", placeholder="- Kemampuan scanning sebelum menerima bola sangat baik.\n- Akurasi umpan lambung diagonal presisi.")
areas_improvement = st.text_area("Area Prioritas Pengembangan (Areas for Improvement)", placeholder="- Footwork dan timing saat duel udara perlu ditingkatkan.\n- Penggunaan kaki kiri dalam situasi under pressure.")
actionable_idp = st.text_area("Rencana Aksi Latihan Mandiri (Actionable IDP)", placeholder="- Wall passing khusus kaki kiri 15 menit pasca latihan (2x seminggu).\n- Latihan plyometric untuk meningkatkan daya ledak melompat.")

st.write("---")

# ==========================================
# PROSES GENERATE RAPOR PRO
# ==========================================
if st.button("🚀 Generate Rapor Standar Pro (PDF)", type="primary"):
    if not nama_pemain:
        st.error("⚠️ Silakan isi Nama Lengkap Pemain terlebih dahulu!")
    else:
        st.success(f"✅ Rapor Pro untuk **{nama_pemain.upper()}** berhasil diproses.")
        
        # Penyiapan Struktur Data
        data_bio = {
            'nama': nama_pemain,
            'ttl': f"{tempat_lahir}, {tanggal_lahir.strftime('%d %b %Y')}",
            'usia': usia_pemain,
            'posisi': posisi_utama,
            'role': role_spesifik if role_spesifik else "Standard Role",
            'kaki': kaki_dominan,
            'tb': tinggi_badan,
            'bb': berat_badan,
            'phv': status_phv
        }
        
        data_fisik_obj = {
            'Sprint 10m Test': {'hasil': sprint_10m, 'target': '< 1.90s (Sangat Baik)'},
            'Sprint 30m Test': {'hasil': sprint_30m, 'target': '< 4.40s (Sangat Baik)'},
            'Yo-Yo IR1 / VO2Max': {'hasil': yoyo_test, 'target': 'Standar U17 Academy Pro'},
            'Illinois Agility Test': {'hasil': illinois_test, 'target': '< 16.0s (Kelincahan Tinggi)'},
            'Vertical Jump Test': {'hasil': vertical_jump, 'target': '> 45 cm (Power Bawah)'}
        }
        
        data_match = {
            'pass_acc': pass_accuracy,
            'aerial': aerial_won,
            'intercept': interceptions_game,
            'video_link': video_url
        }
        
        idp_data = {
            'strengths': key_strengths,
            'improvements': areas_improvement,
            'action_plan': actionable_idp
        }
        
        # Penanganan Upload Foto & Logo
        path_logo_temp = "temp_logo.jpg" if file_logo else None
        path_foto_temp = "temp_foto.jpg" if file_foto else None
        
        if file_logo:
            ext_logo = file_logo.name.split(".")[-1]
            path_logo_temp = f"temp_logo.{ext_logo}"
            with open(path_logo_temp, "wb") as f: f.write(file_logo.getbuffer())

        if file_foto:
            ext_foto = file_foto.name.split(".")[-1]
            path_foto_temp = f"temp_foto.{ext_foto}"
            with open(path_foto_temp, "wb") as f: f.write(file_foto.getbuffer())

        # Buat File PDF Pro
        file_pdf_pro = buat_pdf_pro(data_bio, data_fisik_obj, dict_penilaian, data_match, idp_data, bulan_eval, tahun_eval, path_logo_temp, path_foto_temp)
        
        with open(file_pdf_pro, "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            
        st.download_button(
            label="📥 Unduh Rapor Pro & IDP (PDF)",
            data=PDFbyte,
            file_name=f"Rapor_Pro_{nama_pemain.replace(' ', '_')}_{bulan_eval}_{tahun_eval}.pdf",
            mime="application/pdf"
        )
        
        os.remove(file_pdf_pro)
        if path_logo_temp and os.path.exists(path_logo_temp): os.remove(path_logo_temp)
        if path_foto_temp and os.path.exists(path_foto_temp): os.remove(path_foto_temp)
