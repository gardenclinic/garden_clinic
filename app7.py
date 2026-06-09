import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime, date, timedelta

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Garden Clinic",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── GLOBAL ── */
*, *::before, *::after {
    box-sizing: border-box;
}
html, body, .stApp {
    background: #F0F4F2 !important;
    color: #1A2E23 !important;
    font-family: 'DM Sans', system-ui, sans-serif !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0D3D2B !important;
    border-right: none !important;
    min-width: 230px !important;
}
[data-testid="stSidebar"] * {
    color: #E8F0EB !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.9rem !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
}
section[data-testid="stSidebarNav"] {
    display: none;
}

/* ── PULSE BAR ── */
.pulse-bar {
    background: linear-gradient(90deg, #0D3D2B 0%, #1A5C3E 100%);
    border-radius: 14px;
    padding: 16px 24px;
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
    align-items: center;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(13,61,43,0.12);
}
.pulse-stat {
    display: flex;
    flex-direction: column;
}
.pulse-label {
    font-size: 0.72rem;
    color: #6FCF97;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.pulse-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.35rem;
    font-weight: 500;
    color: #FFFFFF;
    margin-top: 2px;
}
.pulse-divider {
    width: 1px;
    background: rgba(255,255,255,0.15);
    height: 36px;
    align-self: center;
}

/* ── PAGE HEADER ── */
.page-header {
    margin-bottom: 28px;
}
.page-header h1 {
    font-size: 1.7rem !important;
    font-weight: 700 !important;
    color: #0D3D2B !important;
    margin: 0 0 4px 0 !important;
}
.page-header p {
    font-size: 0.9rem;
    color: #5A7A65;
    margin: 0;
}

/* ── CARDS ── */
.card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 22px 24px;
    border: 1px solid #DDE8E1;
    margin-bottom: 18px;
    transition: box-shadow 0.2s;
}
.card:hover {
    box-shadow: 0 6px 24px rgba(0,0,0,0.06);
}
.card h3 {
    margin: 0 0 4px 0;
    font-size: 0.8rem;
    color: #5A7A65;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.card .big-num {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    margin: 0;
}
.card .big-num.green { color: #0D7A4E; }
.card .big-num.red { color: #C0392B; }
.card .big-num.dark { color: #0D3D2B; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px !important;
    border-bottom: 2px solid #DDE8E1 !important;
    padding-bottom: 0 !important;
}
.stTabs button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    color: #5A7A65 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 8px 16px 10px !important;
    border-radius: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs button[aria-selected="true"] {
    color: #0D3D2B !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #0D3D2B !important;
    margin-bottom: -2px !important;
}

/* ── SYSTEM INVOICE RECEIPT BOX ── */
.receipt-box {
    background: #FFFFFF;
    border-left: 5px solid #0D3D2B;
    border-radius: 8px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* ── BUTTONS ── */
.stButton > button {
    background: #0D3D2B !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 10px 20px !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover {
    background: #1A5C3E !important;
    transform: translateY(-1px) !important;
}
button[data-testid="baseButton-primary"] {
    background: #C0392B !important;
}
button[data-testid="baseButton-primary"]:hover {
    background: #A93226 !important;
}

/* ── FIXED BOTTOM FOOTER ── */
.sidebar-footer-text {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.4);
    font-family: 'DM Sans', sans-serif;
    text-align: left;
    padding-left: 16px;
    margin-top: auto;
    padding-top: 30px;
    padding-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE INTERACTION MATRIX
# ─────────────────────────────────────────────
DB_FILE = "garden_clinic_v8.db"

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all(q, p=()):
    db = get_db()
    res = db.execute(q, p).fetchall()
    db.close()
    return res

def fetch_one(q, p=()):
    db = get_db()
    res = db.execute(q, p).fetchone()
    db.close()
    return res

def execute_write(q, p=()):
    db = get_db()
    try:
        with db:
            db.execute(q, p)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

def init_db():
    db = get_db()
    with db:
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL, plaintext_password TEXT DEFAULT '')")
        db.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT, date_of_birth TEXT, gender TEXT, notes TEXT, created_at TEXT)")
        
        db.execute("""CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL UNIQUE, 
            specialty TEXT, 
            manual_visitors_target INTEGER DEFAULT 0,
            manual_commission_payout REAL DEFAULT 0.0
        )""")
        
        db.execute("""CREATE TABLE IF NOT EXISTS reklams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            commission_percent REAL DEFAULT 0.0,
            notes TEXT
        )""")
        
        db.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, category TEXT, price REAL NOT NULL, active INTEGER DEFAULT 1)")
        db.execute("CREATE TABLE IF NOT EXISTS bundles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, description TEXT)")
        
        db.execute("""CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            service_id INTEGER,
            bundle_id INTEGER,
            visit_date TEXT,
            base_price REAL,
            discount_amount REAL,
            net_paid REAL,
            payment_method TEXT DEFAULT 'Cash',
            source_type TEXT DEFAULT 'Direct Walk-in',
            reklam_id INTEGER DEFAULT NULL,
            notes TEXT
        )""")
        
        db.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, category TEXT DEFAULT 'General', amount REAL NOT NULL, date TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, appt_date TEXT, appt_time TEXT, reason TEXT, status TEXT DEFAULT 'Scheduled')")
        db.execute("CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, action TEXT, timestamp TEXT)")
        
        # New Feature Schema Strategy: Yoga Subscription Registries Matrix
        db.execute("""CREATE TABLE IF NOT EXISTS yoga_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            amount_paid REAL NOT NULL,
            payment_date TEXT NOT NULL,
            expiry_date TEXT NOT NULL,
            notes TEXT
        )""")
    db.close()

