# --- ៨. ផ្នែកវិញ្ញាបនបត្រ (Certification) ---
    elif menu == "📜 Certification":
        st.header("📜 JMI Digital Certificate Generator")
        st.write("ជ្រើសរើសឈ្មោះសិស្សដើម្បីចេញវិញ្ញាបនបត្របញ្ចប់ការសិក្សា។")

        if len(st.session_state.students_db) > 0:
            # ឱ្យលោកបណ្ឌិតជ្រើសរើសឈ្មោះសិស្សដែលមានក្នុងបញ្ជី
            selected_student = st.selectbox("ស្វែងរកឈ្មោះសិស្ស:", st.session_state.students_db['Name'])
            
            # ទាញយកទិន្នន័យសិស្សនោះ
            student_info = st.session_state.students_db[st.session_state.students_db['Name'] == selected_student].iloc[0]
            
            if st.button("Generate & Preview Certificate"):
                st.markdown("---")
                # ការរចនាវិញ្ញាបនបត្រដោយប្រើ HTML/CSS ក្នុង Streamlit
                cert_html = f"""
                <div style="border:10px solid #001f3f; padding:50px; text-align:center; background-color:white; border-radius:15px; position:relative;">
                    <div style="border:5px solid #D4AF37; padding:30px;">
                        <h1 style="color:#001f3f; font-family:serif; font-size:40px;">CERTIFICATE OF ACHIEVEMENT</h1>
                        <p style="font-size:20px;">This is to certify that</p>
                        <h2 style="color:#D4AF37; font-size:35px; text-decoration:underline;">{student_info['Name']}</h2>
                        <p style="font-size:18px;">has successfully completed the medical foundation module at</p>
                        <h3 style="color:#001f3f;">JUNIOR MEDICAL INSTITUTE (JMI)</h3>
                        <p style="font-size:16px;">Grade Level: <b>{student_info['Grade']}</b></p>
                        <div style="margin-top:50px; display:flex; justify-content:space-between;">
                            <div style="text-align:center; width:200px;">
                                <hr style="border:1px solid #001f3f;">
                                <p>Date: {datetime.now().strftime("%B %d, %Y")}</p>
                            </div>
                            <div style="text-align:center; width:200px;">
                                <hr style="border:1px solid #001f3f;">
                                <p>Dr. CHAN Sokhoeurn, DBA<br>Academic Director</p>
                            </div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(cert_html, unsafe_allow_html=True)
                st.balloons() # បាញ់ប៉ោងៗអបអរសាទរ
                st.info("💡 លោកបណ្ឌិតអាចចុច Mouse ស្ដាំលើវិញ្ញាបនបត្រ រួចយកពាក្យ 'Print' ដើម្បីរក្សាទុកជា PDF បាន។")
        else:
            st.warning("មិនទាន់មានទិន្នន័យសិស្សនៅឡើយទេ។ សូមទៅកាន់ផ្នែក 'Student Enrollment' ដើម្បីចុះឈ្មោះសិស្សជាមុនសិន។")
