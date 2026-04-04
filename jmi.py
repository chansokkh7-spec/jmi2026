import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# --- ១. ការកំណត់ទម្រង់កម្មវិធី ---
st.set_page_config(page_title="JMI | Strategic Management Portal", page_icon="🏥", layout="wide")

def get_logo_64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_code = get_logo_64("logo.png")

# --- ២. ការរចនា Style (Premium Executive CSS) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@700&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #f8f9fa; }
    .star-gold { color: #D4AF37; font-size: 20px; }
    .star-gray { color: #e0e0e0; font-size: 20px; }
    .cert-paper { background-color: white; border: 12px solid #001f3f; padding: 10px; box-shadow: 0 25px 50px rgba(0,0,0,0.3); max-width: 850px; margin: auto; }
    .cert-border { border: 4px double #D4AF37; padding: 45px; text-align: center; }
    .student-name { font-family: 'Great Vibes', cursive; font-size: 60px; color: #D4AF37; margin: 10px 0; }
    .signature { font-family: 'Great Vibes', cursive; font-size: 35px; color: #001f3f; }
    </style>
    """, unsafe_allow_html=True)

# --- ៣. ការគ្រប់គ្រងទិន្នន័យ ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "JMI-2026-001", "Name": "Sokhoeurn Sovannachak", "Level": "K-G3", "Enroll_Date": "2026-03-25", "Status": "Active", "Skills": []}
    ])

# --- ៤. របារចំហៀងសុវត្ថិភាព ---
st.sidebar.markdown(f"<h1 style='text-align: center; color: #001f3f;'>JMI EXECUTIVE</h1>", unsafe_allow_html=True)
if logo_code:
    st.sidebar.markdown(f'<center><img src="data:image/png;base64,{logo_code}" width="100"></center>', unsafe_allow_html=True)

key = st.sidebar.text_input("Director's Key", type="password", placeholder="Enter Password")

if key == "JMI2026":
    st.sidebar.success(f"Director: Dr. CHAN Sokhoeurn")
    menu = st.sidebar.radio("STRATEGIC MODULES", ["📊 Dashboard", "🎓 Enrollment", "🏅 Skill Passport", "📜 Certification"])

    # --- ៥. Dashboard ---
    if menu == "📊 Dashboard":
        st.title("🏥 JMI Strategic Command Center")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Scholars", len(st.session_state.db))
        c2.metric("Med-Modules", "12 Units")
        c3.metric("Blue Ocean", "Pre-Med K12")
        c4.metric("Capacity", "250 Seats")
        st.dataframe(st.session_state.db.drop(columns=['Skills']), use_container_width=True)

    # --- ៦. Skill Passport (ជាមួយ Star System) ---
    elif menu == "🏅 Skill Passport":
        st.header("🏅 Medical Skill Mastery Passport")
        if not st.session_state.db.empty:
            sel_student = st.selectbox("ជ្រើសរើសសិស្ស:", st.session_state.db['Name'].tolist())
            idx = st.session_state.db.index[st.session_state.db['Name'] == sel_student][0]
            current_skills = st.session_state.db.at[idx, 'Skills']

            available_skills = [
                "Clinical Hygiene & Sterilization", "Human Anatomy Basics", 
                "Vital Signs Monitoring", "Emergency First Aid (CPR)", 
                "Medical Ethics", "Pediatric Nutrition Awareness"
            ]

            # បង្ហាញ Stars និង Progress
            count = len(current_skills)
            percent = count / len(available_skills)
            
            # បង្កើត Stars String
            stars_html = "".join(['<span class="star-gold">★</span>' for _ in range(count)]) + \
                         "".join(['<span class="star-gray">★</span>' for _ in range(len(available_skills)-count)])
            
            st.markdown(f"### Scholar: **{sel_student}**")
            st.markdown(f"Mastery Level: {stars_html} ({int(percent*100)}%)", unsafe_allow_html=True)
            st.progress(percent)

            new_skills = []
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Foundation")
                for s in available_skills[:3]:
                    if st.checkbox(s, value=(s in current_skills), key=s): new_skills.append(s)
            with col2:
                st.subheader("Advanced")
                for s in available_skills[3:]:
                    if st.checkbox(s, value=(s in current_skills), key=s): new_skills.append(s)

            if st.button("💾 Save Progress"):
                st.session_state.db.at[idx, 'Skills'] = new_skills
                st.rerun()
        else:
            st.error("មិនទាន់មានសិស្សក្នុងប្រព័ន្ធ។")

    # --- ៧. Certification (ជាមួយ Stars លើប័ណ្ណ) ---
    elif menu == "📜 Certification":
        st.header("Official JMI Certification Generator")
        if not st.session_state.db.empty:
            target = st.selectbox("Select Recipient:", st.session_state.db['Name'])
            s_info = st.session_state.db[st.session_state.db['Name'] == target].iloc[0]
            
            if st.button("🌟 GENERATE PREMIUM CERTIFICATE"):
                st.balloons()
                count = len(s_info['Skills'])
                # បង្កើត Stars សម្រាប់ដាក់លើប័ណ្ណ
                cert_stars = "".join(['<span style="color:#D4AF37; font-size:30px;">★</span>' for _ in range(count)])
                l_img = f'<img src="data:image/png;base64,{logo_code}" width="120">' if logo_code else '<h1>JMI</h1>'
                
                st.markdown(f"""
                <div class="cert-paper">
                    <div class="cert-border">
                        {l_img}
                        <p style="letter-spacing: 5px; color: #555; margin-bottom: 0;">JUNIOR MEDICAL INSTITUTE</p>
                        <h1 style="font-family: 'Cinzel', serif; color: #001f3f; margin-top:0;">CERTIFICATE</h1>
                        <div style="margin: 10px 0;">{cert_stars}</div>
                        <p style="font-style: italic; font-size: 18px;">This is to certify that</p>
                        <h2 class="student-name">{s_info['Name']}</h2>
                        <p class="cert-text">has successfully completed the <b>Medical Pathway ({s_info['Level']})</b><br>
                        with clinical excellence in {count} key medical competencies.</p>
                        <div style="margin-top: 40px; display: flex; justify-content: space-around; align-items: flex-end;">
                            <div style="text-align: center;">
                                <p style="font-size: 14px;">{datetime.now().strftime("%B %d, %Y")}</p>
                                <div style="border-top: 1px solid #333; width: 150px; padding-top: 5px;">DATE</div>
                            </div>
                            <div style="text-align: center;">
                                <p class="signature">Dr. Chan Sokhoeurn</p>
                                <div style="border-top: 1px solid #333; width: 180px; padding-top: 5px;">ACADEMIC DIRECTOR</div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("🔒 សូមបញ្ចូលលេខកូដសម្ងាត់។")
