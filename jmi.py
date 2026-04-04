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

    # --- ៨. ផ្នែកវិញ្ញាបនបត្រ (CERTIFICATION - PREMIUM DESIGN) ---
    elif menu == "📜 Certification":
        st.header("📜 JMI Executive Certificate Generator")
        
        if not st.session_state.students_db.empty:
            st.write("ជ្រើសរើសសិស្សដើម្បីចេញវិញ្ញាបនបត្រកម្រិត Premium៖")
            selected_name = st.selectbox("ស្វែងរកឈ្មោះសិស្ស:", st.session_state.students_db['Name'])
            s_data = st.session_state.students_db[st.session_state.students_db['Name'] == selected_name].iloc[0]
            
            if st.button("🌟 GENERATE PREMIUM CERTIFICATE"):
                st.balloons()
                
                # រចនាប័ទ្មវិញ្ញាបនបត្រកម្រិតខ្ពស់
                cert_design = f"""
                <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
                
                <div style="background-color: #e0e0e0; padding: 30px; border-radius: 10px;">
                    <div style="background-color: white; border: 15px solid #001f3f; padding: 20px; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                        
                        <div style="border: 5px double #D4AF37; padding: 40px; text-align: center; position: relative;">
                            
                            <h3 style="font-family: 'Cinzel', serif; color: #001f3f; letter-spacing: 8px; margin: 0;">JUNIOR MEDICAL INSTITUTE</h3>
                            <div style="width: 80px; height: 2px; background: #D4AF37; margin: 15px auto;"></div>
                            
                            <h1 style="font-family: 'Cinzel', serif; color: #001f3f; font-size: 45px; margin: 20px 0;">CERTIFICATE</h1>
                            <p style="font-family: 'DM Serif Display', serif; font-size: 20px; color: #555; letter-spacing: 3px;">OF COMPLETION AND EXCELLENCE</p>
                            
                            <p style="font-family: 'DM Serif Display', serif; font-size: 18px; font-style: italic; margin-top: 30px;">This prestigious award is proudly presented to</p>
                            
                            <h2 style="font-family: 'Great Vibes', cursive; font-size: 60px; color: #D4AF37; margin: 10px 0; font-weight: normal;">{s_data['Name']}</h2>
                            
                            <div style="width: 400px; height: 1px; background: #ccc; margin: 0 auto;"></div>
                            
                            <p style="font-family: 'DM Serif Display', serif; font-size: 18px; color: #333; line-height: 1.8; margin-top: 20px;">
                                for outstanding academic achievement and successful mastery of the<br>
                                <strong style="color: #001f3f; font-size: 22px;">Medical Foundation Program ({s_data['Grade']})</strong><br>
                                demonstrating the skills and ethics required for future medical leadership.
                            </p>

                            <div style="margin-top: 50px; display: flex; justify-content: space-around; align-items: center;">
                                <div style="text-align: center;">
                                    <p style="font-family: 'DM Serif Display', serif; border-top: 1px solid #333; padding-top: 5px; width: 180px;">
                                        {datetime.now().strftime("%B %d, %Y")}<br>
                                        <span style="font-size: 12px; color: #777;">DATE OF ISSUANCE</span>
                                    </p>
                                </div>
                                
                                <div style="width: 100px; height: 100px; border: 3px double #D4AF37; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #D4AF37; font-family: 'Cinzel', serif; font-weight: bold; font-size: 12px; transform: rotate(-15deg);">
                                    OFFICIAL<br>SEAL
                                </div>

                                <div style="text-align: center;">
                                    <p style="font-family: 'Great Vibes', cursive; font-size: 28px; color: #001f3f; margin-bottom: -10px;">Dr. Chan Sokhoeurn</p>
                                    <p style="font-family: 'DM Serif Display', serif; border-top: 1px solid #333; padding-top: 5px; width: 180px;">
                                        Academic Director<br>
                                        <span style="font-size: 12px; color: #777;">JMI STRATEGIC BOARD</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_design, unsafe_allow_html=True)
                st.info("💡 ប្រព័ន្ធបានរៀបចំ Template កម្រិត HD។ លោកបណ្ឌិតអាច Print ជា PDF ដើម្បីទទួលបានគុណភាពច្បាស់បំផុត។")
        else:
            st.error("មិនទាន់មានទិន្នន័យសិស្ស។ សូមចុះឈ្មោះសិស្សជាមុនសិន។")
# --- ៩. ទំព័រចាក់សោ (Locked Screen) ---
else:
    st.title("🏥 JMI Strategic Portal")
    st.subheader("Junior Medical Institute Management System")
    st.write("---")
    st.warning("🔒 ផ្នែកនេះត្រូវបានរក្សាសិទ្ធិសម្រាប់តែថ្នាក់ដឹកនាំ JMI ប៉ុណ្ណោះ។")
    st.info("សូមបញ្ចូលលេខកូដសម្ងាត់នៅរបារខាងឆ្វេង ដើម្បីចូលទៅកាន់ប្រព័ន្ធគ្រប់គ្រង។")
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1000&q=80")