init_db()

# ─────────────────────────────────────────────
# AUDIT LOGGER
# ─────────────────────────────────────────────
def log_activity(action_text):
    current_user = st.session_state.get("username", "System")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_write("INSERT INTO system_logs (user, action, timestamp) VALUES (?, ?, ?)", (current_user, action_text, now_str))

# ─────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────
def card(title, value, css_class="dark"):
    return f"""<div class="card">
        <h3>{title}</h3>
        <p class="big-num {css_class}">{value}</p>
    </div>"""

def section_label(text):
    st.markdown(f'<p style="font-weight:700; color:#0D3D2B; font-size:1.1rem; margin-top:10px; margin-bottom:12px;">{text}</p>', unsafe_allow_html=True)

def pulse_bar(stats):
    items = ""
    for i, (label, value) in enumerate(stats):
        if i > 0:
            items += '<div class="pulse-divider"></div>'
        items += f'<div class="pulse-stat"><span class="pulse-label">{label}</span><span class="pulse-value">{value}</span></div>'
    st.markdown(f'<div class="pulse-bar">{items}</div>', unsafe_allow_html=True)

def page_header(title, desc=""):
    st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{desc}</p></div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ENGINE REVENUE BALANCES
# ─────────────────────────────────────────────
def get_financials():
    gross = fetch_one("SELECT SUM(net_paid) as t FROM visits")["t"] or 0.0
    yoga_gross = fetch_one("SELECT SUM(amount_paid) as t FROM yoga_payments")["t"] or 0.0
    total_gross = gross + yoga_gross
    
    exp = fetch_one("SELECT SUM(amount) as t FROM expenses")["t"] or 0.0
    
    docs = fetch_all("SELECT manual_commission_payout FROM doctors")
    total_doc_commissions = sum(d["manual_commission_payout"] for d in docs) if docs else 0.0
    
    reklam_visits = fetch_all("SELECT v.net_paid, r.commission_percent FROM visits v JOIN reklams r ON v.reklam_id = r.id")
    total_reklam_commissions = sum((v["net_paid"] * (v["commission_percent"] / 100.0)) for v in reklam_visits) if reklam_visits else 0.0
    
    total_outflows = exp + total_doc_commissions + total_reklam_commissions
    return total_gross, exp, total_doc_commissions, total_reklam_commissions, total_gross - total_outflows

gross_income, base_expenses, total_commissions, total_reklam_out, net_profit = get_financials()
today_str = date.today().isoformat()
patient_count = fetch_one("SELECT COUNT(*) as c FROM patients")["c"]

