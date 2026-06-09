import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# ----------------------------------------------------
# 1. PREMIUM 2026 SAAS PALETTE & CSS ENGINE
# ----------------------------------------------------
st.set_page_config(page_title="Garden Clinic OS", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Professional Color Palette & Global Resets */
    .stApp {
        background-color: #F8FAF9 !important;
        color: #111827 !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Modern Gradient Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081C15 0%, #0B291B 50%, #123524 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* Premium Glassmorphism Card Design */
    .feature-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 18px;
        padding: 25px;
        border: 1px solid rgba(220, 229, 221, 0.7);
        box-shadow: 0 8px 32px rgba(0,0,0,0.04), inset 0 1px 0 rgba(255,255,255,0.6);
        transition: all .25s ease;
        animation: fadeUp .4s ease;
        margin-bottom: 20px;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
    }
    
    /* Keyframe Animations */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* SaaS Style Custom DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 15px !important;
        overflow: hidden !important;
        border: 1px solid #DCE5DD !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.03) !important;
    }
    
    /* Form Inputs Overrides */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        border-radius: 10px !important;
        border: 1px solid #DCE5DD !important;
        background-color: #FFFFFF !important;
        color: #111827 !important;
    }
    
    /* Premium Mint/Green Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2ECC71 0%, #10B981 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35) !important;
    }
    
    /* Red Alert Deletion Buttons */
    button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
    }
    
    /* Premium Tab Styling */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        color: #557A61 !important;
    }
    button[aria-selected="true"] {
        color: #0B291B !important;
        border-bottom-color: #10B981 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. CORE STORAGE ENGINE (DATABASE ENGINE)
# ----------------------------------------------------
DB_FILE = "garden_clinic_v6.db"

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
        ctx.execute("CREATE TABLE IF NOT EXISTS bundles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL)")
        ctx.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, service_id INTEGER, bundle_id INTEGER,
                visit_date TEXT, base_price REAL, discount_amount REAL, net_paid REAL
            )
        """)
        ctx.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, amount REAL NOT NULL, date TEXT NOT NULL)")
        
        # Safe migration logic: check if column bundle_id exists inside older tables
        try:
            ctx.execute("ALTER TABLE visits ADD COLUMN bundle_id INTEGER")
        except sqlite3.OperationalError:
            pass
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
# AUTOMATED FIRST-OF-THE-MONTH PAYROLL ENGINE
# ----------------------------------------------------
def auto_process_monthly_payroll():
    current_month = datetime.now().strftime("%Y-%m")
    desc_tag = f"Automated Monthly Payroll Outflow: {current_month}"
    
    # Check if payroll has already been locked for the current calendar cycle
    already_paid = fetch_all("SELECT id FROM expenses WHERE description = ?", (desc_tag,))
    if not already_paid:
        staff_salary_row = fetch_all("SELECT SUM(salary) as total FROM employees")
        payroll_burden = staff_salary_row[0]["total"] if staff_salary_row and staff_salary_row[0]["total"] else 0.0
        
        if payroll_burden > 0:
            # Commit processing liability line automatically mapped to the 1st day of the month
            execute_write(
                "INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)",
                (desc_tag, payroll_burden, f"{current_month}-01")
            )

# Execute the salary sweep instantly on workspace access initialization
auto_process_monthly_payroll()


# ----------------------------------------------------
# 3. PREMIUM LOGIN CARD GATEWAY
# ----------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background:white; padding:40px; border-radius:20px; max-width:550px; margin:auto; box-shadow:0 15px 40px rgba(0,0,0,.06); border: 1px solid #ECEFF1;">
            <h1 style="text-align:center; margin:0; color:#0B291B; font-weight:800;">🌿 Garden Clinic</h1>
            <p style="text-align:center; color:#6B7280; margin-top:5px; margin-bottom:25px;">Professional Clinic Workspace Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Staff Authentication", "📝 Provision Access Configuration"])
        
        with tab1:
            log_user = st.text_input("Username Key", key="log_uid")
            log_pass = st.text_input("Security Keypass", type="password", key="log_pwd")
            if st.button("Unlock Dashboard Console 🔓", use_container_width=True):
                user_record = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (log_user.strip(), hash_password(log_pass)))
                if user_record:
                    st.session_state.logged_in = True
                    st.session_state.username = user_record[0]["username"]
                    st.session_state.role = user_record[0]["role"]
                    st.rerun()
                else:
                    st.error("Authentication credentials verified invalid.")
        
        with tab2:
            reg_user = st.text_input("New Identity User String")
            reg_pass = st.text_input("New Account Passcode", type="password")
            reg_role = st.selectbox("Operational Clear Tier", ["Boss", "Accounting", "Reception", "Reception & Accounting"])
            admin_code = st.text_input("Master System Override Admin Code", type="password")
            
            if st.button("Commit Node Profile ✅", use_container_width=True):
                if admin_code != "1011":
                    st.error("Invalid Administrative Master Code. Transaction dropped.")
                elif reg_user and reg_pass:
                    if execute_write("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (reg_user.strip(), hash_password(reg_pass), reg_role)):
                        st.success("Account initialized. Please authenticate via Login tab.")
                    else:
                        st.error("Profile identity conflict found.")
    st.stop()

# ----------------------------------------------------
# 4. SAAS GRADIENT SIDEBAR & BRANDING
# ----------------------------------------------------
st.sidebar.markdown("""
<div style='text-align:center; padding:15px 10px 5px 10px; margin-bottom:10px;'>
    <h2 style='color:#FFFFFF !important; margin:0; font-weight:800; letter-spacing:0.5px;'>🌿 Garden Clinic</h2>
    <p style='color:#34D399 !important; font-size:0.9rem; margin-top:4px; font-weight:500;'>Management OS v6.0</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div style='background:rgba(255,255,255,0.08); padding:12px; border-radius:12px; margin:0 10px 20px 10px; text-align:center;'>
    <span style='color:#D1D5DB !important; font-size:0.85rem;'>Current Active Session:</span><br>
    <strong style='color:#FFFFFF !important; font-size:1rem;'>{st.session_state.username}</strong><br>
    <span style='background:#10B981; color:white; padding:2px 8px; border-radius:20px; font-size:0.75rem; font-weight:bold; display:inline-block; margin-top:5px;'>{st.session_state.role}</span>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Secure Logout 🚪", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown("<br>", unsafe_allow_html=True)

