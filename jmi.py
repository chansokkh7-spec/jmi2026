import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- 1. SETTINGS & MEDICAL BRANDING UI ---
st.set_page_config(page_title="JMI Management System", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.05rem; }
    .main { background-color: #f8f9fa; }
    
    /* === JMI BRAND COLORS (Medical Blue & Clean White) === */
    [data-testid="stSidebar"] {
        background-color: #004a99 !important; 
    }
    
    .logo-container {
        background-color: white;
        padding: 15px;
        border-radius: 0 0 15px 15px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    
    /* Buttons - Medical Action Blue */
    .stButton>button { 
        width: 100%; border-radius: 8px; 
        background-color: #007bff !important; 
        color: white !important; font-weight: bold; 
        height: 45px; border: none;
    }
    
    /* Dashboard Cards */
    .metric-box { 
        background-color: white; padding: 20px; border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); 
        border-top: 5px solid #004a99;
        margin-bottom: 20px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA STORAGE ---
if 'jmi_db' not in st.session_state:
    st.session_state.jmi_db = []

# --- 3. HELPER FUNCTIONS ---
def to_excel_jmi(df, title):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='JMI_Data', startrow=4)
        workbook, worksheet = writer.book, writer.sheets['JMI_Data']
        fmt = workbook.add_format({'bold': True, 'font_size': 16, 'font_color': '#004a99'})
        worksheet.write('A1', 'Junior Medical Institute (JMI)', fmt)
        worksheet.write('A2', f'Report: {title}')
        worksheet.write('A3', f'Date: {datetime.now().strftime("%Y-%m-%d")}')
    return output.getvalue()

def add_student(name, grade, skill_lv, status):
    st.session_state.jmi_db.append({
        "ID": f"JMI-{len(st.session_state.jmi_db)+101}",
        "Student Name": name,
        "Grade Level": grade,
        "Skill Passport Level": skill_lv,
        "Enrollment Status": status,
        "Registration Date": datetime.now().strftime("%Y-%m-%d"),
        "Authorized By": st.session_state.get("role", "Admin")
    })
    st.rerun()

# --- 4. AUTHENTICATION ---
def check_auth():
    st.sidebar.markdown('<div class="logo-container"><h2 style="color:#004a99;margin:0;">JMI Portal</h2></div>', unsafe_allow_html=True)
    if "jmi_auth" not in st.session_state: st.session_state.jmi_auth = False
    
    if not st.session_state.jmi_auth:
        with st.sidebar.form("Login"):
            code = st.text_input("JMI Access Code", type="password")
            if st.form_submit_button("LOGIN"):
                if code == "JMI2026": # លេខកូដសម្ងាត់សម្រាប់ JMI
                    st.session_state.jmi_auth = True
                    st.session_state.role = "Academic Director"
                    st.rerun()
                else: st.sidebar.error("Invalid Code")
        return False
    return True

if not check_auth(): st.stop()

# --- 5. NAVIGATION ---
st.sidebar.markdown("### 📋 MANAGEMENT")
menu = st.sidebar.radio("", ["📊 Dashboard", "🎓 Student Enrollment", "🧬 Skill Passport", "📜 Certification"])

if st.sidebar.button("🚪 LOGOUT"):
    st.session_state.jmi_auth = False
    st.rerun()

# --- 6. HEADER ---
st.markdown(f"""
    <div style="display: flex; align-items: center;">
        <h1 style="color: #004a99;">Junior Medical Institute</h1>
        <span style="margin-left: 20px; padding: 5px 15px; background: #e3f2fd; border-radius: 20px; color: #004a99; font-weight: bold;">
            {st.session_state.role} Mode
        </span>
    </div>
    <p style="color: #666;">Pre-Med from Kindergarten to Grade 12 Excellence</p>
""", unsafe_allow_html=True)
st.divider()

# --- 7. DATABASE PREP ---
df = pd.DataFrame(st.session_state.jmi_db) if st.session_state.jmi_db else pd.DataFrame(columns=["ID", "Student Name", "Grade Level", "Skill Passport Level", "Enrollment Status", "Registration Date"])

# --- 8. MODULES ---

if menu == "📊 Dashboard":
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='metric-box'>👨‍⚕️ Total Students<br><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-box'>🧬 Active Skills<br><h2>{len(df[df['Skill Passport Level'] != 'None'])}</h2></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'>🏫 K-Grade 6<br><h2>{len(df[df['Grade Level'].isin(['Kindergarten', 'Primary'])])}</h2></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='metric-box'>🏥 Capacity<br><h2>250</h2></div>", unsafe_allow_html=True)
    
    st.write("### 📂 Recent Registrations")
    st.dataframe(df, use_container_width=True)
    if not df.empty:
        st.download_button("📥 Download Master Student List", data=to_excel_jmi(df, "Master List"), file_name="JMI_Students.xlsx")

elif menu == "🎓 Student Enrollment":
    st.subheader("New Student Registration")
    with st.form("enroll"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        grade = c2.selectbox("Grade Category", ["Kindergarten", "Primary (G1-G6)", "Secondary (G7-G12)"])
        status = c1.selectbox("Status", ["Enrolled", "Waiting List"])
        skill = c2.selectbox("Initial Skill Level", ["Beginner", "Intermediate", "Advanced"])
        if st.form_submit_button("Register Student"):
            if name: add_student(name, grade, skill, status)

elif menu == "🧬 Skill Passport":
    st.subheader("Medical Skill Tracking")
    if df.empty: st.info("No students registered yet.")
    else:
        target_student = st.selectbox("Select Student", df["Student Name"].tolist())
        st.info(f"Updating Skill Passport for: **{target_student}**")
        col1, col2, col3 = st.columns(3)
        col1.checkbox("Anatomy Basics")
        col1.checkbox("First Aid Level 1")
        col2.checkbox("Nutrition Science")
        col2.checkbox("Microbiology Intro")
        col3.checkbox("Medical Ethics")
        col3.checkbox("Lab Safety")
        st.button("Update Passport")

elif menu == "📜 Certification":
    st.subheader("Certificate Issuance")
    if df.empty: st.info("No data available for certification.")
    else:
        st.write("Select students to issue digital certificates:")
        st.dataframe(df[["ID", "Student Name", "Grade Level"]])
        st.button("Generate Digital Certificates (Bulk)")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.info("v1.0 | JMI Strategic Portal\nDr. CHAN Sokhoeurn, DBA")
