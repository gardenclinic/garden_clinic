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
.card .sub {
    font-size: 0.78rem;
    color: #8EA898;
    margin-top: 4px;
}

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

/* ── INPUTS ── */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input {
    border-radius: 9px !important;
    border: 1.5px solid #DDE8E1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: #FFFFFF !important;
    color: #1A2E23 !important;
    padding: 9px 12px !important;
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
# DATABASE
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
        
        # Updated doctors table with manual metric fields
        db.execute("""CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL UNIQUE, 
            specialty TEXT, 
            comm_type TEXT DEFAULT 'fixed', 
            fixed_rate REAL DEFAULT 10.0,
            manual_visitors_target INTEGER DEFAULT 0,
            manual_commission_payout REAL DEFAULT 0.0
        )""")
        
        # New table for marketing / video creators (reklams)
        db.execute("""CREATE TABLE IF NOT EXISTS reklams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            commission_per_visit REAL DEFAULT 0.0,
            notes TEXT
        )""")
        
        db.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, role TEXT NOT NULL, salary REAL NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, category TEXT, price REAL NOT NULL, active INTEGER DEFAULT 1)")
        db.execute("CREATE TABLE IF NOT EXISTS bundles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, description TEXT)")
        
        # Visits updated to include lead source configuration
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
        
        # Safe migration logic executions
        migrations = [
            ("source_type TEXT", "ALTER TABLE visits ADD COLUMN source_type TEXT DEFAULT 'Direct Walk-in'"),
            ("reklam_id INTEGER", "ALTER TABLE visits ADD COLUMN reklam_id INTEGER DEFAULT NULL"),
            ("manual_visitors_target", "ALTER TABLE doctors ADD COLUMN manual_visitors_target INTEGER DEFAULT 0"),
            ("manual_commission_payout", "ALTER TABLE doctors ADD COLUMN manual_commission_payout REAL DEFAULT 0.0"),
        ]
        for col, definition in migrations:
            try:
                db.execute(definition)
            except:
                pass
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
# HELPERS & INTERFACE BLOCKS
# ─────────────────────────────────────────────
def card(title, value, css_class="dark", subtitle=""):
    return f"""<div class="card">
        <h3>{title}</h3>
        <p class="big-num {css_class}">{value}</p>
        {f'<p class="sub">{subtitle}</p>' if subtitle else ''}
    </div>"""

def section_label(text):
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)

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
# FINANCIAL CALCULATION ENGINE
# ─────────────────────────────────────────────
def get_financials(start=None, end=None):
    q_income = "SELECT SUM(net_paid) as t FROM visits"
    q_expenses = "SELECT SUM(amount) as t FROM expenses"
    params = ()
    if start and end:
        q_income += " WHERE visit_date BETWEEN ? AND ?"
        q_expenses += " WHERE date BETWEEN ? AND ?"
        params = (start, end)
        
    income_row = fetch_one(q_income, params)
    gross = income_row["t"] if income_row and income_row["t"] else 0.0
    
    expenses_row = fetch_one(q_expenses, params)
    exp = expenses_row["t"] if expenses_row and expenses_row["t"] else 0.0
    
    # Calculate Doctor commissions based on their configured manual settings
    docs = fetch_all("SELECT name, manual_commission_payout FROM doctors")
    total_doc_commissions = sum(d["manual_commission_payout"] for d in docs) if docs else 0.0
    
    # Calculate Reklam dynamic commissions accrued
    reklam_totals = fetch_one("""
        SELECT SUM(r.commission_per_visit) as t 
        FROM visits v 
        JOIN reklams r ON v.reklam_id = r.id
    """)
    total_reklam_commissions = reklam_totals["t"] if reklam_totals and reklam_totals["t"] else 0.0
    
    total_out = exp + total_doc_commissions + total_reklam_commissions
    return gross, exp, total_doc_commissions, total_reklam_commissions, total_out, gross - total_out

# Financial execution pulls
gross_income, base_expenses, total_commissions, total_reklam_out, total_outflows, net_profit = get_financials()

today_str = date.today().isoformat()
today_row = fetch_one("SELECT SUM(net_paid) as t, COUNT(*) as c FROM visits WHERE visit_date = ?", (today_str,))
today_revenue = today_row["t"] if today_row and today_row["t"] else 0.0
today_visits = today_row["c"] if today_row else 0
patient_count = fetch_one("SELECT COUNT(*) as c FROM patients")["c"]

