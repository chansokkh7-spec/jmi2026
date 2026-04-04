import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់ទំព័រ (Executive Configuration) ---
st.set_page_config(
    page_title="JMI | Executive Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. រចនាប័ទ្ម CSS សម្រាប់ System និង Premium Certificate ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
    /* System Styling */
    .main { background-color: #f4f7f6; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #001f3f; color: white; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #D4AF37; color: #001f3f; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #D4AF37; }
    
    /* Certificate Styling */
    .cert-outer-wrapper { background-color: #e0e0e0; padding: 40px; border-radius: 15px; }
    .cert-paper { background-color: white; border: 15px solid #001f3f; padding: 20px; position: relative; box-shadow: 0 20px 40px rgba(0,0,0,0.3); max-width: 900px; margin: auto; }
    .cert-gold-border { border: 5px double #D4AF37; padding: 50px; text-align: center; }
    .cert-title { font-family: 'Cinzel', serif; color: #001f3f; font-size: 50px; margin: 10px 0; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 65px; color: #D4AF37; margin: 15px 0; font-weight: normal; }
    .cert-text { font-family: 'DM Serif Display', serif; font-size: 18px; color: #333; line-height: 1.6; }
    .official-seal { width: 110px; height: 110px; border: 3px double #D4AF37; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #D4AF37; font-family: 'Cinzel', serif; font-weight: bold; font-size: 13px; transform: rotate(-15deg); margin: auto; }
    .signature-font { font-family: 'Great Vibes', cursive; font-size: 30px; color: #001f3f; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ផ្នែកចាត់ចែងទិន្នន័យ (Session State Database) ---
if 'students_db' not in st.session_state:
    # បង្កើតទិន្នន័យគំរូសម្រាប់តេស្ត
    st.session_state.students_db = pd.DataFrame([
        {'ID': 'JMI-2026-001', 'Name': 'Sokhoeurn Sovannachak', 'Grade': 'G1-G3', 'Enroll_Date': '2026-03-25', 'Status': 'Active'}
    ])

# --- ៤. របារចំហៀង និងការផ្ទៀងផ្ទាត់ (Sidebar & Security) ---
st.sidebar.image("logo.png", use_container_width=True) # លោកបណ្ឌិតត្រូវមាន file logo.png ក្នុង github ដែរ
st.sidebar.title("JMI EXECUTIVE ACCESS")
access_code = st.sidebar.text_input("Director's Key", type="password", placeholder="••••••••")

if access_code == "JMI2026":
    st.sidebar.success(f"Director: Dr. CHAN Sokhoeurn")
    menu = st.sidebar.radio("STRATEGIC MODULES", 
                            ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Premium Certification"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("EXIT SYSTEM"):
        st.rerun()

    # --- ៥. ទំព័រ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Management")
        st.write("Welcome to the command center of **Junior Medical Institute**.")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scholars", len(st.session_state.students_db))
        c2.metric("Med-Modules", "12")
        c3.metric("Portal Capacity", "250")
        c4.metric("Academic Year", "2026")
        
        st.markdown("### 📋 Enrollment Overview")
        st.dataframe(st.session_state.students_db, use_container_width=True)

    # --- ៦. ទំព័រចុះឈ្មោះ (Enrollment) ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Scholar")
        with st.form("reg_form", clear_on_submit=True):
            col_1, col_2 = st.columns(2)
            with col_1:
                name = st.text_input("Full Name")
                sid = st.text_input("Scholar ID (e.g., JMI-2026-002)")
            with col_2:
                grade = st.selectbox("Grade Level", ["Kindergarten", "G1-G3", "G4-G6", "G7-G9", "G10-G12"])
                status = st.selectbox("Enrollment Type", ["Active Scholar", "Probation"])
            
            if st.form_submit_button("CONFIRM ENROLLMENT"):
                if name and sid:
                    new_entry = {'ID': sid, 'Name': name, 'Grade': grade, 'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': status}
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_entry])], ignore_index=True)
                    st.success(f"Scholar {name} successfully integrated into JMI.")
                else:
                    st.error("Missing critical information.")

    # --- ៧. ផ្នែក Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("Medical Skill Mastery")
        if not st.session_state.students_db.empty:
            sel_student = st.selectbox("Select Student:", st.session_state.students_db['Name'])
            st.info(f"Mastery Tracking for: {sel_student}")
            st.checkbox("Module 1: Clinical Hygiene")
            st.checkbox("Module 2: Human Anatomy Basics")
            st.checkbox("Module 3: Medical Ethics & Empathy")
            st.button("Save Progress")
        else:
            st.warning("No scholars found.")

    # --- ៨. ផ្នែកវិញ្ញាបនបត្រ (Premium Certification) ---
    elif menu == "📜 Premium Certification":
        st.header("📜 Generate Executive Certificate")
        if not st.session_state.students_db.empty:
            target_name = st.selectbox("Search Scholar:", st.session_state.students_db['Name'])
            student_data = st.session_state.students_db[st.session_state.students_db['Name'] == target_name].iloc[0]
            
            if st.button("🌟 GENERATE OFFICIAL DOCUMENT"):
                st.balloons()
                
                # Premium HTML Certificate Design
                certificate_html = f"""
                <div class="cert-outer-wrapper">
                    <div class="cert-paper">
                        <div class="cert-gold-border">
                            <h3 style="font-family: 'Cinzel', serif; color: #001f3f; letter-spacing: 6px; margin: 0;">JUNIOR MEDICAL INSTITUTE</h3>
                            <div style="width: 60px; height: 2px; background: #D4AF37; margin: 10px auto;"></div>
                            
                            <h1 class="cert-title">CERTIFICATE</h1>
                            <p class="cert-text" style="letter-spacing: 4px;">OF ACADEMIC EXCELLENCE</p>
                            
                            <p class="cert-text" style="margin-top: 25px; font-style: italic;">This prestigious award is presented to</p>
                            <h2 class="student-name">{student_data['Name']}</h2>
                            
                            <p class="cert-text">
                                for the successful completion of the <br>
                                <strong style="color: #001f3f; font-size: 20px;">Medical Foundation Pathway ({student_data['Grade']})</strong><br>
                                and demonstrating exceptional dedication to medical science.
                            </p>

                            <div style="margin-top: 40px; display: flex; justify-content: space-around; align-items: center;">
                                <div style="text-align: center;">
                                    <p class="cert-text" style="border-top: 1px solid #333; width: 160px; padding-top: 5px;">
                                        {datetime.now().strftime("%B %d, %Y")}<br><span style="font-size: 10px;">DATE</span>
                                    </p>
                                </div>
                                
                                <div class="official-seal">JMI<br>OFFICIAL<br>SEAL</div>

                                <div style="text-align: center;">
                                    <p class="signature-font">Dr. Chan Sokhoeurn</p>
                                    <p class="cert-text" style="border-top: 1px solid #333; width: 160px; padding-top: 5px;">
                                        Academic Director<br><span style="font-size: 10px;">JMI EXECUTIVE BOARD</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(certificate_html, unsafe_allow_html=True)
                st.write("")
                st.info("💡 Academic Director's Note: Right-click the certificate and select 'Print' to save as high-quality PDF.")
        else:
            st.error("Please enroll a scholar first.")

# --- ៩. ទំព័រចាក់សោ (Access Restricted) ---
else:
    st.title("🏥 JMI Strategic Portal")
    st.markdown("---")
    st.warning("🔒 This system is restricted to JMI Academic Directors.")
    st.info("Please enter your access credentials to proceed.")
