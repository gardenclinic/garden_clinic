import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime, date
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# GOOGLE SHEETS SYNC (OPTIONAL — won't crash if not configured)
# ─────────────────────────────────────────────
def sync_to_sheets(table_name: str, df: pd.DataFrame):
    """Push a dataframe to a Google Sheet worksheet. Silent no-op if GSheets not configured."""
    if not _gsheets_enabled or _gsheets_conn is None:
        return
    try:
        # ADD YOUR SPREADSHEET LINK HERE inside the quotes:
        _gsheets_conn.update(
            spreadsheet="https://docs.google.com/spreadsheets/d/14x5xF6uIvCVo4NedB9KT4T81FHE9EM-QUnkI_x-_sbQ/edit?usp=sharing",
            worksheet=table_name, 
            data=df
        )
    except Exception as e:
        st.sidebar.error(f"Sync failed: {e}") # Temporarily exposing error to see what happens

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
*, *::before, *::after { box-sizing: border-box; }
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
[data-testid="stSidebar"] * { color: #E8F0EB !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
section[data-testid="stSidebarNav"] { display: none; }

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
.pulse-stat { display: flex; flex-direction: column; }
.pulse-label { font-size: 0.72rem; color: #6FCF97; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.pulse-value { font-family: 'DM Mono', monospace; font-size: 1.35rem; font-weight: 500; color: #FFFFFF; margin-top: 2px; }
.pulse-divider { width: 1px; background: rgba(255,255,255,0.15); height: 36px; align-self: center; }

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
.card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 4px 0; font-size: 0.8rem; color: #5A7A65; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.card .big-num { font-family: 'DM Mono', monospace; font-size: 2rem; font-weight: 500; margin: 0; }
.card .big-num.green { color: #0D7A4E; }
.card .big-num.red { color: #C0392B; }
.card .big-num.dark { color: #0D3D2B; }
.card .sub { font-size: 0.78rem; color: #8EA898; margin-top: 4px; }

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
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    border-radius: 9px !important;
    border: 1.5px solid #DDE8E1 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    background: #FFFFFF !important;
    color: #1A2E23 !important;
    padding: 9px 12px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #0D3D2B !important;
    box-shadow: 0 0 0 3px rgba(13,61,43,0.08) !important;
}
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div {
    border-radius: 9px !important;
    border: 1.5px solid #DDE8E1 !important;
    background: #FFFFFF !important;
}
.stTextArea textarea {
    border-radius: 9px !important;
    border: 1.5px solid #DDE8E1 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── RADIO ── */
.stRadio > div { gap: 8px !important; }
.stRadio label { font-size: 0.88rem !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1.5px solid #DDE8E1 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── ALERTS ── */
.stSuccess > div { border-radius: 10px !important; font-size: 0.88rem !important; }
.stError > div { border-radius: 10px !important; font-size: 0.88rem !important; }
.stWarning > div { border-radius: 10px !important; font-size: 0.88rem !important; }
.stInfo > div { border-radius: 10px !important; font-size: 0.88rem !important; }

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

/* ── BADGE ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.badge-green { background: #D1FAE5; color: #065F46; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-red { background: #FEE2E2; color: #991B1B; }
.badge-blue { background: #DBEAFE; color: #1E3A8A; }

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
.receipt-wrap h2 { text-align: center; margin: 0 0 2px; color: #0D3D2B; font-size: 1.1rem; font-family: 'DM Sans', sans-serif; font-weight: 800; }
.receipt-wrap .receipt-sub { text-align: center; font-size: 0.72rem; color: #5A7A65; margin-bottom: 14px; font-family: 'DM Sans', sans-serif; }
.receipt-row { display: flex; justify-content: space-between; margin: 5px 0; }
.receipt-total { font-size: 1rem; font-weight: 700; color: #0D7A4E; border-top: 1px dashed #DDE8E1; padding-top: 10px; margin-top: 10px; }
.receipt-footer { text-align: center; font-size: 0.7rem; color: #8EA898; margin-top: 14px; font-family: 'DM Sans', sans-serif; }
hr.dashed { border: none; border-top: 1px dashed #DDE8E1; margin: 12px 0; }

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
.login-card h1 { color: #0D3D2B; text-align: center; margin: 0 0 4px; font-weight: 800; font-size: 1.8rem; }
.login-card p { text-align: center; color: #5A7A65; font-size: 0.88rem; margin-bottom: 24px; }

/* ── SIDEBAR NAV ACTIVE ── */
div[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.87rem !important;
}

/* ── FORM SUBMIT ── */
.stForm [data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: #0D3D2B !important;
}

/* ── METRIC ── */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1.5px solid #DDE8E1;
    border-radius: 12px;
    padding: 16px 20px;
}
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: #5A7A65 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 1.6rem !important; color: #0D3D2B !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
DB_FILE = "garden_clinic_v7.db"

def hash_password(pw): return hashlib.sha256(pw.encode()).hexdigest()

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
        with db: db.execute(q, p)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()

def init_db():
    db = get_db()
    with db:
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT, date_of_birth TEXT, gender TEXT, notes TEXT, created_at TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS doctors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, specialty TEXT, comm_type TEXT NOT NULL, fixed_rate REAL DEFAULT 0.0)")
        db.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, role TEXT NOT NULL, salary REAL NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS services (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, category TEXT, price REAL NOT NULL, active INTEGER DEFAULT 1)")
        db.execute("CREATE TABLE IF NOT EXISTS bundles (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, price REAL NOT NULL, description TEXT)")
        db.execute("""CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER, doctor_id INTEGER, service_id INTEGER, bundle_id INTEGER,
            visit_date TEXT, base_price REAL, discount_amount REAL, net_paid REAL,
            payment_method TEXT DEFAULT 'Cash', notes TEXT
        )""")
        db.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL, category TEXT DEFAULT 'General', amount REAL NOT NULL, date TEXT NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id INTEGER, doctor_id INTEGER, appt_date TEXT, appt_time TEXT, reason TEXT, status TEXT DEFAULT 'Scheduled')")
        db.execute("CREATE TABLE IF NOT EXISTS referrers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, phone TEXT, commission_rate REAL NOT NULL DEFAULT 0.0, notes TEXT, added_by TEXT, created_at TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS subscriptions (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, amount REAL NOT NULL, billing_day INTEGER DEFAULT 1, category TEXT DEFAULT 'Subscription', active INTEGER DEFAULT 1, added_by TEXT, created_at TEXT)")
        db.execute("CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, action TEXT NOT NULL, details TEXT, timestamp TEXT NOT NULL)")

        # migrations
        for col, definition in [
            ("notes TEXT", "ALTER TABLE visits ADD COLUMN notes TEXT"),
            ("payment_method TEXT", "ALTER TABLE visits ADD COLUMN payment_method TEXT DEFAULT 'Cash'"),
            ("specialty TEXT", "ALTER TABLE doctors ADD COLUMN specialty TEXT"),
            ("category TEXT", "ALTER TABLE services ADD COLUMN category TEXT"),
            ("active INTEGER", "ALTER TABLE services ADD COLUMN active INTEGER DEFAULT 1"),
            ("description TEXT", "ALTER TABLE bundles ADD COLUMN description TEXT"),
            ("date_of_birth TEXT", "ALTER TABLE patients ADD COLUMN date_of_birth TEXT"),
            ("gender TEXT", "ALTER TABLE patients ADD COLUMN gender TEXT"),
            ("patient_notes TEXT", "ALTER TABLE patients ADD COLUMN notes TEXT"),
            ("created_at TEXT", "ALTER TABLE patients ADD COLUMN created_at TEXT"),
            ("category TEXT expenses", "ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT 'General'"),
            ("referred_by TEXT visits", "ALTER TABLE visits ADD COLUMN referred_by TEXT"),
            ("added_by TEXT visits", "ALTER TABLE visits ADD COLUMN added_by TEXT"),
            ("added_by TEXT expenses", "ALTER TABLE expenses ADD COLUMN added_by TEXT"),
        ]:
            try: db.execute(definition)
            except: pass
    db.close()

init_db()

# ─────────────────────────────────────────────
# AUTO PAYROLL
# ─────────────────────────────────────────────
def auto_payroll():
    month = datetime.now().strftime("%Y-%m")
    tag = f"Monthly Payroll — {month}"
    if not fetch_all("SELECT id FROM expenses WHERE description = ?", (tag,)):
        row = fetch_one("SELECT SUM(salary) as t FROM employees")
        total = row["t"] if row and row["t"] else 0.0
        if total > 0:
            execute_write("INSERT INTO expenses (description, category, amount, date) VALUES (?,?,?,?)",
                          (tag, "Payroll", total, f"{month}-01"))

auto_payroll()

# ─────────────────────────────────────────────
# AUTO SUBSCRIPTIONS
# ─────────────────────────────────────────────
def auto_subscriptions():
    month = datetime.now().strftime("%Y-%m")
    active_subs = fetch_all("SELECT * FROM subscriptions WHERE active = 1")
    for sub in active_subs:
        tag = f"Subscription: {sub['name']} — {month}"
        if not fetch_all("SELECT id FROM expenses WHERE description = ?", (tag,)):
            bill_day = sub["billing_day"] if sub["billing_day"] else 1
            bill_date = f"{month}-{bill_day:02d}"
            execute_write(
                "INSERT INTO expenses (description, category, amount, date, added_by) VALUES (?,?,?,?,?)",
                (tag, "Subscription", sub["amount"], bill_date, "System")
            )

auto_subscriptions()

# ─────────────────────────────────────────────
# AUDIT LOG HELPER
# ─────────────────────────────────────────────
def log_action(uname, action, details=""):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_write("INSERT INTO audit_log (username, action, details, timestamp) VALUES (?,?,?,?)",
                  (uname, action, details, ts))

# ─────────────────────────────────────────────
# BELL SOUND
# ─────────────────────────────────────────────
def play_ding():
    components.html("""<script>
    try {
        var ctx = new (window.AudioContext || window.webkitAudioContext)();
        var o = ctx.createOscillator(); var g = ctx.createGain();
        o.type = 'sine'; o.frequency.setValueAtTime(1100, ctx.currentTime);
        g.gain.setValueAtTime(0.18, ctx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.45);
        o.connect(g); g.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.45);
    } catch(e) {}
    </script>""", height=0, width=0)

# ─────────────────────────────────────────────
# HELPERS
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
# FINANCIALS
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
    
    # commissions always all-time for now unless you want to filter
    all_visits = fetch_all("SELECT d.name, d.comm_type, d.fixed_rate, v.net_paid FROM visits v JOIN doctors d ON v.doctor_id = d.id")
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
            if len(v) >= 20: commissions += sum(v) * 0.05
            elif len(v) >= 10: commissions += sum(v) * 0.03

    total_out = exp + commissions
    return gross, exp, commissions, total_out, gross - total_out, doc_visits

gross_income, base_expenses, total_commissions, total_outflows, net_profit, doc_visits = get_financials()

# Today's numbers
today_str = date.today().isoformat()
today_row = fetch_one("SELECT SUM(net_paid) as t, COUNT(*) as c FROM visits WHERE visit_date = ?", (today_str,))
today_revenue = today_row["t"] if today_row and today_row["t"] else 0.0
today_visits = today_row["c"] if today_row else 0

# Patient count
patient_count = fetch_one("SELECT COUNT(*) as c FROM patients")["c"]

# ─────────────────────────────────────────────
# LOGIN
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
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with reg_tab:
            ru = st.text_input("New username")
            rp = st.text_input("New password", type="password")
            role = st.selectbox("Role", ["Boss", "Accounting", "Reception", "Reception & Accounting"])
            code = st.text_input("Admin code", type="password")
            if st.button("Create Account", use_container_width=True):
                if code != "1011":
                    st.error("Invalid admin code.")
                elif ru and rp:
                    if execute_write("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", (ru.strip(), hash_password(rp), role)):
                        st.success("Account created. Sign in above.")
                    else:
                        st.error("Username already taken.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
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
    "Boss": ["📈  Dashboard", "🖥️  Reception", "📊  Accounting", "📅  Appointments", "👥  Accounts", "⚙️  Settings"],
    "Reception & Accounting": ["🖥️  Reception", "📊  Accounting", "📅  Appointments"],
    "Accounting": ["📊  Accounting"],
    "Reception": ["🖥️  Reception", "📅  Appointments"],
}
menus = menu_map.get(role, [])
selected = st.sidebar.radio("Navigation", menus, label_visibility="collapsed")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# GSheets sync button (only shown if configured)
if _gsheets_enabled:
    if st.sidebar.button("☁️ Sync to Google Sheets", use_container_width=True):
        try:
            db_tmp = get_db()
            for tbl in ["visits", "patients", "expenses", "doctors", "employees", "referrers", "subscriptions", "audit_log"]:
                try:
                    df_tbl = pd.read_sql(f"SELECT * FROM {tbl}", db_tmp)
                    sync_to_sheets(tbl, df_tbl)
                except Exception:
                    pass
            db_tmp.close()
            st.sidebar.success("Synced!")
        except Exception as e:
            st.sidebar.error(f"Sync failed: {e}")

if st.sidebar.button("Sign Out", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# ─────────────────────────────────────────────
# MODULE: DASHBOARD
# ─────────────────────────────────────────────
if selected == "📈  Dashboard":
    page_header("Executive Dashboard", f"Showing all-time clinic performance · Today is {date.today().strftime('%A, %B %d %Y')}")
    
    pulse_bar([
        ("Today's Revenue", f"${today_revenue:,.0f}"),
        ("Visits Today", str(today_visits)),
        ("Total Patients", str(patient_count)),
        ("All-Time Revenue", f"${gross_income:,.0f}"),
        ("Net Profit", f"${net_profit:,.0f}"),
    ])

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(card("Gross Revenue", f"${gross_income:,.2f}", "green", "All collected payments"), unsafe_allow_html=True)
    with col2: st.markdown(card("Total Expenses", f"${total_outflows:,.2f}", "red", "Bills + payroll + commissions"), unsafe_allow_html=True)
    with col3: st.markdown(card("Net Profit", f"${net_profit:,.2f}", "dark", "Revenue minus all costs"), unsafe_allow_html=True)
    with col4: st.markdown(card("Doctor Commissions", f"${total_commissions:,.2f}", "dark", "Total owed to doctors"), unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns([3, 2])

    with col_a:
        section_label("Revenue trend")
        visits_raw = fetch_all("SELECT visit_date as Date, net_paid as Revenue FROM visits ORDER BY visit_date ASC")
        if visits_raw:
            df = pd.DataFrame([dict(r) for r in visits_raw])
            df_grouped = df.groupby("Date", as_index=False).sum().set_index("Date")
            st.line_chart(df_grouped, y="Revenue", color="#0D3D2B", height=220)
        else:
            st.info("No visit data yet.")

    with col_b:
        section_label("Doctor performance")
        all_docs = fetch_all("SELECT name, comm_type, fixed_rate FROM doctors")
        rows = []
        for d in all_docs:
            info = doc_visits.get(d["name"], {"visits": [], "comm_type": d["comm_type"], "fixed_rate": d["fixed_rate"]})
            v = info["visits"]
            vol = len(v)
            gen = sum(v)
            if d["comm_type"] == "fixed":
                payout = gen * (d["fixed_rate"] / 100.0)
                model = f"Fixed {d['fixed_rate']}%"
            else:
                if vol >= 20: payout = gen * 0.05; model = "Tiered 5%"
                elif vol >= 10: payout = gen * 0.03; model = "Tiered 3%"
                else: payout = 0; model = "Tiered 0%"
            rows.append({"Doctor": d["name"], "Visits": vol, "Revenue": f"${gen:,.0f}", "Commission": f"${payout:,.0f}", "Model": model})
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No doctors added yet.")

    st.markdown("---")
    section_label("Monthly revenue summary")
    monthly_raw = fetch_all("SELECT substr(visit_date,1,7) as Month, SUM(net_paid) as Revenue, COUNT(*) as Visits FROM visits GROUP BY Month ORDER BY Month DESC")
    if monthly_raw:
        st.dataframe(pd.DataFrame([dict(r) for r in monthly_raw]), use_container_width=True, hide_index=True)
    else:
        st.info("No visit data yet.")

    st.markdown("---")
    section_label("Activity audit log — who added what")
    audit_filter = st.selectbox("Filter by action type", ["All", "New Visit", "Add Expense", "Delete Expense", "Add Referrer", "Remove Referrer", "Add Subscription", "Remove Subscription", "Toggle Subscription", "Referral Commission Paid"], key="audit_filter")
    if audit_filter == "All":
        audit_rows = fetch_all("SELECT timestamp as Time, username as User, action as Action, details as Details FROM audit_log ORDER BY id DESC LIMIT 200")
    else:
        audit_rows = fetch_all("SELECT timestamp as Time, username as User, action as Action, details as Details FROM audit_log WHERE action = ? ORDER BY id DESC LIMIT 200", (audit_filter,))
    if audit_rows:
        st.dataframe(pd.DataFrame([dict(r) for r in audit_rows]), use_container_width=True, hide_index=True)
    else:
        st.info("No activity recorded yet.")

# ─────────────────────────────────────────────
# MODULE: RECEPTION
# ─────────────────────────────────────────────
elif selected == "🖥️  Reception":
    page_header("Reception Desk", "Patient checkout, records, and visit history.")
    pulse_bar([("Today's Revenue", f"${today_revenue:,.0f}"), ("Visits Today", str(today_visits)), ("Total Patients", str(patient_count))])

    t1, t2, t3, t4, t5 = st.tabs(["Checkout", "Patient Records", "Add Patient", "Visit History", "Delete Visit"])

    # ── CHECKOUT ──
    with t1:
        section_label("New checkout")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        services_db = fetch_all("SELECT id, name, price FROM services WHERE active = 1 ORDER BY name")
        bundles_db = fetch_all("SELECT id, name, price FROM bundles ORDER BY name")

        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please add doctors and services in Settings before processing checkouts.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}

            col1, col2 = st.columns(2)
            with col1:
                target_p = st.selectbox("Patient", ["— select —"] + list(p_map.keys()))
                chosen_doc = st.selectbox("Doctor", list(d_map.keys()))
                payment_method = st.selectbox("Payment method", ["Cash", "Card", "Insurance", "Transfer"])
            with col2:
                item_type = st.radio("Item type", ["Service", "Bundle"], horizontal=True)
                srv_id = bnd_id = None
                base_price = 0.0
                chosen_item_name = ""

                if item_type == "Service":
                    if services_db:
                        s_map = {f"{s['name']}  —  ${s['price']:.2f}": (s["id"], s["price"], s["name"]) for s in services_db}
                        chosen = st.selectbox("Service", list(s_map.keys()))
                        srv_id, base_price, chosen_item_name = s_map[chosen]
                    else:
                        st.error("No services configured.")
                else:
                    if bundles_db:
                        b_map = {f"{b['name']}  —  ${b['price']:.2f}": (b["id"], b["price"], b["name"]) for b in bundles_db}
                        chosen = st.selectbox("Bundle", list(b_map.keys()))
                        bnd_id, base_price, chosen_item_name = b_map[chosen]
                    else:
                        st.error("No bundles configured.")

                disc_type = st.radio("Discount", ["None", "Fixed ($)", "Percent (%)"], horizontal=True)
                disc_val = st.number_input("Discount value", min_value=0.0, step=1.0)

            final_due = base_price
            if disc_type == "Fixed ($)": final_due = max(0.0, base_price - disc_val)
            elif disc_type == "Percent (%)": final_due = max(0.0, base_price * (1 - disc_val / 100))

            visit_notes = st.text_area("Visit notes (optional)", height=70)

            # ── How did you find us? ──
            referrers_db = fetch_all("SELECT name FROM referrers ORDER BY name")
            referral_options = ["Walk-in / Direct", "Instagram / Social Media", "Google Search", "Friend / Word of mouth"] + [r["name"] for r in referrers_db]
            how_found = st.selectbox("How did the patient find us?", referral_options)
            # If a referrer name was selected, store it; otherwise store the label
            referred_by_val = how_found if how_found in [r["name"] for r in referrers_db] else None

            st.markdown(f"### Total due: **${final_due:,.2f}**")

            if st.button("Save & Print Receipt", use_container_width=True):
                if target_p == "— select —":
                    st.error("Please select a patient.")
                elif base_price == 0.0:
                    st.error("Please select a service or bundle.")
                else:
                    disc_amt = base_price - final_due
                    execute_write("""
                        INSERT INTO visits (patient_id, doctor_id, service_id, bundle_id, visit_date, base_price, discount_amount, net_paid, payment_method, notes, referred_by, added_by)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (p_map[target_p], d_map[chosen_doc], srv_id, bnd_id, today_str, base_price, disc_amt, final_due, payment_method, visit_notes, referred_by_val, username))
                    log_action(username, "New Visit", f"Patient: {target_p} | Doctor: {chosen_doc} | Paid: ${final_due:.2f} | Via: {how_found}")
                    st.success("Visit saved.")
                    st.session_state.rcpt = {
                        "patient": target_p, "doctor": chosen_doc, "item": chosen_item_name,
                        "base": base_price, "disc": disc_amt, "net": final_due,
                        "method": payment_method, "date": today_str
                    }

            if "rcpt" in st.session_state:
                r = st.session_state.rcpt
                st.markdown(f"""
                <div class="receipt-wrap">
                    <h2>🌿 Garden Clinic</h2>
                    <p class="receipt-sub">Official Receipt · {r['date']}</p>
                    <hr class="dashed">
                    <div class="receipt-row"><span>Patient</span><span>{r['patient']}</span></div>
                    <div class="receipt-row"><span>Doctor</span><span>{r['doctor']}</span></div>
                    <div class="receipt-row"><span>Service</span><span>{r['item']}</span></div>
                    <div class="receipt-row"><span>Payment</span><span>{r['method']}</span></div>
                    <hr class="dashed">
                    <div class="receipt-row"><span>Base price</span><span>${r['base']:,.2f}</span></div>
                    <div class="receipt-row" style="color:#C0392B;"><span>Discount</span><span>-${r['disc']:,.2f}</span></div>
                    <div class="receipt-row receipt-total"><span>Total paid</span><span>${r['net']:,.2f}</span></div>
                    <p class="receipt-footer">Thank you for visiting Garden Clinic</p>
                </div>
                """, unsafe_allow_html=True)

    # ── PATIENT RECORDS ──
    with t2:
        section_label("All patients")
        search = st.text_input("Search by name or phone", placeholder="Type to filter...")
        all_p = fetch_all("SELECT * FROM patients ORDER BY name ASC")
        if search:
            all_p = [p for p in all_p if search.lower() in (p["name"] or "").lower() or search in (p["phone"] or "")]
        if all_p:
            st.dataframe(pd.DataFrame([dict(p) for p in all_p]), use_container_width=True, hide_index=True)
            st.markdown("---")
            section_label("Remove patient")
            del_target = st.selectbox("Select patient to remove", ["— select —"] + [p["name"] for p in all_p])
            if st.button("Remove Patient", type="primary"):
                if del_target != "— select —":
                    execute_write("DELETE FROM patients WHERE name = ?", (del_target,))
                    st.success(f"Removed {del_target}.")
                    st.rerun()
        else:
            st.info("No patients found.")

    # ── ADD PATIENT ──
    with t3:
        section_label("Register new patient")
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Full name *")
            p_phone = st.text_input("Phone number")
            p_dob = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1990-01-15")
        with col2:
            p_gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
            p_notes = st.text_area("Notes / medical background", height=100)
        if st.button("Register Patient"):
            if p_name.strip():
                if execute_write("INSERT INTO patients (name, phone, date_of_birth, gender, notes, created_at) VALUES (?,?,?,?,?,?)",
                                 (p_name.strip(), p_phone.strip(), p_dob.strip(), p_gender, p_notes.strip(), today_str)):
                    st.success(f"Patient '{p_name}' registered.")
                else:
                    st.error("A patient with that name already exists.")
            else:
                st.error("Name is required.")

    # ── VISIT HISTORY ──
    with t4:
        section_label("Patient visit history")
        patients_all = fetch_all("SELECT id, name FROM patients ORDER BY name")
        if patients_all:
            lookup_p = st.selectbox("Select patient", ["— select —"] + [p["name"] for p in patients_all])
            if lookup_p != "— select —":
                pid = next(p["id"] for p in patients_all if p["name"] == lookup_p)
                hist = fetch_all("""
                    SELECT v.id, v.visit_date as Date, d.name as Doctor,
                           COALESCE(s.name, '📦 ' || b.name) as Item,
                           v.base_price as Base, v.discount_amount as Discount,
                           v.net_paid as Paid, v.payment_method as Method, v.notes as Notes
                    FROM visits v
                    JOIN doctors d ON v.doctor_id = d.id
                    LEFT JOIN services s ON v.service_id = s.id
                    LEFT JOIN bundles b ON v.bundle_id = b.id
                    WHERE v.patient_id = ?
                    ORDER BY v.visit_date DESC
                """, (pid,))
                if hist:
                    total_spent = sum(r["Paid"] for r in hist)
                    col1, col2 = st.columns(2)
                    col1.metric("Total visits", len(hist))
                    col2.metric("Total spent", f"${total_spent:,.2f}")
                    st.dataframe(pd.DataFrame([dict(r) for r in hist]), use_container_width=True, hide_index=True)
                else:
                    st.info(f"No visits recorded for {lookup_p}.")
        else:
            st.info("No patients registered yet.")

    # ── DELETE VISIT ──
    with t5:
        section_label("Delete a visit record")
        st.warning("⚠️ Use this to correct data entry errors only. Deleted visits cannot be recovered.")
        all_visits = fetch_all("""
            SELECT v.id, v.visit_date as Date, p.name as Patient, d.name as Doctor,
                   COALESCE(s.name, '📦 ' || b.name) as Item, v.net_paid as Paid
            FROM visits v
            JOIN patients p ON v.patient_id = p.id
            JOIN doctors d ON v.doctor_id = d.id
            LEFT JOIN services s ON v.service_id = s.id
            LEFT JOIN bundles b ON v.bundle_id = b.id
            ORDER BY v.id DESC LIMIT 100
        """)
        if all_visits:
            st.dataframe(pd.DataFrame([dict(r) for r in all_visits]), use_container_width=True, hide_index=True)
            st.markdown("---")
            void_id = st.number_input("Visit ID to delete", min_value=1, step=1)
            if st.button("Delete Visit", type="primary"):
                execute_write("DELETE FROM visits WHERE id = ?", (void_id,))
                st.success(f"Visit #{void_id} deleted.")
                st.rerun()
        else:
            st.info("No visits recorded yet.")

# ─────────────────────────────────────────────
# MODULE: APPOINTMENTS
# ─────────────────────────────────────────────
elif selected == "📅  Appointments":
    page_header("Appointments", "Schedule and manage upcoming patient appointments.")
    
    ta1, ta2 = st.tabs(["Schedule", "View All"])

    with ta1:
        section_label("Book new appointment")
        patients_db = fetch_all("SELECT id, name FROM patients ORDER BY name")
        docs_db = fetch_all("SELECT id, name FROM doctors ORDER BY name")
        if not patients_db or not docs_db:
            st.warning("You need at least one patient and one doctor to book appointments.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            col1, col2 = st.columns(2)
            with col1:
                ap_patient = st.selectbox("Patient", list(p_map.keys()))
                ap_doctor = st.selectbox("Doctor", list(d_map.keys()))
            with col2:
                ap_date = st.date_input("Appointment date", value=date.today())
                ap_time = st.time_input("Time")
                ap_reason = st.text_input("Reason / notes")
            if st.button("Book Appointment"):
                execute_write("INSERT INTO appointments (patient_id, doctor_id, appt_date, appt_time, reason, status) VALUES (?,?,?,?,?,?)",
                              (p_map[ap_patient], d_map[ap_doctor], str(ap_date), str(ap_time), ap_reason, "Scheduled"))
                st.success(f"Appointment booked for {ap_patient} on {ap_date} at {ap_time}.")

    with ta2:
        section_label("Upcoming & recent appointments")
        all_appts = fetch_all("""
            SELECT a.id, a.appt_date as Date, a.appt_time as Time,
                   p.name as Patient, d.name as Doctor, a.reason as Reason, a.status as Status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            ORDER BY a.appt_date DESC, a.appt_time DESC
        """)
        if all_appts:
            df_appts = pd.DataFrame([dict(r) for r in all_appts])
            st.dataframe(df_appts, use_container_width=True, hide_index=True)
            st.markdown("---")
            section_label("Update appointment status")
            col1, col2 = st.columns(2)
            with col1:
                upd_id = st.number_input("Appointment ID", min_value=1, step=1)
            with col2:
                new_status = st.selectbox("New status", ["Scheduled", "Completed", "Cancelled", "No-show"])
            if st.button("Update Status"):
                execute_write("UPDATE appointments SET status = ? WHERE id = ?", (new_status, upd_id))
                st.success(f"Appointment #{upd_id} updated to '{new_status}'.")
                st.rerun()
        else:
            st.info("No appointments booked yet.")

# ─────────────────────────────────────────────
# MODULE: ACCOUNTING
# ─────────────────────────────────────────────
elif selected == "📊  Accounting":
    page_header("Accounting", "Revenue, expenses, and financial health.")
    pulse_bar([
        ("Gross Revenue", f"${gross_income:,.0f}"),
        ("Total Expenses", f"${total_outflows:,.0f}"),
        ("Net Profit", f"${net_profit:,.0f}"),
        ("Doctor Commissions", f"${total_commissions:,.0f}"),
    ])

    col1, col2, col3 = st.columns(3)
    with col1: st.markdown(card("Gross Revenue", f"${gross_income:,.2f}", "green"), unsafe_allow_html=True)
    with col2: st.markdown(card("Total Outflows", f"${total_outflows:,.2f}", "red"), unsafe_allow_html=True)
    with col3: st.markdown(card("Net Profit", f"${net_profit:,.2f}", "dark"), unsafe_allow_html=True)

    st.markdown("---")
    ac1, ac2 = st.columns(2)
    with ac1:
        section_label("Expenses breakdown")
        if total_outflows > 0:
            df_exp = pd.DataFrame({
                "Category": ["Operating Expenses", "Payroll", "Doctor Commissions"],
                "Amount": [base_expenses, 0, total_commissions]
            }).set_index("Category")
            # separate payroll from expenses for chart
            payroll_row = fetch_one("SELECT SUM(amount) as t FROM expenses WHERE category = 'Payroll'")
            payroll_in_exp = payroll_row["t"] if payroll_row and payroll_row["t"] else 0.0
            other_exp = base_expenses - payroll_in_exp
            df_exp2 = pd.DataFrame({
                "Category": ["Other Expenses", "Payroll", "Doctor Commissions"],
                "Amount ($)": [other_exp, payroll_in_exp, total_commissions]
            }).set_index("Category")
            st.bar_chart(df_exp2, y="Amount ($)", color="#C0392B", height=220)
        else:
            st.info("No expense data yet.")

    with ac2:
        section_label("Daily revenue trend")
        visits_raw = fetch_all("SELECT visit_date as Date, net_paid as Revenue FROM visits ORDER BY visit_date ASC")
        if visits_raw:
            df = pd.DataFrame([dict(r) for r in visits_raw])
            df_g = df.groupby("Date").sum().reset_index().set_index("Date")
            st.line_chart(df_g, y="Revenue", color="#0D3D2B", height=220)
        else:
            st.info("No revenue data yet.")

    st.markdown("---")
    ae1, ae2 = st.columns([3, 2])
    with ae1:
        section_label("Expense log")
        filter_cat = st.selectbox("Filter by category", ["All", "General", "Payroll", "Supplies", "Utilities", "Rent", "Equipment", "Marketing", "Subscription", "Other"], key="acc_filter_cat")
        if filter_cat == "All":
            exp_list = fetch_all("SELECT id, date as Date, category as Category, description as Description, amount as Amount FROM expenses ORDER BY id DESC")
        else:
            exp_list = fetch_all("SELECT id, date as Date, category as Category, description as Description, amount as Amount FROM expenses WHERE category = ? ORDER BY id DESC", (filter_cat,))
        if exp_list:
            st.dataframe(pd.DataFrame([dict(r) for r in exp_list]), use_container_width=True, hide_index=True)
        else:
            st.info("No expenses recorded.")

    with ae2:
        section_label("Add expense")
        with st.form("expense_form"):
            e_desc = st.text_input("Description")
            e_cat = st.selectbox("Category", ["General", "Supplies", "Utilities", "Rent", "Equipment", "Marketing", "Other"])
            e_amt = st.number_input("Amount ($)", min_value=0.0, step=10.0)
            e_date = st.date_input("Date", value=date.today())
            if st.form_submit_button("Add Expense"):
                if e_desc and e_amt > 0:
                    execute_write("INSERT INTO expenses (description, category, amount, date, added_by) VALUES (?,?,?,?,?)", (e_desc, e_cat, e_amt, str(e_date), username))
                    log_action(username, "Add Expense", f"{e_desc} | ${e_amt:.2f} | {e_cat}")
                    st.success("Expense added.")
                    st.rerun()
                else:
                    st.error("Description and amount are required.")

    st.markdown("---")
    section_label("Delete expense")
    st.warning("⚠️ Use this to remove an expense added by mistake. This cannot be undone.")
    if role in ["Boss", "Accounting", "Reception & Accounting"]:
        del_exp_list = fetch_all("SELECT id, date, description, amount FROM expenses ORDER BY id DESC LIMIT 100")
        if del_exp_list:
            del_exp_options = {f"#{r['id']} · {r['date']} · {r['description']} · ${r['amount']:.2f}": r["id"] for r in del_exp_list}
            chosen_del_exp = st.selectbox("Select expense to delete", ["— select —"] + list(del_exp_options.keys()), key="del_exp_select")
            if st.button("Delete Expense", type="primary", key="btn_del_expense"):
                if chosen_del_exp != "— select —":
                    exp_id = del_exp_options[chosen_del_exp]
                    execute_write("DELETE FROM expenses WHERE id = ?", (exp_id,))
                    log_action(username, "Delete Expense", f"Deleted expense ID #{exp_id}: {chosen_del_exp}")
                    st.success("Expense deleted.")
                    st.rerun()
        else:
            st.info("No expenses to delete.")

    st.markdown("---")
    # ── REFERRAL COMMISSIONS ──
    section_label("Referral commissions owed this month")
    current_month = datetime.now().strftime("%Y-%m")
    all_referrers = fetch_all("SELECT * FROM referrers ORDER BY name")
    if all_referrers:
        ref_rows = []
        for ref in all_referrers:
            visits_via = fetch_all(
                "SELECT COUNT(*) as c, SUM(net_paid) as total FROM visits WHERE referred_by = ? AND substr(visit_date,1,7) = ?",
                (ref["name"], current_month)
            )
            count = visits_via[0]["c"] if visits_via else 0
            total_rev = visits_via[0]["total"] if visits_via and visits_via[0]["total"] else 0.0
            commission_due = total_rev * (ref["commission_rate"] / 100.0)
            ref_rows.append({
                "Referrer": ref["name"],
                "Rate": f"{ref['commission_rate']}%",
                "Visits This Month": count,
                "Revenue Generated": f"${total_rev:,.2f}",
                "Commission Due": f"${commission_due:,.2f}",
            })
        st.dataframe(pd.DataFrame(ref_rows), use_container_width=True, hide_index=True)
        total_ref_comm = sum(
            (fetch_one("SELECT SUM(net_paid) as t FROM visits WHERE referred_by = ? AND substr(visit_date,1,7) = ?", (r["name"], current_month))["t"] or 0.0) * (r["commission_rate"] / 100.0)
            for r in all_referrers
        )
        st.markdown(f"**Total referral commissions owed this month: ${total_ref_comm:,.2f}**")
        if st.button("Mark All Referral Commissions as Paid (add as expense)"):
            if total_ref_comm > 0:
                tag = f"Referral Commissions — {current_month}"
                if not fetch_all("SELECT id FROM expenses WHERE description = ?", (tag,)):
                    execute_write("INSERT INTO expenses (description, category, amount, date, added_by) VALUES (?,?,?,?,?)",
                                  (tag, "Marketing", total_ref_comm, f"{current_month}-01", username))
                    log_action(username, "Referral Commission Paid", f"${total_ref_comm:.2f} for {current_month}")
                    st.success(f"Referral commissions of ${total_ref_comm:,.2f} recorded as expense.")
                    st.rerun()
                else:
                    st.warning("Referral commissions for this month have already been recorded.")
            else:
                st.info("No referral commissions to record this month.")
    else:
        st.info("No referrers added yet. Add them in Settings → Referrers.")

# ─────────────────────────────────────────────
# MODULE: ACCOUNTS (BOSS ONLY)
# ─────────────────────────────────────────────
elif selected == "👥  Accounts":
    page_header("Accounts", "Manage user access and review full activity logs.")
    accounts_registered = fetch_all("SELECT id, username, role FROM users")
    st.metric("Total user accounts", len(accounts_registered))

    acc_tab1, acc_tab2 = st.tabs(["Profiles & Access", "Activity Log"])

    with acc_tab1:
        section_label("All accounts")
        if accounts_registered:
            st.dataframe(pd.DataFrame([dict(u) for u in accounts_registered]), use_container_width=True, hide_index=True)
            st.markdown("---")
            section_label("Remove account")
            st.warning("⚠️ Removing an account immediately revokes access. Audit history is preserved.")
            killable = ["— select —"] + [u["username"] for u in accounts_registered if u["username"] != username]
            target_del = st.selectbox("Select account to remove", killable, key="burn_user_select")
            if st.button("Delete Account", type="primary", key="btn_del_account"):
                if target_del != "— select —":
                    execute_write("DELETE FROM users WHERE username = ?", (target_del,))
                    log_action(username, "Delete Account", f"Removed: {target_del}")
                    play_ding()
                    st.success(f"Account '{target_del}' removed.")
                    st.rerun()
        else:
            st.info("No accounts found.")

    with acc_tab2:
        section_label("Audit log by user")
        profile_filter = ["All"] + [u["username"] for u in accounts_registered]
        chosen_user = st.selectbox("Filter by user", profile_filter, key="acc_audit_user_filter")
        if chosen_user == "All":
            audit_records = fetch_all("SELECT timestamp as Time, username as User, action as Action, details as Details FROM audit_log ORDER BY id DESC LIMIT 400")
        else:
            audit_records = fetch_all("SELECT timestamp as Time, username as User, action as Action, details as Details FROM audit_log WHERE username = ? ORDER BY id DESC LIMIT 400", (chosen_user,))
        if audit_records:
            st.dataframe(pd.DataFrame([dict(r) for r in audit_records]), use_container_width=True, hide_index=True)
        else:
            st.info("No activity recorded yet.")

# ─────────────────────────────────────────────
# MODULE: SETTINGS
# ─────────────────────────────────────────────
elif selected == "⚙️  Settings":
    page_header("Settings", "Configure doctors, staff, services, and bundles.")

    s1, s2, s3, s4, s5, s6 = st.tabs(["Doctors", "Staff & Payroll", "Services", "Bundles", "🎯 Referrers", "🔄 Subscriptions"])

    # ── DOCTORS ──
    with s1:
        section_label("Add doctor")
        col1, col2 = st.columns(2)
        with col1:
            d_name = st.text_input("Doctor name")
            d_spec = st.text_input("Specialty (e.g. Dermatology)")
        with col2:
            c_mode = st.selectbox("Commission model", ["Tiered (3% at 10+ visits, 5% at 20+)", "Fixed percentage"])
            f_rate = 0.0
            comm_type = "tiered"
            if c_mode == "Fixed percentage":
                comm_type = "fixed"
                f_rate = st.number_input("Fixed rate (%)", min_value=0.0, max_value=100.0, value=50.0)
        if st.button("Add Doctor"):
            if d_name.strip():
                if execute_write("INSERT INTO doctors (name, specialty, comm_type, fixed_rate) VALUES (?,?,?,?)", (d_name.strip(), d_spec.strip(), comm_type, f_rate)):
                    st.success(f"Doctor '{d_name}' added.")
                    st.rerun()
                else:
                    st.error("A doctor with that name already exists.")
            else:
                st.error("Doctor name is required.")

        st.markdown("---")
        section_label("Current doctors")
        all_docs = fetch_all("SELECT * FROM doctors ORDER BY name")
        if all_docs:
            st.dataframe(pd.DataFrame([dict(d) for d in all_docs]), use_container_width=True, hide_index=True)
            del_doc = st.selectbox("Remove doctor", ["— select —"] + [d["name"] for d in all_docs])
            if st.button("Remove Doctor", type="primary"):
                if del_doc != "— select —":
                    execute_write("DELETE FROM doctors WHERE name = ?", (del_doc,))
                    st.success(f"Doctor '{del_doc}' removed.")
                    st.rerun()
        else:
            st.info("No doctors added yet.")

    # ── STAFF ──
    with s2:
        section_label("Add staff member")
        col1, col2, col3 = st.columns(3)
        with col1: emp_name = st.text_input("Full name")
        with col2: emp_role = st.text_input("Role / title")
        with col3: emp_salary = st.number_input("Monthly salary ($)", min_value=0.0, step=100.0)
        st.info("💡 Staff salaries are automatically recorded as an expense on the 1st of each month.")
        if st.button("Add Staff Member"):
            if emp_name.strip() and emp_role.strip():
                if execute_write("INSERT INTO employees (name, role, salary) VALUES (?,?,?)", (emp_name.strip(), emp_role.strip(), emp_salary)):
                    st.success(f"{emp_name} added to payroll.")
                    st.rerun()
                else:
                    st.error("An employee with that name already exists.")
            else:
                st.error("Name and role are required.")

        st.markdown("---")
        section_label("Current staff")
        all_emp = fetch_all("SELECT * FROM employees ORDER BY name")
        if all_emp:
            df_emp = pd.DataFrame([dict(e) for e in all_emp])
            st.dataframe(df_emp, use_container_width=True, hide_index=True)
            total_payroll = sum(e["salary"] for e in all_emp)
            st.markdown(f"**Monthly payroll total: ${total_payroll:,.2f}**")
            del_emp = st.selectbox("Remove employee", ["— select —"] + [e["name"] for e in all_emp])
            if st.button("Remove Employee", type="primary"):
                if del_emp != "— select —":
                    execute_write("DELETE FROM employees WHERE name = ?", (del_emp,))
                    st.success(f"Removed {del_emp} from payroll.")
                    st.rerun()
        else:
            st.info("No staff added yet.")

    # ── SERVICES ──
    with s3:
        section_label("Add service")
        col1, col2, col3 = st.columns(3)
        with col1: s_name = st.text_input("Service name")
        with col2: s_cat = st.selectbox("Category", ["General", "Consultation", "Procedure", "Therapy", "Diagnostic", "Other"])
        with col3: s_price = st.number_input("Price ($)", min_value=0.0, step=10.0)
        if st.button("Add Service"):
            if s_name.strip():
                if execute_write("INSERT INTO services (name, category, price, active) VALUES (?,?,?,1)", (s_name.strip(), s_cat, s_price)):
                    st.success(f"Service '{s_name}' added at ${s_price:.2f}.")
                    st.rerun()
                else:
                    st.error("A service with that name already exists.")
            else:
                st.error("Service name is required.")

        st.markdown("---")
        section_label("Current services")
        all_svc = fetch_all("SELECT * FROM services ORDER BY category, name")
        if all_svc:
            st.dataframe(pd.DataFrame([dict(s) for s in all_svc]), use_container_width=True, hide_index=True)
            del_svc = st.selectbox("Remove service", ["— select —"] + [s["name"] for s in all_svc])
            if st.button("Remove Service", type="primary"):
                if del_svc != "— select —":
                    execute_write("DELETE FROM services WHERE name = ?", (del_svc,))
                    st.success(f"Service '{del_svc}' removed.")
                    st.rerun()
        else:
            st.info("No services added yet.")

    # ── BUNDLES ──
    with s4:
        section_label("Create bundle")
        col1, col2 = st.columns(2)
        with col1:
            b_name = st.text_input("Bundle name (e.g. Premium Care Package)")
            b_price = st.number_input("Bundle price ($)", min_value=0.0, step=25.0)
        with col2:
            b_desc = st.text_area("Description / included services", height=90)
        if st.button("Create Bundle"):
            if b_name.strip() and b_price > 0:
                if execute_write("INSERT INTO bundles (name, price, description) VALUES (?,?,?)", (b_name.strip(), b_price, b_desc.strip())):
                    st.success(f"Bundle '{b_name}' created at ${b_price:.2f}.")
                    st.rerun()
                else:
                    st.error("A bundle with that name already exists.")
            else:
                st.error("Name and price are required.")

        st.markdown("---")
        section_label("Current bundles")
        all_bundles = fetch_all("SELECT * FROM bundles ORDER BY name")
        if all_bundles:
            st.dataframe(pd.DataFrame([dict(b) for b in all_bundles]), use_container_width=True, hide_index=True)
            del_bnd = st.selectbox("Remove bundle", ["— select —"] + [b["name"] for b in all_bundles])
            if st.button("Remove Bundle", type="primary"):
                if del_bnd != "— select —":
                    execute_write("DELETE FROM bundles WHERE name = ?", (del_bnd,))
                    st.success(f"Bundle '{del_bnd}' removed.")
                    st.rerun()
        else:
            st.info("No bundles created yet.")

    # ── REFERRERS ──
    with s5:
        section_label("Add referrer / influencer")
        st.info("💡 Add anyone who promotes the clinic — influencers, video creators, partners. When a patient comes via them, select their name at checkout. Commission is calculated monthly in Accounting.")
        col1, col2 = st.columns(2)
        with col1:
            ref_name = st.text_input("Referrer full name", key="ref_name_input")
            ref_phone = st.text_input("Phone / contact", key="ref_phone_input")
        with col2:
            ref_rate = st.number_input("Commission rate (%)", min_value=0.0, max_value=100.0, step=1.0, value=10.0, key="ref_rate_input")
            ref_notes = st.text_area("Notes (platform, content type, etc.)", height=80, key="ref_notes_input")
        if st.button("Add Referrer", key="btn_add_referrer"):
            if ref_name.strip():
                if execute_write("INSERT INTO referrers (name, phone, commission_rate, notes, added_by, created_at) VALUES (?,?,?,?,?,?)",
                                 (ref_name.strip(), ref_phone.strip(), ref_rate, ref_notes.strip(), username, today_str)):
                    log_action(username, "Add Referrer", f"{ref_name} at {ref_rate}%")
                    st.success(f"Referrer '{ref_name}' added with {ref_rate}% commission.")
                    st.rerun()
                else:
                    st.error("A referrer with that name already exists.")
            else:
                st.error("Name is required.")

        st.markdown("---")
        section_label("Current referrers")
        all_refs = fetch_all("SELECT * FROM referrers ORDER BY name")
        if all_refs:
            st.dataframe(pd.DataFrame([dict(r) for r in all_refs]), use_container_width=True, hide_index=True)
            del_ref = st.selectbox("Remove referrer", ["— select —"] + [r["name"] for r in all_refs], key="del_ref_select")
            if st.button("Remove Referrer", type="primary", key="btn_del_referrer"):
                if del_ref != "— select —":
                    execute_write("DELETE FROM referrers WHERE name = ?", (del_ref,))
                    log_action(username, "Remove Referrer", del_ref)
                    st.success(f"Referrer '{del_ref}' removed.")
                    st.rerun()
        else:
            st.info("No referrers added yet.")

    # ── SUBSCRIPTIONS ──
    with s6:
        section_label("Add monthly subscription")
        st.info("💡 Add recurring monthly costs (software licenses, platform fees, etc.). They are automatically recorded as an expense each month.")
        col1, col2, col3 = st.columns(3)
        with col1:
            sub_name = st.text_input("Subscription name (e.g. Instagram Ads, Clinic Software)", key="sub_name_input")
            sub_cat = st.selectbox("Category", ["Subscription", "Marketing", "Software", "Utilities", "Other"], key="sub_cat_select")
        with col2:
            sub_amount = st.number_input("Monthly amount ($)", min_value=0.0, step=5.0, key="sub_amount_input")
            sub_day = st.number_input("Billing day of month", min_value=1, max_value=28, step=1, value=1, key="sub_day_input")
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Subscriptions auto-post as expenses on the billing day each month.")
        if st.button("Add Subscription", key="btn_add_subscription"):
            if sub_name.strip() and sub_amount > 0:
                if execute_write("INSERT INTO subscriptions (name, amount, billing_day, category, active, added_by, created_at) VALUES (?,?,?,?,1,?,?)",
                                 (sub_name.strip(), sub_amount, int(sub_day), sub_cat, username, today_str)):
                    log_action(username, "Add Subscription", f"{sub_name} ${sub_amount}/mo")
                    st.success(f"Subscription '{sub_name}' added at ${sub_amount:.2f}/month.")
                    st.rerun()
                else:
                    st.error("A subscription with that name already exists.")
            else:
                st.error("Name and amount are required.")

        st.markdown("---")
        section_label("Active subscriptions")
        all_subs = fetch_all("SELECT * FROM subscriptions ORDER BY name")
        if all_subs:
            st.dataframe(pd.DataFrame([dict(s) for s in all_subs]), use_container_width=True, hide_index=True)
            total_monthly = sum(s["amount"] for s in all_subs if s["active"])
            st.markdown(f"**Total active monthly subscriptions: ${total_monthly:,.2f}/month**")
            col1, col2 = st.columns(2)
            with col1:
                toggle_sub = st.selectbox("Pause / activate subscription", ["— select —"] + [s["name"] for s in all_subs], key="toggle_sub_select")
                if st.button("Toggle Active/Paused", key="btn_toggle_sub"):
                    if toggle_sub != "— select —":
                        current_active = next((s["active"] for s in all_subs if s["name"] == toggle_sub), 1)
                        execute_write("UPDATE subscriptions SET active = ? WHERE name = ?", (0 if current_active else 1, toggle_sub))
                        log_action(username, "Toggle Subscription", f"{toggle_sub} → {'Paused' if current_active else 'Active'}")
                        st.success(f"'{toggle_sub}' is now {'paused' if current_active else 'active'}.")
                        st.rerun()
            with col2:
                del_sub = st.selectbox("Remove subscription", ["— select —"] + [s["name"] for s in all_subs], key="del_sub_select")
                if st.button("Remove Subscription", type="primary", key="btn_del_subscription"):
                    if del_sub != "— select —":
                        execute_write("DELETE FROM subscriptions WHERE name = ?", (del_sub,))
                        log_action(username, "Remove Subscription", del_sub)
                        st.success(f"Subscription '{del_sub}' removed.")
                        st.rerun()
        else:
            st.info("No subscriptions added yet.")
