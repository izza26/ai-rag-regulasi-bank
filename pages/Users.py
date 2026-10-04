import streamlit as st
import sqlite3
import pandas as pd
import time

# --- 1. CONFIG HALAMAN ---
st.set_page_config(layout="wide", page_title="MCSA | Users Management")

# --- 2. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            nip TEXT PRIMARY KEY,
            name TEXT,
            dept TEXT,
            password TEXT
        )
    ''')
    c.execute('SELECT count(*) FROM staff')
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO staff VALUES ('2001', 'Kaila Najwa', 'Compliance', 'kaila123')")
        c.execute("INSERT INTO staff VALUES ('2002', 'Aisyah Putri', 'Compliance', 'aisyah123')")
        c.execute("INSERT INTO staff VALUES ('2003', 'Shahaf Lanjaya', 'Compliance', 'shahaf123')")
        conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('users.db')
    df = pd.read_sql_query("SELECT * FROM staff", conn)
    conn.close()
    return df

def add_new_user(nip, name, dept, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO staff VALUES (?, ?, ?, ?)", (nip, name, dept, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

init_db()

# --- 3. POPUP FORM ---
@st.dialog("Tambah Pengguna Baru")
def show_add_user_form():
    st.write("Masukkan data staff compliance baru.")
    new_nip = st.text_input("NIP", placeholder="Contoh: 2024001")
    new_name = st.text_input("Nama Lengkap", placeholder="Nama Staff")
    new_dept = st.selectbox("Departemen", ["Compliance"])
    new_pw = st.text_input("Password Login", placeholder="Buat kata sandi") 
    
    if st.button("Simpan Data"):
        if new_nip and new_name and new_pw:
            success = add_new_user(new_nip, new_name, new_dept, new_pw)
            if success:
                st.success(f"Berhasil menambahkan {new_name}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Gagal! NIP tersebut sudah terdaftar.")
        else:
            st.warning("Mohon lengkapi semua data.")

# --- 4. CSS & LAYOUT (DIPERBAIKI: INDENTASI DIHAPUS) ---
html_layout = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* { font-family: 'Roboto', sans-serif; box-sizing: border-box; }
body { background-color: #F5F7FA; margin: 0; }
[data-testid="stSidebar"], header, footer, [data-testid="stHeader"] { display: none !important; }

/* LAYOUT UTAMA */
.block-container {
padding: 0 !important; margin-top: 100px !important; margin-left: 270px !important;
max-width: calc(100% - 290px) !important;
}

/* SIDEBAR FIXED */
.html-sidebar {
position: fixed; top: 0; left: 0; width: 250px; height: 100vh;
background: white; border-right: 1px solid #E5E7EB;
padding: 25px 15px; z-index: 10000; 
display: flex; flex-direction: column;
}

/* HEADER FIXED */
.html-header {
position: fixed; top: 0; left: 250px; width: calc(100% - 250px); height: 80px;
background: #1E3A8A; display: flex; align-items: center; justify-content: space-between;
padding: 0 40px; z-index: 9999;
}

/* MENU ITEMS */
.menu-item {
padding: 12px 20px; margin-bottom: 5px; border-radius: 8px;
color: #4B5563; font-weight: 500; font-size: 14px;
cursor: pointer; display: flex; align-items: center; gap: 12px;
text-decoration: none !important; transition: 0.2s; display: block;
}
.menu-item:hover { background: #F3F4F6; color: #111; }
.menu-item.active { background: #1E3A8A; color: white; }

/* ALIGNMENT TOMBOL & INPUT */
div[data-testid="stVerticalBlock"] > div:has(div.stButton) { padding-top: 0px !important; }
div.stButton > button {
background-color: #1E3A8A !important; color: white !important;
border-radius: 8px !important; border: none !important;
padding: 0px 25px !important; height: 45px !important; 
width: auto !important; white-space: nowrap !important;
font-weight: 600 !important; margin: 0 !important;
}
div[data-testid="stTextInput"] input { border-radius: 8px !important; border: 1px solid #E2E8F0; height: 45px !important; }

/* TABEL CARD */
.table-card {
background: white; border-radius: 12px; padding: 25px;
box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-top: 10px;
}
.grid-table { display: grid; grid-template-columns: 20% 30% 20% 15% 15%; align-items: center; padding: 15px 10px; }
.table-header { border-bottom: 2px solid #E2E8F0; font-weight: 700; font-size: 13px; color: #1E293B; text-transform: uppercase; }
.table-row { border-bottom: 1px solid #F1F5F9; font-size: 14px; color: #333; transition: 0.2s; }
</style>

<div class="html-sidebar">
<div style="text-align: center; margin-bottom: 30px;">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="130">
</div>
<a href="Admin_Dashboard" target="_self" class="menu-item">📊 Dashboard</a>
<a href="Dokumen" target="_self" class="menu-item">📄 Dokumen</a>
<a href="History_Chat" target="_self" class="menu-item">⏳ History Chat</a>
<div class="menu-item active">👥 Users</div>
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
<div style="color: white; font-size: 22px; font-weight: 600;">MCSA | Users Overview</div>
</div>
"""
st.markdown(html_layout, unsafe_allow_html=True)

# --- 5. KONTEN UTAMA ---
st.markdown("### Manajemen Pengguna")

c1, c2 = st.columns([4, 2], vertical_alignment="center", gap="small")
with c1:
    search_query = st.text_input("Cari", placeholder="Cari berdasarkan NIP atau Nama...", label_visibility="collapsed")
with c2:
    st.markdown('<div style="display: flex; justify-content: flex-end; margin: 0;">', unsafe_allow_html=True)
    if st.button("＋ Tambah Pengguna Baru"):
        show_add_user_form()
    st.markdown('</div>', unsafe_allow_html=True)

# B. TABLE GENERATION
df_users = get_all_users()
if search_query:
    df_users = df_users[df_users['name'].str.contains(search_query, case=False) | df_users['nip'].str.contains(search_query)]

table_html = '<div class="table-card">'
table_html += '<div class="grid-table table-header"><div>NIP</div><div>Nama Lengkap</div><div>Departemen</div><div>Password</div><div>Action</div></div>'

if df_users.empty:
    table_html += '<div style="padding:40px; text-align:center; color:#999;">Data tidak ditemukan</div>'
else:
    for index, row in df_users.iterrows():
        table_html += f"""
<div class="grid-table table-row">
<div style="font-family:monospace; color:#666; font-weight:600;">{row['nip']}</div>
<div style="font-weight:600; color:#333;">{row['name']}</div>
<div><span style="background:#E0F2FE; color:#0369A1; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;">{row['dept']}</span></div>
<div style="font-family:monospace; color:#333;">{row['password']}</div>
<div class="action-icons">
<span style="cursor:pointer">🔑</span>
<span style="cursor:pointer">✏️</span>
<span style="color:#EF4444; cursor:pointer">🗑️</span>
</div>
</div>"""

table_html += '</div>'
st.markdown(table_html, unsafe_allow_html=True)