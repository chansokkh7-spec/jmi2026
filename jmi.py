import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# --- 1. SETTINGS & LUXURY GOLD UI ---
st.set_page_config(page_title="Banan Loft Management", layout="wide", page_icon="🌿")

st.markdown("""
    <style>
    html, body, [class*="st-"] { font-size: 1.05rem; }
    .main { background-color: #fdfdfd; }
    [data-testid="stSidebar"] { background-color: #d4af37 !important; }
    .logo-container {
        background-color: white; padding: 20px; border-radius: 0 0 20px 20px;
        margin-bottom: 20px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * { color: white !important; font-weight: bold; }
    .logo-container * { color: #1e3932 !important; }
    .stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"] { 
        color: #1e3932 !important; background-color: white !important; font-weight: bold; 
    }
    .stButton>button { 
        width: 100%; border-radius: 8px; background-color: #1e3932 !important; 
        color: white !important; font-weight: bold; height: 45px; border: none;
    }
    .metric-box { 
        background-color: white; padding: 20px; border-radius: 12px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-left: 5px solid #d4af37;
        margin-bottom: 20px; min-height: 120px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA STORAGE ---
if 'db' not in st.session_state:
    st.session_state.db = []

# --- 3. HELPER FUNCTIONS (ADVANCED EXCEL EXPORT) ---
def to_excel_with_branding(df, title_text, sheet_name='Report'):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name, startrow=5)
        
        workbook  = writer.book
        worksheet = writer.sheets[sheet_name]

        # Formats
        fmt_title = workbook.add_format({'bold': True, 'font_size': 18, 'font_color': '#1e3932'})
        fmt_subtitle = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#d4af37'})
        fmt_info = workbook.add_format({'font_size': 10, 'italic': True})

        # Insert Branding Text
        worksheet.write('A1', 'Banan Loft Strategic Management', fmt_title)
        worksheet.write('A2', title_text, fmt_subtitle)
        worksheet.write('A3', f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", fmt_info)
        worksheet.write('A4', f"Authorized by: {st.session_state.get('role', 'System')}", fmt_info)

        # Insert Logo if exists
        if os.path.exists(LOCAL_LOGO_PATH):
            worksheet.insert_image('E1', LOCAL_LOGO_PATH, {'x_scale': 0.15, 'y_scale': 0.15})

    return output.getvalue()

def add_to_db(cat, desc, amt, type_val, note=""):
    st.session_state.db.append({
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Category": cat,
        "Description": desc,
        "Amount ($)": amt,
        "Type": type_val,
        "Note": note,
        "Authorized By": st.session_state["role"]
    })
    st.rerun()

# --- 4. LOGIN & LOGO ---
LOCAL_LOGO_PATH = "download.png" 
def check_password():
    st.sidebar.markdown('<div class="logo-container">', unsafe_allow_html=True)
    if os.path.exists(LOCAL_LOGO_PATH):
        st.sidebar.image(LOCAL_LOGO_PATH, use_column_width=True)
    else:
        st.sidebar.markdown("<h1 style='margin:0;'>🌿</h1>", unsafe_allow_html=True)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    if "auth_status" not in st.session_state:
        st.session_state["auth_status"] = False
    if not st.session_state["auth_status"]:
        st.sidebar.markdown("<h3 style='text-align: center; color: white;'>PORTAL ACCESS</h3>", unsafe_allow_html=True)
        with st.sidebar.form("login"):
            pwd = st.text_input("Access Code", type="password")
            if st.form_submit_button("AUTHORIZE"):
                roles = {"GM2026": "General Manager", "INV2026": "Inventory Officer", "FIN2026": "Finance Manager", "CRM2026": "CRM Executive"}
                if pwd in roles:
                    st.session_state.update({"auth_status": True, "role": roles[pwd]})
                    st.rerun()
        return False
    return True

if not check_password(): st.stop()

# --- 5. DATA PREPARATION ---
df_master = pd.DataFrame(st.session_state.db) if st.session_state.db else pd.DataFrame(columns=["Timestamp", "Category", "Description", "Amount ($)", "Type", "Note", "Authorized By"])

# --- 6. NAVIGATION ---
st.sidebar.markdown("### MAIN MENU")
menu = st.sidebar.radio("", ["📊 Dashboard", "💰 Finance", "📦 Inventory", "👥 Staff", "🤝 CRM"])
if st.sidebar.button("🚪 LOGOUT"):
    st.session_state["auth_status"] = False
    st.rerun()

# --- 7. MAIN HEADER ---
head_col1, head_col2 = st.columns([1, 5])
with head_col1:
    if os.path.exists(LOCAL_LOGO_PATH): st.image(LOCAL_LOGO_PATH, width=130)
    else: st.markdown("<h1 style='text-align:right;'>🌿</h1>", unsafe_allow_html=True)
with head_col2:
    st.markdown(f'<div style="padding-top: 15px;"><h1 style="margin-bottom: 0px; color: #1e3932;">Banan Loft Strategic Management</h1><p><b>Operator:</b> {st.session_state["role"]} | 🟢 Online</p></div>', unsafe_allow_html=True)
st.divider()

# --- 8. MODULES ---

# 📊 DASHBOARD
if menu == "📊 Dashboard":
    st.subheader("🚀 Strategic Overview")
    inc = df_master[df_master['Type'] == 'Income']['Amount ($)'].sum()
    exp = df_master[df_master['Type'] == 'Expense']['Amount ($)'].abs().sum()
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"<div class='metric-box'>💰 Net Balance<br><h2>$ {inc-exp:,.2f}</h2></div>", unsafe_allow_html=True)
    with m2: st.markdown(f"<div class='metric-box'>🤝 Members<br><h2>{len(df_master[df_master['Category']=='CRM'])}</h2></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'>👥 Staff<br><h2>{len(df_master[df_master['Category']=='Staff'])}</h2></div>", unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='metric-box'>📅 Today<br><h2>{datetime.now().strftime('%d %b')}</h2></div>", unsafe_allow_html=True)
    
    st.write("### 📜 Master Activity Log")
    st.dataframe(df_master, use_container_width=True)
    if not df_master.empty:
        st.download_button("📥 Export Master Report", data=to_excel_with_branding(df_master, "Master Strategic Log"), file_name='Banan_Master_Report.xlsx')

# 💰 FINANCE
elif menu == "💰 Finance":
    st.subheader("Financial Ledger")
    c1, c2 = st.columns(2)
    with c1:
        with st.form("f_in", clear_on_submit=True):
            st.write("📥 Record Income")
            desc, amt = st.text_input("Source"), st.number_input("Amount ($)", min_value=0.0)
            if st.form_submit_button("Save Income") and desc: add_to_db("Finance", desc, amt, "Income")
    with c2:
        with st.form("f_out", clear_on_submit=True):
            st.write("📤 Record Expense")
            desc, amt = st.text_input("Detail"), st.number_input("Amount ($)", min_value=0.0)
            if st.form_submit_button("Save Expense") and desc: add_to_db("Finance", desc, -amt, "Expense")
    df_fin = df_master[df_master['Category'] == 'Finance']
    st.dataframe(df_fin, use_container_width=True)
    if not df_fin.empty:
        st.download_button("📥 Export Financial Ledger", data=to_excel_with_branding(df_fin, "Financial Ledger Report"), file_name='Banan_Finance.xlsx')

# 📦 INVENTORY
elif menu == "📦 Inventory":
    st.subheader("Inventory Control")
    with st.form("inv", clear_on_submit=True):
        item, qty = st.text_input("Item Name"), st.number_input("Quantity", min_value=0)
        unit = st.selectbox("Unit", ["KG", "Pack", "Bottle", "Box", "Sack"])
        if st.form_submit_button("Update Stock") and item: add_to_db("Inventory", item, 0, f"Qty: {qty} {unit}")
    df_inv = df_master[df_master['Category'] == 'Inventory']
    st.dataframe(df_inv, use_container_width=True)
    if not df_inv.empty:
        st.download_button("📥 Export Inventory Control", data=to_excel_with_branding(df_inv, "Inventory Control List"), file_name='Banan_Inventory.xlsx')

# 👥 STAFF
elif menu == "👥 Staff":
    st.subheader("Human Resources")
    with st.form("stf", clear_on_submit=True):
        name, pos = st.text_input("Name"), st.selectbox("Position", ["Barista", "Server", "Manager", "Chef", "Cleaner"])
        salary = st.number_input("Salary ($)", min_value=0.0)
        if st.form_submit_button("Add Staff") and name: add_to_db("Staff", name, salary, pos)
    df_stf = df_master[df_master['Category'] == 'Staff']
    st.dataframe(df_stf, use_container_width=True)
    if not df_stf.empty:
        st.download_button("📥 Export Human Resources", data=to_excel_with_branding(df_stf, "Human Resources Directory"), file_name='Banan_Staff.xlsx')

# 🤝 CRM
elif menu == "🤝 CRM":
    st.subheader("Membership Management")
    with st.form("crm", clear_on_submit=True):
        cust, tier = st.text_input("Customer Name"), st.selectbox("Tier", ["Silver", "Gold", "VIP"])
        phone = st.text_input("Phone")
        if st.form_submit_button("Register Member") and cust: add_to_db("CRM", cust, 0, tier, f"Tel: {phone}")
    df_crm = df_master[df_master['Category'] == 'CRM']
    st.dataframe(df_crm, use_container_width=True)
    if not df_crm.empty:
        st.download_button("📥 Export Membership Management", data=to_excel_with_branding(df_crm, "Membership Management Database"), file_name='Banan_Members.xlsx')

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.info(f"v15.6 | Branded Export Edition\nDr. CHAN Sokhoeurn, DBA")