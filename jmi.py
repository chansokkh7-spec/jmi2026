import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# --- ១. ការកំណត់ទម្រង់ទំព័រ ---
st.set_page_config(page_title="JMI | Executive Management Portal", page_icon="🏥", layout="wide")

# បង្កើត Function សម្រាប់បំលែងរូបភាពទៅជាស្ទីលដែលអាចប្រើក្នុង HTML បាន
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return None

logo_base64 = get_image_base64("logo.png")

# --- ២. រចនាប័ទ្ម CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
    .stButton>button { width: 100%; border-radius: 8px; background-color: #001f3f; color: white; font-weight: bold; }
    .cert-outer-wrapper { background-color: #e0e0e0; padding: 40px; border-radius: 15px; }
    .cert-paper { background-color: white; border: 15px solid #001f3f; padding: 20px; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.3); max-width: 850px; margin: auto; }
    .cert-gold-border { border: 5px double #D4AF37; padding: 40px; text-align: center; }
    .logo-img { width: 100px; margin-bottom: 10px; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 60px; color: #D4AF37; margin: 10px 0; }
    .cert-title { font-family: 'Cinzel', serif; color: #001f3f; font-size: 40px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ទិន្នន័យ (Session State) ---
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame([
        {'ID': 'JMI-2026-001', 'Name': 'Sokhoeurn Sovannachak', 'Grade': 'G1-G3', 'Enroll_Date': '2026-03-25', 'Status': 'Active'}
    ])

# --- ៤. របារចំហៀង ---
st.sidebar.title("JMI EXECUTIVE ACCESS")
access_code = st.sidebar.text_input("Director's Key", type="password")

if access_code == "JMI2026":
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "📜 Certification"])

    if menu == "📊 Dashboard":
        st.title("🏥 JMI Management Dashboard")
        st.dataframe(st.session_state.students_db, use_container_width=True)

    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("reg_form"):
            name = st.text_input("Full Name")
            sid = st.text_input("Scholar ID")
            grade = st.selectbox("Grade Level", ["G1-G3", "G4-G6", "G7-G9", "G10-G12"])
            if st.form_submit_button("CONFIRM ENROLLMENT"):
                new_entry = {'ID': sid, 'Name': name, 'Grade': grade, 'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': 'Active'}
                st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Scholar {name} enrolled!")

    elif menu == "📜 Certification":
        st.header("📜 Generate Official Certificate")
        target_name = st.selectbox("Search Scholar:", st.session_state.students_db['Name'])
        student_data = st.session_state.students_db[st.session_state.students_db['Name'] == target_name].iloc[0]
        
        if st.button("🌟 GENERATE WITH LOGO"):
            st.balloons()
            
            # បង្កើតកូដ HTML សម្រាប់ Logo
            logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="logo-img">' if logo_base64 else '<h2 style="color:#001f3f;">JMI</h2>'
            
            certificate_html = f"""
            <div class="cert-outer-wrapper">
                <div class="cert-paper">
                    <div class="cert-gold-border">
                        {logo_html}
                        <h3 style="font-family: 'Cinzel', serif; color: #001f3f; letter-spacing: 4px; margin: 0;">JUNIOR MEDICAL INSTITUTE</h3>
                        <div style="width: 50px; height: 2px; background: #D4AF37; margin: 10px auto;"></div>
                        
                        <h1 class="cert-title">CERTIFICATE</h1>
                        <p style="font-family: serif; font-size: 18px; letter-spacing: 3px; color: #555;">OF EXCELLENCE</p>
                        
                        <p style="font-family: serif; font-size: 16px; font-style: italic; margin-top: 20px;">This is to certify that</p>
                        <h2 class="student-name">{student_data['Name']}</h2>
                        
                        <p style="font-family: serif; font-size: 16px; color: #333;">
                            has successfully completed the <b>Medical Foundation Pathway ({student_data['Grade']})</b><br>
                            at the Junior Medical Institute.
                        </p>

                        <div style="margin-top: 40px; display: flex; justify-content: space-around; align-items: center;">
                            <div style="text-align: center;">
                                <p style="font-family: serif; border-top: 1px solid #333; width: 150px; padding-top: 5px;">
                                    {datetime.now().strftime("%B %d, %Y")}<br><span style="font-size: 10px;">DATE</span>
                                </p>
                            </div>
                            <div style="text-align: center;">
                                <p style="font-family: 'Great Vibes', cursive; font-size: 25px; color: #001f3f; margin-bottom: -10px;">Dr. Chan Sokhoeurn</p>
                                <p style="font-family: serif; border-top: 1px solid #333; width: 150px; padding-top: 5px;">
                                    Academic Director<br><span style="font-size: 10px;">EXECUTIVE BOARD</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
            st.markdown(certificate_html, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Portal")
    st.info("សូមបញ្ចូលលេខកូដសម្ងាត់ដើម្បីបន្ត។")
