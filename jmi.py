import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី (Executive Configuration) ---
st.set_page_config(
    page_title="JMI | Strategic Management Portal",
    page_icon="🏥",
    layout="wide"
)

# មុខងារទាញរូបភាព Logo (Base64)
def get_logo_64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_code = get_logo_64("logo.png")

# --- ២. ការរចនា Style (Premium Executive CSS - បញ្ចូលគ្នា និងដោះស្រាយបញ្ហា Syntax) ---
# ចំណុចសំខាន់៖ ត្រូវប្រើ {{ }} ក្នុង CSS ដើម្បីកុំឱ្យ Python ច្រឡំជាមួយ f-string
st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&family=Kantumruy+Pro:wght@400;700&display=swap" rel="stylesheet">
    <style>
    /* កំណត់ Font ខ្មែរ និងឡាតាំងឱ្យមានសោភ័ណភាព */
    html, body, [class*="css"], .stMarkdown {{
        font-family: 'Kantumruy Pro', sans-serif;
    }}
    
    .stApp {{ background-color: #f8f9fa; }}
    
    /* Star Styling */
    .star-gold {{ color: #D4AF37; font-size: 25px; margin-right: 3px; }}
    .star-gray {{ color: #e0e0e0; font-size: 25px; margin-right: 3px; }}
    
    /* Premium Certificate Style */
    .cert-paper {{ 
        background-color: white; 
        border: 12px solid #001f3f; 
        padding: 10px; 
        box-shadow: 0 25px 50px rgba(0,0,0,0.3); 
        max-width: 850px; 
        margin: 30px auto; 
    }}
    .cert-border {{ border: 4px double #D4AF37; padding: 45px; text-align: center; }}
    .cert-header {{ font-family: 'Cinzel', serif; color: #001f3f; font-size: 45px; margin: 0; letter-spacing: 5px; }}
    .student-name {{ font-family: 'Great Vibes', cursive; font-size: 60px; color: #D4AF37; margin: 15px 0; font-weight: normal; }}
    .cert-text {{ font-family: 'DM Serif Display', serif; font-size: 19px; color: #333; line-height: 1.6; }}
    .signature {{ font-family: 'Great Vibes', cursive; font-size: 35px; color: #001f3f; margin-bottom: -15px; }}
    .sig-box {{ border-top: 1px solid #333; width: 200px; margin: auto; padding-top: 5px; font-family: serif; font-size: 14px; color: #333; }}
    
    /* លាក់ Header/Footer មិនចាំបាច់របស់ Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ (Database Persistence) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {
            "ID": "JMI-2026-001", 
            "Name": "Sokhoeurn Sovannachak", 
            "Level": "K-G3", 
            "Enroll_Date": "2026-03-25", 
            "Status": "Active",
            "Skills": ["Human Anatomy Basics"]
        }
    ])

# ធានាថាមាន Column Skills ជានិច្ច
if "Skills" not in st.session_state.db.columns:
    st.session_state.db["Skills"] = [[] for _ in range(len(st.session_state.db))]

# --- ៤. របារចំហៀងសុវត្ថិភាព (Sidebar Security) ---
st.sidebar.markdown(f"<h1 style='text-align: center; color: #001f3f;'>JMI EXECUTIVE</h1>", unsafe_allow_html=True)

if logo_code:
    st.sidebar.markdown(f'<center><img src="data:image/png;base64,{logo_code}" width="120"></center>', unsafe_allow_html=True)
else:
    st.sidebar.markdown("<center><h1 style='font-size:70px;'>🏥</h1></center>", unsafe_allow_html=True)

st.sidebar.markdown("---")
key = st.sidebar.text_input("Director's Key", type="password", placeholder="Enter Password")

# --- ៥. លក្ខខណ្ឌចូលប្រើប្រាស់ប្រព័ន្ធ ---
if key == "JMI2026":
    st.sidebar.success(f"Director: Dr. CHAN Sokhoeurn")
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # --- ៥.១ Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scholars", len(st.session_state.db))
        c2.metric("Med-Modules", "12 Units")
        c3.metric("Blue Ocean Space", "K-12 Medical")
        c4.metric("Capacity", "250 Seats")
        
        st.markdown("### 📋 Student Roster")
        st.dataframe(st.session_state.db.drop(columns=['Skills']), use_container_width=True)

    # --- ៥.២ Enrollment ---
    elif menu == "🎓 Enrollment":
        st.header("Register New Medical Scholar")
        with st.form("enroll_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                sid = st.text_input("Scholar ID")
            with col2:
                level = st.selectbox("Academic Level", ["K-G3", "G4-G6", "G7-G9", "G10-G12"])
                status = st.selectbox("Initial Status", ["Active", "Probation"])
            
            if st.form_submit_button("✅ CONFIRM ENROLLMENT"):
                if name and sid:
                    new_entry = pd.DataFrame([{
                        "ID": sid, "Name": name, "Level": level, 
                        "Enroll_Date": datetime.now().strftime("%Y-%m-%d"), 
                        "Status": status, "Skills": []
                    }])
                    st.session_state.db = pd.concat([st.session_state.db, new_entry], ignore_index=True)
                    st.success(f"Scholar '{name}' added successfully.")
                else:
                    st.error("សូមបំពេញព័ត៌មានឱ្យបានគ្រប់គ្រាន់!")

    # --- ៥.៣ Skill Passport ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Medical Skill Mastery Passport")
        if not st.session_state.db.empty:
            sel_student = st.selectbox("ជ្រើសរើសសិស្ស:", st.session_state.db['Name'].tolist())
            idx = st.session_state.db.index[st.session_state.db['Name'] == sel_student][0]
            
            current_skills = st.session_state.db.at[idx, 'Skills']
            if not isinstance(current_skills, list): current_skills = []

            available_skills = [
                "Clinical Hygiene & Sterilization", "Human Anatomy Basics", 
                "Vital Signs Monitoring", "Emergency First Aid (CPR)", 
                "Medical Ethics", "Pediatric Nutrition Awareness"
            ]

            count = len(current_skills)
            percent = count / len(available_skills)
            
            stars_html = "".join(['<span class="star-gold">★</span>' for _ in range(count)]) + \
                         "".join(['<span class="star-gray">★</span>' for _ in range(len(available_skills)-count)])
            
            st.markdown(f"### Scholar: **{sel_student}**")
            st.markdown(f"**Mastery Level:** {stars_html} ({int(percent*100)}%)", unsafe_allow_html=True)
            st.progress(percent)

            new_selection = []
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.subheader("Foundation Skills")
                for s in available_skills[:3]:
                    if st.checkbox(s, value=(s in current_skills), key=f"sk_{s}"):
                        new_selection.append(s)
            with col_s2:
                st.subheader("Advanced Skills")
                for s in available_skills[3:]:
                    if st.checkbox(s, value=(s in current_skills), key=f"sk_{s}"):
                        new_selection.append(s)

            if st.button("💾 រក្សាទុកការរីកចម្រើន (Save Progress)"):
                st.session_state.db.at[idx, 'Skills'] = new_selection
                st.success(f"ទិន្នន័យរបស់ {sel_student} ត្រូវបានធ្វើបច្ចុប្បន្នភាព!")
                st.rerun()
        else:
            st.info("សូមចុះឈ្មោះសិស្សជាមុនសិន។")

    # --- ៥.៤ Certification ---
    elif menu == "📜 Certification":
        st.header("Official JMI Certification Generator")
        if not st.session_state.db.empty:
            target_cert = st.selectbox("Select Recipient:", st.session_state.db['Name'])
            s_info = st.session_state.db[st.session_state.db['Name'] == target_cert].iloc[0]
            
            if st.button("🌟 GENERATE PREMIUM CERTIFICATE"):
                st.balloons()
                num_stars = len(s_info['Skills'])
                cert_stars = "".join(['<span style="color:#D4AF37; font-size:35px;">★</span>' for _ in range(num_stars)])
                l_img = f'<img src="data:image/png;base64,{logo_code}" width="120">' if logo_code else '<h1>JMI</h1>'
                
                st.markdown(f"""
                <div class="cert-paper">
                    <div class="cert-border">
                        {l_img}
                        <p style="letter-spacing: 6px; color: #555; margin: 10px 0 0 0; font-family: serif; font-size: 14px;">JUNIOR MEDICAL INSTITUTE</p>
                        <h1 class="cert-header">CERTIFICATE</h1>
                        <div style="margin: 10px 0;">{cert_stars}</div>
                        <p class="cert-text" style="font-style: italic; margin-top: 10px;">This prestigious award is presented to</p>
                        <h2 class="student-name">{s_info['Name']}</h2>
                        <p class="cert-text">
                            for the successful mastery and completion of the <br>
                            <span style="color: #001f3f; font-weight: bold; font-size: 22px;">Medical Foundation Pathway ({s_info['Level']})</span><br>
                            demonstrating exceptional dedication to future medical leadership.
                        </p>
                        <div style="margin-top: 40px; display: flex; justify-content: space-around; align-items: flex-end;">
                            <div style="text-align: center;">
                                <p style="font-family: serif; font-size: 16px; margin-bottom: 5px;">{datetime.now().strftime("%B %d, %Y")}</p>
                                <div class="sig-box">DATE OF ISSUE</div>
                            </div>
                            <div style="text-align: center;">
                                <p class="signature">Dr. Chan Sokhoeurn</p>
                                <div class="sig-box">ACADEMIC DIRECTOR<br><span style="font-size: 10px;">DBA, JMI FOUNDER</span></div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.info("💡 Director's Tip: Right-Click > Print > Save as PDF")
        else:
            st.error("មិនទាន់មានទិន្នន័យសិស្សឡើយ។")

# --- ៦. ផ្ទាំងបង្ហាញពេលមិនទាន់ Login ---
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.markdown("---")
    st.info("🔒 **Security Locked:** សូមបញ្ចូល 'Director's Key' នៅ sidebar ខាងឆ្វេង ដើម្បីចូលប្រើប្រាស់។")
    st.image("https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1200&q=80")
