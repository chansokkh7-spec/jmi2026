import streamlit as st
import pandas as pd
import base64
import os

# ១. ការកំណត់ទម្រង់កម្មវិធី
st.set_page_config(page_title="JMI Executive Portal", layout="centered")

# ២. មុខងារទាញរូបភាព Logo
def get_logo_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_code = get_logo_base64("logo.png")

# ៣. ផ្នែកការពារសុវត្ថិភាព (Sidebar)
st.sidebar.header("JMI STRATEGIC ACCESS")
password = st.sidebar.text_input("សូមបញ្ចូលលេខកូដសម្ងាត់", type="password")

if password == "JMI2026":
    st.sidebar.success("ជម្រាបសួរ លោកបណ្ឌិត CHAN Sokhoeurn")
    st.title("🏥 JMI Management System")
    
    # បង្កើត Tab សម្រាប់ងាយស្រួលមើល
    tab1, tab2 = st.tabs(["📊 បញ្ជីឈ្មោះសិស្ស", "📜 បង្កើតវិញ្ញាបនបត្រ"])
    
    with tab1:
        # ទិន្នន័យសិស្សគំរូ
        df = pd.DataFrame([{"ID": "JMI-001", "Name": "Sokhoeurn Sovannachak", "Grade": "G1-G3"}])
        st.subheader("បញ្ជីឈ្មោះសិស្សក្នុងប្រព័ន្ធ")
        st.table(df)
        
    with tab2:
        st.subheader("ទម្រង់វិញ្ញាបនបត្រផ្លូវការ")
        if st.button("🌟 បង្ហាញវិញ្ញាបនបត្រ (Generate)"):
            # បង្ហាញ Logo បើមាន File ត្រឹមត្រូវ
            if logo_code:
                st.markdown(f'<center><img src="data:image/png;base64,{logo_code}" width="150"></center>', unsafe_allow_html=True)
            
            # រចនាផ្ទៃវិញ្ញាបនបត្រ
            st.markdown(f"""
            <div style="border: 10px solid #001f3f; padding: 40px; text-align: center; background-color: white; border-radius: 15px;">
                <h1 style="color: #001f3f; font-family: serif;">JUNIOR MEDICAL INSTITUTE</h1>
                <hr style="border: 2px solid #D4AF37; width: 60%;">
                <h2 style="color: #333;">CERTIFICATE OF ACHIEVEMENT</h2>
                <p style="font-size: 18px;">វិញ្ញាបនបត្រនេះជូនចំពោះ</p>
                <h1 style="color: #D4AF37; font-size: 50px;">{df['Name'][0]}</h1>
                <p style="font-size: 18px;">សម្រាប់ការបញ្ចប់វគ្គសិក្សាផ្នែកវេជ្ជសាស្ត្រកម្រិតដំបូងដោយជោគជ័យ</p>
                <br><br>
                <p style="font-size: 20px;"><b>Dr. CHAN Sokhoeurn</b><br>Academic Director</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("សូមបញ្ចូលលេខកូដសម្ងាត់ក្នុង Sidebar ខាងឆ្វេង ដើម្បីចាប់ផ្ដើមដំណើរការប្រព័ន្ធ។")
