import streamlit as st

def apply_mandiri_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }
        
        /* Warna Sidebar Biru Mandiri */
        [data-testid="stSidebar"] {
            background-color: #003d79;
        }
        
    
        </style>
        """, unsafe_allow_html=True)