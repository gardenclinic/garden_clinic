import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime, date

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
*, *::before, *::after { box-sizing: border-box; }\nhtml, body, .stApp {
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

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea, .stDateInput input {
    background: #FFFFFF !important;
    border: 1px solid #D1DDD6 !important;
    border-radius: 8px !important;
    color: #1A2E23 !important;
    transition: all 0.2s ease;
}
.stTextInput input:focus, .stNumberInput input:focus, .stSelectbox [data-baseweb="select"]:focus, .stTextArea textarea:focus, .stDateInput input:focus {
    border-color: #2F6B52 !important;
    box-shadow: 0 0 0 2px rgba(47,107,82,0.15) !important;
}

/* ── BUTTONS ── */
button[kind="secondary"] {
    background: #2F6B52 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    font-weight: 500 !important;
    transition: background 0.2s;
}
button[kind="secondary"]:hover {
    background: #23513E !important;
}
button[kind="primary"] {
    background: #D9534F !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
}

/* ── METRIC CARDS ── */
div[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    color: #0D3D2B !important;
}
div[data-testid="metric-container"] {
    background: #FFFFFF;
    border: 1px solid #E2EBE6;
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

/* ── TABS ── */
button[data-baseweb="tab"] {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: #617D6E !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #0D3D2B !important;
    border-bottom-color: #2F6B52 !important;
}

/* ── TABLES & BLOCKS ── */
.reportview-container .main .block-container { padding-top: 2rem; }
h1, h2, h3 { color: #0D3D2B !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DB SETUP
# ─────────────────────────────────────────────
DB_FILE = "garden_clinic.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    
    # Financial parameters
    c.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            val_num REAL,
            val_text TEXT
        )
    """)
    
    # One-time Transactions
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT, -- 'Income' or 'Expense'
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)
    
    # Recurring Subscriptions
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            type TEXT, -- 'Income' or 'Expense'
            amount REAL,
            frequency TEXT, -- 'Monthly', 'Annual'
            active INTEGER DEFAULT 1
        )
    """)
    
    # Inventory
    c.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            quantity INTEGER,
            unit TEXT,
            cost_per_unit REAL,
            min_stock INTEGER
        )
    """)
    
    # Audit Logs
    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            details TEXT
        )
    """)
    
    # Insert default admin if missing
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        pwd_hash = hashlib.sha256("clinic2025".encode()).hexdigest()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", ("admin", pwd_hash, "Admin"))
        
    conn.commit()
    conn.close()

init_db()

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def execute_read(query, params=()):
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql_query(query, conn, params=params)

def execute_write(query, params=()):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()

def log_action(user, action, details):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_write("INSERT INTO audit_logs (timestamp, user, action, details) VALUES (?, ?, ?, ?)", (now, user, action, details))

# ─────────────────────────────────────────────
# SESSION STATE & AUTH
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

def login_user(u, p):
    h = hashlib.sha256(p.encode()).hexdigest()
    res = execute_read("SELECT role FROM users WHERE username=? AND password=?", (u, h))
    if not res.empty:
        st.session_state.authenticated = True
        st.session_state.username = u
        st.session_state.role = res.iloc[0]["role"]
        log_action(u, "Login", "Successfully logged in.")
        return True
    return False

def logout_user():
    log_action(st.session_state.username, "Logout", "Logged out.")
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