menus = []
if st.session_state.role == "Boss":
    menus = ["📈 Boss Command Center", "🖥️ Reception Terminal", "📊 Accounting Control Desk", "⚙️ System Configuration"]
elif st.session_state.role == "Reception & Accounting":
    menus = ["🖥️ Reception Terminal", "📊 Accounting Control Desk"]
elif st.session_state.role == "Accounting":
    menus = ["📊 Accounting Control Desk"]
elif st.session_state.role == "Reception":
    menus = ["🖥️ Reception Terminal"]

selected_menu = st.sidebar.radio("Console Navigation Matrix:", menus)

def render_dashboard_header(title, subtitle):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0B291B, #1F5E3B); padding:30px; border-radius:20px; color:white; margin-bottom:25px; box-shadow:0 10px 30px rgba(0,0,0,0.08);">
        <h1 style="margin:0; color:#FFFFFF !important; font-weight:800; font-size:2.2rem;">{title}</h1>
        <p style="margin:8px 0 0 0; color:#34D399; font-size:1.05rem; font-weight:500;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# ----------------------------------------------------
# CORE BUSINESS LOGIC CALCULATION MODULE
# ----------------------------------------------------
gross_in_row = fetch_all("SELECT SUM(net_paid) as total FROM visits")
gross_income = gross_in_row[0]["total"] if gross_in_row and gross_in_row[0]["total"] else 0.0

expenses_row = fetch_all("SELECT SUM(amount) as total FROM expenses")
base_expenses = expenses_row[0]["total"] if expenses_row and expenses_row[0]["total"] else 0.0

