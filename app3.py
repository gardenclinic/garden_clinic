import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# ----------------------------------------------------
# 1. PAGE CONFIG & LUXURY GREEN DESIGN
# ----------------------------------------------------
st.set_page_config(page_title="Garden Clinic OS", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# Injecting Custom CSS for the Luxury Green & Gold Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0A1F16;
        color: #E8F5E9;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #05140E;
        border-right: 1px solid #D4AF37;
    }
    /* Headers and Titles */
    h1, h2, h3, h4 {
        color: #D4AF37 !important;
        font-family: 'Georgia', serif;
        font-weight: 400;
    }
    /* Buttons */
    .stButton>button {
        background-color: #113626;
        color: #D4AF37;
        border: 1px solid #D4AF37;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37;
        color: #0A1F16;
        border: 1px solid #E8F5E9;
    }
    /* Inputs and Metrics */
    [data-testid="stMetricValue"] {
        color: #D4AF37 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #A5D6A7 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. DATABASE & SECURITY INITIALIZATION
# ----------------------------------------------------
DB_FILE = "garden_clinic.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    ctx = get_db_connection()
    with ctx:
        # Users Table (Login System)
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Patients, Doctors, Services, Visits
        ctx.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT)")
        ctx.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE)")
        ctx.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL)")
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER, doctor_id INTEGER, service_id INTEGER,
                visit_date TEXT, price_paid REAL,
                FOREIGN KEY(patient_id) REFERENCES patients(id),
                FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(service_id) REFERENCES services(id)
            )
        """)
        # Expenses Table (Accounting)
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)
    ctx.close()

init_db()

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
# 3. AUTHENTICATION & LOGIN SYSTEM
# ----------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🌿 Garden Clinic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A5D6A7;'>Secure Enterprise Portal</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔒 Secure Login", "📝 Register New Account"])
        
        with tab1:
            log_user = st.text_input("Username", key="log_user")
            log_pass = st.text_input("Password", type="password", key="log_pass")
            if st.button("Access Dashboard", use_container_width=True):
                user_record = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (log_user.strip(), hash_password(log_pass)))
                if user_record:
                    st.session_state.logged_in = True
                    st.session_state.username = user_record[0]["username"]
                    st.session_state.role = user_record[0]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        
        with tab2:
            st.warning("Admin Note: In a live system, registration should be locked. Left open for setup.")
            reg_user = st.text_input("New Username")
            reg_pass = st.text_input("New Password", type="password")
            reg_role = st.selectbox("Assign Role", ["Boss", "Accounting", "Reception", "Doctor"])
            if st.button("Register Account", use_container_width=True):
                if reg_user and reg_pass:
                    if execute_write("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (reg_user.strip(), hash_password(reg_pass), reg_role)):
                        st.success("Account created successfully! You can now log in.")
                    else:
                        st.error("Username already exists.")
                else:
                    st.error("Please fill all fields.")
    st.stop() # Stops the rest of the app from loading if not logged in

# ----------------------------------------------------
# 4. MAIN APPLICATION (LOGGED IN)
# ----------------------------------------------------
st.sidebar.markdown(f"### Welcome, {st.session_state.username}")
st.sidebar.caption(f"Access Level: {st.session_state.role}")
if st.sidebar.button("Log Out"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

# Determine available menus based on role
menus = []
if st.session_state.role == "Boss":
    menus = ["📈 Boss Command Center", "📊 Accounting & Finance", "⚙️ Clinic System Settings", "👩‍💻 Reception Desk"]
elif st.session_state.role == "Accounting":
    menus = ["📊 Accounting & Finance"]
elif st.session_state.role == "Reception":
    menus = ["👩‍💻 Reception Desk"]
elif st.session_state.role == "Doctor":
    menus = ["🩺 Doctor's Schedule"]

selected_menu = st.sidebar.radio("Navigation", menus)

# ----------------------------------------------------
# MODULE A: RECEPTION DESK
# ----------------------------------------------------
if selected_menu == "👩‍💻 Reception Desk":
    st.title("🌿 Patient Intake & Reception")
    tab1, tab2 = st.tabs(["🆕 New Patient", "⚡ Log Visit"])
    
    with tab1:
        p_name = st.text_input("Patient Full Name")
        p_phone = st.text_input("Contact Mobile")
        if st.button("Register Patient File"):
            if execute_write("INSERT INTO patients (name, phone) VALUES (?, ?)", (p_name.strip(), p_phone)):
                st.success("Patient saved!")
            else:
                st.error("Patient already exists.")

    with tab2:
        all_patients = fetch_all("SELECT id, name FROM patients")
        all_docs = fetch_all("SELECT id, name FROM doctors")
        all_services = fetch_all("SELECT id, name, price FROM services")
        
        if not all_docs or not all_services:
            st.error("System incomplete. A Boss must add Doctors and Services first.")
        else:
            p_options = {p["name"]: p["id"] for p in all_patients}
            d_options = {d["name"]: d["id"] for d in all_docs}
            s_options = {f"{s['name']} (${s['price']})": (s["id"], s["price"]) for s in all_services}
            
            selected_p = st.selectbox("Select Patient", [""] + list(p_options.keys()))
            if selected_p:
                history = fetch_all("SELECT v.visit_date, d.name as doc, s.name as srv FROM visits v JOIN doctors d ON v.doctor_id = d.id JOIN services s ON v.service_id = s.id WHERE v.patient_id = ? ORDER BY v.id DESC LIMIT 1", (p_options[selected_p],))
                if history:
                    st.info(f"Last Visit: {history[0]['visit_date']} | {history[0]['srv']} with {history[0]['doc']}")
                
            chosen_doc = st.selectbox("Assign Doctor", list(d_options.keys()))
            chosen_srv = st.selectbox("Treatment", list(s_options.keys()))
            v_date = st.date_input("Date")
            srv_id, base_price = s_options[chosen_srv]
            
            if st.button("Submit Visit Log"):
                if selected_p:
                    execute_write("INSERT INTO visits (patient_id, doctor_id, service_id, visit_date, price_paid) VALUES (?, ?, ?, ?, ?)", (p_options[selected_p], d_options[chosen_doc], srv_id, str(v_date), base_price))
                    st.success("Visit successfully logged.")

# ----------------------------------------------------
# MODULE B: ACCOUNTING & FINANCE
# ----------------------------------------------------
elif selected_menu == "📊 Accounting & Finance":
    st.title("⚖️ Financial Ledger")
    
    # Calc Income
    income_data = fetch_all("SELECT SUM(price_paid) as total FROM visits")
    total_income = income_data[0]["total"] if income_data and income_data[0]["total"] else 0.0
    
    # Calc Expenses
    expense_data = fetch_all("SELECT SUM(amount) as total FROM expenses")
    total_expenses = expense_data[0]["total"] if expense_data and expense_data[0]["total"] else 0.0
    
    # Profit
    profit = total_income - total_expenses
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}")
    col3.metric("Net Profit", f"${profit:,.2f}")
    
    st.markdown("---")
    st.subheader("Add Clinic Expense")
    with st.form("expense_form"):
        e_desc = st.text_input("Expense Description (e.g., Rent, Equipment, Utilities)")
        e_amount = st.number_input("Cost Amount ($)", min_value=0.0, step=10.0)
        e_date = st.date_input("Date of Expense")
        if st.form_submit_button("Log Expense"):
            if e_desc and e_amount > 0:
                execute_write("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (e_desc, e_amount, str(e_date)))
                st.success("Expense added! Refresh page to update metrics.")
                st.rerun()
                
    st.markdown("---")
    st.subheader("Recent Expense Logs")
    e_logs = fetch_all("SELECT date, description, amount FROM expenses ORDER BY id DESC LIMIT 10")
    if e_logs:
        st.dataframe(pd.DataFrame([dict(e) for e in e_logs]), use_container_width=True)

# ----------------------------------------------------
# MODULE C: BOSS COMMAND CENTER
# ----------------------------------------------------
elif selected_menu == "📈 Boss Command Center":
    st.title("👑 Executive Dashboard")
    st.caption("Complete overview of clinic operations and doctor commissions.")
    
    raw_logs = fetch_all("""
        SELECT p.name as patient, d.name as doctor, s.name as service, v.price_paid as revenue, v.visit_date as date
        FROM visits v JOIN patients p ON v.patient_id = p.id JOIN doctors d ON v.doctor_id = d.id JOIN services s ON v.service_id = s.id
    """)
    if not raw_logs:
        st.info("No active data. Wait for reception to log visits.")
    else:
        df = pd.DataFrame([dict(r) for r in raw_logs])
        all_docs_db = fetch_all("SELECT name FROM doctors")
        commission_table = []
        
        for d_row in all_docs_db:
            d_name = d_row["name"]
            df_doc = df[df["doctor"] == d_name]
            p_count = len(df_doc)
            rev = df_doc["revenue"].sum()
            
            if p_count >= 20: pct, pay = "5%", rev * 0.05
            elif p_count >= 10: pct, pay = "3%", rev * 0.03
            else: pct, pay = "0%", 0.0
            
            commission_table.append({"Doctor": d_name, "Patients": p_count, "Generated": f"${rev:,.2f}", "Tier": pct, "Payout": f"${pay:,.2f}"})
            
        st.subheader("Doctor Performance & Payroll")
        st.dataframe(pd.DataFrame(commission_table), use_container_width=True)

# ----------------------------------------------------
# MODULE D: SYSTEM SETTINGS
# ----------------------------------------------------
elif selected_menu == "⚙️ Clinic System Settings":
    st.title("System Settings")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Add Doctor")
        d_name = st.text_input("Name")
        if st.button("Save Doctor") and d_name:
            execute_write("INSERT INTO doctors (name) VALUES (?)", (d_name.strip(),))
            st.success("Doctor Added")
    with c2:
        st.subheader("Add Service")
        s_name = st.text_input("Treatment Name")
        s_price = st.number_input("Price", 0.0)
        if st.button("Save Service") and s_name:
            execute_write("INSERT INTO services (name, price) VALUES (?, ?)", (s_name.strip(), s_price))
            st.success("Service Added")
