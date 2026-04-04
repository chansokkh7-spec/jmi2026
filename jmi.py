import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import os

# --- ១. ការកំណត់ទម្រង់ទំព័រ (Master Configuration) ---
st.set_page_config(
    page_title="JMI | Executive Management Portal",
    page_icon="🏥",
    layout="wide"
)

# Function សម្រាប់បំលែងរូបភាព Logo ទៅជា Base64
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

logo_b64 = get_image_base64("logo.png")

# --- ២. រចនាប័ទ្ម CSS (កែសម្រួលដើម្បីកុំឱ្យលោត Error លើអេក្រង់) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
    /* UI Styling */
    .stApp { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.2em; background-color: #001f3f; color: white; font-weight: bold; border: none; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 6px solid #D4AF37; }
    
    /* Certificate Styling */
    .cert-outer-wrapper { background: #f0f0f0; padding: 30px; border-radius: 15px; display: flex; justify-content: center; }
    .cert-paper { background-color: white; border: 12px solid #001f3f; padding: 10px; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.2); width: 100%; max-width: 800px; }
    .cert-gold-border { border: 4px double #D4AF37; padding: 40px; text-align: center; }
    .cert-logo-img { width: 120px; margin-bottom: 15px; }
    .cert-title { font-family: 'Cinzel', serif; color: #001f3f; font-size: 40px; margin: 5px 0; letter-spacing: 5px; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 55px; color: #D4AF37; margin: 10px 0; font-weight: normal; }
    .cert-text { font-family: 'DM Serif Display', serif; font-size: 17px; color: #333; line-height: 1.6; }
    .signature-box { border-top: 1px solid #333; width: 180px; padding-top: 8px; margin: auto; font-family: serif; font-size: 14px; }
    .signature-font { font-family: 'Great Vibes', cursive; font-size: 30px; color: #001f3f; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame([
        {'ID': 'JMI-2026-001', 'Name': 'Sokhoeurn Sovannachak', 'Grade': 'G1-G3', 'Enroll_Date': '2026-03-25', 'Status': 'Active'}
    ])

# --- ៤. ប្រព័ន្ធសុវត្ថិភាព ---
st.sidebar.title("JMI EXECUTIVE PORTAL")
access_code = st.sidebar.text_input("Director's Access Key", type="password", placeholder="••••••••")

if access_code == "JMI2026":
    st.sidebar.success("Authorized: Dr. CHAN Sokhoeurn")
    menu = st.sidebar.radio("MAIN NAVIGATION", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Mastery", "📜 Certification"])
    
    if st.sidebar.button("🔒 LOGOUT"):
        st.rerun()

    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scholars", len(st.session_state.students_db))
        c2.metric("Available Seats", 250 - len(st.session_state.students_db))
        c3.metric("System Status", "Stable")
        st.dataframe(st.session_state.students_db, use_container_width=True)

    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            sid = st.text_input("Scholar ID")
            grade = st.selectbox("Academic Level", ["K-G3", "G4-G6", "G7-G9", "G10-G12"])
            if st.form_submit_button("SAVE ENROLLMENT"):
                if name and sid:
                    new_s = {'ID': sid, 'Name': name, 'Grade': grade, 'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': 'Active'}
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_s])], ignore_index=True)
                    st.success("Success!")

    elif menu == "📜 Certification":
        st.header("📜 Certificate Generator")
        target_name = st.selectbox("Select Scholar:", st.session_state.students_db['Name'])
        s_data = st.session_state.students_db[st.session_state.students_db['Name'] == target_name].iloc[0]
        
        if st.button("🌟 GENERATE CERTIFICATE"):
            # បង្កើត HTML សម្រាប់ Logo
            logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="cert-logo-img">' if logo_b64 else '<h2 style="color:#001f3f; font-family:Cinzel;">JMI</h2>'

            certificate_html = f"""
            <div class="cert-outer-wrapper">
                <div class="cert-paper">
                    <div class="cert-gold-border">
                        {logo_html}
                        <h3 style="font-family: 'Cinzel', serif; color: #001f3f; letter-spacing: 4px; margin: 0;">JUNIOR MEDICAL INSTITUTE</h3>
                        <div style="width: 60px; height: 2px; background: #D4AF37; margin: 12px auto;"></div>
                        <h1 class="cert-title">CERTIFICATE</h1>
                        <p class="cert-text" style="font-style: italic; margin-top: 20px;">This award is presented to</p>
                        <h2 class="student-name">{s_data['Name']}</h2>
                        <p class="cert-text">
                            for successful completion of the <br>
                            <strong style="color: #001f3f;">Medical Foundation Pathway ({s_data['Grade']})</strong>
                        </p>
                        <div style="margin-top: 40px; display: flex; justify-content: space-around; align-items: flex-end;">
                            <div style="text-align: center;">
                                <p style="margin-bottom: 5px; font-family: serif;">{datetime.now().strftime("%B %d, %Y")}</p>
                                <div class="signature-box">DATE OF ISSUE</div>
                            </div>
                            <div style="text-align: center;">
                                <p class="signature-font">Dr. Chan Sokhoeurn</p>
                                <div class="signature-box">Academic Director</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(certificate_html, unsafe_allow_html=True)

else:
    # ទំព័រ Lock (កែសម្រួលដើម្បីកុំឱ្យ Error)
    st.title("🏥 JMI Strategic Command Portal")
    st.warning("🔒 Restricted Access. Please enter Director's Key in the sidebar.")
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1200&q=80")
