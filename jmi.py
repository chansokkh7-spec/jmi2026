import streamlit as st
import pandas as pd
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់ទំព័រ (Configuration) ---
st.set_page_config(
    page_title="JMI | Executive Management Portal",
    page_icon="🏥",
    layout="wide"
)

# --- ២. រចនាប័ទ្មពណ៌ និង CSS (Custom Styling) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #001f3f; color: white; font-weight: bold; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-left: 5px solid #D4AF37; }
    .cert-container { border:10px solid #001f3f; padding:50px; text-align:center; background-color:white; border-radius:15px; position:relative; color: #001f3f; }
    .cert-inner { border:5px solid #D4AF37; padding:30px; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ផ្នែកចាត់ចែងទិន្នន័យ (Database Simulation) ---
# កំណត់ឱ្យរក្សាទុកទិន្នន័យបណ្ដោះអាសន្ន (Session State)
if 'students_db' not in st.session_state:
    # បង្កើតទិន្នន័យគំរូខ្លះៗ ដើម្បីឱ្យលោកបណ្ឌិតងាយស្រួលតេស្តមើល Certificate
    st.session_state.students_db = pd.DataFrame([
        {'ID': 'JMI-2026-001', 'Name': 'Sokhoeurn Sovannachak', 'Grade': 'G1-G3', 'Enroll_Date': '2026-03-01', 'Status': 'Active'}
    ])

# --- ៤. របារចំហៀង និងការផ្ទៀងផ្ទាត់ (Sidebar & Auth) ---
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.title("JMI STRATEGIC ACCESS")
access_code = st.sidebar.text_input("Academic Director Code", type="password", placeholder="••••••••")

if access_code == "JMI2026":
    st.sidebar.success("Welcome, Dr. CHAN Sokhoeurn")
    
    # ម៉ឺនុយបញ្ជា (Navigation)
    menu = st.sidebar.radio("MAIN MENU", 
                            ["📊 Dashboard", "🎓 Student Enrollment", "🏅 Skill Passport", "📜 Certification"])
    
    st.sidebar.markdown("---")
    if st.sidebar.button("LOGOUT SYSTEM"):
        st.rerun()

    # --- ៥. ទំព័រ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Management Dashboard")
        st.write(f"Logged in as: **Dr. CHAN Sokhoeurn, DBA**")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", len(st.session_state.students_db))
        col2.metric("Active Modules", "12")
        col3.metric("Capacity", "250", "Left: " + str(250 - len(st.session_state.students_db)))
        col4.metric("JMI Status", "Operational")
        
        st.markdown("### 📋 Recent Registrations")
        if not st.session_state.students_db.empty:
            st.dataframe(st.session_state.students_db, use_container_width=True)
        else:
            st.info("No students enrolled yet.")

    # --- ៦. ទំព័រចុះឈ្មោះ (Student Enrollment) ---
    elif menu == "🎓 Student Enrollment":
        st.header("Student Registration Portal")
        with st.form("enroll_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                s_name = st.text_input("Student Full Name", placeholder="Enter Name")
                s_id = st.text_input("Student ID", placeholder="JMI-2026-XXXX")
            with col_b:
                s_grade = st.selectbox("Grade Level", ["Kindergarten", "G1-G3", "G4-G6", "G7-G9", "G10-G12"])
                s_status = st.selectbox("Enrollment Status", ["Active", "On-Hold"])
            
            submitted = st.form_submit_button("REGISTER TO SYSTEM")
            
            if submitted:
                if s_name and s_id:
                    new_student = {
                        'ID': s_id, 'Name': s_name, 'Grade': s_grade, 
                        'Enroll_Date': datetime.now().strftime("%Y-%m-%d"), 'Status': s_status
                    }
                    st.session_state.students_db = pd.concat([st.session_state.students_db, pd.DataFrame([new_student])], ignore_index=True)
                    st.success(f"Student '{s_name}' has been successfully added to JMI Database!")
                else:
                    st.error("Please provide both Name and ID.")

    # --- ៧. ផ្នែក Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("Medical Skill Tracking")
        if not st.session_state.students_db.empty:
            target = st.selectbox("Select Student to Track:", st.session_state.students_db['Name'])
            st.info(f"Setting skills for: {target}")
            
            cols = st.columns(2)
            with cols[0]:
                st.checkbox("Hygiene & Sanitation")
                st.checkbox("Anatomy Basics")
            with cols[1]:
                st.checkbox("Emergency First Aid")
                st.checkbox("Medical Ethics")
            st.button("Update Passport")
        else:
            st.warning("Enroll students first to use this feature.")

    # --- ៨. ផ្នែកវិញ្ញាបនបត្រ (CERTIFICATION - FIXED) ---
    elif menu == "📜 Certification":
        st.header("📜 JMI Digital Certificate Generator")
        
        if not st.session_state.students_db.empty:
            st.write("ជ្រើសរើសសិស្សដើម្បី Preview និងបោះពុម្ពវិញ្ញាបនបត្រ៖")
            selected_name = st.selectbox("ស្វែងរកឈ្មោះសិស្ស:", st.session_state.students_db['Name'])
            
            # ទាញយកទិន្នន័យសិស្ស
            s_data = st.session_state.students_db[st.session_state.students_db['Name'] == selected_name].iloc[0]
            
            if st.button("GENERATE OFFICIAL CERTIFICATE"):
                st.balloons()
                # ការរចនាវិញ្ញាបនបត្រជា HTML
                cert_design = f"""
                <div class="cert-container">
                    <div class="cert-inner">
                        <h1 style="font-family:serif; font-size:45px; margin-bottom:10px;">CERTIFICATE</h1>
                        <h3 style="letter-spacing: 5px; margin-bottom:30px;">OF ACHIEVEMENT</h3>
                        <p style="font-size:20px; font-style:italic;">This is to officially certify that</p>
                        <h2 style="color:#D4AF37; font-size:40px; font-family: 'DM Sans'; margin:20px 0;">{s_data['Name']}</h2>
                        <p style="font-size:18px; line-height:1.6;">
                            has successfully demonstrated excellence and completed the <br>
                            <b>Medical Foundation Program ({s_data['Grade']})</b><br>
                            at the Junior Medical Institute.
                        </p>
                        <div style="margin-top:60px; display:flex; justify-content:space-around;">
                            <div style="text-align:center;">
                                <p style="border-top:2px solid #001f3f; padding-top:10px; width:200px;">
                                    {datetime.now().strftime("%B %d, %Y")}<br><b>Date of Issue</b>
                                </p>
                            </div>
                            <div style="text-align:center;">
                                <p style="border-top:2px solid #001f3f; padding-top:10px; width:200px;">
                                    Dr. CHAN Sokhoeurn, DBA<br><b>Academic Director</b>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_design, unsafe_allow_html=True)
                st.write("")
                st.info("💡 គន្លឹះ៖ លោកបណ្ឌិតអាចចុច Mouse ស្ដាំលើរូបវិញ្ញាបនបត្រ រួចយក 'Print' ដើម្បី Save ជា PDF ទុកជូនសិស្ស។")
        else:
            st.error("System Error: No student data found. Please enroll a student first.")

# --- ៩. ទំព័រចាក់សោ (Locked Screen) ---
else:
    st.title("🏥 JMI Strategic Portal")
    st.subheader("Junior Medical Institute Management System")
    st.write("---")
    st.warning("🔒 ផ្នែកនេះត្រូវបានរក្សាសិទ្ធិសម្រាប់តែថ្នាក់ដឹកនាំ JMI ប៉ុណ្ណោះ។")
    st.info("សូមបញ្ចូលលេខកូដសម្ងាត់នៅរបារខាងឆ្វេង ដើម្បីចូលទៅកាន់ប្រព័ន្ធគ្រប់គ្រង។")
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1000&q=80")
