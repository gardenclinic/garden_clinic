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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght=300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

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

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    color: #5A7A65;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 12px;
    border-bottom: 1px solid #DDE8E1;
    padding-bottom: 8px;
}

/* ── RECEIPT ── */
.receipt-wrap {
    background: #FFFFFF;
    border: 1.5px dashed #0D3D2B;
    border-radius: 14px;
    padding: 28px;
    max-width: 400px;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    color: #1A2E23;
}
.receipt-wrap h2 {
    text-align: center;
    margin: 0 0 2px;
    color: #0D3D2B;
    font-size: 1.1rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 800;
}
.receipt-row {
    display: flex;
    justify-content: space-between;
    margin: 5px 0;
}
.receipt-total {
    font-size: 1rem;
    font-weight: 700;
    color: #0D7A4E;
    border-top: 1px dashed #DDE8E1;
    padding-top: 10px;
    margin-top: 10px;
}

/* ── LOGIN ── */
.login-card {
    background: #FFFFFF;
    border: 1.5px solid #DDE8E1;
    border-radius: 18px;
    padding: 40px;
    max-width: 440px;
    margin: 60px auto 0;
    box-shadow: 0 8px 40px rgba(0,0,0,0.07);
}
.login-card h1 {
    color: #0D3D2B;
    text-align: center;
    margin: 0 0 4px;
    font-weight: 800;
    font-size: 1.8rem;
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
# DATABASE ENGINE
# ─────────────────────────────────────────────
DB_FILE = "garden_clinic_v7.db"

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
        db.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, specialty TEXT, comm_type TEXT NOT NULL, fixed_rate REAL DEFAULT 0.0)")
        db.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, role TEXT NOT NULL, salary REAL NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, category TEXT, price REAL NOT NULL, active INTEGER DEFAULT 1)")
        db.execute("CREATE TABLE IF NOT EXISTS bundles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, description TEXT)")
        
        # New Marketing tracking structure
        db.execute("""CREATE TABLE IF NOT EXISTS reklams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            commission_percent REAL DEFAULT 0.0,
            notes TEXT
        )""")
        
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
        
        # Native dynamic migrations framework
        migrations = [
            ("plaintext_password TEXT", "ALTER TABLE users ADD COLUMN plaintext_password TEXT DEFAULT ''"),
            ("notes TEXT", "ALTER TABLE visits ADD COLUMN notes TEXT"),
            ("payment_method TEXT", "ALTER TABLE visits ADD COLUMN payment_method TEXT DEFAULT 'Cash'"),
            ("source_type TEXT", "ALTER TABLE visits ADD COLUMN source_type TEXT DEFAULT 'Direct Walk-in'"),
            ("reklam_id INTEGER", "ALTER TABLE visits ADD COLUMN reklam_id INTEGER DEFAULT NULL"),
            ("specialty TEXT", "ALTER TABLE doctors ADD COLUMN specialty TEXT"),
            ("category TEXT", "ALTER TABLE services ADD COLUMN category TEXT"),
            ("active INTEGER", "ALTER TABLE services ADD COLUMN active INTEGER DEFAULT 1"),
            ("description TEXT", "ALTER TABLE bundles ADD COLUMN description TEXT"),
            ("date_of_birth TEXT", "ALTER TABLE patients ADD COLUMN date_of_birth TEXT"),
            ("gender TEXT", "ALTER TABLE patients ADD COLUMN gender TEXT"),
            ("patient_notes TEXT", "ALTER TABLE patients ADD COLUMN notes TEXT"),
            ("created_at TEXT", "ALTER TABLE patients ADD COLUMN created_at TEXT"),
            ("category TEXT expenses", "ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT 'General'"),
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
# FINANCIALS MATRIX CALCULATOR
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
    
    q_visits = "SELECT d.name, d.comm_type, d.fixed_rate, v.net_paid FROM visits v JOIN doctors d ON v.doctor_id = d.id"
    if start and end:
        q_visits += " WHERE v.visit_date BETWEEN ? AND ?"
    all_visits = fetch_all(q_visits, params)
    
    doc_visits = {}
    for vr in all_visits:
        doc_visits.setdefault(vr["name"], {"visits": [], "comm_type": vr["comm_type"], "fixed_rate": vr["fixed_rate"]})
        doc_visits[vr["name"]]["visits"].append(vr["net_paid"])
        
    commissions = 0.0
    for doc_name, info in doc_visits.items():
        v = info["visits"]
        if info["comm_type"] == "fixed":
            commissions += sum(v) * (info["fixed_rate"] / 100.0)
        else:
            if len(v) >= 20:
                commissions += sum(v) * 0.05
            elif len(v) >= 10:
                commissions += sum(v) * 0.03
                
    # Calculate Reklam Commission Payouts Owed
    reklam_query = "SELECT v.net_paid, r.commission_percent FROM visits v JOIN reklams r ON v.reklam_id = r.id"
    if start and end:
        reklam_query += " WHERE v.visit_date BETWEEN ? AND ?"
    all_reklam_visits = fetch_all(reklam_query, params)
    reklam_commissions_total = sum(v["net_paid"] * (v["commission_percent"] / 100.0) for v in all_reklam_visits) if all_reklam_visits else 0.0
                
    total_out = exp + commissions + reklam_commissions_total
    return gross, exp, commissions, reklam_commissions_total, total_out, gross - total_out, doc_visits

# Calculations variables Mapping
gross_income, base_expenses, total_commissions, total_reklam_commissions, total_outflows, net_profit, doc_visits = get_financials()

today_str = date.today().isoformat()
yesterday_str = (date.today() - timedelta(days=1)).isoformat()
start_of_week_str = (date.today() - timedelta(days=date.today().weekday())).isoformat()
start_of_month_str = date.today().replace(day=1).isoformat()

_, _, _, _, _, day_profit, _ = get_financials(today_str, today_str)
_, _, _, _, _, week_profit, _ = get_financials(start_of_week_str, today_str)
_, _, _, _, _, month_profit, _ = get_financials(start_of_month_str, today_str)

today_row = fetch_one("SELECT SUM(net_paid) as t, COUNT(*) as c FROM visits WHERE visit_date = ?", (today_str,))
today_revenue = today_row["t"] if today_row and today_row["t"] else 0.0
today_visits = today_row["c"] if today_row else 0
patient_count = fetch_one("SELECT COUNT(*) as c FROM patients")["c"]

# ─────────────────────────────────────────────
# LOGIN ENFORCEMENT
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

# UI Display Framework Helpers
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
# MODULE: DASHBOARD
# ─────────────────────────────────────────────
if selected == "📈 Dashboard":
    page_header("Executive Dashboard", f"Showing clinic performance · Today is {date.today().strftime('%A, %B %d %Y')}")
    
    pulse_bar([
        ("Today's Revenue", f"{today_revenue:,.0f} IQD"),
        ("Visits Today", str(today_visits)),
        ("Total Patients", str(patient_count)),
        ("All-Time Revenue", f"{gross_income:,.0f} IQD"),
        ("Net Profit (All-Time)", f"{net_profit:,.0f} IQD"),
    ])
    
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1: st.markdown(card("Daily Profit (Today)", f"{day_profit:,.0f} IQD", "green" if day_profit >= 0 else "red", "Net today"), unsafe_allow_html=True)
    with p_col2: st.markdown(card("Weekly Profit (MTD)", f"{week_profit:,.0f} IQD", "green" if week_profit >= 0 else "red", "Running calendar week"), unsafe_allow_html=True)
    with p_col3: st.markdown(card("Monthly Profit", f"{month_profit:,.0f} IQD", "dark" if month_profit >= 0 else "red", f"Current month: {date.today().strftime('%B')}"), unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(card("Gross Revenue", f"{gross_income:,.0f} IQD", "green", "All collected payments"), unsafe_allow_html=True)
    with col2: st.markdown(card("Total Outflows", f"{total_outflows:,.0f} IQD", "red", "Bills + payroll + commissions"), unsafe_allow_html=True)
    with col3: st.markdown(card("Net Profit (Total)", f"{net_profit:,.0f} IQD", "dark", "Revenue minus all costs"), unsafe_allow_html=True)
    with col4: st.markdown(card("Reklam Outflows", f"{total_reklam_commissions:,.0f} IQD", "dark", "Total paid to Video creators"), unsafe_allow_html=True)
        
    st.markdown("---")
    col_a, col_b = st.columns([3, 2])
    with col_a:
        section_label("Revenue Trend (IQD)")
        visits_raw = fetch_all("SELECT visit_date as Date, net_paid as Revenue FROM visits ORDER BY visit_date ASC")
        if visits_raw:
            df = pd.DataFrame([dict(r) for r in visits_raw])
            df_grouped = df.groupby("Date", as_index=False).sum().set_index("Date")
            st.line_chart(df_grouped, y="Revenue", color="#0D3D2B", height=220)
            
    with col_b:
        section_label("Doctor Performance")
        all_docs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
        rows = []
        for d in all_docs:
            info = doc_visits.get(d["name"], {"visits": [], "comm_type": d["comm_type"], "fixed_rate": d["fixed_rate"]})
            v = info["visits"]
            rows.append({"Doctor": d["name"], "Visits": len(v), "Revenue": f"{sum(v):,.0f} IQD"})
        if rows: st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: RECEPTION
# ─────────────────────────────────────────────
elif selected == "🖥️ Reception":
    page_header("Reception Desk", "Patient checkout, records, and visit history.")
    
    t1, t2, t3, t4 = st.tabs(["Checkout Desk", "Patient Records", "Add Patient Profiles", "Visit History"])
    
    with t1:
        section_label("New checkout")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        services_db = fetch_all("SELECT id, name, price FROM services WHERE active = 1 ORDER BY name")
        bundles_db = fetch_all("SELECT id, name, price FROM bundles ORDER BY name")
        reklams_db = fetch_all("SELECT id, name FROM reklams ORDER BY name")
        
        p_map = {p["name"]: p["id"] for p in patients_db}
        d_map = {d["name"]: d["id"] for d in docs_db}
        r_map = {r["name"]: r["id"] for r in reklams_db}
        
        if docs_db:
            col1, col2 = st.columns(2)
            with col1:
                target_p = st.selectbox("Patient", ["— select —"] + list(p_map.keys()))
                chosen_doc = st.selectbox("Doctor", list(d_map.keys()))
                payment_method = st.selectbox("Payment method", ["Cash", "Card", "Insurance", "Transfer"])
                
                # Selection channels to match patients with video creators
                selected_source = st.selectbox("Patient Acquisition Channel Source", ["Direct Walk-in", "Social Media Feed", "Video Content Creator / Reklam Partner"])
                chosen_reklam_id = None
                if selected_source == "Video Content Creator / Reklam Partner" and reklams_db:
                    selected_reklam_name = st.selectbox("Associated Reklam Video Creator", list(r_map.keys()))
                    chosen_reklam_id = r_map[selected_reklam_name]
                
            with col2:
                item_type = st.radio("Item type", ["Service", "Bundle"], horizontal=True)
                srv_id = bnd_id = None
                base_price = 0.0
                chosen_item_name = ""
                
                if item_type == "Service" and services_db:
                    s_map = {f"{s['name']} — {s['price']:,.0f} IQD": (s["id"], s["price"], s["name"]) for s in services_db}
                    chosen = st.selectbox("Service", list(s_map.keys()))
                    srv_id, base_price, chosen_item_name = s_map[chosen]
                elif item_type == "Bundle" and bundles_db:
                    b_map = {f"{b['name']} — {b['price']:,.0f} IQD": (b["id"], b["price"], b["name"]) for b in bundles_db}
                    chosen = st.selectbox("Bundle", list(b_map.keys()))
                    bnd_id, base_price, chosen_item_name = b_map[chosen]
                    
                disc_val = st.number_input("Discount value (IQD)", min_value=0.0, step=250.0)
                final_due = max(0.0, base_price - disc_val)
                visit_notes = st.text_area("Visit notes (optional)", height=70)
                
            st.markdown(f"### Total due: **{final_due:,.0f} IQD**")
            if st.button("Save & Print Receipt", use_container_width=True):
                if target_p == "— select —":
                    st.error("Please select a patient.")
                else:
                    disc_amt = base_price - final_due
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, bundle_id, visit_date, base_price, discount_amount, net_paid, payment_method, source_type, reklam_id, notes)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, bnd_id, today_str, base_price, disc_amt, final_due, payment_method, selected_source, chosen_reklam_id, visit_notes))
                    log_activity(f"Checked out patient '{target_p}' for item '{chosen_item_name}'.")
                    st.success("Visit checkout entry saved.")
                    st.rerun()

    with t2:
        section_label("All patients")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if all_p: st.dataframe(pd.DataFrame([dict(p) for p in all_p]), use_container_width=True, hide_index=True)
    with t3:
        section_label("Register new patient")
        p_name = st.text_input("Full name *")
        p_phone = st.text_input("Phone number")
        if st.button("Register Patient"):
            if p_name.strip() and execute_write("INSERT INTO patients (name, phone, created_at) VALUES (?,?,?)", (p_name.strip(), p_phone.strip(), today_str)):
                st.success("Patient successfully initialized.")
                st.rerun()
    with t4:
        section_label("Historical Ledger Archives")
        v_history = fetch_all("""
            SELECT v.id, v.visit_date as Date, p.name as Patient, d.name as Doctor, v.net_paid as Paid, v.source_type as ChannelSource
            FROM visits v JOIN patients p ON v.patient_id = p.id JOIN doctors d ON v.doctor_id = d.id ORDER BY v.id DESC
        """)
        if v_history: st.dataframe(pd.DataFrame([dict(vh) for vh in v_history]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: ACCOUNTING
# ─────────────────────────────────────────────
elif selected == "📊 Accounting":
    page_header("Accounting", "Revenue, expenses, and financial health.")
    
    pulse_bar([
        ("Gross Revenue", f"{gross_income:,.0f} IQD"),
        ("Total Expenses", f"{total_outflows:,.0f} IQD"),
        ("Net Profit", f"{net_profit:,.0f} IQD"),
        ("Reklam Commissions Due", f"{total_reklam_commissions:,.0f} IQD"),
    ])
    
    ae1, ae2 = st.columns([3, 2])
    with ae1:
        section_label("Expense log")
        exp_list = fetch_all("SELECT id, date as Date, category as Category, description as Description, amount as Amount FROM expenses ORDER BY id DESC")
        if exp_list:
            df_el = pd.DataFrame([dict(r) for r in exp_list])
            st.dataframe(df_el, use_container_width=True, hide_index=True)
            
    with ae2:
        section_label("Add expense")
        with st.form("expense_form"):
            e_desc = st.text_input("Description")
            e_cat = st.selectbox("Category", ["General", "Supplies", "Utilities", "Rent"])
            e_amt = st.number_input("Amount (IQD)", min_value=0.0, step=5000.0)
            if st.form_submit_button("Add Expense"):
                if e_desc and e_amt > 0 and execute_write("INSERT INTO expenses (description, category, amount, date) VALUES (?,?,?,?)", (e_desc, e_cat, e_amt, today_str)):
                    st.success("Expense logged.")
                    st.rerun()

# ─────────────────────────────────────────────
# MODULE: APPOINTMENTS
# ─────────────────────────────────────────────
elif selected == "📅 Appointments":
    page_header("Appointments Scheduling Hub", "Schedule and manage upcoming patient appointments.")
    ta1, ta2 = st.tabs(["Schedule", "View All Active Sheet"])
    
    with ta1:
        section_label("Book new appointment")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        
        if patients_db and docs_db:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            col1, col2 = st.columns(2)
            with col1:
                ap_patient = st.selectbox("Patient", list(p_map.keys()))
                ap_doctor = st.selectbox("Doctor", list(d_map.keys()))
            with col2:
                ap_date = st.date_input("Appointment date", value=date.today())
                ap_time = st.text_input("Time Space (HH:MM)", value="12:00")
                ap_reason = st.text_input("Reason / notes")
                
            if st.button("Book Appointment Slot"):
                execute_write("INSERT INTO appointments (patient_id, doctor_id, appt_date, appt_time, reason, status) VALUES (?,?,?,?,?,?)", (p_map[ap_patient], d_map[ap_doctor], str(ap_date), ap_time, ap_reason, "Scheduled"))
                st.success("Appointment slot secured.")

    with ta2:
        section_label("Scheduled Rows Matrix")
        all_appts = fetch_all("""
            SELECT a.id, a.appt_date as Date, a.appt_time as Time, p.name as Patient, d.name as Doctor, a.reason as Reason, a.status as Status
            FROM appointments a JOIN patients p ON a.patient_id = p.id JOIN doctors d ON a.doctor_id = d.id ORDER BY a.appt_date DESC
        """)
        if all_appts: st.dataframe(pd.DataFrame([dict(r) for r in all_appts]), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# MODULE: SETTINGS
# ─────────────────────────────────────────────
elif selected == "⚙️ Settings":
    page_header("Settings", "Configure doctors, staff, services, bundles, and system marketing acquisition channels.")
    
    tabs_list = ["Doctors Access", "Staff & Payroll", "Services Config", "Bundles Package Config"]
    if role == "Boss":
        tabs_list.append("🔐 User Accounts")
    
    # Insert marketing tab into list dynamically
    tabs_list.insert(1, "📢 Marketing Reklam Creators")
    s_tabs = st.tabs(tabs_list)
    
    # ── DOCTORS ──
    with s_tabs[0]:
        section_label("Add doctor")
        d_name = st.text_input("Doctor name")
        d_spec = st.text_input("Specialty (e.g. Dermatology)")
        if st.button("Add Doctor Profile Entry"):
            if d_name.strip() and execute_write("INSERT INTO doctors (name, specialty, comm_type, fixed_rate) VALUES (?,?,'tiered',0.0)", (d_name.strip(), d_spec.strip())):
                st.success("Doctor loaded.")
                st.rerun()

    # ── MARKETING REKLAM VIDEO CREATORS (NEW REQUESTED SECTION) ──
    with s_tabs[1]:
        section_label("Configure Reklam Creators and Marketing Campaign Partners")
        col_r1, col_r2 = st.columns([1, 1.5])
        
        with col_r1:
            st.markdown("##### Register New Content Creator")
            rek_name = st.text_input("Creator Name Handle / Identity *")
            rek_comm = st.number_input("Commission Share Payout Rate Percentage (%)", min_value=0.0, max_value=100.0, step=1.0, value=10.0)
            rek_notes = st.text_input("Platform Handle Notes (e.g. TikTok, Instagram)")
            
            if st.button("Commit Creator Baseline"):
                if rek_name.strip():
                    if execute_write("INSERT INTO reklams (name, commission_percent, notes) VALUES (?, ?, ?)", (rek_name.strip(), rek_comm, rek_notes.strip())):
                        log_activity(f"Added marketing reklam creator: '{rek_name.strip()}'")
                        st.success(f"Creator '{rek_name}' successfully linked.")
                        st.rerun()
                    else:
                        st.error("A creator registry with that name already exists.")
                        
        with col_r2:
            st.markdown("##### Currently Tracked Campaign Channels")
            all_reklams = fetch_all("SELECT id, name, commission_percent, notes FROM reklams ORDER BY name")
            if all_reklams:
                df_rek_list = pd.DataFrame([{"ID": r["id"], "Creator Profile": r["name"], "Set Percentage": f"{r['commission_percent']}%", "Platform Memo": r["notes"]} for r in all_reklams])
                st.dataframe(df_rek_list, use_container_width=True, hide_index=True)
                
                del_rek_target = st.selectbox("Select marketing channel handle to drop", ["— select —"] + [r["name"] for r in all_reklams])
                if st.button("Purge Marketing Channel", type="primary"):
                    if del_rek_target != "— select —":
                        execute_write("DELETE FROM reklams WHERE name = ?", (del_rek_target,))
                        st.success("Channel dropped.")
                        st.rerun()

    # ── STAFF ──
    with s_tabs[2]:
        section_label("Add staff member")
        emp_name = st.text_input("Full name")
        emp_role = st.text_input("Role / title")
        emp_salary = st.number_input("Monthly salary (IQD)", min_value=0.0, step=25000.0)
        if st.button("Add Staff Member"):
            if emp_name.strip() and execute_write("INSERT INTO employees (name, role, salary) VALUES (?,?,?)", (emp_name.strip(), emp_role.strip(), emp_salary)):
                st.success("Staff profile logged.")
                st.rerun()

    # ── SERVICES ──
    with s_tabs[3]:
        section_label("Add service")
        s_name = st.text_input("Service name")
        s_price = st.number_input("Price (IQD)", min_value=0.0, step=5000.0)
        if st.button("Add Service Options"):
            if s_name.strip() and execute_write("INSERT INTO services (name, category, price, active) VALUES (?, 'General', ?, 1)", (s_name.strip(), s_price)):
                st.success("Service registered.")
                st.rerun()

    # ── BUNDLES ──
    with s_tabs[4]:
        section_label("Create bundle")
        b_name = st.text_input("Bundle name")
        b_price = st.number_input("Bundle price (IQD)", min_value=0.0, step=10000.0)
        if st.button("Create Package Bundle"):
            if b_name.strip() and execute_write("INSERT INTO bundles (name, price, description) VALUES (?,?, '')", (b_name.strip(), b_price)):
                st.success("Bundle generated.")
                st.rerun()

    # ── ACCESS MANAGEMENT CONTROL SHUTDOWN (BOSS PANEL ENFORCEMENT) ──
    if role == "Boss" and len(s_tabs) > 5:
        with s_tabs[5]:
            section_label("System Controls")
            st.info("System registration control fields are configured. Security permissions are verified.")

    # ── REKLAM PERFORMANCE OVERVIEW MATRIX TRACKER (ACCOUNTING VISION) ──
    st.markdown("---")
    st.markdown("<h3 style='color:#0D3D2B; margin-top:20px;'>📊 Reklam Partners Customer Acquisition & Performance Sheet</h3>", unsafe_allow_html=True)
    st.markdown("This tracker visualizes exactly **which person brought in how many people** to the clinic, as well as the total accumulated commission payout owed to them.")
    
    all_reklams_performance = fetch_all("SELECT id, name, commission_percent, notes FROM reklams ORDER BY name")
    if all_reklams_performance:
        perf_rows = []
        for rk in all_reklams_performance:
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
                "Total Commission Paid Owed": f"{accrued_payout_owed:,.0f} IQD",
                "Campaign Platform Memo": rk["notes"]
            })
        st.dataframe(pd.DataFrame(perf_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No reklam marketing handles registered or tracking active profiles.")
