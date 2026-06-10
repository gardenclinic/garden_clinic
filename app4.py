# In your sidebar or settings section:
st.sidebar.markdown("### 💾 Database Management")

# 1. Download Backup Button
try:
    with open("garden_clinic_v7.db", "rb") as f:
        st.sidebar.download_button(
            label="📥 Download DB Backup",
            data=f.read(),
            file_name="garden_clinic_backup.db",
            mime="application/octet-stream"
        )
except FileNotFoundError:
    st.sidebar.info("No database file found to back up yet.")

# 2. Restore Backup Uploader
uploaded_backup = st.sidebar.file_uploader("📤 Restore DB Backup", type=["db"])
if uploaded_backup is not None:
    with open("garden_clinic_v7.db", "wb") as f:
        f.write(uploaded_backup.getbuffer())
    st.sidebar.success("Database restored! Please refresh the page.")
    # In your sidebar or settings section:
st.sidebar.markdown("### 💾 Database Management")

# 1. Download Backup Button
try:
    with open("garden_clinic_v7.db", "rb") as f:
        st.sidebar.download_button(
            label="📥 Download DB Backup",
            data=f.read(),
            file_name="garden_clinic_backup.db",
            mime="application/octet-stream"
        )
except FileNotFoundError:
    st.sidebar.info("No database file found to back up yet.")

# 2. Restore Backup Uploader
uploaded_backup = st.sidebar.file_uploader("📤 Restore DB Backup", type=["db"])
if uploaded_backup is not None:
    with open("garden_clinic_v7.db", "wb") as f:
        f.write(uploaded_backup.getbuffer())
    st.sidebar.success("Database restored! Please refresh the page.")
