import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# ----------------------------------------------------
# 1. LUXURY DESIGN DESIGN & CSS INJECTION
# ----------------------------------------------------
st.set_page_config(page_title="Garden Clinic OS - Premium", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Global Base Styling */
    .stApp {
        background: linear-gradient(135deg, #04140C 0%, #0A2416 100%);
        color: #E2EAF4;
        font-family: 'Playfair Display', 'Georgia', serif;
    }
    
    /* Top Bar Visibility Fix */
    header, [data-testid="stHeader"] {
        background-color: rgba(4, 20, 12, 0.8) !important;
    }

    /* Sidebar Luxury Framing */
    [data-testid="stSidebar"] {
        background-color: #020C07 !important;
        border-right: 2px solid #D4AF37;
        box-shadow: 5px 0px 25px rgba(0,0,0,0.7);
    }
    
    /* Premium Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #D4AF37 !important;
        font-family: 'Playfair Display', serif !important;
        letter-spacing: 1px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
    }

    /* Custom Premium Card Containers */
    .luxury-card {
        background: rgba(17, 54, 38, 0.4);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-left: 4px solid #D4AF37;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Metrics Highlighting */
    [data-testid="stMetricValue"] {
        color: #D4AF37 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        font-family: 'Courier New', monospace;
    }
    [data-testid="stMetricLabel"] {
        color: #A5D6A7 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem !important;
    }

    /* Interactive Inputs Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color: #061F13 !important;
        color: #E2EAF4 !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 4px !important;
    }
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.5) !important;
    }

    /* Custom Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #113626 0%, #0A2416 100%) !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        padding: 10px 24px !important;
        border-radius: 4px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        transition: all 0.3s ease-in-out !important;
    }
    .stButton>button:hover {
        background: #D4AF37 !important;
        color: #04140C !important;
        box-shadow: 0 0 15px #D4AF37;
        transform: translateY(-2px);
    }

    /* Styled Tables */
    div[data-testid="stDataFrame"] table {
        background-color: #051A10 !important;
        color: #E2EAF4 !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
    }
    
    /* Tabs System UI Luxury Updates */
    button[data-baseweb="tab"] {
        color: #A5D6A7 !important;
        font-size: 1.1rem !important;
    }
    button[aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom-color: #D4AF37 !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. DATA INFRASTRUCTURE (SQLITE ENGINE)
# ----------------------------------------------------
DB_FILE = "garden_clinic_v2.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    ctx = get_db_connection()
    with ctx:
        # Users Table (Supports Combined Roles)
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Patients Table
        ctx.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT)")
        
        # Doctors Table (With Customizable Commision Structures)
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                comm_type TEXT NOT NULL, -- 'tiered' or 'fixed'
                fixed_rate REAL DEFAULT 0.0
            )
        """)
        # General Employees Table
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                role TEXT NOT NULL,
                salary REAL NOT NULL
            )
        """)
        # Services Table
        ctx.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL)")
        
        # Extended Visits Table (with discount tracking)
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER, doctor_id INTEGER, service_id INTEGER,
                visit_date TEXT, base_price REAL, discount_amount REAL, net_paid REAL,
                FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE,
                FOREIGN KEY(doctor_id) REFERENCES doctors(id),
                FOREIGN KEY(service_id) REFERENCES services(id)
            )
        """)
        # Expenses Ledger
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
# 3. LOCKBOX SYSTEM (ACCESS LOG IN)
# ----------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom:0;'>🌿 GARDEN CLINIC</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37; letter-spacing: 3px; font-size: 0.95rem; margin-bottom: 30px;'>MEDICAL OPERATIONS & FINANCIAL HARMONY</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔒 Portal Verification", "📝 Provision User Access"])
        
        with tab1:
            log_user = st.text_input("System Username", key="log_user")
            log_pass = st.text_input("Secure Password", type="password", key="log_pass")
            if st.button("Unlock Environment", use_container_width=True):
                user_record = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (log_user.strip(), hash_password(log_pass)))
                if user_record:
                    st.session_state.logged_in = True
                    st.session_state.username = user_record[0]["username"]
                    st.session_state.role = user_record[0]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials entered.")
        
        with tab2:
            st.markdown("<p style='color: #A5D6A7;'>System authorization required to create access configurations.</p>", unsafe_allow_html=True)
            reg_user = st.text_input("Desired Username")
            reg_pass = st.text_input("Access Password", type="password")
            reg_role = st.selectbox("Designated Staff Role", ["Boss", "Accounting", "Reception", "Reception & Accounting", "Doctor"])
            admin_code = st.text_input("Master Admin Code Required", type="password")
            
            if st.button("Create Account Profile", use_container_width=True):
                if admin_code != "1011":
                    st.error("❌ Invalid Admin Code. Creation authorization denied.")
                elif reg_user and reg_pass:
                    if execute_write("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (reg_user.strip(), hash_password(reg_pass), reg_role)):
                        st.success("Account profile authenticated and saved. Access ready via Login.")
                    else:
                        st.error("This profile identity already exists within the ledger.")
                else:
                    st.error("Please fill in all identity variables.")
    st.stop()

# ----------------------------------------------------
# 4. ENVIRONMENT ROUTING ARCHITECTURE
# ----------------------------------------------------
st.sidebar.markdown(f"<h3 style='margin-bottom:0;'>🌿 Garden Clinic OS</h3>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: #A5D6A7; font-size:0.85rem;'>USER: {st.session_state.username} | <span style='color: #D4AF37;'>{st.session_state.role}</span></p>", unsafe_allow_html=True)

if st.sidebar.button("Lock Console", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

# Dynamic Menu Generation Based on Roles (Including the new Hybrid option)
menus = []
current_role = st.session_state.role

if current_role == "Boss":
    menus = ["👑 Boss Command Center", "👩‍💻 Reception Terminal", "📊 Financial & Payroll Ledger", "⚙️ System Customizer"]
elif current_role == "Reception & Accounting":
    menus = ["👩‍💻 Reception Terminal", "📊 Financial & Payroll Ledger"]
elif current_role == "Accounting":
    menus = ["📊 Financial & Payroll Ledger"]
elif current_role == "Reception":
    menus = ["👩‍💻 Reception Terminal"]
elif current_role == "Doctor":
    menus = ["🩺 Clinic Schedule Logs"]

selected_menu = st.sidebar.radio("Navigation Matrix", menus)

# ----------------------------------------------------
# MODULE A: RECEPTION TERMINAL (Discounts & Deletions)
# ----------------------------------------------------
if selected_menu == "👩‍💻 Reception Terminal":
    st.title("🌿 Patient Intake & Management Console")
    
    rt_tab1, rt_tab2, rt_tab3 = st.tabs(["📝 Patient Check-In / Session Logging", "👥 Registered Database & File Purging", "🆕 Add New Patient Profile"])
    
    with rt_tab3:
        st.subheader("Onboard New Patient Record")
        p_name = st.text_input("Patient Full Legal Name")
        p_phone = st.text_input("Primary Contact Phone Line")
        if st.button("Commit Patient File"):
            if p_name.strip():
                if execute_write("INSERT INTO patients (name, phone) VALUES (?, ?)", (p_name.strip(), p_phone.strip())):
                    st.success(f"Success: Active file created for {p_name}.")
                else:
                    st.error("Validation Error: This identity profile is already in use.")
            else:
                st.error("Process Failed: Name cannot be blank.")

    with rt_tab2:
        st.subheader("Active Clinic Directory")
        st.caption("Review active records or permanently purge selected profiles.")
        
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if not all_p:
            st.info("Directory currently empty.")
        else:
            p_df = pd.DataFrame([dict(x) for x in all_p])
            st.dataframe(p_df, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### 🚨 Dangerous Actions: Purge Records")
            del_target = st.selectbox("Select Patient Profile to PERMANENTLY Delete", [""] + list(p_df["name"].values))
            if st.button("Execute Complete Profile Purge", type="primary"):
                if del_target:
                    execute_write("DELETE FROM patients WHERE name = ?", (del_target,))
                    st.success(f"Medical file belonging to '{del_target}' has been deleted from the registry.")
                    st.rerun()
                else:
                    st.warning("Please choose a target to remove.")

    with rt_tab1:
        st.subheader("Process Current Checkout Session")
        
        patients_db = fetch_all("SELECT id, name FROM patients")
        docs_db = fetch_all("SELECT id, name, comm_type, fixed_rate FROM doctors")
        services_db = fetch_all("SELECT id, name, price FROM services")
        
        if not docs_db or not services_db:
            st.error("Infrastructure Error: The Boss must populate Doctors and Services configuration models first.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {f"{d['name']} ({d['comm_type'].upper()})": d["id"] for d in docs_db}
            s_map = {f"{s['name']} (${s['price']})": (s["id"], s["price"]) for s in services_db}
            
            target_p = st.selectbox("Lookup Client File Name", [""] + list(p_map.keys()))
            
            # --- INTELLIGENT HISTORICAL PATIENT TRACING ENGINE ---
            if target_p:
                p_id = p_map[target_p]
                history = fetch_all("""
                    SELECT v.visit_date, d.name as doc_name, s.name as srv_name, v.net_paid 
                    FROM visits v JOIN doctors d ON v.doctor_id = d.id JOIN services s ON v.service_id = s.id
                    WHERE v.patient_id = ? ORDER BY v.id DESC LIMIT 1
                """, (p_id,))
                
                if history:
                    st.markdown(f"""
                        <div class="luxury-card">
                            <h4>📜 Smart Historical Trace Found</h4>
                            <p><b>Last Session Date:</b> {history[0]['visit_date']}<br>
                            <b>Allocated Treatment:</b> {history[0]['srv_name']} by <b>{history[0]['doc_name']}</b><br>
                            <b>Amount Contributed:</b> ${history[0]['net_paid']:,.2f}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("✨ Fresh File: This patient has no previously registered visits.")
            
            st.markdown("---")
            chosen_doc = st.selectbox("Assign Practitioner On-Duty", list(d_map.keys()))
            chosen_srv = st.selectbox("Assigned Medical Service / Procedure", list(s_map.keys()))
            custom_date = st.date_input("Transaction Log Date", datetime.now())
            
            # --- FULL VALUE DISCOUNT IMPLEMENTATION SCHEME ---
            st.markdown("#### 🎫 Value Modification / Adjustments")
            disc_type = st.radio("Discount Application Framework", ["None", "Flat Rate Cash Deductible ($)", "Percentage Based (%)"])
            disc_val = st.number_input("Discount Value", min_value=0.0, step=1.0)
            
            srv_id, base_retail_price = s_map[chosen_srv]
            
            # Compute Final Price Deductions
            final_due = base_retail_price
            deducted = 0.0
            if disc_type == "Flat Rate Cash Deductible ($)":
                deducted = disc_val
                final_due = max(0.0, base_retail_price - disc_val)
            elif disc_type == "Percentage Based (%)":
                deducted = base_retail_price * (disc_val / 100.0)
                final_due = max(0.0, base_retail_price - deducted)
                
            st.markdown(f"### Total Adjusted Invoice: <span style='color:#D4AF37;'>${final_due:,.2f}</span> <small>(Saved ${deducted:,.2f})</small>", unsafe_allow_html=True)
            
            if st.button("Authorize Session Payment & Close Log", use_container_width=True):
                if not target_p:
                    st.error("Validation Error: Session cannot be logged without selecting an active patient profile.")
                else:
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, visit_date, base_price, discount_amount, net_paid)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, str(custom_date), base_retail_price, deducted, final_due))
                    st.success("Transaction written to blockchain storage channel. Allocation successful.")
                    st.balloons()

