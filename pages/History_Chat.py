import streamlit as st

# --- 1. CONFIG HALAMAN ---
st.set_page_config(layout="wide", page_title="MCSA | History Chat")

# --- 2. DATA DUMMY HISTORY ---
history_data = [
    {"no": 1, "user": "Kaila Najwa", "q": "Batas transfer valas asing", "ans": "PJOK No. 12/PJOK.01/2017.pdf"},
    {"no": 2, "user": "Aisyah Putri", "q": "Sanksi pelanggaran APU", "ans": "UU No 8 Tahun 2010"},
    {"no": 3, "user": "Shahaf Lanjaya", "q": "Dokumen KYC nasabah korporasi", "ans": "SEBI No. 34/2023.pdf"},
    {"no": 4, "user": "Amira Alissiya", "q": "Batas transfer valas asing", "ans": "PJOK No. 12/PJOK.01/2017.pdf"},
    {"no": 5, "user": "Hilmy Chanu", "q": "Sanksi pelanggaran APU", "ans": "UU No 8 Tahun 2010"},
    {"no": 6, "user": "Kaila Najwa", "q": "Dokumen KYC nasabah korporasi", "ans": "SEBI No. 34/2023.pdf"},
    {"no": 7, "user": "Aisyah Putri", "q": "Batas transfer valas asing", "ans": "PJOK No. 12/PJOK.01/2017.pdf"},
    {"no": 8, "user": "Shahaf Lanjaya", "q": "Sanksi pelanggaran APU", "ans": "UU No 8 Tahun 2010"},
    {"no": 9, "user": "Amira Alissiya", "q": "Dokumen KYC nasabah korporasi", "ans": "SEBI No. 34/2023.pdf"},
    {"no": 10, "user": "Hilmy Chanu", "q": "Batas transfer valas asing", "ans": "PJOK No. 12/PJOK.01/2017.pdf"},
]

