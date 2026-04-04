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

# --- ២. រចនាប័ទ្ម CSS (Global Styling & Certificate) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
    /* UI Styling */
    .main { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.2em; background-color: #001f3f; color: white; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #D4AF37; color: #001f3f; border: 1px solid #001f3f; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 6px solid #D4AF37; }
    
    /* Certificate Styling */
    .cert-outer-wrapper { background: linear-gradient(135deg, #e0e0e0 0%, #ffffff 100%); padding: 50px; border-radius: 15px; display: flex; justify-content: center; }
    .cert-paper { background-color: white; border: 12px solid #001f3f; padding: 15px; position: relative; box-shadow: 0 25px 50px rgba(0,0,0,0.25); width: 850px; }
    .cert-gold-border { border: 4px double #D4AF37; padding: 45px; text-align: center; }
    
    .cert-logo { width: 110px; margin-bottom: 20px; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.1)); }
    .cert-title { font-family: 'Cinzel', serif; color: #001f3f; font-size: 44px; margin: 5px 0; letter-spacing: 6px; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 62px; color: #D4AF37; margin: 15px 0; font-weight: normal; text-shadow: 1px 1px 2px rgba(0,0,0,0.05); }
    .cert-text { font-family: 'DM Serif Display', serif; font-size: 18px; color: #333; line-height: 1.7; }
    .signature-box { border-top: 1px solid #333; width: 180px; padding-top: 8px; margin: auto; }
    .signature-font { font-family: 'Great Vibes', cursive; font-size: 32px; color: #001f3f; margin-bottom: -12px; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Data Persistence) ---
if 'students_db' not in st.session_state:
    # បញ្ជីឈ្មោះសិស្សដំបូង (អាចចុះឈ្មោះថែមបានតាមចិត្ត)
    st.session_state.students_db = pd.DataFrame([
        {'ID': 'JMI-2026-001', 'Name': 'Sokhoeurn Sovannachak', 'Grade': 'G1-G3', 'Enroll_Date': '2026-03-25', 'Status': 'Active'}
    ])

# --- ៤. ប្រព័ន្ធសុវត្ថិភាព និងម៉ឺនុយ (Security & Navigation) ---
st.sidebar.title("JMI EXECUTIVE PORTAL")
access_code = st.sidebar.text_input("Director's Access Key", type="password", placeholder="••••••••")

if access_code == "JMI2026":
    st.sidebar.success(f"Director: Dr. CHAN Sokhoeurn")
    menu = st.sidebar.radio("MAIN NAVIGATION", 
                            ["📊 Executive Dashboard", "🎓 Student Enrollment", "🏅 Skill Mastery", "📜 Digital Certification"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 LOGOUT"):
        st.rerun()

    # --- ៥. ទំព័រ Dashboard (ពិនិត្យគ្រប់ចំនួនសិស្ស) ---
    if menu == "📊 Executive Dashboard":
        st.title("🏥 JMI Management Command Center")
        st.write(f"រាយការណ៍ទិន្នន័យគិតត្រឹមថ្ងៃទី៖ **{datetime.now().strftime('%d %B %Y')}**")
        
        c1, c2, c3, c4 = st.columns(4)
        total_s = len(st.session_state.students_db)
        c1.metric("Total Scholars", total_s)
        c2.metric("Available Seats", 250 - total_s)
        c3.metric("Medical Modules", "12")
        c4.metric("System Status", "Stable")
        
        st.markdown("### 📋 Current Enrollment List")
        st.dataframe(st.session_state.students_db, use_container_width=True)

    # --- ៦. ទំព័រចុះឈ្មោះ (ពិនិត្យការបញ្ចូលទិន្នន័យ) ---
    elif menu == "🎓 Student Enrollment":
        st.header("Register New Scholar to JMI")
        with st.form("enroll_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Scholar's Full Name")
                sid = st.text_input("Assigned ID (e.g. JMI-2026-XXX)")
            with col2:
                grade = st.selectbox("Academic Level", ["K-G3", "G4-G6", "G7-G9", "G10-G12"])
                status = st.selectbox("Enrollment Status", ["Active", "Probation", "On-Hold"])
            
            if st.form_submit_button("✅ CONFIRM & SAVE ENROLLMENT"):
                if name and sid:
                    new_student = {
                        'ID': sid, 'Name': name, 'Grade': grade, 
                        'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': status
                    }
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                    st.success(f"Scholar '{name}' has been successfully added to the database.")
                else:
                    st.warning("Please enter both Name and ID to proceed.")

    # --- ៧. ទំព័រ Skill Mastery (ពិនិត្យជំនាញ) ---
    elif menu == "🏅 Skill Mastery":
        st.header("Medical Skill Tracking")
        if not st.session_state.students_db.empty:
            sel_student = st.selectbox("Select Scholar to evaluate:", st.session_state.students_db['Name'])
            st.info(f"Setting Mastery Levels for: **{sel_student}**")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.checkbox("Clinical Hygiene & Safety")
                st.checkbox("Anatomy Foundation")
            with col_s2:
                st.checkbox("Emergency Response (First Aid)")
                st.checkbox("Medical Ethics & Empathy")
            
            if st.button("Update Scholar's Passport"):
                st.toast("Data updated successfully!")
        else:
            st.error("No student data found. Please enroll a student first.")

    # --- ៨. ទំព័រវិញ្ញាបនបត្រ (ពិនិត្យ Logo និងការ Print) ---
    elif menu == "📜 Digital Certification":
        st.header("📜 JMI Executive Certificate Generator")
        if not st.session_state.students_db.empty:
            target_name = st.selectbox("Select Scholar for Certification:", st.session_state.students_db['Name'])
            s_data = st.session_state.students_db[st.session_state.students_db['Name'] == target_name].iloc[0]
            
            if st.button("🌟 GENERATE HIGH-QUALITY CERTIFICATE"):
                st.balloons()
                
                # បង្កើត HTML សម្រាប់ Logo (ប្រសិនបើគ្មាន Logo វានឹងបង្ហាញអក្សរ JMI ជំនួស)
                if logo_b64:
                    logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="cert-logo">'
                else:
                    logo_html = '<h2 style="color:#001f3f; font-family:Cinzel; margin-bottom:20px;">JMI</h2>'

                certificate_html = f"""
                <div class="cert-outer-wrapper">
                    <div class="cert-paper">
                        <div class="cert-gold-border">
                            {logo_html}
                            <h3 style="font-family: 'Cinzel', serif; color: #001f3f; letter-spacing: 5px; margin: 0;">JUNIOR MEDICAL INSTITUTE</h3>
                            <div style="width: 60px; height: 2px; background: #D4AF37; margin: 12px auto;"></div>
                            
                            <h1 class="cert-title">CERTIFICATE</h1>
                            <p class="cert-text" style="letter-spacing: 4px; font-weight: bold; color: #555;">OF EXCELLENCE & ACHIEVEMENT</p>
                            
                            <p class="cert-text" style="margin-top: 25px; font-style: italic;">This prestigious award is proudly presented to</p>
                            <h2 class="student-name">{s_data['Name']}</h2>
                            
                            <p class="cert-text">
                                for the successful mastery and completion of the <br>
                                <strong style="color: #001f3f; font-size: 22px;">Medical Foundation Pathway ({s_data['Grade']})</strong><br>
                                proving readiness for future medical leadership and excellence.
                            </p>

                            <div style="margin-top: 50px; display: flex; justify-content: space-around; align-items: flex-end;">
                                <div style="text-align: center;">
                                    <p class="cert-text" style="font-size: 14px; margin-bottom: 5px;">{datetime.now().strftime("%B %d, %Y")}</p>
                                    <div class="signature-box">DATE OF ISSUE</div>
                                </div>
                                <div style="text-align: center;">
                                    <p class="signature-font">Dr. Chan Sokhoeurn</p>
                                    <div class="signature-box">
                                        Academic Director<br><span style="font-size: 10px;">JMI STRATEGIC BOARD</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(certificate_html, unsafe_allow_html=True)
                st.write("")
                st.info("💡 **Director's Tip:** To save this certificate, **Right-Click** on it and select **'Print'**, then choose **'Save as PDF'** for a high-resolution version.")
        else:
            st.error("Access Denied: Please add a student to the system first.")

# --- ៩. ទំព័រ Locked (ប្រសិនបើគ្មាន Key) ---
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.markdown("---")
    st.warning("🔒 **Security Notice:** This system is encrypted and restricted to the JMI Executive Board.")
    st.info("Please enter the **Academic Director's Key** in the sidebar to gain access.")
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1200&q=80", caption="Developing the next generation of medical leaders.")
