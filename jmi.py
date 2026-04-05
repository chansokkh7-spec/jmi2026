import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# --- ១. Config ---
st.set_page_config(page_title="JMI Portal", page_icon="🏥", layout="wide")

# --- ២. CSS (បំបែកដាច់ដោយឡែកដើម្បីកុំឱ្យរាយប៉ាយលើអេក្រង់) ---
style_block = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Kantumruy+Pro:wght@400;700&display=swap');
    html, body, [class*="css"], .stMarkdown { font-family: 'Kantumruy Pro', sans-serif; }
    .stApp { background-color: #f8f9fa; }
    .cert-paper { 
        background: white; border: 10px solid #001f3f; padding: 30px; 
        text-align: center; max-width: 750px; margin: auto; 
        border-radius: 10px; box-shadow: 0 15px 40px rgba(0,0,0,0.2); 
    }
    .student-name { color: #D4AF37; font-size: 45px; font-weight: bold; margin: 20px 0; }
</style>
"""
st.markdown(style_block, unsafe_allow_html=True)

# --- ៣. ទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([{"ID": "JMI-001", "Name": "Sokhoeurn Sovannachak", "Level": "K-G3", "Skills": []}])

# --- ៤. Sidebar ---
st.sidebar.title("JMI EXECUTIVE")
st.sidebar.markdown("<center><h1 style='font-size:70px;'>🏥</h1></center>", unsafe_allow_html=True)
pwd = st.sidebar.text_input("Director's Key", type="password")

# --- ៥. Logic ដំណើរការ ---
if pwd == "JMI2026":
    menu = st.sidebar.radio("MENU", ["📊 Dashboard", "🎓 Enrollment", "📜 Certification"])
    
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Command Center")
        st.dataframe(st.session_state.db.drop(columns=['Skills']), use_container_width=True)
        
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("reg"):
            name = st.text_input("Full Name")
            sid = st.text_input("Scholar ID")
            if st.form_submit_button("✅ SAVE"):
                if name and sid:
                    new_st = pd.DataFrame([{"ID": sid, "Name": name, "Level": "K-G3", "Skills": []}])
                    st.session_state.db = pd.concat([st.session_state.db, new_st], ignore_index=True)
                    st.success("Done!")
                
    elif menu == "📜 Certification":
        st.header("Certificate Generator")
        sel = st.selectbox("Select Student", st.session_state.db['Name'])
        if st.button("🌟 GENERATE"):
            st.balloons()
            st.markdown(f"""
            <div class="cert-paper">
                <h1 style="color:#001f3f; letter-spacing:5px;">CERTIFICATE</h1>
                <p style="font-style:italic;">This is to certify that</p>
                <div class="student-name">{sel}</div>
                <p>has successfully mastered the Medical Foundation Pathway.</p>
                <div style="margin-top:50px;">
                    <p><b>Dr. Chan Sokhoeurn</b></p>
                    <p style="font-size:12px; border-top:1px solid #333; width:200px; margin:auto;">ACADEMIC DIRECTOR</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("🔒 សូមបញ្ចូល Password 'JMI2026' នៅខាងឆ្វេង។")
