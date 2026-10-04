import streamlit as st
import sqlite3

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="MCSA | Login", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- 2. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None

# --- CEK STATUS LOGIN ---
if st.session_state.logged_in:
    st.switch_page("pages/Admin_Dashboard.py")

# --- 3. LOGIKA TAMPILAN LOGIN ---
if not st.session_state.logged_in:
    # --- CSS KHUSUS ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        
        /* 1. BACKGROUND GRADASI BIRU */
        .stApp {
            background-color: #0064ac;
            background-image: linear-gradient(135deg, #0076c8 0%, #004b87 100%);
        }

        /* 2. HIDE ELEMENT BAWAAN */
        header, footer, [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

        /* 3. KARTU PUTIH */
        .block-container {
            background-color: #ffffff;
            width: 450px !important;
            max-width: 90% !important;
            padding: 2.5rem !important;
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
            margin: auto;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            zoom: 0.9; 
        }

        /* 4. FIX TEXT INPUT (SAMAKAN LEBAR & CEGAH TERPOTONG) */
        div[data-testid="stTextInput"] {
            width: 100% !important;
            margin-bottom: 20px !important;
        }

        /* Menargetkan kontainer oval agar selalu penuh 100% */
        div[data-testid="stTextInput"] > div {
            width: 100% !important;
        }
        
        div[data-testid="stTextInput"] > div > div {
            background-color: white !important;
            border: 2px solid #d1d5db !important;
            border-radius: 100px !important;
            height: 50px !important;
            padding: 0 15px !important;
            width: 100% !important; /* Paksa lebar penuh di sini */
            display: flex !important;
            align-items: center !important;
        }

        /* Menghilangkan border internal Streamlit yang sering bikin efek 'terpotong' */
        div[data-testid="stTextInput"] > div > div:focus-within {
            border-color: #005dab !important;
            box-shadow: 0 0 0 1px #005dab !important;
        }

        div[data-testid="stTextInput"] input {
            color: #333 !important;
            font-size: 15px !important;
            padding-left: 40px !important;
            height: 100% !important;
            width: 100% !important;
            border: none !important; /* Hapus border asli input agar tidak tumpang tindih */
        }

        /* 5. FIX TOMBOL LOGIN (DIBUAT FULL WIDTH) */
        div.stButton, div.stButton > button {
            width: 100% !important;
        }

        div.stButton > button {
            background-color: #003D79 !important;
            color: white !important;
            border-radius: 100px !important;
            height: 50px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            margin-top: 10px !important;
        }

        /* 5. FIX TOMBOL LOGIN (DIBUAT FULL WIDTH SEPERTI INPUT) */
        /* Menargetkan semua pembungkus tombol agar lebarnya 100% */
        div[data-testid="stVerticalBlock"] > div:has(div.stButton) {
            width: 100% !important;
        }

        div.stButton {
            width: 100% !important;
        }

        div.stButton > button {
            width: 100% !important; /* KUNCI: Menyamakan lebar dengan input */
            background-color: #003D79 !important;
            color: white !important;
            border-radius: 100px !important;
            height: 50px !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            border: none !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            margin: 0 !important;
        }

        div.stButton > button:hover {
            background-color: #002e59 !important;
            transform: translateY(-2px);
            color: white !important;
        }

        /* 6. IKON NIP & PASSWORD */
        div[data-testid="stTextInput"] input[type="text"] {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="%23999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 15px center !important;
        }
        
        div[data-testid="stTextInput"] input[type="password"] {
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="%23999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>') !important;
            background-repeat: no-repeat !important;
            background-position: 15px center !important;
        }

        .footer-secure {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            font-size: 12px;
            color: #888;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- TAMPILAN (LAYOUT) ---
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image("https://upload.wikimedia.org/wikipedia/id/thumb/f/fa/Bank_Mandiri_logo.svg/1200px-Bank_Mandiri_logo.svg.png", use_container_width=True)

    st.markdown("""
        <div style="text-align: center; margin-top: 15px; margin-bottom: 30px;">
            <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #000; font-family: 'Roboto', sans-serif;">
                Mandiri Compliance Smart Assistant
            </h3>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #666;">
                Secure On-Premise Login
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Menggunakan container untuk memastikan input dan tombol sejajar
    with st.container():
        nip = st.text_input("NIP", placeholder="NIP (Nomor Induk Pegawai)", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Kata Sandi", label_visibility="collapsed")
        
        # Tombol sekarang akan otomatis mengikuti lebar container berkat CSS di atas
        if st.button("Login"):
            if nip == "999" and password == "admin":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.switch_page("pages/Admin_Dashboard.py")
            else:
                try:
                    conn = sqlite3.connect('users.db')
                    c = conn.cursor()
                    c.execute("SELECT name, dept FROM staff WHERE nip=? AND password=?", (nip, password))
                    result = c.fetchone()
                    conn.close()
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.user_name = result[0]
                        st.session_state.role = "Staff"
                        st.switch_page("pages/Staff_Dashboard.py")
                    else:
                        st.error("NIP atau Kata Sandi salah!")
                except Exception as e:
                    st.error(f"Sistem Error: {e}")

    st.markdown("""
        <div class="footer-secure">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
            Koneksi Aman Terenkripsi
        </div>
    """, unsafe_allow_html=True)