# ─────────────────────────────────────────────
# SECURITY LOGIN ENFORCEMENT
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<div style='text-align:center; padding:30px;'><h1>🌿 Garden Clinic Portal</h1></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Sign In Matrix", use_container_width=True):
            rec = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (u.strip(), hash_password(p)))
            if rec:
                st.session_state.logged_in = True
                st.session_state.username = rec[0]["username"]
                st.session_state.role = rec[0]["role"]
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# ─────────────────────────────────────────────
# CONTROL SIDEBAR
# ─────────────────────────────────────────────
role = st.session_state.role
username = st.session_state.username

st.sidebar.markdown(f"""
    <div style="padding: 16px;">
        <div style="font-size:1.3rem; font-weight:800; color:#FFFFFF;">🌿 Garden Clinic</div>
        <div style="font-size:0.8rem; color:#6FCF97;">User: {username} ({role})</div>
    </div>
""", unsafe_allow_html=True)

menu_map = {
    "Boss": ["📈 Dashboard", "🖥️ Reception", "📊 Accounting", "📅 Appointments", "⚙️ Settings"],
    "Reception & Accounting": ["🖥️ Reception", "📊 Accounting", "📅 Appointments"],
    "Accounting": ["📊 Accounting"],
    "Reception": ["🖥️ Reception", "📅 Appointments"],
}
selected = st.sidebar.radio("Navigation Engine", menu_map.get(role, []), label_visibility="collapsed")

