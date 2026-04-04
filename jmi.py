import streamlit as st
import pandas as pd
import base64
import os

# ការកំណត់ទម្រង់ទំព័រ
st.set_page_config(page_title="JMI Portal", layout="wide")

# បំលែង Logo ទៅជាកូដរូបភាព
def get_image_64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

img_data = get_image_64("logo.png")

# ប្រព័ន្ធការពារ (Password)
pwd = st.sidebar.text_input("លេខកូដសម្ងាត់", type="password")

if pwd == "JMI2026":
    st.sidebar.success("សួស្ដី លោកបណ្ឌិត CHAN Sokhoeurn")
    
    # បង្កើតទិន្នន័យសិស្ស
    df = pd.DataFrame([{"ID": "JMI-001", "Name": "Sokhoeurn Sovannachak", "Grade": "G1-G3"}])
    
    tab1, tab2 = st.tabs(["📊 បញ្ជីឈ្មោះ", "📜 វិញ្ញាបនបត្រ"])
    
    with tab1:
        st.subheader("បញ្ជីឈ្មោះសិស្ស JMI")
        st.table(df)
        
    with tab2:
        if st.button("បង្កើតវិញ្ញាបនបត្រ"):
            if img_data:
                st.markdown(f'<center><img src="data:image/png;base64,{img_data}" width="120"></center>', unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="border: 10px solid #001f3f; padding: 40px; text-align: center; background-color: white;">
                <h1 style="color: #001f3f; font-family: serif;">JUNIOR MEDICAL INSTITUTE</h1>
                <hr style="border: 2px solid #D4AF37; width: 50%;">
                <h2>CERTIFICATE</h2>
                <p>This award is presented to</p>
                <h1 style="color: #D4AF37;">{df['Name'][0]}</h1>
                <p>For successful completion of the Medical Foundation Pathway</p>
                <br><br>
                <p><b>Dr. CHAN Sokhoeurn</b><br>Academic Director</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.title("🏥 JMI Strategic Command Portal")
    st.info("សូមបញ្ចូលលេខកូដសម្ងាត់ក្នុងរបារខាងឆ្វេង ដើម្បីចូលប្រើប្រាស់។")
