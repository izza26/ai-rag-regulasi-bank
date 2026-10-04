import streamlit as st
import os
import sys
import time

# --- JEMBATAN KONEKSI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from rag_engine import save_uploaded_file, ingest_document, get_list_of_files, delete_file

# --- 1. CONFIG HALAMAN ---
st.set_page_config(layout="wide", page_title="MCSA | Manajemen Dokumen")

# --- 2. CSS & LAYOUT (WAJIB RAPAT KIRI) ---
html_layout = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* { font-family: 'Roboto', sans-serif; box-sizing: border-box; }
[data-testid="stSidebar"], header, footer, [data-testid="stHeader"] { display: none !important; }
.block-container { padding: 0 !important; margin-top: 100px !important; margin-left: 270px !important; max-width: calc(100% - 290px) !important; }
.html-sidebar { position: fixed; top: 0; left: 0; width: 250px; height: 100vh; background: white; border-right: 1px solid #ddd; padding: 25px 15px; z-index: 10000; display: flex; flex-direction: column; }
.html-header { position: fixed; top: 0; left: 250px; width: calc(100% - 250px); height: 80px; background: #1E3A8A; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; z-index: 9999; }
.menu-item { display: block; padding: 12px 20px; margin-bottom: 5px; color: #4B5563; text-decoration: none; border-radius: 8px; font-weight: 500; font-size: 14px; transition: 0.2s;text-decoration: none !important; /* Menghapus garis bawah */ }
.menu-item:hover { background: #f0f2f6; color: #000; }
.menu-item.active { background: #1E3A8A; color: white; }
.profile-footer { margin-top: auto; border-top: 1px solid #eee; padding-top: 15px; display: flex; align-items: center; gap: 10px; }
h3 { font-size: 20px !important; }
</style>
<div class="html-sidebar">
<div style="text-align: center; margin-bottom: 30px;">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="130">
</div>
<a href="Admin_Dashboard" target="_self" class="menu-item">📊 Dashboard</a>
<div class="menu-item active">📄 Dokumen</div>
<a href="History_Chat" target="_self" class="menu-item">⏳ History Chat</a>
<a href="Users" target="_self" class="menu-item">👥 Users</a>
<a href="Settings" target="_self" class="menu-item">⚙️ Settings</a>
<div class="profile-footer">
<img src="https://www.w3schools.com/howto/img_avatar.png" style="width: 35px; height: 35px; border-radius: 50%;">
<div style="line-height: 1.2;">
<div style="font-size: 13px; font-weight: 700; color: #333;">Admin IT</div>
<div style="font-size: 11px; color: #888;">NIP: 999001</div>
</div>
</div>
</div>
<div class="html-header">
<div style="color: white; font-size: 22px; font-weight: 600;">MCSA | Dokumen Overview</div>
<div style="background: rgba(255,255,255,0.2); border-radius: 20px; padding: 8px 15px; color: white; width: 300px;">🔍 Search data...</div>
</div>
"""
st.markdown(html_layout, unsafe_allow_html=True)

# --- 3. LOGIKA UPLOAD ---
@st.dialog("Upload Dokumen")
def show_upload_form():
    uploaded_file = st.file_uploader("Pilih File PDF", type=["pdf"])
    if st.button("Proses & Simpan"):
        if uploaded_file:
            with st.spinner("Sedang membaca dokumen..."):
                try:
                    path = save_uploaded_file(uploaded_file)
                    ingest_document(path)
                    st.success("Berhasil!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# --- 4. TAMPILAN UTAMA ---
c1, c2 = st.columns([5, 1])
with c1:
    st.markdown("### 📂 Manajemen Dokumen")
    st.caption("Upload dan kelola dokumen regulasi (PDF) untuk Knowledge Base AI.")
with c2:
    if st.button("＋ Upload Baru"):
        show_upload_form()

# --- 5. LIST DOKUMEN ---
files = get_list_of_files()
if not files:
    st.info("Belum ada dokumen yang diupload. Silakan upload dokumen PDF.")
else:
    for f in files:
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])
            col1.write(f"📄 **{f}**")
            if col2.button("Hapus", key=f):
                delete_file(f)
                st.rerun()