# ----------------------------------------------------
# MODULE B: FINANCIAL & PAYROLL LEDGER
# ----------------------------------------------------
elif selected_menu == "📊 Financial & Payroll Ledger":
    st.title("⚖️ General Ledger & Asset Balance Sheet")
    
    # Financial Aggregations
    gross_in_row = fetch_all("SELECT SUM(net_paid) as total FROM visits")
    gross_income = gross_in_row[0]["total"] if gross_in_row and gross_in_row[0]["total"] else 0.0
    
    expenses_row = fetch_all("SELECT SUM(amount) as total FROM expenses")
    base_expenses = expenses_row[0]["total"] if expenses_row and expenses_row[0]["total"] else 0.0
    
    # Calculate Staff Payroll Burden Automatically
    staff_salary_row = fetch_all("SELECT SUM(salary) as total FROM employees")
    payroll_burden = staff_salary_row[0]["total"] if staff_salary_row and staff_salary_row[0]["total"] else 0.0
    
    # Calculate Dynamic Commissions Total Burden
    all_visits_raw = fetch_all("""
        SELECT d.name, d.comm_type, d.fixed_rate, v.net_paid
        FROM visits v JOIN doctors d ON v.doctor_id = d.id
    """)
    doc_payroll_totals = {}
    total_commission_burden = 0.0
    
    # Group totals first for tiered math
    for vr in all_visits_raw:
        doc_payroll_totals[vr["name"]] = doc_payroll_totals.get(vr["name"], []) + [vr["net_paid"]]
        
    all_docs_configs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
    for dc in all_docs_configs:
        v_list = doc_payroll_totals.get(dc["name"], [])
        count = len(v_list)
        total_rev = sum(v_list)
        
        if dc["comm_type"] == "fixed":
            total_commission_burden += total_rev * (dc["fixed_rate"] / 100.0)
        else: # tiered system logic
            if count >= 20: total_commission_burden += total_rev * 0.05
            elif count >= 10: total_commission_burden += total_rev * 0.03

    total_outflows = base_expenses + payroll_burden + total_commission_burden
    net_surplus = gross_income - total_outflows
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Gross Revenue", f"${gross_income:,.2f}")
    col2.metric("Operating Expenses", f"${base_expenses:,.2f}")
    col3.metric("Staff Payroll Outflow", f"${(payroll_burden + total_commission_burden):,.2f}")
    col4.metric("Net Operational Profit", f"${net_surplus:,.2f}")
    
    st.markdown("---")
    
    fl_tab1, fl_tab2 = st.tabs(["💸 Log Operating Expense Outflows", "📋 Operational Ledger Data Rows"])
    
    with fl_tab1:
        st.subheader("Log General Capital Outflow")
        with st.form("exp_form_lux"):
            e_desc = st.text_input("Expense Categorization / Description (e.g. Utility Grid, Premium Oils)")
            e_amt = st.number_input("Disbursal Total ($)", min_value=0.0, step=10.0)
            e_date = st.date_input("Disbursal Entry Timestamp", datetime.now())
            if st.form_submit_button("Record Financial Liability"):
                if e_desc and e_amt > 0:
                    execute_write("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (e_desc, e_amt, str(e_date)))
                    st.success("Expense liability updated. Analytics updated.")
                    st.rerun()
    with fl_tab2:
        st.subheader("Historical Corporate Expense Flows")
        logs = fetch_all("SELECT date, description, amount FROM expenses ORDER BY id DESC")
        if logs:
            st.dataframe(pd.DataFrame([dict(l) for l in logs]), use_container_width=True)

# ----------------------------------------------------
# MODULE C: CROWN EXECUTIVE BOARD (THE BOSS PLATFORM)
# ----------------------------------------------------
elif selected_menu == "👑 Boss Command Center":
    st.title("👑 Garden Clinic Corporate Command Center")
    st.caption("Live high-resolution visibility into clinical performance, operational payroll vectors, and customized doctor payouts.")
    
    # Load and process performance grids
    all_v = fetch_all("""
        SELECT d.name as doctor, d.comm_type, d.fixed_rate, v.net_paid as rev
        FROM visits v JOIN doctors d ON v.doctor_id = d.id
    """)
    
    st.markdown("### 🩺 Practitioner Yield & Commission Ledger Matrices")
    
    doc_struct = {}
    for row in all_v:
        doc_struct[row["doctor"]] = doc_struct.get(row["doctor"], []) + [row["rev"]]
        
    doc_configs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
    payout_reporting_engine = []
    
    for d_conf in doc_configs:
        name = d_conf["name"]
        ctype = d_conf["comm_type"]
        frate = d_conf["fixed_rate"]
        
        sessions = doc_struct.get(name, [])
        volume = len(sessions)
        gross_gen = sum(sessions)
        
        if ctype == "fixed":
            applied_strategy = f"Custom Fixed ({frate}%)"
            payout_cash = gross_gen * (frate / 100.0)
        else:
            if volume >= 20:
                applied_strategy = "Tiered Matrix (5% High Volume)"
                payout_cash = gross_gen * 0.05
            elif volume >= 10:
                applied_strategy = "Tiered Matrix (3% Mid Volume)"
                payout_cash = gross_gen * 0.03
            else:
                applied_strategy = "Tiered Matrix (0% Base Volume)"
                payout_cash = 0.0
                
        payout_reporting_engine.append({
            "Medical Specialist": name,
            "Operating Compensation Model": applied_strategy,
            "Patient Case Volume": volume,
            "Gross Intake Revenue Generated": f"${gross_gen:,.2f}",
            "Calculated Payroll Payout": f"${payout_cash:,.2f}"
        })
        
    st.dataframe(pd.DataFrame(payout_reporting_engine), use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 👥 Operational Clinic General Employee Payroll")
    staff_db = fetch_all("SELECT name, role, salary FROM employees ORDER BY salary DESC")
    if staff_db:
        st.dataframe(pd.DataFrame([dict(stf) for stf in staff_db]), use_container_width=True)
    else:
        st.info("No standard employees logged in payroll infrastructure database pipelines.")

# ----------------------------------------------------
# MODULE D: CONFIGURATION CONTROL PLATFORM
# ----------------------------------------------------
elif selected_menu == "⚙️ System Customizer":
    st.title("⚙️ Global Clinic Parameter Customization Suite")
    
    sc_tab1, sc_tab2, sc_tab3 = st.tabs(["👨‍⚕️ Provision Specialist Medical Staff", "👥 Onboard Standard Salaried Employees", "💆‍♂️ Deploy Luxury Therapy Formulations"])
    
    with sc_tab1:
        st.subheader("Configure New Medical Specialist Parameters")
        d_name = st.text_input("Practitioner Full Identity Title (e.g. Dr. Eveline)")
        
        # Fully customizable compensation choice architecture
        c_mode = st.selectbox("Compensation Strategy Model", ["Tiered Performance Metrics (3% at 10, 5% at 20)", "Custom Fixed Fee Percentage System"])
        
        f_percentage = 0.0
        db_comm_type = "tiered"
        if c_mode == "Custom Fixed Fee Percentage System":
            db_comm_type = "fixed"
            f_percentage = st.number_input("Custom Target Percentage Per Session Take (%)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
            
        if st.button("Deploy Specialist Parameters to Base Engine"):
            if d_name.strip():
                if execute_write("INSERT INTO doctors (name, comm_type, fixed_rate) VALUES (?, ?, ?)", (d_name.strip(), db_comm_type, f_percentage)):
                    st.success(f"Parameters mapped. Specialist '{d_name}' activated on network.")
                else:
                    st.error("Operation Denied: Identity conflicts exist in database.")
                    
    with sc_tab2:
        st.subheader("Onboard Standard Operational Staff & Base Wages")
        emp_name = st.text_input("Employee Legal Name")
        emp_role = st.text_input("Operational Title (e.g. Clinical Nurse Coordinator, Executive Security)")
        emp_salary = st.number_input("Agreed Fixed Monthly Base Salary ($)", min_value=0.0, step=100.0)
        
        if st.button("Commit Salary Framework File"):
            if emp_name and emp_role:
                if execute_write("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)", (emp_name.strip(), emp_role.strip(), emp_salary)):
                    st.success(f"Salary framework compiled and initialized for {emp_name}.")
                else:
                    st.error("Error: Employee records indicate entry match duplicate.")

    with sc_tab3:
        st.subheader("Publish Treatment Matrix Item Line")
        s_name = st.text_input("Therapeutic Label (e.g. Cryotherapy Decompression)")
        s_price = st.number_input("Retail Valuation Frame Price ($)", min_value=0.0, step=10.0)
        
        if st.button("Publish Service Line to Front Desk"):
            if s_name.strip():
                if execute_write("INSERT INTO services (name, price) VALUES (?, ?)", (s_name.strip(), s_price)):
                    st.success(f"Service SKU launched: '{s_name}' indexed at ${s_price:,.2f}.")
                else:
                    st.error("Operation Aborted: Item naming collisions exist.")
