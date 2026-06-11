import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import hashlib
from datetime import datetime, date
import streamlit.components.v1 as components
import json

# ─────────────────────────────────────────────
# GOOGLE SHEETS CLOUD CONNECTION
# ─────────────────────────────────────────────
import streamlit as st
# Change your import to the native Streamlit connections module:
from streamlit.connections import GSheetsConnection

# Establish the connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Read the data (adjust the spreadsheet name/URL as needed for your code)
df = conn.read()
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
# DATABASE (ULTRA-RESILIENT SELF-HEALING CLOUD)
# ─────────────────────────────────────────────
import sqlite3
import re
import hashlib
import numpy as np
import pandas as pd
DB_FILE = "garden_clinic_v7.db"

class SafeRow:
    """Prevents Subscriptable/NoneType crashes by returning 0 or empty strings on empty queries"""
    def __init__(self, data=None):
        self.data = data if data else {}
    def __getitem__(self, key):
        return self.data.get(key, 0)
    def get(self, key, default=None):
        return self.data.get(key, default)
    def __bool__(self):
        return bool(self.data)

def auto_patch_error(e, q):
    """Automatically fixes missing columns AND missing tables on the fly!"""
    err_msg = str(e).lower()
    
    # 1. Auto-Heal Missing Tables
    if "no such table" in err_msg:
        tbl_match = re.search(r"no such table:\s*(\w+)", err_msg)
        if tbl_match:
            tbl_name = tbl_match.group(1)
            insert_match = re.search(r"insert\s+into\s+" + tbl_name + r"\s*\(([^)]+)\)", q, re.IGNORECASE)
            if insert_match:
                cols = [c.strip() for c in insert_match.group(1).split(",")]
                col_defs = ", ".join([f"{c} TEXT" for c in cols])
                create_q = f"CREATE TABLE IF NOT EXISTS {tbl_name} ({col_defs});"
            else:
                create_q = f"CREATE TABLE IF NOT EXISTS {tbl_name} (id TEXT PRIMARY KEY, name TEXT, role TEXT, salary TEXT, title TEXT, date TEXT);"
            
            try:
                conn = sqlite3.connect(DB_FILE, check_same_thread=False)
                conn.execute(create_q)
                conn.commit()
                conn.close()
                return True
            except:
                pass

    # 2. Auto-Heal Missing Columns
    col_name = None
    tbl_name = None
    if "no such column" in err_msg:
        col_match = re.search(r"no such column:\s*(\w+)", err_msg)
        if col_match:
            col_name = col_match.group(1)
            tbl_match = re.search(r"(?:from|join|insert\s+into|update)\s+(\w+)", q, re.IGNORECASE)
            if tbl_match:
                tbl_name = tbl_match.group(1)
                
    elif "has no column named" in err_msg:
        match = re.search(r"table\s+(\w+)\s+has\s+no\s+column\s+named\s+(\w+)", err_msg)
        if match:
            tbl_name = match.group(1)
            col_name = match.group(2)
    
    if col_name and tbl_name:
        try:
            conn = sqlite3.connect(DB_FILE, check_same_thread=False)
            conn.execute(f"ALTER TABLE {tbl_name} ADD COLUMN {col_name} TEXT;")
            conn.commit()
            conn.close()
            return True
        except:
            pass
    return False

