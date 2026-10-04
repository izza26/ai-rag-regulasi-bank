import streamlit as st
import sqlite3
from datetime import datetime
import json

# --- 1. CONFIG HALAMAN ---
st.set_page_config(
    page_title="MCSA | Staff Chat", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# --- 2. CEK LOGIN & INISIALISASI SESSION STATE ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# MENGAMBIL DATA LOGIN YANG AKTIF
# Pastikan kunci 'user_nip' dan 'user_name' sesuai dengan yang diset di app.py saat login
user_nip = st.session_state.get('user_nip', 'unknown') 
user_name = st.session_state.get('user_name', 'Staff')

# --- 3. CSS CUSTOM ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; color: white !important; }
    footer { display: none !important; }
    .stApp { background-color: #f8f9fa; }
    
    .custom-header {
        position: fixed; top: 0; left: 0; right: 0; height: 70px;
        background-color: #1E3A8A; display: flex; justify-content: space-between; align-items: center;
        padding: 0 30px; z-index: 99; color: white;
    }
    .header-left { display: flex; align-items: center; gap: 40px; padding-left: 40px; }
    .block-container { padding-top: 100px !important; }

    [data-testid="stSidebar"] {
        background-color: #ffffff !important; 
        border-right: 1px solid #E5E7EB;
    }
    
    div[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 0px !important;
        gap: 0rem !important;
    }

    div[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background-color: #1E3A8A !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 45px !important;
        width: 100% !important;
    }

    div[data-testid="stSidebar"] div.stButton > button:not([kind="primary"]) {
        background-color: #ffffff !important;
        color: #333333 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        font-size: 10px !important;
        padding: 10px 15px !important;
        margin-bottom: 12px !important;
        width: 100% !important;
        min-height: unset !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
        overflow: hidden !important;
        white-space: normal !important;
        text-overflow: clip !important;
    }

    /* --- TAMBAHAN UNTUK WARNA BUBBLE CHAT USER --- */
    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) {
        flex-direction: row-reverse;
        text-align: right;
    }

    div[data-testid="stChatMessage"]:has(div[aria-label="Chat message from user"]) .stMarkdown {
        background-color: #1E3A8A !important; /* Warna Biru */
        color: white !important;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIKA DATABASE ---
def get_user_history():
    conn = sqlite3.connect('chat_history.db')
    c = conn.cursor()
    # Menampilkan riwayat hanya milik user yang sedang login
    c.execute("SELECT id, title, messages FROM history WHERE nip = ? ORDER BY timestamp DESC", (user_nip,))
    rows = c.fetchall()
    conn.close()
    return rows

def save_chat_to_db():
    """Menyimpan data chat lengkap dengan NIP user aktif"""
    if st.session_state.messages:
        conn = sqlite3.connect('chat_history.db')
        c = conn.cursor()
        msg_json = json.dumps(st.session_state.messages)
        title = st.session_state.messages[0]['content'][:50]
        
        # Menggunakan user_nip yang ditarik dari session state
        current_nip = st.session_state.get('user_nip', 'unknown')
        
        if st.session_state.current_chat_id:
            c.execute("UPDATE history SET messages = ?, nip = ? WHERE id = ?", 
                      (msg_json, current_nip, st.session_state.current_chat_id))
        else:
            c.execute("INSERT INTO history (nip, title, messages, timestamp) VALUES (?, ?, ?, ?)",
                      (current_nip, title, msg_json, datetime.now()))
            st.session_state.current_chat_id = c.lastrowid
        conn.commit()
        conn.close()

# --- 5. SIDEBAR CUSTOM ---
with st.sidebar:
    if st.button("➕ Chat Baru", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.current_chat_id = None
        st.rerun()
    
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 16px; font-weight: 700; color: #1E3A8A; padding-left: 10px; margin-bottom: 10px;">💬 Riwayat Chat</p>', unsafe_allow_html=True)
    
    history_data = get_user_history()
    for chat_id, title, msgs in history_data:
        if st.button(title, key=f"h_{chat_id}", use_container_width=True):
            st.session_state.messages = json.loads(msgs)
            st.session_state.current_chat_id = chat_id
            st.rerun()
            
    st.markdown("<div style='flex-grow: 1; min-height: 15vh;'></div>", unsafe_allow_html=True)
    if st.button("⬅️ Logout", use_container_width=True, type="primary"):
        st.session_state.logged_in = False
        st.switch_page("app.py")

# --- 6. RENDER HEADER ---
st.markdown(f"""
    <div class="custom-header">
        <div class="header-left">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Bank_Mandiri_logo_2016.svg/2560px-Bank_Mandiri_logo_2016.svg.png" width="100" style="filter: brightness(0) invert(1);">
            <div style="font-size: 18px; font-weight: 400; opacity: 0.8;">| MCSA | Compliance Assistant</div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; color:white;">
            <img src="https://www.w3schools.com/howto/img_avatar.png" width="35" style="border-radius: 50%;">
            <span style="font-weight: 500;">{user_name}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 7. LOGIKA CHAT ---
if not st.session_state.messages:
    st.markdown(f"<div style='text-align:center; margin-top:15vh;'><h1 style='color:#1E3A8A; font-size: 36px;'>Selamat Datang {user_name} ! 👋</h1></div>", unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ketik Pertanyaan Anda Disini..."):
    from rag_engine import answer_question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Menganalisa..."):
            answer, sources = answer_question(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # MEMANGGIL FUNGSI SIMPAN DENGAN DATA NIP TERBARU
    save_chat_to_db()
    st.rerun()