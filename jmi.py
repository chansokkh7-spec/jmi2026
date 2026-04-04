import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់ទំព័រ (Configuration) ---
st.set_page_config(
    page_title="JMI | Executive Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. រចនាប័ទ្មពណ៌ (Custom Styling) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #001f3f; color: white; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ផ្នែកចាត់ចែងទិន្នន័យ (Session State) ---
if 'students_db' not in st.session_state:
    st.session_state.students_db = pd.DataFrame(columns=['ID', 'Name', 'Grade', 'Enroll_Date', 'Status'])

# --- ៤. របារចំហៀង និងការផ្ទៀងផ្ទាត់ (Sidebar & Auth) ---
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.title("JMI ACCESS")
access_code = st.sidebar.text_input("Access Code", type="password", placeholder="Enter Code Here")

if access_code == "JMI2026":
    st.sidebar.success("Authorized: Dr. CHAN Sokhoeurn")
    
    # ម៉ឺនុយបញ្ជា (Navigation)
    menu = st.sidebar.radio("MANAGEMENT MENU", 
                            ["📊 Dashboard", "🎓 Student Enrollment", "🏅 Skill Passport", "📜 Certification"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("LOGOUT"):
        st.rerun()

    # --- ៥. ទំព័រ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Dashboard")
        st.write(f"Welcome back, **Dr. CHAN Sokhoeurn**. Monitoring JMI growth and excellence.")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", len(st.session_state.students_db))
        col2.metric("Active Modules", "12")
        col3.metric("Capacity", "250", "Full")
        col4.metric("System Version", "1.0.2")
        
        st.markdown("### Recent Activities")
        if len(st.session_state.students_db) > 0:
            st.table(st.session_state.students_db.tail(5))
        else:
            st.info("No student data available yet.")

    # --- ៦. ទំព័រចុះឈ្មោះ (Student Enrollment) ---
    elif menu == "🎓 Student Enrollment":
        st.header("Student Registration Portal")
        with st.form("enroll_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                s_name = st.text_input("Student Full Name", placeholder="e.g. Sokhoeurn Sovannachak")
                s_id = st.text_input("Student ID", placeholder="JMI-2026-XXXX")
            with col_b:
                s_grade = st.selectbox("Grade Level", ["Kindergarten", "G1-G3", "G4-G6", "G7-G9", "G10-G12"])
                s_status = st.selectbox("Status", ["Active", "On-Hold"])
            
            submitted = st.form_submit_button("Register New Student")
            
            if submitted:
                if s_name and s_id:
                    new_student = {
                        'ID': s_id, 'Name': s_name, 'Grade': s_grade, 
                        'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': s_status
                    }
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                    st.success(f"Successfully registered {s_name}!")
                else:
                    st.error("Please fill in all required fields.")

    # --- ៧. ផ្នែក Skill Passport (សម្រាប់ពេទ្យក្មេង) ---
    elif menu == "🏅 Skill Passport":
        st.header("Medical Skill Tracking")
        st.write("Monitor student's progress in medical foundation skills.")
        if len(st.session_state.students_db) > 0:
            target_student = st.selectbox("Select Student", st.session_state.students_db['Name'])
            st.info(f"Tracking skills for: {target_student}")
            
            # ឧទាហរណ៍ជំនាញ
            skills = ["Basic Hygiene", "Anatomy Basics", "First Aid", "Medical Ethics"]
            for s in skills:
                st.checkbox(f"Module: {s}")
        else:
            st.warning("Please enroll students first.")

    # --- ៨. ផ្នែកវិញ្ញាបនបត្រ (Certification) ---
    elif menu == "📜 Certification":
        st.header("Certificate Generator")
        st.write("Generate and issue digital certificates for JMI graduates.")
        st.button("Preview Certificate Template")

# --- ៩. ករណីមិនទាន់មានលេខកូដ ---
else:
    st.title("🏥 JMI Strategic Portal")
    st.markdown("""
        ### Junior Medical Institute (JMI)
        *Pre-Med from Kindergarten to Grade 12 Excellence*
        
        ---
        **Access Restricted:** Please enter the Academic Director's Access Code in the sidebar to enter the management system.
    """)
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="Developing the next generation of medical leaders.")