if 'db_initialized' not in st.session_state:
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        # Create core application tables comprehensively
        conn.execute("CREATE TABLE IF NOT EXISTS users (id TEXT, username TEXT, password TEXT, password_hash TEXT, role TEXT, name TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS patients (id TEXT, name TEXT, phone TEXT, age TEXT, gender TEXT, address TEXT, history TEXT, date TEXT, dob TEXT, notes TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS expenses (id TEXT, description TEXT, amount TEXT, date TEXT, category TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS appointments (id TEXT, patient_id TEXT, date TEXT, time TEXT, status TEXT, notes TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS staff (id TEXT, name TEXT, role TEXT, salary TEXT, title TEXT, date TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS employees (id TEXT, name TEXT, role TEXT, salary TEXT, title TEXT, date TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS doctors (id TEXT, name TEXT, comm_type TEXT, fixed_rate TEXT, commission_rate TEXT);")
        conn.execute("CREATE TABLE IF NOT EXISTS visits (id TEXT, doctor_id TEXT, patient_id TEXT, net_paid TEXT, date TEXT, notes TEXT);")
        conn.commit()
        
        try:
            conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT;")
            conn.commit()
        except:
            pass
            
        if 'sh' in globals() and sh is not None:
            for ws in sh.worksheets():
                if ws.title == "Sheet1" and len(sh.worksheets()) > 1:
                    continue
                try:
                    records = ws.get_all_records()
                    if records:
                        df = pd.DataFrame(records)
                        df.to_sql(ws.title, conn, if_exists='replace', index=False)
                except:
                    pass
        conn.close()
    except Exception as e:
        st.error(f"🔴 Local DB Init Error: {e}")
    st.session_state.db_initialized = True