if st.sidebar.button("Sign Out Session", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown('<div class="sidebar-footer-text">(crate it by haryad)</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CORE VIEWPORT CONTROLLERS
# ─────────────────────────────────────────────
if selected == "📈 Dashboard":
    page_header("Executive Clinic Dashboard")
    pulse_bar([
        ("Total Gross Income", f"{gross_income:,.0f} IQD"),
        ("System Registered Patients", str(patient_count)),
        ("Net Operating Profit", f"{net_profit:,.0f} IQD"),
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(card("Gross Revenue Flow", f"{gross_income:,.0f} IQD", "green"), unsafe_allow_html=True)
    with col2: st.markdown(card("Expenses Logged", f"{base_expenses:,.0f} IQD", "red"), unsafe_allow_html=True)
    with col3: st.markdown(card("Doctor Commissions", f"{total_commissions:,.0f} IQD", "dark"), unsafe_allow_html=True)
    with col4: st.markdown(card("Reklam Commissions", f"{total_reklam_out:,.0f} IQD", "dark"), unsafe_allow_html=True)

elif selected == "🖥️ Reception":
    page_header("Reception Desk Hub")
    t1, t2, t3, t4 = st.tabs(["Checkout Processing Desk", "Patient Directory Profiles", "Add New Profile", "Visit Records History"])
    
    with t1:
        section_label("Patient Visit Invoice Checkout Processing")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        services_db = fetch_all("SELECT id, name, price FROM services WHERE active = 1 ORDER BY name")
        bundles_db = fetch_all("SELECT id, name, price FROM bundles ORDER BY name")
        reklams_db = fetch_all("SELECT id, name FROM reklams ORDER BY name")
        
        p_map = {p["name"]: p["id"] for p in patients_db}
        d_map = {d["name"]: d["id"] for d in docs_db}
        r_map = {r["name"]: r["id"] for r in reklams_db}
        
        col1, col2 = st.columns(2)
        with col1:
            target_p = st.selectbox("Select Patient Profile *", ["— select —"] + list(p_map.keys()))
            chosen_doc = st.selectbox("Assigning Clinic Physician", list(d_map.keys()))
            payment_method = st.selectbox("Payment Gateway Type", ["Cash", "Card", "Insurance", "Transfer"])
            selected_source = st.selectbox("Marketing Stream Source", ["Direct Walk-in", "Social Media", "Friend Referral", "Video Content Creator / Reklam Partner"])
            
            chosen_reklam_id = None
            if selected_source == "Video Content Creator / Reklam Partner" and reklams_db:
                selected_reklam_name = st.selectbox("Select Associated Reklam Partner", list(r_map.keys()))
                chosen_reklam_id = r_map[selected_reklam_name]
                
        with col2:
            item_type = st.radio("Treatment Base", ["Service", "Bundle"], horizontal=True)
            base_price = 0.0
            srv_id = bnd_id = None
            chosen_item_name = ""
            
            if item_type == "Service" and services_db:
                s_map = {f"{s['name']} — {s['price']:,.0f} IQD": (s["id"], s["price"], s["name"]) for s in services_db}
                chosen_s = st.selectbox("Select Catalog Service", list(s_map.keys()))
                srv_id, base_price, chosen_item_name = s_map[chosen_s]
            elif item_type == "Bundle" and bundles_db:
                b_map = {f"{b['name']} — {b['price']:,.0f} IQD": (b["id"], b["price"], b["name"]) for b in bundles_db}
                chosen_b = st.selectbox("Select Package Bundle", list(b_map.keys()))
                bnd_id, base_price, chosen_item_name = b_map[chosen_b]
                
            disc_val = st.number_input("Discount Value Value Deduction (IQD)", min_value=0.0, step=500.0)
            final_due = max(0.0, base_price - disc_val)
            visit_notes = st.text_area("Internal Checkout Memo Notes", height=60)

        st.markdown(f"### Total Invoice Amount Due: **{final_due:,.0f} IQD**")
        
        # ── RECEIPT BUG FIX SOLUTION: PERSIST RECEIPT VIEW UPON SUCCESSFUL WRITE ──
        if st.button("Complete Payment Receipt Ledger Entry", use_container_width=True):
            if target_p == "— select —":
                st.error("Please pick a valid patient profile designation.")
            else:
                disc_amt = base_price - final_due
                success = execute_write("""
                    INSERT INTO visits (patient_id, doctor_id, service_id, bundle_id, visit_date, base_price, discount_amount, net_paid, payment_method, source_type, reklam_id, notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                """, (p_map[target_p], d_map[chosen_doc], srv_id, bnd_id, today_str, base_price, disc_amt, final_due, payment_method, selected_source, chosen_reklam_id, visit_notes))
                
                if success:
                    log_activity(f"Generated invoice visit check out ledger profile: {target_p}")
                    st.markdown(f"""
                    <div class="receipt-box">
                        <h4 style="color:#0D3D2B; margin-top:0;">📄 GARDEN CLINIC OFFICIAL RECEIPT</h4>
                        <p><b>Patient Name:</b> {target_p}<br>
                        <b>Attending Doctor:</b> {chosen_doc}<br>
                        <b>Treatment Charged:</b> {chosen_item_name}<br>
                        <b>Base Price:</b> {base_price:,.0f} IQD | <b>Discount Allowed:</b> {disc_amt:,.0f} IQD<br>
                        <span style="font-size:1.2rem; color:#0D7A4E;"><b>Total Amount Net Paid:</b> {final_due:,.0f} IQD ({payment_method})</span></p>
                        <p style="font-size:0.8rem; color:#8EA898; margin-bottom:0;">Transaction logged safely on {today_str}.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.toast("Invoice receipt compiled and rendered below.", icon="✅")

    with t2:
        section_label("Registered Clinical Patient Roster Index")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if all_p: st.dataframe(pd.DataFrame([dict(p) for p in all_p]), use_container_width=True, hide_index=True)

    with t3:
        section_label("Instantiate Patient File Record Profile")
        p_name = st.text_input("Patient Full Identification Label Name *")
        p_phone = st.text_input("Active Target Contact Line Matrix")
        if st.button("Save New Patient Identity Folder"):
            if p_name.strip() and execute_write("INSERT INTO patients (name, phone, created_at) VALUES (?,?,?)", (p_name.strip(), p_phone.strip(), today_str)):
                st.success("New structural patient profile registered.")
                st.rerun()

    with t4:
        section_label("Historical Invoice Archive Ledger Sheet")
        v_history = fetch_all("""
            SELECT v.id as [Receipt ID], v.visit_date as Date, p.name as Patient, d.name as Doctor, v.net_paid as [Net Paid], v.source_type as [Source Channel]
            FROM visits v JOIN patients p ON v.patient_id = p.id JOIN doctors d ON v.doctor_id = d.id ORDER BY v.id DESC
        """)
        if v_history:
            st.dataframe(pd.DataFrame([dict(vh) for vh in v_history]), use_container_width=True, hide_index=True)
            st.markdown("---")
            receipt_map = {f"Receipt ID: {vh['Receipt ID']} — {vh['Patient']} ({vh['Net Paid']:,.0f} IQD)": vh['Receipt ID'] for vh in v_history}
            target_del_receipt = st.selectbox("Select error receipt entry to purge", ["— select —"] + list(receipt_map.keys()))
            if st.button("Purge Erroneous Receipt Profile Permanently", type="primary"):
                if target_del_receipt != "— select —":
                    execute_write("DELETE FROM visits WHERE id = ?", (receipt_map[target_del_receipt],))
                    st.success("Receipt row wiped out securely.")
                    st.rerun()

elif selected == "📊 Accounting":
    page_header("Accounting Department Ledger Sheet")
    
    # ── YOGA MONTHLY SUBSCRIPTION TAB AND GENERAL LOGS EXPENSES ──
    acc_tabs = st.tabs(["💸 General Outflow Expenses", "🧘 Monthly Yoga Memberships & Subscriptions"])
    
    with acc_tabs[0]:
        col1, col2 = st.columns(2)
        with col1:
            section_label("Add Operational Costs Expense Line")
            with st.form("exp_f"):
                e_desc = st.text_input("Expense Allocation Tag Context Description Line")
                e_amt = st.number_input("Total Disbursed Sum Amount (IQD)", min_value=0.0, step=1000.0)
                if st.form_submit_button("Log Outflow"):
                    if e_desc and e_amt > 0 and execute_write("INSERT INTO expenses (description, category, amount, date) VALUES (?, 'General', ?, ?)", (e_desc, e_amt, today_str)):
                        st.success("Expense registered.")
                        st.rerun()
        with col2:
            section_label("Current Monthly Expenses Sheet Records")
            all_exp = fetch_all("SELECT id, date as Date, description as Description, amount as Amount FROM expenses ORDER BY id DESC")
            if all_exp:
                st.dataframe(pd.DataFrame([{"Date": x["Date"], "Description": x["Description"], "Amount": f"{x['Amount']:,.0f} IQD"} for x in all_exp]), use_container_width=True, hide_index=True)
                st.markdown("---")
                exp_map = {f"{x['Date']} — {x['Description']} ({x['Amount']:,.0f} IQD)": x["id"] for x in all_exp}
                target_del_exp = st.selectbox("Select mistaken expense item row to delete", ["— select —"] + list(exp_map.keys()))
                if st.button("Delete Selected Expense", type="primary"):
                    if target_del_exp != "— select —":
                        execute_write("DELETE FROM expenses WHERE id = ?", (exp_map[target_del_exp],))
                        st.success("Expense log line purged.")
                        st.rerun()
                        
    with acc_tabs[1]:
        section_label("🧘 Monthly Subscription Management Panel (Yoga Studio)")
        st.info("Log patients paying recurring flat-rate fees for monthly yoga programs. These track cycles independently from basic direct checkouts.")
        
        y_col1, y_col2 = st.columns([1, 1.6])
        with y_col1:
            st.markdown("##### Log New Monthly Membership Payment")
            patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
            yoga_p_map = {p["name"]: p["id"] for p in patients_db}
            
            chosen_yoga_p = st.selectbox("Select Subscribed Yoga Student", ["— select —"] + list(yoga_p_map.keys()))
            yoga_fee = st.number_input("Monthly Fee Paid (IQD)", min_value=0.0, step=5000.0, value=50000.0)
            
            start_d = st.date_input("Membership Activation Date", value=date.today())
            end_d = st.date_input("Subscription Expiry Renewable Date", value=date.today() + timedelta(days=30))
            yoga_notes = st.text_input("Class Allocation/Timing Notes")
            
            if st.button("Authorize Yoga Monthly Entry Slot"):
                if chosen_yoga_p == "— select —":
                    st.error("Please pick an active patient row identifier.")
                else:
                    success_yoga = execute_write("""
                        INSERT INTO yoga_payments (patient_id, amount_paid, payment_date, expiry_date, notes)
                        VALUES (?, ?, ?, ?, ?)
                    """, (yoga_p_map[chosen_yoga_p], yoga_fee, str(start_d), str(end_d), yoga_notes))
                    if success_yoga:
                        log_activity(f"Registered monthly yoga membership payment for {chosen_yoga_p}")
                        st.success(f"Subscription confirmed for {chosen_yoga_p} until {end_d}!")
                        st.rerun()
                        
        with y_col2:
            st.markdown("##### Active Subscriptions & Renewable Sheets Ledger")
            yoga_history = fetch_all("""
                SELECT y.id, p.name as Student, y.amount_paid as [Fee Paid], y.payment_date as [Start Date], y.expiry_date as [Expiry Date], y.notes as [Class Notes]
                FROM yoga_payments y JOIN patients p ON y.patient_id = p.id ORDER BY y.id DESC
            """)
            if yoga_history:
                yoga_rows_clean = []
                for yh in yoga_history:
                    # Color check helper flag context tracking validation for expiration tags
                    expiry_parsed = datetime.strptime(yh["Expiry Date"], "%Y-%m-%d").date()
                    status_flag = "🟢 Active" if expiry_parsed >= date.today() else "🔴 Expired / Needs Renewal"
                    
                    yoga_rows_clean.append({
                        "Payment ID": yh["id"],
                        "Yoga Member Student": yh["Student"],
                        "Monthly Fee Paid": f"{yh['Fee Paid']:,.0f} IQD",
                        "Cycle Start": yh["Start Date"],
                        "Renewal Expiry Boundary": yh["Expiry Date"],
                        "Current Status": status_flag,
                        "Class Notes": yh["Class Notes"]
                    })
                st.dataframe(pd.DataFrame(yoga_rows_clean), use_container_width=True, hide_index=True)
                
                st.markdown("---")
                yoga_del_map = {f"ID: {y['Payment ID']} — Student: {y['Yoga Member Student']}": y['Payment ID'] for y in yoga_rows_clean}
                target_del_yoga = st.selectbox("Select error membership log row to delete", ["— select —"] + list(yoga_del_map.keys()))
                if st.button("Delete Subscription Entry Log Row", type="primary"):
                    if target_del_yoga != "— select —":
                        execute_write("DELETE FROM yoga_payments WHERE id = ?", (yoga_del_map[target_del_yoga],))
                        st.success("Subscription ledger row deleted.")
                        st.rerun()

elif selected == "📅 Appointments":
    page_header("Appointments Matrix Hub")
    all_ap = fetch_all("""
        SELECT a.appt_date as Date, a.appt_time as Time, p.name as Patient, d.name as Doctor, a.reason as Reason FROM appointments a 
        JOIN patients p ON a.patient_id = p.id JOIN doctors d ON a.doctor_id = d.id
    """)
    if all_ap: st.dataframe(pd.DataFrame([dict(x) for x in all_ap]), use_container_width=True, hide_index=True)

elif selected == "⚙️ Settings":
    page_header("Clinical System Controls & Setup Configuration Settings")
    
    set_tabs_list = ["Physician Roster", "📢 Marketing Reklam Creators", "Service Catalog Config", "Treatment Bundles Catalog"]
    s_tabs = st.tabs(set_tabs_list)
    
    with s_tabs[0]:
        section_label("Configure Clinic Doctor Commission Overrides")
        with st.form("doc_f"):
            dn = st.text_input("Physician Full Name *")
            ds = st.text_input("Specialty Designation")
            if st.form_submit_button("Save Doctor Profile Line"):
                if dn.strip() and execute_write("INSERT INTO doctors (name, specialty) VALUES (?,?)", (dn.strip(), ds.strip())):
                    st.success("Doctor saved.")
                    st.rerun()

    with s_tabs[1]:
        section_label("📢 Marketing Reklam Video Creators Configuration Profile")
        col_rek1, col_rek2 = st.columns([1, 1.5])
        with col_rek1:
            st.markdown("##### Add New Content Creator Row")
            rek_name_in = st.text_input("Partner Profile Name Identity Identifier *")
            rek_comm_per = st.number_input("Commission Share Rate Percentage (%)", min_value=0.0, max_value=100.0, step=0.5, value=10.0)
            rek_notes_in = st.text_input("Platform Handle Campaign Notes (e.g. Instagram campaign)")
            if st.button("Commit Marketing Asset Link"):
                if rek_name_in.strip() and execute_write("INSERT INTO reklams (name, commission_percent, notes) VALUES (?,?,?)", (rek_name_in.strip(), rek_comm_per, rek_notes_in.strip())):
                    st.success("Reklam partner added safely.")
                    st.rerun()
        with col_rek2:
            st.markdown("##### Current Registered Marketing Reklam Channels")
            all_reklams_listed = fetch_all("SELECT id, name, commission_percent, notes FROM reklams ORDER BY name")
            if all_reklams_listed:
                st.dataframe(pd.DataFrame([{"ID": r["id"], "Name Handle": r["name"], "Percentage Rate": f"{r['commission_percent']}%", "Notes": r["notes"]} for r in all_reklams_listed]), use_container_width=True, hide_index=True)

    with s_tabs[2]:
        section_label("Add Base Catalog Services Options")
        with st.form("svc_f"):
            sn = st.text_input("Treatment Description Text Label Name")
            sp = st.number_input("Catalog Base Rate (IQD)", min_value=0.0, step=5000.0)
            if st.form_submit_button("Save Service Asset Entry"):
                if sn.strip() and execute_write("INSERT INTO services (name, price) VALUES (?,?)", (sn.strip(), sp)):
                    st.success("Service added.")
                    st.rerun()

    with s_tabs[3]:
        section_label("Configure Bundles Options")
        with st.form("bnd_f"):
            bn = st.text_input("Care Package Group Title Label")
            bp = st.number_input("Bundle Allotted Rate Fee (IQD)", min_value=0.0, step=5000.0)
            if st.form_submit_button("Save Care Package Bundle"):
                if bn.strip() and execute_write("INSERT INTO bundles (name, price) VALUES (?,?)", (bn.strip(), bp)):
                    st.success("Package bundle added.")
                    st.rerun()

    # ─────────────────────────────────────────────
    # ── REQUESTED SECTION: BELOW SETTINGS REKLAM PERFORMANCE BROUGHT OVERVIEW ──
    # ─────────────────────────────────────────────
    st.markdown("---")
    st.markdown("<h3 style='color:#0D3D2B; margin-top:20px;'>📊 Reklam Partners Customer Acquisition & Performance Sheet</h3>", unsafe_allow_html=True)
    st.markdown("This tracker visualizes exactly **which person brought in how many people** to the clinic, as well as the total accumulated commission payout owed to them.")
    
    all_reklams_performance = fetch_all("SELECT id, name, commission_percent, notes FROM reklams ORDER BY name")
    if all_reklams_performance:
        perf_rows = []
        for rk in all_reklams_performance:
            # Query the precise customer visits driven by this individual's promotional channels
            referred_visits = fetch_all("""
                SELECT v.id, p.name as PatientName, v.net_paid, v.visit_date 
                FROM visits v 
                JOIN patients p ON v.patient_id = p.id 
                WHERE v.reklam_id = ?
            """, (rk["id"],))
            
            total_people_brought = len(referred_visits)
            total_revenue_from_partner = sum(v["net_paid"] for v in referred_visits)
            accrued_payout_owed = sum(v["net_paid"] * (rk["commission_percent"] / 100.0) for v in referred_visits)
            
            perf_rows.append({
                "Partner Name Handle": rk["name"],
                "Commission Rate Set": f"{rk['commission_percent']}%",
                "Total People Brought In": f"{total_people_brought} patients",
                "Total Clinic Revenue Driven": f"{total_revenue_from_partner:,.0f} IQD",
                "Total Commission Accumulated Owed": f"{accrued_payout_owed:,.0f} IQD",
                "Campaign Platform Memo": rk["notes"]
            })
            
        st.dataframe(pd.DataFrame(perf_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No reklam marketing handles registered or tracking active profiles.")