staff_salary_row = fetch_all("SELECT SUM(salary) as total FROM employees")
payroll_burden = staff_salary_row[0]["total"] if staff_salary_row and staff_salary_row[0]["total"] else 0.0

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

# ----------------------------------------------------
# MODULE A: CROWN EXECUTIVE DASHBOARD (THE BOSS)
# ----------------------------------------------------
if selected_menu == "📈 Boss Command Center":
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #0B291B, #2ECC71); padding:35px; border-radius:20px; color:white; box-shadow: 0 12px 30px rgba(11,41,27,0.15); margin-bottom:25px;">
        <h1 style="margin:0; color:white !important; font-weight:800; font-size:2.4rem;">👑 Executive Dashboard</h1>
        <h2 style="margin:10px 0 5px 0; color:#34D399 !important; font-weight:700; font-family:monospace;">Today's Clinic Profit: ${net_profit:,.2f}</h2>
        <p style="margin:5px 0 0 0; opacity:0.9; font-size:1rem;">Real-time automated analytics tracking clinic revenue profiles, operational payroll liabilities, and practitioner performance logs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="feature-card"><h3>📈 Gross Revenue</h3><h1 style="color:#0B291B; margin:10px 0 0 0; font-weight:800;">${gross_income:,.2f}</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="feature-card"><h3>📉 Operational Outflow</h3><h1 style="color:#EF4444; margin:10px 0 0 0; font-weight:800;">${total_outflows:,.2f}</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="feature-card"><h3>💰 Net Surplus Margin</h3><h1 style="color:#10B981; margin:10px 0 0 0; font-weight:800;">${net_profit:,.2f}</h1></div>', unsafe_allow_html=True)

    st.markdown("### 🩺 Practitioner Yield & Performance Matrix")
    payout_table = []
    for d_conf in all_docs_configs:
        name = d_conf["name"]
        ctype = d_conf["comm_type"]
        frate = d_conf["fixed_rate"]
        sessions = doc_payroll_totals.get(name, [])
        volume = len(sessions)
        gross_gen = sum(sessions)
        
        if ctype == "fixed":
            applied_strategy = f"Custom Fixed Take-Home ({frate}%)"
            payout_cash = gross_gen * (frate / 100.0)
        else:
            if volume >= 20: applied_strategy = "Tiered Matrix Strategy (5%)"; payout_cash = gross_gen * 0.05
            elif len(sessions) >= 10: applied_strategy = "Tiered Matrix Strategy (3%)"; payout_cash = gross_gen * 0.03
            else: applied_strategy = "Tiered Matrix Strategy (0%)"; payout_cash = 0.0
                
        payout_table.append({"Medical Specialist": name, "Assigned Model Framework": applied_strategy, "Case Volumes": volume, "Gross Revenue Contribution": f"${gross_gen:,.2f}", "Calculated Payroll Due": f"${payout_cash:,.2f}"})
    
    if payout_table:
        st.dataframe(pd.DataFrame(payout_table), use_container_width=True)
    else:
        st.info("No active medical specialist data sets recorded inside the local cluster.")

