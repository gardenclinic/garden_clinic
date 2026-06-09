import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Advanced Clinic OS", layout="wide", initial_sidebar_state="expanded")

# ----------------------------------------------------
# 1. DATABASE INITIALIZATION (SQLite Real Persistence)
# ----------------------------------------------------
DB_FILE = "clinic_storage.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    ctx = get_db_connection()
    with ctx:
        # Patients Table
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                phone TEXT
            )
        """)
        # Doctors Table
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        # Services Table
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL
            )
        """)
        # Visits Table
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                doctor_id INTEGER,
                service_id INTEGER,
                visit_date TEXT,
                price_paid REAL,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(service_id) REFERENCES services(id)
            )
        """)
    ctx.close()

init_db()

# ----------------------------------------------------
# 2. SIDEBAR NAVIGATION & SECURITY MOCK
# ----------------------------------------------------
st.sidebar.title("💎 Clinic Management OS")
st.sidebar.markdown("---")
role = st.sidebar.radio("Navigate Workspace:", [
    "👩‍💻 Reception Desk", 
    "💼 Boss Analytics Dashboard",
    "⚙️ Clinic System Settings"
])

# ----------------------------------------------------
# 3. HELPER DATA FETCHERS
# ----------------------------------------------------
def fetch_all(query, params=()):
    db = get_db_connection()
    res = db.execute(query, params).fetchall()
    db.close()
    return res

def execute_write(query, params=()):
    db = get_db_connection()
    try:
        with db:
            db.execute(query, params)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

# ----------------------------------------------------
# MODULE A: CLINIC SYSTEM SETTINGS (Add Doctors/Services)
# ----------------------------------------------------
if role == "⚙️ Clinic System Settings":
    st.title("System Configuration")
    st.caption("Manage your clinic staff, inventory, and therapy items here.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍⚕️ Manage Onboarded Doctors")
        doc_name = st.text_input("Doctor Name (e.g., Dr. Marcus)")
        if st.button("Onboard Doctor", use_container_width=True):
            if doc_name.strip():
                if execute_write("INSERT INTO doctors (name) VALUES (?)", (doc_name.strip(),)):
                    st.success(f"{doc_name} added to system database!")
                else:
                    st.error("This doctor is already registered.")
            else:
                st.warning("Name field cannot be blank.")
                
        # Show Current Doctors
        docs = fetch_all("SELECT name FROM doctors")
        if docs:
            st.dataframe(pd.DataFrame([dict(d) for d in docs]), use_container_width=True)

    with col2:
        st.subheader("💆‍♂️ Manage Therapy Services")
        srv_name = st.text_input("Service Title (e.g., Spine Adjusting)")
        srv_price = st.number_input("Standard Service Price ($)", min_value=0.0, step=5.0)
        if st.button("Deploy Service Item", use_container_width=True):
            if srv_name.strip():
                if execute_write("INSERT INTO services (name, price) VALUES (?, ?)", (srv_name.strip(), srv_price)):
                    st.success(f"Service '{srv_name}' deployed at ${srv_price}!")
                else:
                    st.error("This service already exists.")
            else:
                st.warning("Service name cannot be empty.")
                
        # Show Current Services
        srvs = fetch_all("SELECT name, price FROM services")
        if srvs:
            st.dataframe(pd.DataFrame([dict(s) for s in srvs]), use_container_width=True)

# ----------------------------------------------------
# MODULE B: RECEPTION DESK
# ----------------------------------------------------
elif role == "👩‍💻 Reception Desk":
    st.title("Patient Intake & Registration Hub")
    
    tab1, tab2 = st.tabs(["🆕 Patient Intake Form", "⚡ Live Check-In / Log Visit"])
    
    with tab1:
        st.subheader("Register a Brand New Patient File")
        p_name = st.text_input("Patient Full Name")
        p_phone = st.text_input("Contact Mobile Phone")
        if st.button("Commit File to Database"):
            if p_name.strip():
                if execute_write("INSERT INTO patients (name, phone) VALUES (?, ?)", (p_name.strip(), p_phone)):
                    st.success(f"New medical record generated for: {p_name}")
                else:
                    st.error("A patient file under this name already exists.")
            else:
                st.error("Patient Name is a mandatory field.")

    with tab2:
        st.subheader("Process Patient Session")
        
        # Get live data for selection boxes
        all_patients = fetch_all("SELECT id, name FROM patients")
        all_docs = fetch_all("SELECT id, name FROM doctors")
        all_services = fetch_all("SELECT id, name, price FROM services")
        
        if not all_docs or not all_services:
            st.info("⚠️ Action Required: Please go to 'Clinic System Settings' to add doctors and services first before checkout.")
        else:
            p_options = {p["name"]: p["id"] for p in all_patients}
            d_options = {d["name"]: d["id"] for d in all_docs}
            s_options = {f"{s['name']} (${s['price']})": (s["id"], s["price"]) for s in all_services}
            
            selected_p_name = st.selectbox("Search / Select Registered Patient", [""] + list(p_options.keys()))
            
            # --- SMART HISTORY ENGINE ---
            if selected_p_name:
                p_id = p_options[selected_p_name]
                history = fetch_all("""
                    SELECT v.visit_date, d.name as doc_name, s.name as srv_name, v.price_paid 
                    FROM visits v
                    JOIN doctors d ON v.doctor_id = d.id
                    JOIN services s ON v.service_id = s.id
                    WHERE v.patient_id = ?
                    ORDER BY v.id DESC LIMIT 3
                """, (p_id,))
                
                if history:
                    st.markdown("### 📜 Smart File Retrieval (Last Active Records)")
                    for i, row in enumerate(history):
                        if i == 0:
                            st.info(f"**⚡ MOST RECENT VISIT ({row['visit_date']}):** Treated by **{row['doc_name']}** for **{row['srv_name']}** (Collected: ${row['price_paid']})")
                        else:
                            st.text(f"• Past session ({row['visit_date']}): {row['srv_name']} via {row['doc_name']}")
                else:
                    st.warning("🆕 First recorded clinical entry for this patient file.")
            
            st.markdown("---")
            # Log new entry inputs
            chosen_doc_name = st.selectbox("Assign Duty Practitioner", list(d_options.keys()))
            chosen_srv_label = st.selectbox("Allocated Medical Treatment/Service", list(s_options.keys()))
            custom_date = st.date_input("Consultation Date Entry", datetime.now())
            
            srv_id, base_price = s_options[chosen_srv_label]
            
            if st.button("Finalize Consultation Receipt & Log", use_container_width=True):
                if not selected_p_name:
                    st.error("Failed: You must select a registered patient.")
                else:
                    success = execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, visit_date, price_paid)
                        VALUES (?, ?, ?, ?, ?)
                    """, (p_options[selected_p_name], d_options[chosen_doc_name], srv_id, str(custom_date), base_price))
                    if success:
                        st.success(f"Transaction Recorded! ${base_price} allocated to financial pipeline under {chosen_doc_name}.")
                        st.balloons()