def hash_password(pw): 
    return hashlib.sha256(pw.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def sync_local_to_sheets():
    """Pushes any updates from the local database file straight to Google Sheets while removing bad floats"""
    if 'sh' not in globals() or sh is None:
        return
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            if table.startswith('sqlite_'):
                continue
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            
            # Deep clean NaN / Float compliance errors
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.fillna("")
            
            try:
                ws = sh.worksheet(table)
            except gspread.WorksheetNotFound:
                ws = sh.add_worksheet(title=table, rows="1000", cols="26")
            
            ws.clear()
            headers = [str(col) for col in df.columns]
            clean_rows = [[str(val) if val is not None else "" for val in row] for row in df.values.tolist()]
            upload_data = [headers] + clean_rows
            
            try:
                ws.update(range_name="A1", values=upload_data)
            except:
                ws.update(upload_data)
            
        try:
            default_ws = sh.worksheet("Sheet1")
            if len(sh.worksheets()) > 1:
                sh.del_worksheet(default_ws)
        except:
            pass
        conn.close()
        st.toast("✅ Successfully synced data to Google Sheets!", icon="☁️")
    except Exception as e:
        pass # Silently drop background errors to avoid disrupting runtime

def fetch_all(q, p=()):
    try:
        with sqlite3.connect("clinic.db") as conn:
            db = conn.cursor()
            res = db.execute(q, p).fetchall()
            return res
    except sqlite3.OperationalError as e:
        # If a table doesn't exist yet, return an empty list gracefully instead of crashing
        if "no such table" in str(e).lower():
            return []
        raise e
def fetch_one(q, p=()):
    try:
        with sqlite3.connect("clinic.db") as conn:
            db = conn.cursor()
            res = db.execute(q, p).fetchone()
            return res
    except sqlite3.OperationalError as e:
        if "no such table" in str(e).lower():
            return None
        raise e

def get_financials():
    # Safe default values in case tables are missing on day one
    gross_income = 0.0
    base_expenses = 0.0
    total_commissions = 0.0
    net_profit = 0.0
    doc_visits = {}

    all_visits = fetch_all("SELECT d.name, d.comm_type, d.fixed_rate, v.net_paid FROM visits v JOIN doctors d ON v.doctor_id = d.id")
    
    # Process calculations only if we have records
    for name, comm_type, fixed_rate, net_paid in all_visits:
        gross_income += net_paid
        doc_visits[name] = doc_visits.get(name, 0) + 1
        if comm_type == "Fixed":
            total_commissions += fixed_rate
        else:
            total_commissions += (net_paid * 0.30) # 30% default split
            
    net_profit = gross_income - base_expenses - total_commissions
    return gross_income, base_expenses, total_commissions, gross_income - total_commissions, net_profit, doc_visits
   
# ─────────────────────────────────────────────
# BELL SOUND HELPER
# ─────────────────────────────────────────────
def play_ding():
    components.html("""
    <script>
    try {
        var context = new (window.AudioContext || window.webkitAudioContext)();
        var osc = context.createOscillator();
        var gain = context.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1100, context.currentTime);
        gain.gain.setValueAtTime(0.2, context.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.5);
        osc.connect(gain);
        gain.connect(context.destination);
        osc.start();
        osc.stop(context.currentTime + 0.5);
    } catch(e) { console.log(e); }
    </script>
    """, height=0, width=0)

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

# Access the first element of the returned tuple (index 0)
patient_count_row = fetch_one("SELECT COUNT(*) FROM patients")
patient_count = patient_count_row[0] if patient_count_row else 0
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
                        log_action("System", "Create Account", f"User: {ru.strip()} | Role: {role}")
                        st.success("Account created. Sign in above.")
                        play_ding()
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
    audit_filter = st.selectbox("Filter by action type", ["All", "New Visit", "New Patient", "Remove Patient", "Add Expense", "Delete Expense", "Add Referrer", "Remove Referrer", "Add Subscription", "Remove Subscription", "Toggle Subscription", "Referral Commission Paid"], key="audit_filter")
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
                    play_ding()
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
                    log_action(username, "Remove Patient", f"Patient Name: {del_target}")
                    st.success(f"Removed {del_target}.")
                    play_ding()
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
                    log_action(username, "New Patient", f"Added patient: {p_name.strip()} | Gender: {p_gender}")
                    st.success(f"Patient '{p_name}' registered.")
                    play_ding()
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
                log_action(username, "Delete Visit", f"Voided visit reference ID: #{void_id}")
                st.success(f"Visit #{void_id} deleted.")
                play_ding()
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
                log_action(username, "Book Appointment", f"Scheduled appointment for {ap_patient} with Doc ID: {d_map[ap_doctor]} on {ap_date}")
                st.success(f"Appointment booked for {ap_patient} on {ap_date} at {ap_time}.")
                play_ding()

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
                log_action(username, "Update Appointment", f"Changed Appt ID #{upd_id} layout to {new_status}")
                st.success(f"Appointment #{upd_id} updated to '{new_status}'.")
                play_ding()
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
                    play_ding()
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
                    play_ding()
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
                    play_ding()
                    st.rerun()
                else:
                    st.warning("Referral commissions for this month have already been recorded.")
            else:
                st.info("No referral commissions to record this month.")
    else:
        st.info("No referrers added yet. Add them in Settings → Referrers.")

# ─────────────────────────────────────────────
# MODULE: ACCOUNTS (BOSS ONLY VIEW)
# ─────────────────────────────────────────────
elif selected == "👥  Accounts":
    if role != "Boss":
        st.error("🔒 Security Access Violation. This interface is restricted to executive 'Boss' accounts only.")
    else:
        page_header("Accounts Control Center", "Manage administrative staff profiles, system registrations, and log trackers.")
        
        accounts_registered = fetch_all("SELECT id, username, role FROM users")
        st.metric("Total User Accounts Configured", len(accounts_registered))
        
        acc_tab1, acc_tab2 = st.tabs(["🔒 Profiles & Access control", "📜 Activity tracking ledger"])
        
        with acc_tab1:
            section_label("System Registration Roster")
            if accounts_registered:
                df_profiles = pd.DataFrame([dict(u) for u in accounts_registered])
                st.dataframe(df_profiles, use_container_width=True, hide_index=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                section_label("Decommission Employee Access Account")
                st.warning("⚠️ Attention: Revoking an account instantly disconnects workspace rights. Historical audit trails are preserved inside ledger logs.")
                
                # Prevent a Boss from deleting their own currently active session account
                killable_users = [u["username"] for u in accounts_registered if u["username"] != username]
                selection_pool = ["— select profile —"] + killable_users
                target_user_burn = st.selectbox("Select employee handle to delete", selection_pool, key="burn_user_select")
                
                if st.button("Permanently Delete Account", type="primary"):
                    if target_user_burn != "— select profile —":
                        execute_write("DELETE FROM users WHERE username = ?", (target_user_burn,))
                        log_action(username, "Delete Account", f"Purged security access profile for: {target_user_burn}")
                        st.success(f"Security Profile '{target_user_burn}' wiped successfully from application database runtime.")
                        play_ding()
                        st.rerun()
                    else:
                        st.error("Please pick an active staff profile from selection tray before trying to trigger deletion processes.")
            else:
                st.info("No administrative profiles found.")
                
        with acc_tab2:
            section_label("Cross-Examine Operational Logs By User Profile")
            profile_list_filter = ["Show All Operations"] + [u["username"] for u in accounts_registered]
            chosen_profile_audit = st.selectbox("Filter audit lines by specific employee profile name", profile_list_filter)
            
            if chosen_profile_audit == "Show All Operations":
                audit_records = fetch_all("SELECT timestamp as [Time Marked], username as [Staff Member], action as [Operation], details as [Action Breakdown] FROM audit_log ORDER BY id DESC LIMIT 400")
            else:
                audit_records = fetch_all("SELECT timestamp as [Time Marked], username as [Staff Member], action as [Operation], details as [Action Breakdown] FROM audit_log WHERE username = ? ORDER BY id DESC LIMIT 400", (chosen_profile_audit,))
                
            if audit_records:
                st.dataframe(pd.DataFrame([dict(row) for row in audit_records]), use_container_width=True, hide_index=True)
            else:
                st.info(f"No specific adjustments or transactions indexed yet under user selection: '{chosen_profile_audit}'")

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
                    log_action(username, "Add Doctor", f"Name: {d_name.strip()} | Specialty: {d_spec.strip()} | Model: {comm_type}")
                    st.success(f"Doctor '{d_name}' added.")
                    play_ding()
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
                    log_action(username, "Remove Doctor", f"Removed Doctor Name: {del_doc}")
                    st.success(f"Doctor '{del_doc}' removed.")
                    play_ding()
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
                    log_action(username, "Add Staff", f"Employee: {emp_name.strip()} | Role: {emp_role.strip()} | Salary: ${emp_salary}")
                    st.success(f"{emp_name} added to payroll.")
                    play_ding()
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
                    log_action(username, "Remove Staff", f"Fired/Removed employee: {del_emp}")
                    st.success(f"Removed {del_emp} from payroll.")
                    play_ding()
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
                    log_action(username, "Add Service", f"Service catalog item: {s_name.strip()} | Price: ${s_price}")
                    st.success(f"Service '{s_name}' added at ${s_price:.2f}.")
                    play_ding()
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
                    log_action(username, "Remove Service", f"Deleted Service: {del_svc}")
                    st.success(f"Service '{del_svc}' removed.")
                    play_ding()
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
                    log_action(username, "Create Bundle", f"Package created: {b_name.strip()} | Priced: ${b_price}")
                    st.success(f"Bundle '{b_name}' created at ${b_price:.2f}.")
                    play_ding()
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
                    log_action(username, "Remove Bundle", f"Deleted Bundle: {del_bnd}")
                    st.success(f"Bundle '{del_bnd}' removed.")
                    play_ding()
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
                    play_ding()
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
                    play_ding()
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
                    play_ding()
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
                        play_ding()
                        st.rerun()
            with col2:
                del_sub = st.selectbox("Remove subscription", ["— select —"] + [s["name"] for s in all_subs], key="del_sub_select")
                if st.button("Remove Subscription", type="primary", key="btn_del_subscription"):
                    if del_sub != "— select —":
                        execute_write("DELETE FROM subscriptions WHERE name = ?", (del_sub,))
                        log_action(username, "Remove Subscription", del_sub)
                        st.success(f"Subscription '{del_sub}' removed.")
                        play_ding()
                        st.rerun()
        else:
            st.info("No subscriptions added yet.")