# ----------------------------------------------------
# MODULE B: RECEPTION DESK MODULE
# ----------------------------------------------------
elif selected_menu == "🖥️ Reception Terminal":
    render_dashboard_header("🖥️ Smart Front Desk Workspace", "Patient intake registers, invoice processing, and real-time ledger records deletion tools.")
    
    rt_1, rt_2, rt_3, rt_4 = st.tabs([
        "⚡ Run Checkout Session & Print Receipt", 
        "👥 Patient Central Index Records", 
        "➕ Create New Profile Record",
        "📜 Live Ledger Audit Log"
    ])
    
    with rt_3:
        st.subheader("Onboard New Patient Registry Node")
        p_name = st.text_input("Patient Full Legal Name")
        p_phone = st.text_input("Primary Contact Phone Link")
        if st.button("Commit Base Profile File"):
            if p_name.strip() and execute_write("INSERT INTO patients (name, phone) VALUES (?, ?)", (p_name.strip(), p_phone.strip())):
                st.success(f"Successfully processed profile setup for: {p_name}.")
            else:
                st.error("Validation Error: Profile string cannot be null or duplicate key matches exist.")

    with rt_2:
        st.subheader("Active Medical Database Profile Index")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if all_p:
            st.dataframe(pd.DataFrame([dict(x) for x in all_p]), use_container_width=True)
            st.markdown("---")
            st.markdown("#### 🚨 Safe Purging Registry Operations")
            del_target = st.selectbox("Select Target Client Record to Drop Permanently", [""] + [x["name"] for x in all_p])
            if st.button("Execute Complete Registry Purge", type="primary"):
                if del_target:
                    execute_write("DELETE FROM patients WHERE name = ?", (del_target,))
                    st.success(f"System purged patient file associated with target string ID: '{del_target}'.")
                    st.rerun()
        else:
            st.info("No patient registries currently stored inside local DB storage chains.")

    with rt_1:
        st.subheader("Generate Real-time Client Checkout Log")
        patients_db = fetch_all("SELECT id, name FROM patients")
        docs_db = fetch_all("SELECT id, name FROM doctors")
        services_db = fetch_all("SELECT id, name, price FROM services")
        bundles_db = fetch_all("SELECT id, name, price FROM bundles")
        
        if not docs_db or (not services_db and not bundles_db):
            st.warning("Action Required: Please navigate to global setup and initialize active catalog services, bundles, and doctor configurations.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            
            target_p = st.selectbox("Lookup Base Client Node File", [""] + list(p_map.keys()))
            chosen_doc = st.selectbox("Assign Consulting Practitioner on Duty", list(d_map.keys()))
            
            # Hybrid Selection Engine: Choose between Individual SKU or Bundle Pack
            item_classification = st.radio("Item Matrix Classification", ["Standard Service SKU Line", "Custom Built Package Bundle"], horizontal=True)
            
            srv_id = None
            bnd_id = None
            base_price = 0.0
            chosen_item_name = ""
            
            if item_classification == "Standard Service SKU Line":
                if services_db:
                    s_map = {f"✨ {s['name']} (${s['price']})": (s["id"], s["price"], s["name"]) for s in services_db}
                    chosen_srv_str = st.selectbox("Select Performed Formulation SKU Line", list(s_map.keys()))
                    if chosen_srv_str:
                        srv_id, base_price, chosen_item_name = s_map[chosen_srv_str]
                else:
                    st.error("No individual service lines configured inside catalog metrics.")
            else:
                if bundles_db:
                    b_map = {f"🎁 {b['name']} (${b['price']})": (b["id"], b["price"], b["name"]) for b in bundles_db}
                    chosen_bnd_str = st.selectbox("Select Target Active Package Bundle", list(b_map.keys()))
                    if chosen_bnd_str:
                        bnd_id, base_price, chosen_item_name = b_map[chosen_bnd_str]
                else:
                    st.error("No multi-tier custom bundles designed inside catalog data sets.")
            
            st.markdown("⚙️ **Dynamic Checkout Invoice Deduction Overrides**")
            disc_type = st.radio("Deduction Type Framework", ["None Adjustment", "Flat Nominal Cash Override ($)", "Relative Percentage Shift (%)"], horizontal=True)
            disc_val = st.number_input("Deduction Factor Quantity", min_value=0.0, step=1.0)
            
            final_due = base_price
            if disc_type == "Flat Nominal Cash Override ($)":
                final_due = max(0.0, base_price - disc_val)
            elif disc_type == "Relative Percentage Shift (%)":
                final_due = max(0.0, base_price - (base_price * (disc_val / 100.0)))
                
            st.markdown(f"### Total Balance Outstanding: **${final_due:,.2f}**")
            
            if st.button("Log Ledger Settlement & Display Receipt", use_container_width=True):
                if not target_p:
                    st.error("Operation Aborted: Target recipient profile cannot be initialized empty.")
                elif base_price == 0.0:
                    st.error("Operation Aborted: Cannot invoice an empty item structure configuration line.")
                else:
                    deducted = base_price - final_due
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, bundle_id, visit_date, base_price, discount_amount, net_paid)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, bnd_id, str(datetime.now().strftime("%Y-%m-%d")), base_price, deducted, final_due))
                    
                    st.success("Ledger verification completed successfully.")
                    
                    st.session_state.receipt_ready = True
                    st.session_state.rcpt_patient = target_p
                    st.session_state.rcpt_doc = chosen_doc
                    st.session_state.rcpt_srv = chosen_item_name
                    st.session_state.rcpt_base = base_price
                    st.session_state.rcpt_disc = deducted
                    st.session_state.rcpt_net = final_due

            if "receipt_ready" in st.session_state and st.session_state.receipt_ready:
                st.markdown("---")
                st.markdown("### 🖨️ Formatted Invoice Receipt Node")
                
                receipt_html = f"""
                <div id="print-area" style="background:#FFFFFF; color:#111827; padding:25px; border:2px dashed #0B291B; border-radius:14px; font-family:'Courier New', monospace; max-width:420px; margin:0 auto; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h2 style="text-align:center; margin:0 0 5px 0; color:#0B291B; font-weight:800;">🌿 GARDEN CLINIC</h2>
                    <p style="text-align:center; margin:0; font-size:13px; color:#4B5563;">Premium Healthcare Services Ledger</p>
                    <p style="text-align:center; margin:4px 0 0 0; font-size:11px; color:#6B7280;">Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                    <hr style="border-top:1px dashed #DCE5DD; margin:15px 0;">
                    <p style="margin:5px 0;"><b>Patient Identity:</b> {st.session_state.rcpt_patient}</p>
                    <p style="margin:5px 0;"><b>Practitioner:</b> {st.session_state.rcpt_doc}</p>
                    <p style="margin:5px 0;"><b>Charged Item:</b> {st.session_state.rcpt_srv}</p>
                    <hr style="border-top:1px dashed #DCE5DD; margin:15px 0;">
                    <p style="margin:5px 0; color:#4B5563;">Standard Base Rate: <span style="float:right;">${st.session_state.rcpt_base:,.2f}</span></p>
                    <p style="margin:5px 0; color:#EF4444;">Adjustments Deducted: <span style="float:right;">-${st.session_state.rcpt_disc:,.2f}</span></p>
                    <h3 style="margin:15px 0 0 0; color:#10B981; font-weight:800; font-size:1.3rem;">NET PAID: <span style="float:right;">${st.session_state.rcpt_net:,.2f}</span></h3>
                    <hr style="border-top:1px dashed #DCE5DD; margin:15px 0;">
                    <p style="text-align:center; font-size:12px; color:#6B7280; margin:0; font-style:italic;">Operational Validation Verification Log Complete</p>
                </div>
                """
                st.markdown(receipt_html, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.button("Print Document Receipt 🖨️", on_click=lambda: st.markdown("<script>window.print();</script>", unsafe_allow_html=True), use_container_width=True)

    with rt_4:
        st.subheader("🛠️ Transaction Ledger Management Control Console")
        st.markdown("Review running logs of patient sessions processed inside the clinic ecosystem. Use this sector to drop mistyped session invoices.")
        
        audit_raw_logs = fetch_all("""
            SELECT v.id, v.visit_date as Date, p.name as Patient, d.name as Doctor, 
                   COALESCE(s.name, '[Bundle Pack] ' || b.name) as ChargedItem, v.net_paid as Paid
            FROM visits v
            JOIN patients p ON v.patient_id = p.id
            JOIN doctors d ON v.doctor_id = d.id
            LEFT JOIN services s ON v.service_id = s.id
            LEFT JOIN bundles b ON v.bundle_id = b.id
            ORDER BY v.id DESC
        """)
        
        if audit_raw_logs:
            df_audit = pd.DataFrame([dict(x) for x in audit_raw_logs])
            st.dataframe(df_audit, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### 🚨 Reverse Session Verification Invoice")
            target_void_id = st.number_input("Input Target Row Identification Index Key (ID Number)", min_value=1, step=1)
            if st.button("Void and Expunge Selected Invoice Node", type="primary"):
                execute_write("DELETE FROM visits WHERE id = ?", (target_void_id,))
                st.success(f"Successfully deleted and reversed transaction rows corresponding to row reference matrix '{target_void_id}'.")
                st.rerun()
        else:
            st.info("No transactional checkout logs captured inside storage nodes yet.")

# ----------------------------------------------------
# MODULE C: UNDERSTANDABLE ACCOUNTING LAYOUT (NATIVE CHARTS)
# ----------------------------------------------------
elif selected_menu == "📊 Accounting Control Desk":
    render_dashboard_header("📊 Financial Health & Asset Balance Suite", "Granular revenue flow tracing, balance analysis, and resource expenditure allocation management tools.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🟢 Net Cash Inflow</h3>
            <h1 style="color:#10B981; margin:5px 0 0 0; font-weight:800;">${gross_income:,.2f}</h1>
            <p style="color:#6B7280; font-size:0.85rem; margin-top:5px;">Gross collected sales pipeline turnover metrics.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <h3>🔴 Net Cost Outflows</h3>
            <h1 style="color:#EF4444; margin:5px 0 0 0; font-weight:800;">${total_outflows:,.2f}</h1>
            <p style="color:#6B7280; font-size:0.85rem; margin-top:5px;">Operating costs + automated monthly salaries + commissions.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <h3>💰 Executive Profit Margin</h3>
            <h1 style="color:#0B291B; margin:5px 0 0 0; font-weight:800;">${net_profit:,.2f}</h1>
            <p style="color:#6B7280; font-size:0.85rem; margin-top:5px;">Net remaining operational capital surplus.</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.subheader("📊 Operational Analytics (Native Rendering Engine)")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Corporate Resource Expenditure Outflow Breakdown")
        if total_outflows > 0:
            df_exp = pd.DataFrame({
                "Expense Stream": ["Operating Bills", "Automated Salaries", "Specialist Commissions"],
                "Total Allocated ($)": [base_expenses, payroll_burden, total_commission_burden]
            }).set_index("Expense Stream")
            st.bar_chart(df_exp, y="Total Allocated ($)", color="#EF4444")
        else:
            st.info("Awaiting structural expenditure entries to map out data models.")
            
    with chart_col2:
        st.markdown("#### Retrospective Inflow Growth Velocity Track")
        visit_logs_raw = fetch_all("SELECT v.visit_date as Date, v.net_paid as Collected FROM visits v ORDER BY v.id ASC")
        if visit_logs_raw:
            df_rev = pd.DataFrame([dict(vl) for vl in visit_logs_raw])
            df_line = df_rev.groupby("Date", as_index=False).sum().set_index("Date")
            st.line_chart(df_line, y="Collected", color="#10B981")
        else:
            st.info("Awaiting historical transaction inputs to map acceleration matrix vectors.")
            
    st.markdown("---")
    
    acc_split_1, acc_split_2 = st.columns(2)
    with acc_split_1:
        st.subheader("📥 General Expense Matrix Adjustments Log")
        all_exps_listed = fetch_all("SELECT id, date as Date, description as Label, amount as Cost FROM expenses ORDER BY id DESC")
        if all_exps_listed:
            st.dataframe(pd.DataFrame([dict(x) for x in all_exps_listed]), use_container_width=True)
        else:
            st.info("No custom business operation expenditures locked into history.")
            
    with acc_split_2:
        st.subheader("📤 Record New General Expenditure Liability")
        with st.form("exp_form_saas"):
            e_desc = st.text_input("Cost Allocation Tag / Label (e.g. Infrastructure Rent, Bio Supplies)")
            e_amt = st.number_input("Disbursement Net Capital Volatility ($)", min_value=0.0, step=25.0)
            if st.form_submit_button("Authorize Outflow Asset Allocation"):
                if e_desc and e_amt > 0:
                    execute_write("INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)", (e_desc, e_amt, str(datetime.now().strftime("%Y-%m-%d"))))
                    st.success("Expense added successfully.")
                    st.rerun()

# ----------------------------------------------------
# MODULE D: SYSTEM CONFIGURATION
# ----------------------------------------------------
elif selected_menu == "⚙️ System Configuration":
    render_dashboard_header("⚙️ Global Setup Console Suite", "Modify, expand, and structure active practitioners, standard clinical support wages, and therapeutic pricing lists.")
    
    set1, set2, set3, set4 = st.tabs([
        "👨‍⚕️ Map Medical Specialist Structures", 
        "👥 Configure General Support Payrolls", 
        "💆‍♂️ Deploy Treatment Catalog Items",
        "🎁 Create Multi-Service Bundles"
    ])
    
    with set1:
        st.subheader("Configure New Medical Specialist Framework Node")
        d_name = st.text_input("Specialist Professional Title Name")
        c_mode = st.selectbox("Select Target Payout Allocation Method", ["Tiered Volume Analytics Metrics Matrix (3%/5%)", "Customized Fixed Percentage Take Home Model"])
        
        f_percentage = 0.0
        db_comm_type = "tiered"
        if c_mode == "Customized Fixed Percentage Take Home Model":
            db_comm_type = "fixed"
            f_percentage = st.number_input("Assigned Static Base Percentage Take Split Per Case (%)", min_value=0.0, max_value=100.0, value=50.0)
            
        if st.button("Onboard Practitioner Structure Model"):
            if d_name.strip() and execute_write("INSERT INTO doctors (name, comm_type, fixed_rate) VALUES (?, ?, ?)", (d_name.strip(), db_comm_type, f_percentage)):
                st.success(f"Practitioner profile for '{d_name}' verified and successfully written onto configuration registers.")
                st.rerun()
                
    with set2:
        st.subheader("Onboard Support Staff Base Salary Wage File")
        st.markdown("ℹ️ *Note: The total sum configuration written below automatically bills the system as an operational expenditure on the 1st of every month.*")
        emp_name = st.text_input("Employee Complete Identity Label")
        emp_role = st.text_input("Operational Structural Title Role")
        emp_salary = st.number_input("Agreed Static Monthly Remuneration ($)", min_value=0.0, step=100.0)
        if st.button("Save Wage Configuration Profile"):
            if emp_name and emp_role and execute_write("INSERT INTO employees (name, role, salary) VALUES (?, ?, ?)", (emp_name.strip(), emp_role.strip(), emp_salary)):
                st.success(f"Salary parameters structured successfully for: {emp_name}.")
                st.rerun()

    with set3:
        st.subheader("Deploy New Therapeutic Action Items Catalog Line")
        s_name = st.text_input("Formulation / Treatment Identification Naming")
        s_price = st.number_input("Retail Valuation Frame Base Pricing ($)", min_value=0.0, step=10.0)
        if st.button("Publish Service SKU to Main Grid"):
            if s_name.strip() and execute_write("INSERT INTO services (name, price) VALUES (?, ?)", (s_name.strip(), s_price)):
                st.success(f"Service formulation line item '{s_name}' indexed successfully at ${s_price:,.2f}.")
                st.rerun()

    with set4:
        st.subheader("🎁 Engineer Multi-tier Product Bundles")
        st.markdown("Create high-value medical product combinations or specialty care treatment packages with custom package-level pricing options.")
        
        b_name = st.text_input("Bundle / Treatment Package Title Name (e.g., Bundle 2 Executive Pack)")
        b_price = st.number_input("Set Package Vault Base Retail Price ($)", min_value=0.0, step=25.0)
        
        if st.button("Launch Custom Pack SKU to Catalog"):
            if b_name.strip() and b_price > 0:
                if execute_write("INSERT INTO bundles (name, price) VALUES (?, ?)", (b_name.strip(), b_price)):
                    st.success(f"Successfully engineered package configuration matrix entry for '{b_name}' locked at ${b_price:,.2f}.")
                    st.rerun()
                else:
                    st.error("Operation Denied: A package bundle with that precise string name already occupies active catalog cells.")
            else:
                st.error("Validation Dropped: Bundle name configuration values cannot register empty.")