# ----------------------------------------------------
# MODULE C: BOSS DASHBOARD
# ----------------------------------------------------
elif role == "💼 Boss Analytics Dashboard":
    st.title("Clinic Executive Financial Command Center")
    
    # Load all transactions from database
    raw_logs = fetch_all("""
        SELECT v.id, p.name as patient, d.name as doctor, s.name as service, v.price_paid as revenue, v.visit_date as date
        FROM visits v
        JOIN patients p ON v.patient_id = p.id
        JOIN doctors d ON v.doctor_id = d.id
        JOIN services s ON v.service_id = s.id
    """)
    
    if not raw_logs:
        st.info("System Engine Online. Financial performance dashboard will compute figures once clinic check-ins begin.")
    else:
        df = pd.DataFrame([dict(r) for r in raw_logs])
        
        # High-level metrics
        total_gross = df["revenue"].sum()
        total_volume = len(df)
        
        m1, m2 = st.columns(2)
        m1.metric("Gross Collected Revenue", f"${total_gross:,.2f}")
        m2.metric("Total Medical Consultations Run", f"{total_volume} Sessions")
        
        st.markdown("---")
        st.subheader("🩺 Dynamic Commission Matrix Report")
        
        # Calculate real-time tiered logic grouped by doctor database entries
        all_docs_db = fetch_all("SELECT name FROM doctors")
        commission_table = []
        
        for d_row in all_docs_db:
            d_name = d_row["name"]
            df_doc = df[df["doctor"] == d_name]
            
            patient_count = len(df_doc)
            revenue_generated = df_doc["revenue"].sum()
            
            # Tier Calculation
            if patient_count >= 20:
                tier_applied = "5%"
                payout = revenue_generated * 0.05
            elif patient_count >= 10:
                tier_applied = "3%"
                payout = revenue_generated * 0.03
            else:
                tier_applied = "0% (Base Rate)"
                payout = 0.00
                
            commission_table.append({
                "Practitioner": d_name,
                "Volume (Patients Seen)": patient_count,
                "Gross Revenue Brought In": f"${revenue_generated:,.2f}",
                "Commission Tier Triggered": tier_applied,
                "Payroll Disbursal Amount": f"${payout:,.2f}"
            })
            
        st.dataframe(pd.DataFrame(commission_table), use_container_width=True)
        
        st.markdown("---")
        st.subheader("📜 Comprehensive Electronic Ledger Rows")
        st.dataframe(df[["date", "patient", "doctor", "service", "revenue"]], use_container_width=True)
