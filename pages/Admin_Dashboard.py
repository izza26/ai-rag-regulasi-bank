import streamlit as st
import pandas as pd
import altair as alt
import os

# --- 1. LOGIKA HITUNG DOKUMEN ---
def count_documents(folder_path="./data"):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return 0
    # Menghitung file asli di dalam folder data
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return len(files)

total_docs = count_documents()

# --- 2. CONFIG HALAMAN ---
st.set_page_config(layout="wide", page_title="MCSA | Dashboard")

# --- 3. DATA DUMMY CHART ---
chart_data = pd.DataFrame({
    'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'] * 3,
    'Nilai': [10, 25, 45, 60, 80, 95, 120, 5, 15, 30, 50, 80, 110, 140, 2, 10, 25, 40, 60, 85, 100],
    'Kategori': ['Peraturan OJK']*7 + ['Peraturan BI']*7 + ['Internal Policy']*7
})

# PERBAIKAN POSISI JUDUL
chart = alt.Chart(chart_data).mark_line(strokeWidth=3).encode(
    x=alt.X('Bulan', sort=None, axis=alt.Axis(grid=False, tickSize=0, labelColor='#888')),
    y=alt.Y('Nilai', axis=alt.Axis(grid=True, gridColor='#f0f0f0', tickSize=0, labelColor='#888')),
    color=alt.Color('Kategori', legend=alt.Legend(orient='top', title=None)),
    tooltip=['Bulan', 'Nilai', 'Kategori']
).properties(
    title=alt.TitleParams(
        text='Aktivitas Pengguna', 
        fontSize=16, 
        fontWeight=600, 
        anchor='start', 
        offset=20,   
        dx=20        
    ),
    height=350,
    background='#FFFFFF',
).configure_view(strokeWidth=0, continuousHeight=350)

# --- 4. UI HTML & CSS ---
html_layout = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* {{ font-family: 'Roboto', sans-serif; box-sizing: border-box; }}
body {{ background-color: #F5F7FA; margin: 0; }}

[data-testid="stSidebar"], header, footer, [data-testid="stHeader"] {{ display: none !important; }}

.block-container {{
    padding: 0 !important; margin-top: 100px !important; margin-left: 270px !important;
    max-width: calc(100% - 290px) !important;
}}

.html-sidebar {{
    position: fixed; top: 0; left: 0; width: 250px; height: 100vh;
    background: white; border-right: 1px solid #E5E7EB;
    padding: 25px 15px; z-index: 10000; display: flex; flex-direction: column;
}}
.html-header {{
    position: fixed; top: 0; left: 250px; width: calc(100% - 250px); height: 80px;
    background: #1E3A8A; display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; z-index: 9999;
}}

.menu-item {{
    padding: 12px 20px; margin-bottom: 5px; border-radius: 8px;
    color: #4B5563; font-weight: 500; font-size: 14px;
    cursor: pointer; display: flex; align-items: center; gap: 12px;
    text-decoration: none !important; transition: 0.2s; display: block;
}}
.menu-item.active {{ background: #1E3A8A; color: white; }}

.kpi-card {{
    background: white; padding: 25px; border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); display: flex; align-items: center; gap: 20px;
}}
.icon-box {{ width: 50px; height: 50px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 20px; }}
.bg-blue {{ background: #E0F2FE; color: #0284C7; }}

</style>

<div class="html-sidebar">
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="130">
    </div>
    <div class="menu-item active">📊 Dashboard</div>
    <a href="Dokumen" target="_self" class="menu-item">📄 Dokumen</a>
    <a href="History_Chat" target="_self" class="menu-item">⏳ History Chat</a>
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
    <div style="color: white; font-size: 22px; font-weight: 600;">MCSA | Dashboard Overview</div>
    <div style="background: rgba(255,255,255,0.2); border-radius: 20px; padding: 8px 15px; color: white; width: 300px;">
        🔍 Search data...
    </div>
</div>
"""
st.markdown(html_layout, unsafe_allow_html=True)

# --- 5. DASHBOARD CONTENT ---
st.markdown("### Dashboard")
st.markdown('<div style="margin-bottom: 20px;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 30px;">
    <div class="kpi-card">
        <div class="icon-box bg-blue">📄</div>
        <div>
            <div style="color:#64748B; font-size:13px; font-weight:500;">Total Dokumen</div>
            <div style="font-size:28px; font-weight:700; color:#1E293B;">{total_docs}</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="icon-box" style="background:#ECFEFF; color:#06B6D4;">💬</div>
        <div>
            <div style="color:#64748B; font-size:13px; font-weight:500;">Total Obrolan</div>
            <div style="font-size:28px; font-weight:700; color:#1E293B;">320</div>
        </div>
    </div>
    <div class="kpi-card">
        <div class="icon-box" style="background:#EEF2FF; color:#6366F1;">⚡</div>
        <div>
            <div style="color:#64748B; font-size:13px; font-weight:500;">Waktu Respon</div>
            <div style="font-size:28px; font-weight:700; color:#1E293B;">1.5s</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

c_left, c_right = st.columns([2, 1])
with c_left:
    st.altair_chart(chart, use_container_width=True)

with c_right:
    st.markdown("""
    <div style="background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); height: 100%;">
        <div style="font-weight:700; font-size:16px; margin-bottom:15px; color:#333;">Pertanyaan Terpopuler</div>
        <div style="padding:15px 0; border-bottom:1px solid #eee; font-size:14px;">Apa kriteria nasabah risiko tinggi?</div>
        <div style="padding:15px 0; border-bottom:1px solid #eee; font-size:14px;">Batas waktu pengaduan nasabah?</div>
        <div style="padding:15px 0; border-bottom:1px solid #eee; font-size:14px;">Sanksi keterlambatan laporan OJK?</div>
    </div>
    """, unsafe_allow_html=True)