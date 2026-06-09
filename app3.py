import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# ----------------------------------------------------
# 1. FRESH MIX DESIGN (DARK GREEN + LIGHT GREEN + WHITE)
# ----------------------------------------------------
st.set_page_config(page_title="Garden Clinic OS", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Main Light White Canvas background */
    .stApp {
        background-color: #F4F7F5;
        color: #1A3020;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Deep Dark Green Sidebar Header */
    [data-testid="stSidebar"] {
        background-color: #0B291B !important;
        border-right: 3px solid #2ECC71;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Crisp White Luxury Content Cards */
    .feature-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E1E8E3;
        box-shadow: 0 4px 12px rgba(11, 41, 27, 0.05);
        margin-bottom: 20px;
    }
    
    /* Headers - Strong Forest Green */
    h1, h2, h3, h4, h5, h6 {
        color: #0B291B !important;
        font-weight: 700 !important;
    }
    
    /* Clean Minty Vibrant Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2ECC71 0%, #27AE60 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 22px !important;
        border-radius: 8px !important;
        box-shadow: 0 3px 8px rgba(46, 204, 113, 0.2);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
    }
    
    /* Secondary Delete Buttons style override */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%) !important;
        box-shadow: 0 3px 8px rgba(231, 76, 60, 0.2) !important;
    }
    
    /* Clear Financial Metrics Layout */
    [data-testid="stMetricValue"] {
        color: #0B291B !important;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #557A61 !important;
        font-weight: 600;
    }

    /* Print View Frame Specific Styling */
    @media print {
        body * {
            visibility: hidden;
        }
        #print-area, #print-area * {
            visibility: visible;
        }
        #print-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            background-color: white;
            color: black;
            padding: 30px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. CORE STORAGE ENGINE (DATABASE ENGINE)