# --- 3. UI HTML SHELL (CSS STYLE) ---
html_layout = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* { font-family: 'Roboto', sans-serif; box-sizing: border-box; }
body { background-color: #F5F7FA; margin: 0; }

/* LAYOUT */
.block-container {
    padding: 0 !important; margin-top: 100px !important; margin-left: 270px !important;
    max-width: calc(100% - 290px) !important;
}
[data-testid="stSidebar"], header, footer, [data-testid="stHeader"] { display: none !important; }

/* SIDEBAR & HEADER FIXED */
.html-sidebar {
    position: fixed; top: 0; left: 0; width: 250px; height: 100vh;
    background: white; border-right: 1px solid #E5E7EB;
    padding: 25px 15px; z-index: 10000; display: flex; flex-direction: column;
}
.html-header {
    position: fixed; top: 0; left: 250px; width: calc(100% - 250px); height: 80px;
    background: #1E3A8A; display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; z-index: 9999;
}

/* MENU */
.menu-item {
    padding: 12px 20px; margin-bottom: 5px; border-radius: 8px;
    color: #4B5563; font-weight: 500; font-size: 14px;
    cursor: pointer; display: flex; align-items: center; gap: 12px;
    text-decoration: none !important; transition: 0.2s; display: block;
}
.menu-item:hover { background: #F3F4F6; color: #111; }
.menu-item.active { background: #1E3A8A; color: white; }

.header-search-bar {
    background: rgba(255,255,255,0.2); border-radius: 20px;
    padding: 8px 15px; color: white; font-size: 14px;
    width: 300px; display: flex; align-items: center; gap: 10px;
}

/* TABLE CONTAINER */
.history-card {
    background: white; border-radius: 12px; padding: 25px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.02); margin-top: 20px;
}

/* GRID TABLE */
.grid-table {
    display: grid; grid-template-columns: 50px 1.5fr 2fr 2fr 80px;
    align-items: center; padding: 15px 10px;
}
.table-header {
    border-bottom: 1px solid #E2E8F0; font-weight: 600; font-size: 13px; color: #64748B;
}
.table-row {
    border-bottom: 1px solid #F1F5F9; font-size: 14px; color: #333; transition: 0.2s;
}
.table-row:hover { background: #F8FAFC; }

.action-icons span { cursor: pointer; margin-right: 12px; font-size: 16px; color: #64748B; }
.action-icons span:hover { color: #1E3A8A; }

/* PAGINATION */
.pagination {
    display: flex; justify-content: space-between; align-items: center;
    margin-top: 25px; color: #94A3B8; font-size: 13px;
}
.page-btn {
    width: 30px; height: 30px; display: flex; align-items: center; justify-content: center;
    border-radius: 6px; background: #F1F5F9; cursor: pointer; color: #64748B;
    margin-left: 5px; font-weight: 500;
}
.page-btn.active { background: #1E3A8A; color: white; }

/* CUSTOM INPUT SEARCH (BIAR RAPI) */
div[data-testid="stTextInput"] input { border-radius: 20px !important; border: 1px solid #E2E8F0; padding-left: 15px; }
</style>

<div class="html-sidebar">
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="130">
    </div>
    <a href="Admin_Dashboard" target="_self" class="menu-item">📊 Dashboard</a>
    <a href="Dokumen" target="_self" class="menu-item">📄 Dokumen</a>
    <div class="menu-item active">⏳ History Chat</div>
    <a href="Users" target="_self" class="menu-item">👥 Users</a>
    <a href="Settings" target="_self" class="menu-item">⚙️ Settings</a>
    <div style="margin-top: auto; border-top: 1px solid #eee; padding-top: 15px; display: flex; align-items: center; gap: 10px;">
        <img src="https://www.w3schools.com/howto/img_avatar.png" style="width: 35px; height: 35px; border-radius: 50%;">
        <div style="line-height: 1.2;">
            <div style="font-size: 13px; font-weight: 700; color: #333;">Admin IT</div>
            <div style="font-size: 11px; color: #888;">NIP: 999001</div>
        </div>
    </div>
</div>

<div class="html-header">
    <div style="color: white; font-size: 22px; font-weight: 600;">MCSA | History Chat Overview</div>
    <div class="header-search-bar">
        <span>🔍</span> <span style="opacity: 0.8;">Search data...</span>
    </div>
</div>
"""
st.markdown(html_layout, unsafe_allow_html=True)


# --- 4. ISI KONTEN UTAMA ---
st.markdown("### History Chat")

# A. SEARCH BAR (Native Widget di Luar Card)
# Gunakan columns biar tidak terlalu lebar
c_search, c_space = st.columns([1, 2])
with c_search:
    search_q = st.text_input("Cari", placeholder="Cari berdasarkan Nama...", label_visibility="collapsed")


# B. STRING BUILDER TABEL (HTML DI RAPATKAN KE KIRI!)
# 1. Buka Container
html_content = '<div class="history-card">'

# 2. Header
html_content += """
<div class="grid-table table-header">
    <div>No</div>
    <div>Pengguna</div>
    <div>Pertanyaan</div>
    <div>Jawaban</div>
    <div>Aksi</div>
</div>
"""

# 3. Filter & Loop Data
filtered_data = [d for d in history_data if search_q.lower() in d['user'].lower()] if search_q else history_data

if not filtered_data:
    html_content += '<div style="padding:30px; text-align:center; color:#888;">Data tidak ditemukan</div>'
else:
    for item in filtered_data:
        # PENTING: HTML DI BAWAH INI SAYA TARUH RATA KIRI (TANPA SPASI)
        html_content += f"""
<div class="grid-table table-row">
<div>{item['no']}</div>
<div style="font-weight:500;">{item['user']}</div>
<div>{item['q']}</div>
<div style="color:#475569;">{item['ans']}</div>
<div class="action-icons">
<span>👁️</span>
<span>🗑️</span>
</div>
</div>
"""

# 4. Pagination & Tutup
html_content += """
<div class="pagination">
    <div>Showing data 1 to 10 of 200 entries</div>
    <div style="display:flex;">
        <div class="page-btn">&lt;</div>
        <div class="page-btn active">1</div>
        <div class="page-btn">2</div>
        <div class="page-btn">3</div>
        <div class="page-btn">4</div>
        <div style="margin: 0 8px;">...</div>
        <div class="page-btn">10</div>
        <div class="page-btn">&gt;</div>
    </div>
</div>
</div> 
"""

# 5. RENDER FINAL
st.markdown(html_content, unsafe_allow_html=True)