# ─────────────────────────────────────────────
# AUTHENTICATION SCREEN
# ─────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("<div style='max-width: 420px; margin: 8rem auto padding: 2rem; background: white; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    st.title("🌿 Garden Clinic")
    st.subheader("Financial Management Core")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In", use_container_width=True, type="secondary"):
        if login_user(username, password):
            st.success("Access Granted.")
            st.rerun()
        else:
            st.error("Invalid credentials.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# APPLICATION NAVIGATION
# ─────────────────────────────────────────────
username = st.session_state.username
role = st.session_state.role

st.sidebar.markdown(f"<h2 style='color:#E8F0EB; margin-bottom:0;'>Garden Clinic</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color:#A3BFB0; font-size:0.85rem; margin-top:0;'>User: {username} ({role})</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin: 0.5rem 0 1.5rem 0;'>", unsafe_allow_html=True)

menu = st.sidebar.radio("NAVIGATE", ["Overview & Dash", "Transactions Ledger", "Subscriptions Manager", "Inventory & Costs", "System Tools"])

st.sidebar.markdown("<div style='position: fixed; bottom: 20px;'>", unsafe_allow_html=True)
if st.sidebar.button("Log Out", key="logout_btn"):
    logout_user()
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MODULE 1: OVERVIEW & DASHBOARD
# ─────────────────────────────────────────────
if menu == "Overview & Dash":
    st.title("Financial Overview")
    
    # Fetch Data
    df_tx = execute_read("SELECT * FROM transactions")
    df_sub = execute_read("SELECT * FROM subscriptions WHERE active = 1")
    
    # Calculate One-Time
    inc_ot = df_tx[df_tx["type"] == "Income"]["amount"].sum()
    exp_ot = df_tx[df_tx["type"] == "Expense"]["amount"].sum()
    
    # Calculate Monthly Recurring Rates
    inc_rec = 0.0
    exp_rec = 0.0
    for _, row in df_sub.iterrows():
        amt = row["amount"]
        if row["frequency"] == "Annual":
            amt /= 12.0
        if row["type"] == "Income":
            inc_rec += amt
        else:
            exp_rec += amt
            
    net_ot = inc_ot - exp_ot
    net_rec_monthly = inc_rec - exp_rec
    
    # Display KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Net One-Time Ledger", f"{net_ot:,.2f} IQD")
    c2.metric("Est. Monthly Recurring Revenue", f"{inc_rec:,.2f} IQD")
    c3.metric("Est. Monthly Recurring Burn", f"{exp_rec:,.2f} IQD")
    
    st.markdown("---")
    
    cc1, cc2 = st.columns(2)
    with cc1:
        st.subheader("Recent One-Time Ledger Events")
        if not df_tx.empty:
            st.dataframe(df_tx.sort_values(by="date", ascending=False).head(10), use_container_width=True, hide_index=True)
        else:
            st.info("No records found in transactional logs.")
            
    with cc2:
        st.subheader("Active Recurring Subscriptions")
        if not df_sub.empty:
            st.dataframe(df_sub, use_container_width=True, hide_index=True)
        else:
            st.info("No active recurring lines running currently.")

# ─────────────────────────────────────────────
# MODULE 2: TRANSACTIONS LEDGER
# ─────────────────────────────────────────────
elif menu == "Transactions Ledger":
    st.title("Transactions Ledger")
    
    t1, t2 = st.tabs(["Record Transaction", "Historical Registry"])
    
    with t1:
        st.subheader("Log New Movement")
        with st.form("tx_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            tx_date = col1.date_input("Date of Event", date.today())
            tx_type = col2.selectbox("Movement Type", ["Income", "Expense"])
            tx_cat = col3.text_input("Category / Classification", placeholder="e.g. Consultancy, Utilities, Fertilizars")
            
            col4, col5 = st.columns([1, 2])
            tx_amt = col4.number_input("Absolute Amount (IQD)", min_value=0.0, step=50.0)
            tx_desc = col5.text_input("Detailed Memo Description")
            
            if st.form_submit_button("Commit Entry to Database"):
                if tx_amt <= 0:
                    st.error("Amount must be greater than zero.")
                elif not tx_cat.strip():
                    st.error("Category tag field is required.")
                else:
                    execute_write(
                        "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                        (tx_date.strftime("%Y-%m-%d"), tx_type, tx_cat.strip(), tx_amt, tx_desc.strip())
                    )
                    log_action(username, "Insert Transaction", f"{tx_type}: {tx_amt} IQD to {tx_cat}")
                    st.success("Transaction entry written successfully.")
                    
    with t2:
        st.subheader("Complete Records Ledger")
        df_all = execute_read("SELECT * FROM transactions ORDER BY date DESC")
        if not df_all.empty:
            # Inline Deletion Capability
            st.dataframe(df_all, use_container_width=True, hide_index=True)
            
            st.markdown("### Void / Delete Entry Record")
            del_id = st.number_input("Target Transaction ID to Void", min_value=1, step=1)
            if st.button("Execute Transaction Void", type="primary"):
                match = execute_read("SELECT * FROM transactions WHERE id = ?", (del_id,))
                if not match.empty:
                    execute_write("DELETE FROM transactions WHERE id = ?", (del_id,))
                    log_action(username, "Void Transaction", f"ID {del_id} details: {match.iloc[0]['amount']} IQD")
                    st.success(f"Transaction ID {del_id} dropped from ledger logs permanently.")
                    st.rerun()
                else:
                    st.error("Target Transaction ID match not found inside database index.")
        else:
            st.info("No records matching queries.")

# ─────────────────────────────────────────────
# MODULE 3: SUBSCRIPTIONS MANAGER
# ─────────────────────────────────────────────
elif menu == "Subscriptions Manager":
    st.title("Subscriptions & Regular Burn Rates")
    
    t1, t2 = st.tabs(["Deploy Recurring Profile", "Manage Profiles Configuration"])
    
    with t1:
        st.subheader("Establish Recurrent Dynamic Pipeline")
        with st.form("sub_form", clear_on_submit=True):
            sub_name = st.text_input("Unique Pipeline Name / Identifier", placeholder="e.g. Premium Hub Workspace Tier")
            col1, col2, col3 = st.columns(3)
            sub_type = col1.selectbox("Directional Mode", ["Expense", "Income"])
            sub_amt = col2.number_input("Cost Rate per Iteration (IQD)", min_value=0.0, step=10.0)
            sub_freq = col3.selectbox("Frequency Interval", ["Monthly", "Annual"])
            
            if st.form_submit_button("Instantiate Pipeline Routine"):
                if not sub_name.strip():
                    st.error("A unique name identifying this operational row is mandatory.")
                elif sub_amt <= 0:
                    st.error("Rate metrics must scale above zero values.")
                else:
                    try:
                        execute_write(
                            "INSERT INTO subscriptions (name, type, amount, frequency, active) VALUES (?, ?, ?, ?, 1)",
                            (sub_name.strip(), sub_type, sub_amt, sub_freq)
                        )
                        log_action(username, "Create Subscription", f"{sub_name} ({sub_type}) - {sub_amt} IQD {sub_freq}")
                        st.success(f"Pipeline flow for '{sub_name}' initialized successfully.")
                    except sqlite3.IntegrityError:
                        st.error("A subscription profile allocation with that tracking designation already exists.")
                        
    with t2:
        st.subheader("Operational Pipeline Settings")
        all_subs = execute_read("SELECT * FROM subscriptions").to_dict(orient="records")
        
        if all_subs:
            # Table formatting representation
            st.dataframe(pd.DataFrame(all_subs), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### State Controls Switch")
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

# ─────────────────────────────────────────────
# MODULE 4: INVENTORY & COSTS
# ─────────────────────────────────────────────
elif menu == "Inventory & Costs":
    st.title("Clinic Stock Supply & Capital Valuation")
    
    t1, t2 = st.tabs(["Stock Asset Ledger", "Replenish / Log Inventory Unit"])
    
    with t1:
        st.subheader("Active On-Hand Supply Manifest")
        df_inv = execute_read("SELECT *, (quantity * cost_per_unit) AS total_asset_value FROM inventory")
        
        if not df_inv.empty:
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
            
            # Global Metrics
            total_val = df_inv["total_asset_value"].sum()
            st.metric("Aggregate Calculated Inventory Asset Worth", f"{total_val:,.2f} IQD")
            
            # Alerts tracking
            low_stock = df_inv[df_inv["quantity"] <= df_inv["min_stock"]]
            if not low_stock.empty:
                st.warning(f"⚠️ Restock Notification: {len(low_stock)} operational items hit target critical minimum bounds.")
                st.dataframe(low_stock[["item_name", "quantity", "min_stock"]], use_container_width=True, hide_index=True)
        else:
            st.info("The inventory tracking matrix sheet is currently empty.")
            
    with t2:
        st.subheader("Register / Adjust Material Parameters")
        with st.form("inventory_form", clear_on_submit=True):
            i_name = st.text_input("Item Track Designation Name", placeholder="e.g. Premium Organic Plant Mix Type B")
            col1, col2 = st.columns(2)
            i_qty = col1.number_input("Current Item Quantity On-Hand Count", min_value=0, step=1)
            i_unit = col2.text_input("Unit Scale Label Metric", placeholder="e.g. bags, liters, vials")
            
            col3, col4 = st.columns(2)
            i_cost = col3.number_input("Unit Purchase Evaluation Value Cost (IQD)", min_value=0.0, step=1.0)
            i_min = col4.number_input("Minimum Safe Stock Threshold Parameter", min_value=0, step=1)
            
            if st.form_submit_button("Write Manifest Adjustments"):
                if not i_name.strip() or not i_unit.strip():
                    st.error("Name and structural measurement configuration context labels are required fields.")
                else:
                    # UPSERT strategy simulation logic inside SQL engine execution
                    existing = execute_read("SELECT id FROM inventory WHERE item_name = ?", (i_name.strip(),))
                    if not existing.empty:
                        execute_write(
                            "UPDATE inventory SET quantity=?, unit=?, cost_per_unit=?, min_stock=? WHERE item_name=?",
                            (i_qty, i_unit.strip(), i_cost, i_min, i_name.strip())
                        )
                        log_action(username, "Update Inventory", f"Adjusted {i_name.strip()} details to Count: {i_qty}")
                        st.success(f"Existing tracking dataset parameters updated successfully for item '{i_name}'.")
                    else:
                        execute_write(
                            "INSERT INTO inventory (item_name, quantity, unit, cost_per_unit, min_stock) VALUES (?, ?, ?, ?, ?)",
                            (i_name.strip(), i_qty, i_unit.strip(), i_cost, i_min)
                        )
                        log_action(username, "Create Inventory", f"Initialized item row entry {i_name.strip()} counts: {i_qty}")
                        st.success(f"New structural item tracing profile created successfully for '{i_name}'.")

# ─────────────────────────────────────────────
# MODULE 5: SYSTEM TOOLS
# ─────────────────────────────────────────────
elif menu == "System Tools":
    st.title("System Infrastructure Controls Engine")
    
    if role != "Admin":
        st.error("Security Restriction Protocol: Access to core configuration architecture requires elevated administrative rights.")
        st.stop()
        
    t1, t2 = st.tabs(["User Security Directory", "Audit Operational Log Framework"])
    
    with t1:
        st.subheader("System Access Profiles Management")
        df_users = execute_read("SELECT username, role FROM users")
        st.dataframe(df_users, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("Provision New User Context Profile")
        with st.form("user_provision_form", clear_on_submit=True):
            new_u = st.text_input("New Username Allocation")
            new_p = st.text_input("Initial Temporary Password Parameter", type="password")
            new_r = st.selectbox("Functional Privilege Scope Assignment Role", ["Staff", "Admin"])
            
            if st.form_submit_button("Provision User Access Profile Token"):
                if not new_u.strip() or not new_p.strip():
                    st.error("Operational fields mapping for credential validation setup must be filled completely.")
                else:
                    h_pass = hashlib.sha256(new_p.encode()).hexdigest()
                    try:
                        execute_write("INSERT INTO users VALUES (?, ?, ?)", (new_u.strip(), h_pass, new_r))
                        log_action(username, "Create User", f"Provisioned access credentials schema for user account: {new_u.strip()}")
                        st.success("New structural authentication profile created successfully inside server indexes.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("That specific identity index credential mapping allocation is already taken by another system context.")
                        
    with t2:
        st.subheader("System Infrastructure Operational Action Audit Log Logs")
        df_logs = execute_read("SELECT * FROM audit_logs ORDER BY timestamp DESC")
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            if st.button("Flush Archival Logs Records Database Manifest completely", type="primary"):
                execute_write("DELETE FROM audit_logs")
                log_action(username, "Purge System Logs", "Logs records cache flushed completely by admin privilege token command execution.")
                st.success("Internal runtime tracker records data arrays formatted back down onto zeroes state index layout elements.")
                st.rerun()
        else:
            st.info("Audit log tables currently report no historical runtime logging modifications data tracks arrays.")