# ----------------------------------------------------
DB_FILE = "garden_clinic_v3.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    ctx = get_db_connection()
    with ctx:
        ctx.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL)")
        ctx.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT)")
        ctx.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, comm_type TEXT NOT NULL, fixed_rate REAL DEFAULT 0.0)")
        ctx.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, role TEXT NOT NULL, salary REAL NOT NULL)")
        ctx.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL)")
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, service_id INTEGER,
                visit_date TEXT, base_price REAL, discount_amount REAL, net_paid REAL
            )
        """)
        ctx.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, amount REAL NOT NULL, date TEXT NOT NULL)")
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
# 3. ENVIRONMENT LOG IN GATEWAY
# ----------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #0B291B; margin-top: 40px;'>🌿 Garden Clinic Workspace</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2ECC71; font-weight:600;'>Clean. Fast. Simple.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Staff Login", "🆕 Create Employee Access"])
        
        with tab1:
            log_user = st.text_input("Username Identifier")
            log_pass = st.text_input("Security Password", type="password")
            if st.button("Enter Workplace 🔓", use_container_width=True):
                user_record = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (log_user.strip(), hash_password(log_pass)))
                if user_record:
                    st.session_state.logged_in = True
                    st.session_state.username = user_record[0]["username"]
                    st.session_state.role = user_record[0]["role"]
                    st.rerun()
                else:
                    st.error("Invalid credentials entered.")
        
        with tab2:
            reg_user = st.text_input("New System Username")
            reg_pass = st.text_input("New System Password", type="password")
            reg_role = st.selectbox("Designated Access Tier", ["Boss", "Accounting", "Reception", "Reception & Accounting"])
            admin_code = st.text_input("Master Verification Admin Code", type="password")
            
            if st.button("Authorize Account Creation ✅", use_container_width=True):
                if admin_code != "1011":
                    st.error("Access Code Incorrect. Registration rejected.")
                elif reg_user and reg_pass:
                    if execute_write("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (reg_user.strip(), hash_password(reg_pass), reg_role)):
                        st.success("Staff profile generated perfectly. Go to Login tab!")
                    else:
                        st.error("Username already registered.")

    st.stop()

# ----------------------------------------------------
# 4. STAFF ROUTING WORKSPACE
# ----------------------------------------------------
st.sidebar.markdown(f"### 🏢 Garden Clinic Admin")
st.sidebar.markdown(f"👤 **User:** `{st.session_state.username}`\n🔑 **Tier:** `{st.session_state.role}`")
if st.sidebar.button("Exit Platform 🚪", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("---")

menus = []
if st.session_state.role == "Boss":
    menus = ["📈 Boss Command Center", "🖥️ Reception Desk", "📊 Accounting & Balance Sheet", "⚙️ Clinic Global Settings"]
elif st.session_state.role == "Reception & Accounting":
    menus = ["🖥️ Reception Desk", "📊 Accounting & Balance Sheet"]
elif st.session_state.role == "Accounting":
    menus = ["📊 Accounting & Balance Sheet"]
elif st.session_state.role == "Reception":
    menus = ["🖥️ Reception Desk"]

selected_menu = st.sidebar.radio("Navigate Apps:", menus)

# ----------------------------------------------------
# MODULE A: RECEPTION DESK WITH PRINT RECEIPTS
# ----------------------------------------------------
if selected_menu == "🖥️ Reception Desk":
    st.title("🖥️ Smart Front Desk Terminal")
    
    rt_1, rt_2, rt_3 = st.tabs(["⚡ Log Session & Receipt", "👥 Patient Directory", "➕ Add New Patient Profile"])
    
    with rt_3:
        st.subheader("Create a Fresh Patient Profile")
        p_name = st.text_input("Patient Full Name")
        p_phone = st.text_input("Phone Number")
        if st.button("Save Profile"):
            if p_name.strip() and execute_write("INSERT INTO patients (name, phone) VALUES (?, ?)", (p_name.strip(), p_phone.strip())):
                st.success(f"Success: Active file created for {p_name}.")
            else:
                st.error("Missing fields or file already exists.")

    with rt_2:
        st.subheader("Manage Current Clinic Roster")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if all_p:
            st.dataframe(pd.DataFrame([dict(x) for x in all_p]), use_container_width=True)
            st.markdown("---")
            del_target = st.selectbox("Permanently Delete Patient Profile", [""] + [x["name"] for x in all_p])
            if st.button("Execute Profile Deletion", type="primary"):
                if del_target:
                    execute_write("DELETE FROM patients WHERE name = ?", (del_target,))
                    st.success(f"Profile '{del_target}' has been removed.")
                    st.rerun()
        else:
            st.info("No records loaded yet.")

    with rt_1:
        st.subheader("Quick Patient Checkout Session")
        
        patients_db = fetch_all("SELECT id, name FROM patients")
        docs_db = fetch_all("SELECT id, name FROM doctors")
        services_db = fetch_all("SELECT id, name, price FROM services")
        
        if not docs_db or not services_db:
            st.warning("Action Required: Please go to settings and add your Doctors and Services first.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            s_map = {f"{s['name']} (${s['price']})": (s["id"], s["price"], s["name"]) for s in services_db}
            
            target_p = st.selectbox("Find Patient File", [""] + list(p_map.keys()))
            chosen_doc = st.selectbox("Assign Doctor", list(d_map.keys()))
            chosen_srv = st.selectbox("Select Therapy / Procedure", list(s_map.keys()))
            
            st.markdown("⚙️ **Instant Price Adjustments / Discounts**")
            disc_type = st.radio("Discount Type", ["None", "Flat Rate Cash ($)", "Percentage (%)"], horizontal=True)
            disc_val = st.number_input("Value to Deduct", min_value=0.0, step=1.0)
            
            srv_id, base_price, srv_name = s_map[chosen_srv]
            
            final_due = base_price
            if disc_type == "Flat Rate Cash ($)":
                final_due = max(0.0, base_price - disc_val)
            elif disc_type == "Percentage (%)":
                final_due = max(0.0, base_price - (base_price * (disc_val / 100.0)))
                
            st.markdown(f"### Total Invoice Due: **${final_due:,.2f}**")
            
            if st.button("Log Checkout & Show Invoice", use_container_width=True):
                if not target_p:
                    st.error("You must choose a patient profile first.")
                else:
                    deducted = base_price - final_due
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, visit_date, base_price, discount_amount, net_paid)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, str(datetime.now().strftime("%Y-%m-%d")), base_price, deducted, final_due))
                    
                    st.success("Session saved to ledger database!")
                    
                    # Store variables for live receipt printing block
                    st.session_state.receipt_ready = True
                    st.session_state.rcpt_patient = target_p
                    st.session_state.rcpt_doc = chosen_doc
                    st.session_state.rcpt_srv = srv_name
                    st.session_state.rcpt_base = base_price
                    st.session_state.rcpt_disc = deducted
                    st.session_state.rcpt_net = final_due

            # --- RECEIPT GENERATION WINDOW ---
            if "receipt_ready" in st.session_state and st.session_state.receipt_ready:
                st.markdown("---")
                st.markdown("### 🖨️ Live Invoice Receipt Print Preview")
                
                # HTML structured layout clean receipt box
                receipt_html = f"""
                <div id="print-area" style="background:#FFF; color:#000; padding:20px; border:2px dashed #0B291B; border-radius:8px; font-family:monospace; max-width:400px; margin:0 auto;">
                    <h2 style="text-align:center; margin:0; color:#0B291B;">🌿 GARDEN CLINIC</h2>
                    <p style="text-align:center; margin:2px 0; font-size:12px;">Operational Invoice Receipt</p>
                    <p style="text-align:center; margin:0; font-size:11px;">Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    <hr style="border-top:1px dashed #000;">
                    <p><b>Patient:</b> {st.session_state.rcpt_patient}</p>
                    <p><b>Attending Specialist:</b> {st.session_state.rcpt_doc}</p>
                    <p><b>Treatment SKU:</b> {st.session_state.rcpt_srv}</p>
                    <hr style="border-top:1px dashed #000;">
                    <p>Standard Retail Rate: <span style="float:right;">${st.session_state.rcpt_base:,.2f}</span></p>
                    <p style="color:red;">Discounts Subtracted: <span style="float:right;">-${st.session_state.rcpt_disc:,.2f}</span></p>
                    <h3 style="margin:5px 0 0 0;">TOTAL DUE: <span style="float:right;">${st.session_state.rcpt_net:,.2f}</span></h3>
                    <hr style="border-top:1px dashed #000;">
                    <p style="text-align:center; font-size:12px; margin:0;">Thank you for choosing Garden Clinic!</p>
                </div>
                """
                st.markdown(receipt_html, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Triggers browser print window directly
                st.button("Click to Print Receipt 🖨️", on_click=lambda: st.markdown("<script>window.print();</script>", unsafe_allow_html=True), use_container_width=True)

# ----------------------------------------------------
# MODULE B: UNDERSTANDABLE ACCOUNTING LAYOUT
# ----------------------------------------------------
elif selected_menu == "📊 Accounting & Balance Sheet":
    st.title("📊 Clear Financial Health Dashboard")
    st.caption("Simplified cash tracking framework showing exact money paths.")
    
    # Financial data loaders
    gross_in_row = fetch_all("SELECT SUM(net_paid) as total FROM visits")
    gross_income = gross_in_row[0]["total"] if gross_in_row and gross_in_row[0]["total"] else 0.0
    
    expenses_row = fetch_all("SELECT SUM(amount) as total FROM expenses")
    base_expenses = expenses_row[0]["total"] if expenses_row and expenses_row[0]["total"] else 0.0
    
    staff_salary_row = fetch_all("SELECT SUM(salary) as total FROM employees")
    payroll_burden = staff_salary_row[0]["total"] if staff_salary_row and staff_salary_row[0]["total"] else 0.0
    
    # Calculate Total Commission burden
    all_visits_raw = fetch_all("SELECT d.name, d.comm_type, d.fixed_rate, v.net_paid FROM visits v JOIN doctors d ON v.doctor_id = d.id")
    doc_payroll_totals = {}
    total_commission_burden = 0.0
    for vr in all_visits_raw:
        doc_payroll_totals[vr["name"]] = doc_payroll_totals.get(vr["name"], []) + [vr["net_paid"]]
        
    all_docs_configs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
    for dc in all_docs_configs:
        v_list = doc_payroll_totals.get(dc["name"], [])
        if dc["comm_type"] == "fixed":
            total_commission_burden += sum(v_list) * (dc["fixed_rate"] / 100.0)
        else:
            if len(v_list) >= 20: total_commission_burden += sum(v_list) * 0.05
            elif len(v_list) >= 10: total_commission_burden += sum(v_list) * 0.03

    total_outflows = base_expenses + payroll_burden + total_commission_burden
    net_profit = gross_income - total_outflows
    
    # Side-by-Side Easy Metrics Columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.metric("🟢 Total Cash Inflows", f"${gross_income:,.2f}")
        st.caption("Gross revenue collected from front desk treatment entries.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.metric("🔴 Total Cash Outflows", f"${total_outflows:,.2f}")
        st.caption("Operating costs + Staff wages + Commission payouts.")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.metric("💰 Final Net Profit Margin", f"${net_profit:,.2f}")
        st.caption("Net remaining capital after clear bills deductions.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown("---")
    
    acc_col1, acc_col2 = st.columns(2)
    
    with acc_col1:
        st.subheader("📥 Incoming Revenue Records")
        visit_logs = fetch_all("SELECT v.visit_date as Date, p.name as Patient, v.net_paid as Collected FROM visits v JOIN patients p ON v.patient_id = p.id ORDER BY v.id DESC")
        if visit_logs:
            st.dataframe(pd.DataFrame([dict(vl) for vl in visit_logs]), use_container_width=True)
        else:
            st.info("No dynamic income logged yet.")
            
    with acc_col2:
        st.subheader("📤 Log New Operational Expense Outflow")
        with st.form("exp_form"):
            e_desc = st.text_input("Expense Title (e.g. Clinic Rent, Utility Grid, Inventory)")
            e_amt = st.number_input("Amount Disbursed ($)", min_value=0.0, step=50.0)
            if st.form_submit_button("Record Bill Outflow"):
                if e_desc and e_amt > 0:
                    execute_write("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (e_desc, e_amt, str(datetime.now().strftime("%Y-%m-%d"))))
                    st.success("Outflow item added.")
                    st.rerun()

# ----------------------------------------------------
# MODULE C: CROWN EXECUTIVE DASHBOARD (THE BOSS)
# ----------------------------------------------------
elif selected_menu == "📈 Boss Command Center":
    st.title("👑 High Level Management Hub")
    
    st.markdown("### 🩺 Doctors Commissions & Custom Yields Matrix")
    all_v = fetch_all("SELECT d.name as doctor, d.comm_type, d.fixed_rate, v.net_paid as rev FROM visits v JOIN doctors d ON v.doctor_id = d.id")
    
    doc_struct = {}
    for row in all_v:
        doc_struct[row["doctor"]] = doc_struct.get(row["doctor"], []) + [row["rev"]]
        
    doc_configs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
    payout_table = []
    
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
                applied_strategy = "Tiered System (5%)"
                payout_cash = gross_gen * 0.05
            elif volume >= 10:
                applied_strategy = "Tiered System (3%)"
                payout_cash = gross_gen * 0.03
            else:
                applied_strategy = "Tiered System (0% Base)"
                payout_cash = 0.0
                
        payout_table.append({
            "Specialist": name,
            "Pay Strategy Assigned": applied_strategy,
            "Visits Run": volume,
            "Total Inflow Generated": f"${gross_gen:,.2f}",
            "Payroll Due Out": f"${payout_cash:,.2f}"
        })
    st.dataframe(pd.DataFrame(payout_table), use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 👥 Operational Salaried Employees Payroll List")
    staff_db = fetch_all("SELECT name, role, salary FROM employees ORDER BY salary DESC")
    if staff_db:
        st.dataframe(pd.DataFrame([dict(stf) for stf in staff_db]), use_container_width=True)
    else:
        st.info("No salaried staff configured. Use the settings page to add basic employees.")

# ----------------------------------------------------
# MODULE D: SYSTEM MANAGEMENT SETTINGS
# ----------------------------------------------------
elif selected_menu == "⚙️ Clinic Global Settings":
    st.title("⚙️ Global Setup Console")
    
    set1, set2, set3 = st.tabs(["👨‍⚕️ Setup Doctors", "👥 Setup General Staff Salaries", "💆‍♂️ Setup Clinic Service Items"])
    
    with set1:
        st.subheader("Configure Doctor Profile & Payout Logic")
        d_name = st.text_input("Doctor Name")
        c_mode = st.selectbox("Select Pay Rate Structure", ["Standard Tiered Metric (3%/5%)", "Custom Fixed Take-Home Percentage"])
        
        f_percentage = 0.0
        db_comm_type = "tiered"
        if c_mode == "Custom Fixed Take-Home Percentage":
            db_comm_type = "fixed"
            f_percentage = st.number_input("Custom Target Take-Home Percentage (%)", min_value=0.0, max_value=100.0, value=50.0)
            
        if st.button("Onboard Doctor Into Engine"):
            if d_name.strip() and execute_write("INSERT INTO doctors (name, comm_type, fixed_rate) VALUES (?, ?, ?)", (d_name.strip(), db_comm_type, f_percentage)):
                st.success(f"Doctor '{d_name}' activated perfectly on profile logs.")
                
    with set2:
        st.subheader("Add Salaried Employee Details")
        emp_name = st.text_input("Employee Legal Name")
        emp_role = st.text_input("Operational Title Role (e.g. Receptionist, Nurse Analyst)")
        emp_salary = st.number_input("Fixed Base Monthly Wage ($)", min_value=0.0, step=100.0)
        if st.button("Save Employee Profile"):
            if emp_name and emp_role and execute_write("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)", (emp_name.strip(), emp_role.strip(), emp_salary)):
                st.success(f"Salary metrics structured for {emp_name}.")

    with set3:
        st.subheader("Add Treatment Service Offerings")
        s_name = st.text_input("Treatment Action Label")
        s_price = st.number_input("Retail Price Tag ($)", min_value=0.0, step=10.0)
        if st.button("Publish Service Offering"):
            if s_name.strip() and execute_write("INSERT INTO services (name, price) VALUES (?, ?)", (s_name.strip(), s_price)):
                st.success(f"Service Item '{s_name}' indexed successfully at ${s_price:,.2f}.")