# ─────────────────────────────────────────────
# LOGIN CONTROLLER
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""<div class="login-card">
        <h1>🌿 Garden Clinic</h1>
        <p>Clinic Management System</p>
    </div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        login_tab, reg_tab = st.tabs(["Sign In", "Create Account"])
        
        with login_tab:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Sign In →", use_container_width=True):
                rec = fetch_all("SELECT * FROM users WHERE username = ? AND password_hash = ?", (u.strip(), hash_password(p)))
                if rec:
                    st.session_state.logged_in = True
                    st.session_state.username = rec[0]["username"]
                    st.session_state.role = rec[0]["role"]
                    log_activity("User signed into session.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
        with reg_tab:
            ru = st.text_input("New username")
            rp = st.text_input("New password", type="password")
            role_choice = st.selectbox("Role", ["Boss", "Accounting", "Reception", "Reception & Accounting"])
            code = st.text_input("Admin code", type="password")
            if st.button("Create Account", use_container_width=True):
                if code != "1011":
                    st.error("Invalid admin code.")
                elif ru and rp:
                    if execute_write("INSERT INTO users (username, password_hash, role, plaintext_password) VALUES (?,?,?,?)", (ru.strip(), hash_password(rp), role_choice, rp.strip())):
                        st.success("Account created. Sign in above.")
                    else:
                        st.error("Username already taken.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
role = st.session_state.role
username = st.session_state.username

st.sidebar.markdown(f"""
    <div style="padding: 20px 16px 16px; border-bottom: 1px solid rgba(255,255,255,0.1);">
        <div style="font-size:1.4rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.5px;">🌿 Garden Clinic</div>
        <div style="font-size:0.75rem; color:#6FCF97; margin-top:2px; font-weight:500;">Management System</div>
    </div>
    <div style="padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom:8px;">
        <div style="font-size:0.7rem; color:#6FCF97; text-transform:uppercase; letter-spacing:0.06em;">Signed in as</div>
        <div style="font-size:0.95rem; color:#FFFFFF; font-weight:600; margin-top:2px;">{username}</div>
        <div style="font-size:0.72rem; background:rgba(111,207,151,0.2); color:#6FCF97; display:inline-block; padding:2px 8px; border-radius:20px; margin-top:4px; font-weight:600;">{role}</div>
    </div>
""", unsafe_allow_html=True)

menu_map = {
    "Boss": ["📈 Dashboard", "🖥️ Reception", "📊 Accounting", "📅 Appointments", "⚙️ Settings"],
    "Reception & Accounting": ["🖥️ Reception", "📊 Accounting", "📅 Appointments"],
    "Accounting": ["📊 Accounting"],
    "Reception": ["🖥️ Reception", "📅 Appointments"],
}
menus = menu_map.get(role, [])
selected = st.sidebar.radio("Navigation", menus, label_visibility="collapsed")

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Sign Out", use_container_width=True):
    log_activity("User signed out.")
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.markdown('<div class="sidebar-footer-text">(crate it by haryad)</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODULE: DASHBOARD
# ─────────────────────────────────────────────
if selected == "📈 Dashboard":
    page_header("Executive Dashboard", f"Clinic overview targets · {date.today().strftime('%A, %B %d %Y')}")
    
    pulse_bar([
        ("Today's Revenue", f"{today_revenue:,.0f} IQD"),
        ("Visits Today", str(today_visits)),
        ("Total Patients", str(patient_count)),
        ("Net Profit", f"{net_profit:,.0f} IQD"),
    ])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(card("Gross Revenue", f"{gross_income:,.0f} IQD", "green"), unsafe_allow_html=True)
    with col2:
        st.markdown(card("Base Operational Expenses", f"{base_expenses:,.0f} IQD", "red"), unsafe_allow_html=True)
    with col3:
        st.markdown(card("Doctor Commission Owed", f"{total_commissions:,.0f} IQD", "dark"), unsafe_allow_html=True)
    with col4:
        st.markdown(card("Reklam Marketing Owed", f"{total_reklam_out:,.0f} IQD", "dark"), unsafe_allow_html=True)

    # Manual Target Overview & Payouts for Doctors
    st.markdown("---")
    st.subheader("👨‍⚕️ Manual Doctor Commision Control Panel")
    all_docs_metrics = fetch_all("SELECT id, name, specialty, manual_visitors_target, manual_commission_payout FROM doctors")
    
    if all_docs_metrics:
        doc_rows = []
        for d in all_docs_metrics:
            actual_count = fetch_one("SELECT COUNT(*) as c FROM visits WHERE doctor_id = ?", (d["id"],))["c"]
            doc_rows.append({
                "Doctor Name": d["name"],
                "Specialty": d["specialty"],
                "Actual Visitors This Month": actual_count,
                "Configured Target Visitors": d["manual_visitors_target"],
                "Manual Commission Payout Settled": f"{d['manual_commission_payout']:,.0f} IQD"
            })
        st.dataframe(pd.DataFrame(doc_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No doctors configured.")

    st.markdown("---")
    section_label("Recent Activity Tracker Logs")
    recent_logs = fetch_all("SELECT timestamp as Timestamp, user as [User Agent], action as [Action Executed] FROM system_logs ORDER BY id DESC LIMIT 10")
    if recent_logs:
        st.dataframe(pd.DataFrame([dict(l) for l in recent_logs]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: RECEPTION
# ─────────────────────────────────────────────
elif selected == "🖥️ Reception":
    page_header("Reception Desk", "Patient checkout and registration profiles.")
    
    t1, t2, t3, t4 = st.tabs(["Checkout Desk", "Patient Records", "Add Patient Profile", "Visit History Ledger"])
    
    # ── CHECKOUT DESK ──
    with t1:
        section_label("New Patient Checkout Processing")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        services_db = fetch_all("SELECT id, name, price FROM services WHERE active = 1 ORDER BY name")
        bundles_db = fetch_all("SELECT id, name, price FROM bundles ORDER BY name")
        reklams_db = fetch_all("SELECT id, name FROM reklams ORDER BY name")
        
        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please configure doctors and treatment items in Settings to proceed.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            r_map = {r["name"]: r["id"] for r in reklams_db}
            
            col1, col2 = st.columns(2)
            with col1:
                target_p = st.selectbox("Patient Profile Selection", ["— select —"] + list(p_map.keys()))
                chosen_doc = st.selectbox("Assigning Doctor", list(d_map.keys()))
                payment_method = st.selectbox("Payment Gateway Method", ["Cash", "Card", "Insurance", "Transfer"])
                
                # Dynamic Question Integration: Where did you find us?
                st.markdown("##### 🔍 Marketing Referral Channel")
                source_options = ["Direct Walk-in", "Social Media (Organic)", "Friend Referral", "Video Content Creator / Reklam Partner"]
                selected_source = st.selectbox("Where did you find us?", source_options)
                
                chosen_reklam_id = None
                if selected_source == "Video Content Creator / Reklam Partner":
                    if reklams_db:
                        selected_reklam_name = st.selectbox("Select Reklam Partner Name", list(r_map.keys()))
                        chosen_reklam_id = r_map[selected_reklam_name]
                    else:
                        st.info("No reklam video partners registered under Settings yet.")
                
            with col2:
                item_type = st.radio("Treatment Selection Base", ["Service", "Bundle"], horizontal=True)
                srv_id = bnd_id = None
                base_price = 0.0
                chosen_item_name = ""
                
                if item_type == "Service":
                    if services_db:
                        s_map = {f"{s['name']} — {s['price']:,.0f} IQD": (s["id"], s["price"], s["name"]) for s in services_db}
                        chosen = st.selectbox("Service Treatment", list(s_map.keys()))
                        srv_id, base_price, chosen_item_name = s_map[chosen]
                else:
                    if bundles_db:
                        b_map = {f"{b['name']} — {b['price']:,.0f} IQD": (b["id"], b["price"], b["name"]) for b in bundles_db}
                        chosen = st.selectbox("Care Package Bundle", list(b_map.keys()))
                        bnd_id, base_price, chosen_item_name = b_map[chosen]
                        
                disc_type = st.radio("Apply Discount Option", ["None", "Fixed (IQD)", "Percent (%)"], horizontal=True)
                disc_val = st.number_input("Discount Deducted Value", min_value=0.0, step=250.0)
                
                final_due = base_price
                if disc_type == "Fixed (IQD)":
                    final_due = max(0.0, base_price - disc_val)
                elif disc_type == "Percent (%)":
                    final_due = max(0.0, base_price * (1 - disc_val / 100))
                    
                visit_notes = st.text_area("Internal Checkout Memo Notes", height=70)
                
            st.markdown(f"### Net Total Settlement Amount: **{final_due:,.0f} IQD**")
            if st.button("Complete Payment Receipt Ledger Entry", use_container_width=True):
                if target_p == "— select —":
                    st.error("Please assign an absolute valid patient identity record profile.")
                else:
                    disc_amt = base_price - final_due
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, bundle_id, visit_date, base_price, discount_amount, net_paid, payment_method, source_type, reklam_id, notes)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, bnd_id, today_str, base_price, disc_amt, final_due, payment_method, selected_source, chosen_reklam_id, visit_notes))
                    
                    log_activity(f"Checked out patient '{target_p}' via channel '{selected_source}' for total {final_due:,.0f} IQD.")
                    st.success("Ledger transactional checkout documented successfully.")
                    st.rerun()

    # ── PATIENT RECORDS ──
    with t2:
        section_label("Registered Patient Directory Index")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if all_p:
            st.dataframe(pd.DataFrame([dict(p) for p in all_p]), use_container_width=True, hide_index=True)
            st.markdown("---")
            section_label("Archive / Drop Patient Document")
            del_target = st.selectbox("Select patient profile to entirely remove", ["— select —"] + [p["name"] for p in all_p])
            if st.button("Purge Patient File Data Base Path", type="primary"):
                if del_target != "— select —":
                    execute_write("DELETE FROM patients WHERE name = ?", (del_target,))
                    log_activity(f"Removed patient profile completely: '{del_target}'")
                    st.success(f"Purged data path profile folder reference targeting '{del_target}'.")
                    st.rerun()

    # ── ADD PATIENT ──
    with t3:
        section_label("File Registration Wizard For New Patients")
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Full Patient Name Identifier *")
            p_phone = st.text_input("Active Personal Phone Matrix Contact")
            p_dob = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1995-06-20")
        with col2:
            p_gender = st.selectbox("Biological Demographic Gender", ["Prefer not to say", "Male", "Female"])
            p_notes = st.text_area("Clinical Summary Medical Conditions / History Background Notes", height=100)
            
        if st.button("Commit Profile Record Entry"):
            if p_name.strip():
                if execute_write("INSERT INTO patients (name, phone, date_of_birth, gender, notes, created_at) VALUES (?,?,?,?,?,?)", (p_name.strip(), p_phone.strip(), p_dob.strip(), p_gender, p_notes.strip(), today_str)):
                    log_activity(f"Added patient profile: '{p_name.strip()}'")
                    st.success(f"Profile directory entry instantiated targeting target context: '{p_name}'.")
                    st.rerun()
            else:
                st.error("Identification full name string parameter field cannot remain completely blank.")

    # ── VISIT HISTORY ──
    with t4:
        section_label("Visit Records Ledger Historical Overview")
        v_history = fetch_all("""
            SELECT v.id as [Visit ID], v.visit_date as Date, p.name as Patient, d.name as Doctor, 
                   v.net_paid as [Net Paid], v.source_type as [Referral Source]
            FROM visits v 
            JOIN patients p ON v.patient_id = p.id
            JOIN doctors d ON v.doctor_id = d.id
            ORDER BY v.id DESC
        """)
        if v_history:
            st.dataframe(pd.DataFrame([dict(vh) for vh in v_history]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: APPOINTMENTS
# ─────────────────────────────────────────────
elif selected == "📅 Appointments":
    page_header("Appointments Scheduling Desk")
    ta1, ta2 = st.tabs(["Book New Slots", "Comprehensive Active Schedule Sheet"])
    
    with ta1:
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        if patients_db and docs_db:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            col1, col2 = st.columns(2)
            with col1:
                ap_p = st.selectbox("Target Patient Profile", list(p_map.keys()))
                ap_d = st.selectbox("Assign Consultation Doctor Slot", list(d_map.keys()))
            with col2:
                ap_date = st.date_input("Target Date Calendar", value=date.today())
                ap_time = st.text_input("Target Clock Time Representation Slot", value="14:30")
                ap_reason = st.text_input("Operational Reason / Clinical Complaint Description")
                
            if st.button("Finalize Appointment Registration Path"):
                execute_write("INSERT INTO appointments (patient_id, doctor_id, appt_date, appt_time, reason) VALUES (?,?,?,?,?)", (p_map[ap_p], d_map[ap_d], str(ap_date), ap_time, ap_reason))
                log_activity(f"Booked slot for '{ap_p}' with doctor '{ap_d}'.")
                st.success("Calendar slot reserved and committed.")

    with ta2:
        all_ap = fetch_all("""
            SELECT a.id as ID, a.appt_date as Date, a.appt_time as Time, p.name as Patient, d.name as Doctor, a.reason as Reason, a.status as Status
            FROM appointments a 
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
        """)
        if all_ap:
            st.dataframe(pd.DataFrame([dict(x) for x in all_ap]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: ACCOUNTING
# ─────────────────────────────────────────────
elif selected == "📊 Accounting":
    page_header("Accounting Department", "Comprehensive business ledger monitoring and cost audits.")
    
    col1, col2 = st.columns(2)
    with col1:
        section_label("Document Business Expense Output Outflows")
        with st.form("add_exp_form"):
            e_desc = st.text_input("Expense Description Target Line")
            e_cat = st.selectbox("Expense Allocation Category Row", ["General", "Supplies", "Utilities", "Rent", "Equipment", "Marketing"])
            e_amt = st.number_input("Amount Paid Out Context (IQD)", min_value=0.0, step=1000.0)
            if st.form_submit_button("Log Transaction"):
                if e_desc and e_amt > 0:
                    execute_write("INSERT INTO expenses (description, category, amount, date) VALUES (?,?,?,?)", (e_desc, e_cat, e_amt, today_str))
                    log_activity(f"Logged expenditure operational line: '{e_desc}' for {e_amt:,.0f} IQD")
                    st.success("Expenditure row entry finalized.")
                    st.rerun()
    with col2:
        section_label("Comprehensive Operational Outflow Sheet Log")
        all_exp = fetch_all("SELECT date as Date, category as Category, description as Description, amount as Amount FROM expenses ORDER BY date DESC")
        if all_exp:
            st.dataframe(pd.DataFrame([dict(ex) for ex in all_exp]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: SETTINGS
# ─────────────────────────────────────────────
elif selected == "⚙️ Settings":
    page_header("Settings & Clinical Configuration Profiles")
    
    set_tabs_list = ["Doctor Roster Configuration", "📢 Reklam Partners (Marketing)", "Services Options", "Bundles", "🔐 Account Matrix Management"]
    s_tabs = st.tabs(set_tabs_list)
    
    # ── DOCTOR CONFIGURATION WITH MANUAL OVERRIDES ──
    with s_tabs[0]:
        section_label("Configure Roster Doctors & Adjust Commission Parameters Manually")
        
        with st.form("doctor_add_form"):
            doc_name_str = st.text_input("Physician Identity Name *")
            doc_spec_str = st.text_input("Area of Expertise Specialty Designation")
            initial_visitors_target = st.number_input("Target Visitors Bound Goal Amount", min_value=0, step=1, value=0)
            initial_comm_payout = st.number_input("Manual Settled Commission Value Payout (IQD)", min_value=0.0, step=5000.0, value=0.0)
            
            if st.form_submit_button("Register Doctor Profile"):
                if doc_name_str.strip():
                    if execute_write("INSERT INTO doctors (name, specialty, manual_visitors_target, manual_commission_payout) VALUES (?,?,?,?)", 
                                  (doc_name_str.strip(), doc_spec_str.strip(), initial_visitors_target, initial_comm_payout)):
                        log_activity(f"Added doctor profile: '{doc_name_str.strip()}' with custom commission settings.")
                        st.success(f"Profile baseline saved targeting '{doc_name_str}'.")
                        st.rerun()
                else:
                    st.error("Name field required verification parameters filled.")
                    
        st.markdown("---")
        section_label("Modify Dynamic Performance Commissions Owed & Target Visitor Thresholds Manually")
        
        current_physicians = fetch_all("SELECT id, name, specialty, manual_visitors_target, manual_commission_payout FROM doctors ORDER BY name")
        if current_physicians:
            for phys in current_physicians:
                with st.expander(f"⚙️ Adjustment Parameters Panel — Dr. {phys['name']} ({phys['specialty']})"):
                    col_edit1, col_edit2 = st.columns(2)
                    with col_edit1:
                        new_target_visitors = st.number_input(f"Set Target Visitors Metric Amount", min_value=0, step=1, value=int(phys['manual_visitors_target']), key=f"t_v_{phys['id']}")
                    with col_edit2:
                        new_comm_val_override = st.number_input(f"Set Manual Total Commission Owed (IQD)", min_value=0.0, step=1000.0, value=float(phys['manual_commission_payout']), key=f"c_p_{phys['id']}")
                        
                    if st.button(f"Save Manual Values Configuration Matrix Paths", key=f"btn_save_doc_{phys['id']}"):
                        execute_write("UPDATE doctors SET manual_visitors_target = ?, manual_commission_payout = ? WHERE id = ?", (new_target_visitors, new_comm_val_override, phys['id']))
                        log_activity(f"Manually modified target metrics/commissions for Doctor '{phys['name']}' to {new_target_visitors} visitors and {new_comm_val_override:,.0f} IQD payout.")
                        st.success(f"System updated parameters baseline fields safely.")
                        st.rerun()
                        
            st.markdown("---")
            section_label("Delete Doctor Profiles")
            target_drop_doc = st.selectbox("Select doctor profile line to completely archive", ["— select —"] + [d["name"] for d in current_physicians])
            if st.button("Delete Doctor From Database File", type="primary"):
                if target_drop_doc != "— select —":
                    execute_write("DELETE FROM doctors WHERE name = ?", (target_drop_doc,))
                    log_activity(f"Removed physician clinical reference file index: '{target_drop_doc}'")
                    st.success("Target context file erased safely.")
                    st.rerun()

    # ── NEW TAB: REKLAMS / VIDEO CREATORS MARKETING COMMISSION ENGINE ──
    with s_tabs[1]:
        section_label("📢 Video Content Creators & Marketing Reklam Partners Registry")
        st.info("Configure social media marketing creators or promo handles. Every patient referral recorded under checkout will log commission payments due for them.")
        
        col_rek1, col_rek2 = st.columns([1, 1.5])
        with col_rek1:
            st.markdown("##### Add New Promotional Reklam Profile")
            rek_name_in = st.text_input("Content Creator / Reklam Partner Name Identity Identifier")
            rek_comm_per = st.number_input("Flat Commission Settled Due Per Referred Patient Visit (IQD)", min_value=0.0, step=500.0, value=0.0)
            rek_notes_in = st.text_input("Social Handle Profile / Notes Reference (e.g., TikTok Video campaign)")
            
            if st.button("Register Marketing Asset"):
                if rek_name_in.strip():
                    if execute_write("INSERT INTO reklams (name, commission_per_visit, notes) VALUES (?,?,?)", (rek_name_in.strip(), rek_comm_per, rek_notes_in.strip())):
                        log_activity(f"Created advertising promotional partner profile: '{rek_name_in.strip()}' paying {rek_comm_per:,.0f} IQD per patient checkout track.")
                        st.success("Marketing promotional handle registered.")
                        st.rerun()
                else:
                    st.error("Name context matrix required validation fields.")
                    
        with col_rek2:
            st.markdown("##### Current Advertising Partners & Accumulating Commission Metrics Sheets")
            all_reklams_listed = fetch_all("SELECT id, name, commission_per_visit, notes FROM reklams ORDER BY name")
            if all_reklams_listed:
                rek_rows_view = []
                for rk in all_reklams_listed:
                    referral_count = fetch_one("SELECT COUNT(*) as c FROM visits WHERE reklam_id = ?", (rk["id"],))["c"]
                    total_owed_accrued = referral_count * rk["commission_per_visit"]
                    rek_rows_view.append({
                        "Partner ID": rk["id"],
                        "Partner Name Handle": rk["name"],
                        "Commission / Lead Visit": f"{rk['commission_per_visit']:,.0f} IQD",
                        "Total Checked Visits Referred": referral_count,
                        "Accumulated Total Commissions Owed": f"{total_owed_accrued:,.0f} IQD",
                        "Platform Memo Campaign Notes": rk["notes"]
                    })
                st.dataframe(pd.DataFrame(rek_rows_view), use_container_width=True, hide_index=True)
                
                st.markdown("---")
                target_del_rek = st.selectbox("Select marketing partner profile item to completely drop", ["— select —"] + [rk["name"] for rk in all_reklams_listed])
                if st.button("Remove Reklam Partner Reference Track", type="primary"):
                    if target_del_rek != "— select —":
                        execute_write("DELETE FROM reklams WHERE name = ?", (target_del_rek,))
                        log_activity(f"Purged marketing reklam handle row object: '{target_del_rek}'")
                        st.success("Marketing row target entry cleared from system path indices.")
                        st.rerun()

    # ── SERVICES ──
    with s_tabs[2]:
        section_label("Clinic Standard Catalog Services Configuration Desk")
        with st.form("svc_add_form"):
            srv_n = st.text_input("New Treatment Service Identifier Description Text Line")
            srv_p = st.number_input("Standard Catalog Base Price Asset Tag (IQD)", min_value=0.0, step=5000.0)
            if st.form_submit_button("Add Treatment Service Type"):
                if srv_n.strip():
                    execute_write("INSERT INTO services (name, price, active) VALUES (?,?,1)", (srv_n.strip(), srv_p))
                    log_activity(f"Created service: '{srv_n.strip()}'.")
                    st.success("Treatment profile logged.")
                    st.rerun()
        st.markdown("---")
        all_s = fetch_all("SELECT id, name, price FROM services WHERE active = 1")
        if all_s:
            st.dataframe(pd.DataFrame([dict(sk) for sk in all_s]), use_container_width=True, hide_index=True)

    # ── BUNDLES ──
    with s_tabs[3]:
        section_label("Configure Treatment Package Bundles")
        with st.form("bnd_add_form"):
            bnd_n = st.text_input("Bundle Group Description Label Name")
            bnd_p = st.number_input("Package Price Bundle Allocation (IQD)", min_value=0.0, step=5000.0)
            if st.form_submit_button("Create Package Bundle Option"):
                if bnd_n.strip():
                    execute_write("INSERT INTO bundles (name, price) VALUES (?,?)", (bnd_n.strip(), bnd_p))
                    log_activity(f"Created catalog bundle: '{bnd_n.strip()}'.")
                    st.success("Bundle catalog profile saved.")
                    st.rerun()

    # ── ACCOUNT MATRIX MANAGEMENT (BOSS CONTROL DESK ONLY) ──
    with s_tabs[4]:
        if role != "Boss":
            st.error("Administrative privilege verification requirements unmet.")
        else:
            section_label("System Registration Access Identity Profiles Control Desk")
            sys_users = fetch_all("SELECT id, username, role, plaintext_password FROM users ORDER BY username")
            st.metric("Total Authorized Accounts Registered", len(sys_users))
            
            raw_u_list = []
            for usr in sys_users:
                raw_u_list.append({
                    "Account ID": usr["id"],
                    "Username Handle": usr["username"],
                    "System Control Privilege Role": usr["role"],
                    "Plaintext Password String Representation": usr["plaintext_password"] if usr["plaintext_password"] else "— Enforced Hash Override —"
                })
            st.dataframe(pd.DataFrame(raw_u_list), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            col_u1, col_u2 = st.columns(2)
            with col_u1:
                st.markdown("##### Change User Password Access Credentials")
                t_user_edit = st.selectbox("Select target account identity", [u["username"] for u in sys_users])
                new_pw_str = st.text_input("Enter alternative password path string configuration", type="password")
                if st.button("Apply Security Overwrite"):
                    if new_pw_str.strip():
                        h_new = hash_password(new_pw_str)
                        execute_write("UPDATE users SET password_hash = ?, plaintext_password = ? WHERE username = ?", (h_new, new_pw_str.strip(), t_user_edit))
                        log_activity(f"Administrative password change forced targeting user profile login: '{t_user_edit}'")
                        st.success("Security credentials updated.")
                        st.rerun()
            with col_u2:
                st.markdown("##### Revoke System Profile Session Entry Access")
                t_user_del = st.selectbox("Select user profile target to delete", ["— select —"] + [u["username"] for u in sys_users if u["username"] != username])
                if st.button("Purge Profile Permanently", type="primary"):
                    if t_user_del != "— select —":
                        execute_write("DELETE FROM users WHERE username = ?", (t_user_del,))
                        log_activity(f"Completely terminated session access rights and removed user: '{t_user_del}'")
                        st.success(f"Purged profile reference identifier: '{t_user_del}'.")
                        st.rerun()

    st.markdown("---")
    section_label("Global System Operational Audit Trace Records")
    all_logs = fetch_all("SELECT timestamp as Timestamp, user as [User Agent], action as [Trace Activity Execution Line] FROM system_logs ORDER BY id DESC LIMIT 20")
    if all_logs:
        st.dataframe(pd.DataFrame([dict(lx) for lx in all_logs]), use_container_width=True, hide_index=True)
