import streamlit as st

# --- 1. CONFIG HALAMAN ---
st.set_page_config(layout="wide", page_title="MCSA | Settings")

# --- 2. UI HTML SHELL (RATA KIRI) ---
html_layout = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
* { font-family: 'Roboto', sans-serif; box-sizing: border-box; }
body { background-color: #F5F7FA; margin: 0; }
[data-testid="stSidebar"], header, footer, [data-testid="stHeader"] { display: none !important; }

/* CONTENT SHIFT */
.block-container {
padding: 0 !important;
margin-top: 100px !important;
margin-left: 270px !important;
max-width: calc(100% - 290px) !important;
}

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

/* MENU STYLE */
.menu-item {
padding: 12px 20px; margin-bottom: 5px; border-radius: 8px;
color: #4B5563; font-weight: 500; font-size: 14px;
cursor: pointer; display: flex; align-items: center; gap: 12px;
text-decoration: none !important; transition: 0.2s; display: block;
}
.menu-item:hover { background: #F3F4F6; color: #111; }
.menu-item.active { background: #1E3A8A; color: white; }

/* SETTINGS SPECIFIC STYLE */
.banner-card {
background: white; border-radius: 12px; padding: 25px;
border: 1px solid #E2E8F0;
border-left: 5px solid #1E3A8A; 
box-shadow: 0 2px 5px rgba(0,0,0,0.02); margin-bottom: 30px;
}
.section-title {
font-size: 18px; font-weight: 700; color: #1E293B;
margin-top: 20px; margin-bottom: 15px;
border-bottom: 1px solid #E2E8F0; padding-bottom: 10px;
}
.setting-label { font-weight: 600; font-size: 14px; color: #1E293B; }
.setting-desc { font-size: 13px; color: #64748B; margin-top: 2px; line-height: 1.4; }

/* FORCE BLUE WIDGETS */
div[data-testid="stToggle"] label[data-checked="true"] span[class^="st-"] {
    background-color: #1E3A8A !important;
}
div[data-testid="stCheckbox"] label span[data-checked="true"] div:first-child {
    background-color: #1E3A8A !important;
    border-color: #1E3A8A !important;
}

/* CSS KHUSUS TOMBOL LOGOUT (WARNA BIRU, LEBIH KECIL, RATA KANAN) */
.stButton {
    display: flex;
    justify-content: flex-end; /* Menggeser ke kanan dalam kolomnya */
}

.stButton > button {
    background-color: #1E3A8A !important; /* Warna biru senada */
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 6px 25px !important; /* Padding disesuaikan */
    font-size: 13px !important; /* Font lebih kecil */
    font-weight: 600 !important;
    width: auto !important; /* Tidak memenuhi lebar kolom */
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #162d6b !important;
    transform: translateY(-1px);
}

</style>

<div class="html-sidebar">
<div style="text-align: center; margin-bottom: 30px;">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="130">
</div>
<a href="Admin_Dashboard" target="_self" class="menu-item">📊 Dashboard</a>
<a href="Dokumen" target="_self" class="menu-item">📄 Dokumen</a>
<a href="History_Chat" target="_self" class="menu-item">⏳ History Chat</a>
<a href="Users" target="_self" class="menu-item">👥 Users</a>
<div class="menu-item active">⚙️ Settings</div>
<div style="margin-top: auto; border-top: 1px solid #eee; padding-top: 15px; display: flex; align-items: center; gap: 10px;">
<img src="https://www.w3schools.com/howto/img_avatar.png" style="width: 35px; height: 35px; border-radius: 50%;">
<div style="line-height: 1.2;">
<div style="font-size: 13px; font-weight: 700; color: #333;">Admin IT</div>
<div style="font-size: 11px; color: #888;">NIP: 999001</div>
</div>
</div>
</div>

<div class="html-header">
<div style="color: white; font-size: 22px; font-weight: 600;">MCSA | Settings Overview</div>
</div>
"""
st.markdown(html_layout, unsafe_allow_html=True)

# --- 3. ISI KONTEN UTAMA ---

# 1. Banner Info
st.markdown("""
<div class="banner-card">
    <div style="font-weight:700; font-size:15px; margin-bottom:5px; color:#333;">Your application is currently on the free plan</div>
    <div style="font-size:13px; color:#666;">Paid plans offer higher usage limits, additional branches and much more. <a href="#" style="color:#1E3A8A;">Learn more here.</a></div>
</div>
""", unsafe_allow_html=True)

# 2. Section: General
st.markdown('<div class="section-title">General</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3, 1])
with c1:
    st.markdown('<div class="setting-label" style="margin-bottom:10px;">Notify me when..</div>', unsafe_allow_html=True)
    st.checkbox("Daily productivity update", value=True)
    st.checkbox("New event created", value=True)
    st.checkbox("When added on new team", value=True)
with c2:
    st.markdown('<div style="text-align:right; color:#1E3A8A; font-size:13px; cursor:pointer; font-weight:500;">About Notifications?</div>', unsafe_allow_html=True)

st.write("") 

t1_col_text, t1_col_btn = st.columns([4, 1])
with t1_col_text:
    st.markdown("""
    <div class="setting-label">Desktop Notifications</div>
    <div class="setting-desc">Receive desktop notifications whenever your organisation requires your attentions</div>
    """, unsafe_allow_html=True)
with t1_col_btn:
    st.toggle("desktop_notif", value=True, label_visibility="collapsed")

st.markdown("<hr style='margin:15px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

t2_col_text, t2_col_btn = st.columns([4, 1])
with t2_col_text:
    st.markdown("""
    <div class="setting-label">Email Notifications</div>
    <div class="setting-desc">Receive email whenever your organisation requires your attentions</div>
    """, unsafe_allow_html=True)
with t2_col_btn:
    st.toggle("email_notif", value=False, label_visibility="collapsed")

# 3. Section: My Settings
st.markdown('<div style="margin-top: 40px;" class="section-title">My Settings</div>', unsafe_allow_html=True)

s1_col_text, s1_col_input = st.columns([3, 1])
with s1_col_text:
    st.markdown("""
    <div class="setting-label">Appearance</div>
    <div class="setting-desc">Customize your theme looks on your device</div>
    """, unsafe_allow_html=True)
with s1_col_input:
    st.selectbox("theme_select", ["Light", "Dark", "System"], label_visibility="collapsed")

st.markdown("<hr style='margin:15px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

s2_col_text, s2_col_input = st.columns([4, 1])
with s2_col_text:
    st.markdown("""
    <div class="setting-label">Two-factor authentication</div>
    <div class="setting-desc">Keep your account secure by enabling 2FA via SMS or using a temporary one-time passcode (OTP)</div>
    """, unsafe_allow_html=True)
with s2_col_input:
    st.toggle("2fa_toggle", value=True, label_visibility="collapsed")

st.markdown("<hr style='margin:15px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

s3_col_text, s3_col_input = st.columns([3, 1])
with s3_col_text:
    st.markdown("""
    <div class="setting-label">Language</div>
    <div class="setting-desc">Customize how you theme look on your device</div>
    """, unsafe_allow_html=True)
with s3_col_input:
    st.selectbox("lang_select", ["English", "Bahasa Indonesia"], label_visibility="collapsed")

# 4. Section: Accessibility
st.markdown('<div style="margin-top: 40px;" class="section-title">Accessibility</div>', unsafe_allow_html=True)
st.markdown("""
<div class="setting-label">Text size</div>
<div class="setting-desc">Customize your text size looks on your device</div>
""", unsafe_allow_html=True)
st.slider("text_size_slider", 10, 30, 14, label_visibility="collapsed")

# 5. Section: Account Actions (Logout)
st.markdown('<div style="margin-top: 40px;" class="section-title">Account Actions</div>', unsafe_allow_html=True)
l_col_text, l_col_btn = st.columns([3, 1])
with l_col_text:
    st.markdown("""
    <div class="setting-label">Sign Out</div>
    <div class="setting-desc">Log out of your current session and return to the login screen.</div>
    """, unsafe_allow_html=True)
with l_col_btn:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.switch_page("app.py")

st.write("")
st.write("")