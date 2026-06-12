import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime, date
import streamlit.components.v1 as components
from supabase import create_client

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Garden Clinic", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: #F0F4F2 !important; color: #1A2E23 !important; font-family: 'DM Sans', system-ui, sans-serif !important; }
[data-testid="stSidebar"] { background: #0D3D2B !important; border-right: none !important; min-width: 230px !important; }
[data-testid="stSidebar"] * { color: #E8F0EB !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.9rem !important; }
section[data-testid="stSidebarNav"] { display: none; }
.pulse-bar { background: linear-gradient(90deg, #0D3D2B 0%, #1A5C3E 100%); border-radius: 14px; padding: 16px 24px; display: flex; gap: 32px; flex-wrap: wrap; align-items: center; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(13,61,43,0.12); }
.pulse-stat { display: flex; flex-direction: column; }
.pulse-label { font-size: 0.72rem; color: #6FCF97; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
.pulse-value { font-family: 'DM Mono', monospace; font-size: 1.35rem; font-weight: 500; color: #FFFFFF; margin-top: 2px; }
.pulse-divider { width: 1px; background: rgba(255,255,255,0.15); height: 36px; align-self: center; }
.page-header { margin-bottom: 28px; }
.page-header h1 { font-size: 1.7rem !important; font-weight: 700 !important; color: #0D3D2B !important; margin: 0 0 4px 0 !important; }
.page-header p { font-size: 0.9rem; color: #5A7A65; margin: 0; }
.card { background: #FFFFFF; border-radius: 14px; padding: 22px 24px; border: 1px solid #DDE8E1; margin-bottom: 18px; transition: box-shadow 0.2s; }
.card:hover { box-shadow: 0 6px 24px rgba(0,0,0,0.06); }
.card h3 { margin: 0 0 4px 0; font-size: 0.8rem; color: #5A7A65; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.card .big-num { font-family: 'DM Mono', monospace; font-size: 2rem; font-weight: 500; margin: 0; }
.card .big-num.green { color: #0D7A4E; }
.card .big-num.red { color: #C0392B; }
.card .big-num.dark { color: #0D3D2B; }
.card .sub { font-size: 0.78rem; color: #8EA898; margin-top: 4px; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 4px !important; border-bottom: 2px solid #DDE8E1 !important; padding-bottom: 0 !important; }
.stTabs button[data-baseweb="tab"] { background: transparent !important; border: none !important; color: #5A7A65 !important; font-size: 0.88rem !important; font-weight: 500 !important; padding: 8px 16px 10px !important; border-radius: 0 !important; font-family: 'DM Sans', sans-serif !important; }
.stTabs button[aria-selected="true"] { color: #0D3D2B !important; font-weight: 700 !important; border-bottom: 2px solid #0D3D2B !important; margin-bottom: -2px !important; }
.stButton > button { background: #0D3D2B !important; color: #FFFFFF !important; border: none !important; border-radius: 9px !important; font-weight: 600 !important; font-size: 0.88rem !important; padding: 10px 20px !important; font-family: 'DM Sans', sans-serif !important; transition: background 0.15s, transform 0.1s !important; }
.stButton > button:hover { background: #1A5C3E !important; transform: translateY(-1px) !important; }
button[data-testid="baseButton-primary"] { background: #C0392B !important; }
button[data-testid="baseButton-primary"]:hover { background: #A93226 !important; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input { border-radius: 9px !important; border: 1.5px solid #DDE8E1 !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; background: #FFFFFF !important; color: #1A2E23 !important; padding: 9px 12px !important; }
.stSelectbox > div > div > div, .stMultiSelect > div > div > div { border-radius: 9px !important; border: 1.5px solid #DDE8E1 !important; background: #FFFFFF !important; }
.stTextArea textarea { border-radius: 9px !important; border: 1.5px solid #DDE8E1 !important; font-family: 'DM Sans', sans-serif !important; }
.stRadio > div { gap: 8px !important; }
[data-testid="stDataFrame"] { border-radius: 12px !important; overflow: hidden !important; border: 1.5px solid #DDE8E1 !important; }
.stSuccess > div, .stError > div, .stWarning > div, .stInfo > div { border-radius: 10px !important; font-size: 0.88rem !important; }
.section-label { font-size: 0.75rem; font-weight: 700; color: #5A7A65; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 12px; border-bottom: 1px solid #DDE8E1; padding-bottom: 8px; }
.receipt-wrap { background: #FFFFFF; border: 1.5px dashed #0D3D2B; border-radius: 14px; padding: 28px; max-width: 400px; font-family: 'DM Mono', monospace; font-size: 0.82rem; color: #1A2E23; }
.receipt-wrap h2 { text-align: center; margin: 0 0 2px; color: #0D3D2B; font-size: 1.1rem; font-family: 'DM Sans', sans-serif; font-weight: 800; }
.receipt-wrap .receipt-sub { text-align: center; font-size: 0.72rem; color: #5A7A65; margin-bottom: 14px; font-family: 'DM Sans', sans-serif; }
.receipt-row { display: flex; justify-content: space-between; margin: 5px 0; }
.receipt-total { font-size: 1rem; font-weight: 700; color: #0D7A4E; border-top: 1px dashed #DDE8E1; padding-top: 10px; margin-top: 10px; }
.receipt-footer { text-align: center; font-size: 0.7rem; color: #8EA898; margin-top: 14px; font-family: 'DM Sans', sans-serif; }
hr.dashed { border: none; border-top: 1px dashed #DDE8E1; margin: 12px 0; }
.login-card { background: #FFFFFF; border: 1.5px solid #DDE8E1; border-radius: 18px; padding: 40px; max-width: 440px; margin: 60px auto 0; box-shadow: 0 8px 40px rgba(0,0,0,0.07); }
.login-card h1 { color: #0D3D2B; text-align: center; margin: 0 0 4px; font-weight: 800; font-size: 1.8rem; }
.login-card p { text-align: center; color: #5A7A65; font-size: 0.88rem; margin-bottom: 24px; }
.stForm [data-testid="stFormSubmitButton"] button { width: 100%; background: #0D3D2B !important; }
[data-testid="stMetric"] { background: #FFFFFF; border: 1.5px solid #DDE8E1; border-radius: 12px; padding: 16px 20px; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; color: #5A7A65 !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 1.6rem !important; color: #0D3D2B !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SUPABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_sb():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# ── CORE DB HELPERS ──
def sb_all(table, filters=None, order=None, desc_order=False, limit=None):
    try:
        q = get_sb().table(table).select("*")
        if filters:
            for k, v in filters.items():
                q = q.eq(k, v)
        if order:
            q = q.order(order, desc=desc_order)
        if limit:
            q = q.limit(limit)
        return q.execute().data or []
    except:
        return []

def sb_one(table, filters):
    rows = sb_all(table, filters=filters)
    return rows[0] if rows else None

def sb_insert(table, data):
    try:
        get_sb().table(table).insert(data).execute()
        return True
    except Exception as e:
        return False

def sb_delete(table, col, val):
    try:
        get_sb().table(table).delete().eq(col, val).execute()
        return True
    except:
        return False

def sb_update(table, data, col, val):
    try:
        get_sb().table(table).update(data).eq(col, val).execute()
        return True
    except:
        return False

def sb_exists(table, col, val):
    try:
        res = get_sb().table(table).select("id").eq(col, val).execute()
        return len(res.data) > 0
    except:
        return False

def sb_sum(table, col, filters=None):
    rows = sb_all(table, filters=filters)
    return sum(float(r.get(col) or 0) for r in rows)

def sb_count(table, filters=None):
    return len(sb_all(table, filters=filters))

# ── COMPLEX JOIN HELPERS ──
def get_visits_joined(limit=100, patient_id=None):
    visits = sb_all("visits", order="id", desc_order=True, limit=limit)
    if patient_id:
        visits = [v for v in visits if v.get("patient_id") == patient_id]
    if not visits:
        return []
    patients = {p["id"]: p["name"] for p in sb_all("patients")}
    doctors  = {d["id"]: d["name"] for d in sb_all("doctors")}
    services = {s["id"]: s["name"] for s in sb_all("services")}
    bundles  = {b["id"]: b["name"] for b in sb_all("bundles")}
    result = []
    for v in visits:
        svc_name = services.get(v.get("service_id"), "")
        bnd_name = bundles.get(v.get("bundle_id"), "")
        item = svc_name if svc_name else f"📦 {bnd_name}"
        result.append({
            "id": v["id"],
            "Date": v.get("visit_date",""),
            "Patient": patients.get(v.get("patient_id"),""),
            "Doctor": doctors.get(v.get("doctor_id"),""),
            "Item": item,
            "Base": float(v.get("base_price") or 0),
            "Discount": float(v.get("discount_amount") or 0),
            "Paid": float(v.get("net_paid") or 0),
            "Method": v.get("payment_method",""),
            "Notes": v.get("notes",""),
        })
    return result

def get_appointments_joined():
    appts = sb_all("appointments", order="appt_date", desc_order=True)
    if not appts:
        return []
    patients = {p["id"]: p["name"] for p in sb_all("patients")}
    doctors  = {d["id"]: d["name"] for d in sb_all("doctors")}
    return [{
        "id": a["id"],
        "Date": a.get("appt_date",""),
        "Time": a.get("appt_time",""),
        "Patient": patients.get(a.get("patient_id"),""),
        "Doctor": doctors.get(a.get("doctor_id"),""),
        "Reason": a.get("reason",""),
        "Status": a.get("status",""),
    } for a in appts]

def get_financials():
    visits  = sb_all("visits")
    doctors = sb_all("doctors")
    expenses_rows = sb_all("expenses")

    gross = sum(float(v.get("net_paid") or 0) for v in visits)
    total_exp = sum(float(e.get("amount") or 0) for e in expenses_rows)

    doc_map = {}
    for v in visits:
        did = v.get("doctor_id")
        if did:
            doc_map.setdefault(did, []).append(float(v.get("net_paid") or 0))

    commissions = 0.0
    doc_visits = {}
    for d in doctors:
        paid_list = doc_map.get(d["id"], [])
        doc_visits[d["name"]] = {"visits": paid_list, "comm_type": d["comm_type"], "fixed_rate": float(d.get("fixed_rate") or 0)}
        if d["comm_type"] == "fixed":
            commissions += sum(paid_list) * (float(d.get("fixed_rate") or 0) / 100.0)
        else:
            n = len(paid_list)
            if n >= 20:   commissions += sum(paid_list) * 0.05
            elif n >= 10: commissions += sum(paid_list) * 0.03

    total_out = total_exp + commissions
    return gross, total_exp, commissions, total_out, gross - total_out, doc_visits

# ── MISC HELPERS ──
def hash_password(pw): return hashlib.sha256(pw.encode()).hexdigest()

def log_action(uname, action, details=""):
    sb_insert("audit_log", {"username": uname, "action": action, "details": details,
                             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

def play_ding():
    components.html("""<script>
    try { var c=new(window.AudioContext||window.webkitAudioContext)(),o=c.createOscillator(),g=c.createGain();
    o.type='sine';o.frequency.setValueAtTime(1100,c.currentTime);g.gain.setValueAtTime(0.18,c.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+0.45);o.connect(g);g.connect(c.destination);
    o.start();o.stop(c.currentTime+0.45);}catch(e){}</script>""", height=0, width=0)

def card(title, value, css_class="dark", subtitle=""):
    return f'<div class="card"><h3>{title}</h3><p class="big-num {css_class}">{value}</p>{f"<p class=sub>{subtitle}</p>" if subtitle else ""}</div>'

def section_label(text):
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)

def pulse_bar(stats):
    items = ""
    for i, (label, value) in enumerate(stats):
        if i > 0: items += '<div class="pulse-divider"></div>'
        items += f'<div class="pulse-stat"><span class="pulse-label">{label}</span><span class="pulse-value">{value}</span></div>'
    st.markdown(f'<div class="pulse-bar">{items}</div>', unsafe_allow_html=True)

def page_header(title, desc=""):
    st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{desc}</p></div>', unsafe_allow_html=True)

# ── AUTO PAYROLL ──
def auto_payroll():
    month = datetime.now().strftime("%Y-%m")
    tag = f"Monthly Payroll — {month}"
    if not sb_exists("expenses", "description", tag):
        total = sb_sum("employees", "salary")
        if total > 0:
            sb_insert("expenses", {"description": tag, "category": "Payroll",
                                   "amount": total, "date": f"{month}-01", "added_by": "System"})

auto_payroll()

# ── AUTO SUBSCRIPTIONS ──
def auto_subscriptions():
    month = datetime.now().strftime("%Y-%m")
    for sub in sb_all("subscriptions", filters={"active": 1}):
        tag = f"Subscription: {sub['name']} — {month}"
        if not sb_exists("expenses", "description", tag):
            day = int(sub.get("billing_day") or 1)
            sb_insert("expenses", {"description": tag, "category": "Subscription",
                                   "amount": float(sub["amount"]), "date": f"{month}-{day:02d}", "added_by": "System"})

auto_subscriptions()

# ─────────────────────────────────────────────
# FINANCIALS (run once per page load)
# ─────────────────────────────────────────────
gross_income, base_expenses, total_commissions, total_outflows, net_profit, doc_visits = get_financials()

today_str = date.today().isoformat()
today_visits_rows = sb_all("visits", filters={"visit_date": today_str})
today_revenue = sum(float(v.get("net_paid") or 0) for v in today_visits_rows)
today_visits_count = len(today_visits_rows)
patient_count = sb_count("patients")

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="login-card"><h1>🌿 Garden Clinic</h1><p>Clinic Management System</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        login_tab, reg_tab = st.tabs(["Sign In", "Create Account"])
        with login_tab:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Sign In →", use_container_width=True):
                users = sb_all("users", filters={"username": u.strip()})
                match = [x for x in users if x.get("password_hash") == hash_password(p)]
                if match:
                    st.session_state.logged_in = True
                    st.session_state.username = match[0]["username"]
                    st.session_state.role = match[0]["role"]
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with reg_tab:
            ru = st.text_input("New username")
            rp = st.text_input("New password", type="password")
            role_sel = st.selectbox("Role", ["Boss", "Accounting", "Reception", "Reception & Accounting"])
            code = st.text_input("Admin code", type="password")
            if st.button("Create Account", use_container_width=True):
                if code != "1011":
                    st.error("Invalid admin code.")
                elif ru and rp:
                    if sb_exists("users", "username", ru.strip()):
                        st.error("Username already taken.")
                    else:
                        sb_insert("users", {"username": ru.strip(), "password_hash": hash_password(rp), "role": role_sel})
                        log_action("System", "Create Account", f"User: {ru.strip()} | Role: {role_sel}")
                        st.success("Account created. Sign in above.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
role = st.session_state.role
username = st.session_state.username

st.sidebar.markdown(f"""
<div style="padding:20px 16px 16px;border-bottom:1px solid rgba(255,255,255,0.1);">
    <div style="font-size:1.4rem;font-weight:800;color:#FFFFFF;">🌿 Garden Clinic</div>
    <div style="font-size:0.75rem;color:#6FCF97;margin-top:2px;font-weight:500;">Management System</div>
</div>
<div style="padding:14px 16px;border-bottom:1px solid rgba(255,255,255,0.1);margin-bottom:8px;">
    <div style="font-size:0.7rem;color:#6FCF97;text-transform:uppercase;letter-spacing:0.06em;">Signed in as</div>
    <div style="font-size:0.95rem;color:#FFFFFF;font-weight:600;margin-top:2px;">{username}</div>
    <div style="font-size:0.72rem;background:rgba(111,207,151,0.2);color:#6FCF97;display:inline-block;padding:2px 8px;border-radius:20px;margin-top:4px;font-weight:600;">{role}</div>
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
# DASHBOARD
# ─────────────────────────────────────────────
if selected == "📈  Dashboard":
    page_header("Executive Dashboard", f"Today is {date.today().strftime('%A, %B %d %Y')}")
    pulse_bar([("Today's Revenue", f"${today_revenue:,.0f}"), ("Visits Today", str(today_visits_count)),
               ("Total Patients", str(patient_count)), ("All-Time Revenue", f"${gross_income:,.0f}"), ("Net Profit", f"${net_profit:,.0f}")])

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(card("Gross Revenue", f"${gross_income:,.2f}", "green", "All collected payments"), unsafe_allow_html=True)
    with c2: st.markdown(card("Total Expenses", f"${total_outflows:,.2f}", "red", "Bills + payroll + commissions"), unsafe_allow_html=True)
    with c3: st.markdown(card("Net Profit", f"${net_profit:,.2f}", "dark", "Revenue minus all costs"), unsafe_allow_html=True)
    with c4: st.markdown(card("Doctor Commissions", f"${total_commissions:,.2f}", "dark", "Total owed to doctors"), unsafe_allow_html=True)

    st.markdown("---")
    ca, cb = st.columns([3,2])
    with ca:
        section_label("Revenue trend")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df = pd.DataFrame([{"Date": v["visit_date"], "Revenue": float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df.groupby("Date").sum(), y="Revenue", color="#0D3D2B", height=220)
        else: st.info("No visit data yet.")
    with cb:
        section_label("Doctor performance")
        rows = []
        for d in sb_all("doctors", order="name"):
            info = doc_visits.get(d["name"], {"visits":[], "comm_type": d["comm_type"], "fixed_rate": float(d.get("fixed_rate") or 0)})
            v = info["visits"]; vol = len(v); gen = sum(v)
            if d["comm_type"] == "fixed":
                payout = gen * (float(d.get("fixed_rate") or 0)/100); model = f"Fixed {d.get('fixed_rate')}%"
            else:
                if vol>=20: payout=gen*0.05; model="Tiered 5%"
                elif vol>=10: payout=gen*0.03; model="Tiered 3%"
                else: payout=0; model="Tiered 0%"
            rows.append({"Doctor": d["name"], "Visits": vol, "Revenue": f"${gen:,.0f}", "Commission": f"${payout:,.0f}", "Model": model})
        if rows: st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else: st.info("No doctors added yet.")

    st.markdown("---")
    section_label("Monthly revenue summary")
    if all_v if 'all_v' in dir() else False:
        df_m = pd.DataFrame([{"Month": v["visit_date"][:7], "Revenue": float(v.get("net_paid") or 0)} for v in sb_all("visits")])
        if not df_m.empty:
            df_m = df_m.groupby("Month").agg(Revenue=("Revenue","sum"), Visits=("Revenue","count")).reset_index().sort_values("Month", ascending=False)
            st.dataframe(df_m, use_container_width=True, hide_index=True)
    else:
        all_v2 = sb_all("visits")
        if all_v2:
            df_m = pd.DataFrame([{"Month": v["visit_date"][:7], "Revenue": float(v.get("net_paid") or 0)} for v in all_v2])
            df_m = df_m.groupby("Month").agg(Revenue=("Revenue","sum"), Visits=("Revenue","count")).reset_index().sort_values("Month", ascending=False)
            st.dataframe(df_m, use_container_width=True, hide_index=True)
        else: st.info("No visit data yet.")

    st.markdown("---")
    section_label("Activity audit log")
    af = st.selectbox("Filter by action", ["All","New Visit","New Patient","Remove Patient","Add Expense","Delete Expense","Add Referrer","Remove Referrer","Add Subscription","Remove Subscription","Referral Commission Paid"], key="audit_filter")
    audit_rows = sb_all("audit_log", order="id", desc_order=True, limit=200)
    if af != "All": audit_rows = [r for r in audit_rows if r.get("action") == af]
    if audit_rows:
        st.dataframe(pd.DataFrame([{"Time": r["timestamp"], "User": r["username"], "Action": r["action"], "Details": r.get("details","")} for r in audit_rows]), use_container_width=True, hide_index=True)
    else: st.info("No activity recorded yet.")

# ─────────────────────────────────────────────
# RECEPTION
# ─────────────────────────────────────────────
elif selected == "🖥️  Reception":
    page_header("Reception Desk", "Patient checkout, records, and visit history.")
    pulse_bar([("Today's Revenue", f"${today_revenue:,.0f}"), ("Visits Today", str(today_visits_count)), ("Total Patients", str(patient_count))])
    t1,t2,t3,t4,t5 = st.tabs(["Checkout","Patient Records","Add Patient","Visit History","Delete Visit"])

    with t1:
        section_label("New checkout")
        patients_db = sb_all("patients", order="name")
        docs_db     = sb_all("doctors",  order="name")
        services_db = [s for s in sb_all("services", order="name") if s.get("active") == 1]
        bundles_db  = sb_all("bundles",  order="name")

        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please add doctors and services in Settings before processing checkouts.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1:
                target_p = st.selectbox("Patient", ["— select —"] + list(p_map.keys()))
                chosen_doc = st.selectbox("Doctor", list(d_map.keys()))
                payment_method = st.selectbox("Payment method", ["Cash","Card","Insurance","Transfer"])
            with c2:
                item_type = st.radio("Item type", ["Service","Bundle"], horizontal=True)
                srv_id = bnd_id = None; base_price = 0.0; chosen_item_name = ""
                if item_type == "Service":
                    if services_db:
                        s_map = {f"{s['name']}  —  ${float(s['price']):.2f}": (s["id"], float(s["price"]), s["name"]) for s in services_db}
                        chosen = st.selectbox("Service", list(s_map.keys()))
                        srv_id, base_price, chosen_item_name = s_map[chosen]
                    else: st.error("No services configured.")
                else:
                    if bundles_db:
                        b_map = {f"{b['name']}  —  ${float(b['price']):.2f}": (b["id"], float(b["price"]), b["name"]) for b in bundles_db}
                        chosen = st.selectbox("Bundle", list(b_map.keys()))
                        bnd_id, base_price, chosen_item_name = b_map[chosen]
                    else: st.error("No bundles configured.")
                disc_type = st.radio("Discount", ["None","Fixed ($)","Percent (%)"], horizontal=True)
                disc_val  = st.number_input("Discount value", min_value=0.0, step=1.0)

            final_due = base_price
            if disc_type == "Fixed ($)":   final_due = max(0.0, base_price - disc_val)
            elif disc_type == "Percent (%)": final_due = max(0.0, base_price*(1-disc_val/100))
            visit_notes = st.text_area("Visit notes (optional)", height=70)

            referrers_db = sb_all("referrers", order="name")
            ref_names = [r["name"] for r in referrers_db]
            referral_options = ["Walk-in / Direct","Instagram / Social Media","Google Search","Friend / Word of mouth"] + ref_names
            how_found = st.selectbox("How did the patient find us?", referral_options)
            referred_by_val = how_found if how_found in ref_names else None

            st.markdown(f"### Total due: **${final_due:,.2f}**")
            if st.button("Save & Print Receipt", use_container_width=True):
                if target_p == "— select —": st.error("Please select a patient.")
                elif base_price == 0.0: st.error("Please select a service or bundle.")
                else:
                    disc_amt = base_price - final_due
                    sb_insert("visits", {"patient_id": p_map[target_p], "doctor_id": d_map[chosen_doc],
                        "service_id": srv_id, "bundle_id": bnd_id, "visit_date": today_str,
                        "base_price": base_price, "discount_amount": disc_amt, "net_paid": final_due,
                        "payment_method": payment_method, "notes": visit_notes,
                        "referred_by": referred_by_val, "added_by": username})
                    log_action(username, "New Visit", f"Patient: {target_p} | Doctor: {chosen_doc} | Paid: ${final_due:.2f} | Via: {how_found}")
                    play_ding()
                    st.success("Visit saved.")
                    st.session_state.rcpt = {"patient": target_p, "doctor": chosen_doc, "item": chosen_item_name,
                        "base": base_price, "disc": disc_amt, "net": final_due, "method": payment_method, "date": today_str}

            if "rcpt" in st.session_state:
                r = st.session_state.rcpt
                st.markdown(f"""<div class="receipt-wrap">
                    <h2>🌿 Garden Clinic</h2><p class="receipt-sub">Official Receipt · {r['date']}</p>
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
                </div>""", unsafe_allow_html=True)

    with t2:
        section_label("All patients")
        search = st.text_input("Search by name or phone", placeholder="Type to filter...")
        all_p = sb_all("patients", order="name")
        if search: all_p = [p for p in all_p if search.lower() in (p.get("name","")).lower() or search in (p.get("phone","") or "")]
        if all_p:
            st.dataframe(pd.DataFrame(all_p), use_container_width=True, hide_index=True)
            st.markdown("---"); section_label("Remove patient")
            del_target = st.selectbox("Select patient to remove", ["— select —"] + [p["name"] for p in all_p])
            if st.button("Remove Patient", type="primary"):
                if del_target != "— select —":
                    sb_delete("patients", "name", del_target)
                    log_action(username, "Remove Patient", del_target)
                    play_ding(); st.success(f"Removed {del_target}."); st.rerun()
        else: st.info("No patients found.")

    with t3:
        section_label("Register new patient")
        c1,c2 = st.columns(2)
        with c1:
            p_name  = st.text_input("Full name *")
            p_phone = st.text_input("Phone number")
            p_dob   = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1990-01-15")
        with c2:
            p_gender = st.selectbox("Gender", ["Prefer not to say","Male","Female","Other"])
            p_notes  = st.text_area("Notes / medical background", height=100)
        if st.button("Register Patient"):
            if p_name.strip():
                if sb_exists("patients", "name", p_name.strip()):
                    st.error("A patient with that name already exists.")
                else:
                    sb_insert("patients", {"name": p_name.strip(), "phone": p_phone.strip(),
                        "date_of_birth": p_dob.strip(), "gender": p_gender,
                        "notes": p_notes.strip(), "created_at": today_str})
                    log_action(username, "New Patient", f"{p_name.strip()} | {p_gender}")
                    play_ding(); st.success(f"Patient '{p_name}' registered.")
            else: st.error("Name is required.")

    with t4:
        section_label("Patient visit history")
        patients_all = sb_all("patients", order="name")
        if patients_all:
            lookup_p = st.selectbox("Select patient", ["— select —"] + [p["name"] for p in patients_all])
            if lookup_p != "— select —":
                pid = next(p["id"] for p in patients_all if p["name"] == lookup_p)
                hist = get_visits_joined(limit=500, patient_id=pid)
                if hist:
                    total_spent = sum(h["Paid"] for h in hist)
                    cc1,cc2 = st.columns(2)
                    cc1.metric("Total visits", len(hist)); cc2.metric("Total spent", f"${total_spent:,.2f}")
                    st.dataframe(pd.DataFrame(hist), use_container_width=True, hide_index=True)
                else: st.info(f"No visits recorded for {lookup_p}.")
        else: st.info("No patients registered yet.")

    with t5:
        section_label("Delete a visit record")
        st.warning("⚠️ Use this to correct data entry errors only.")
        all_visits_j = get_visits_joined(limit=100)
        if all_visits_j:
            st.dataframe(pd.DataFrame(all_visits_j), use_container_width=True, hide_index=True)
            st.markdown("---")
            void_id = st.number_input("Visit ID to delete", min_value=1, step=1)
            if st.button("Delete Visit", type="primary"):
                sb_delete("visits", "id", void_id)
                log_action(username, "Delete Visit", f"Voided visit ID #{void_id}")
                play_ding(); st.success(f"Visit #{void_id} deleted."); st.rerun()
        else: st.info("No visits recorded yet.")

# ─────────────────────────────────────────────
# APPOINTMENTS
# ─────────────────────────────────────────────
elif selected == "📅  Appointments":
    page_header("Appointments", "Schedule and manage upcoming patient appointments.")
    ta1,ta2 = st.tabs(["Schedule","View All"])
    with ta1:
        section_label("Book new appointment")
        patients_db = sb_all("patients", order="name")
        docs_db     = sb_all("doctors",  order="name")
        if not patients_db or not docs_db:
            st.warning("You need at least one patient and one doctor to book appointments.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1:
                ap_patient = st.selectbox("Patient", list(p_map.keys()))
                ap_doctor  = st.selectbox("Doctor",  list(d_map.keys()))
            with c2:
                ap_date   = st.date_input("Appointment date", value=date.today())
                ap_time   = st.time_input("Time")
                ap_reason = st.text_input("Reason / notes")
            if st.button("Book Appointment"):
                sb_insert("appointments", {"patient_id": p_map[ap_patient], "doctor_id": d_map[ap_doctor],
                    "appt_date": str(ap_date), "appt_time": str(ap_time), "reason": ap_reason, "status": "Scheduled"})
                log_action(username, "Book Appointment", f"{ap_patient} with {ap_doctor} on {ap_date}")
                play_ding(); st.success(f"Appointment booked for {ap_patient} on {ap_date} at {ap_time}.")
    with ta2:
        section_label("Upcoming & recent appointments")
        all_appts = get_appointments_joined()
        if all_appts:
            st.dataframe(pd.DataFrame(all_appts), use_container_width=True, hide_index=True)
            st.markdown("---"); section_label("Update appointment status")
            c1,c2 = st.columns(2)
            with c1: upd_id = st.number_input("Appointment ID", min_value=1, step=1)
            with c2: new_status = st.selectbox("New status", ["Scheduled","Completed","Cancelled","No-show"])
            if st.button("Update Status"):
                sb_update("appointments", {"status": new_status}, "id", upd_id)
                log_action(username, "Update Appointment", f"Appt #{upd_id} → {new_status}")
                play_ding(); st.success(f"Appointment #{upd_id} updated to '{new_status}'."); st.rerun()
        else: st.info("No appointments booked yet.")

# ─────────────────────────────────────────────
# ACCOUNTING
# ─────────────────────────────────────────────
elif selected == "📊  Accounting":
    page_header("Accounting", "Revenue, expenses, and financial health.")
    pulse_bar([("Gross Revenue", f"${gross_income:,.0f}"), ("Total Expenses", f"${total_outflows:,.0f}"),
               ("Net Profit", f"${net_profit:,.0f}"), ("Doctor Commissions", f"${total_commissions:,.0f}")])
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(card("Gross Revenue",  f"${gross_income:,.2f}",  "green"), unsafe_allow_html=True)
    with c2: st.markdown(card("Total Outflows", f"${total_outflows:,.2f}", "red"),   unsafe_allow_html=True)
    with c3: st.markdown(card("Net Profit",     f"${net_profit:,.2f}",    "dark"),   unsafe_allow_html=True)

    st.markdown("---")
    ac1,ac2 = st.columns(2)
    with ac1:
        section_label("Expenses breakdown")
        payroll_total = sum(float(e.get("amount") or 0) for e in sb_all("expenses") if e.get("category") == "Payroll")
        other_exp = base_expenses - payroll_total
        if total_outflows > 0:
            df_e = pd.DataFrame({"Category": ["Other Expenses","Payroll","Doctor Commissions"],
                                  "Amount ($)": [other_exp, payroll_total, total_commissions]}).set_index("Category")
            st.bar_chart(df_e, y="Amount ($)", color="#C0392B", height=220)
        else: st.info("No expense data yet.")
    with ac2:
        section_label("Daily revenue trend")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df_v = pd.DataFrame([{"Date": v["visit_date"], "Revenue": float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df_v.groupby("Date").sum(), y="Revenue", color="#0D3D2B", height=220)
        else: st.info("No revenue data yet.")

    st.markdown("---")
    ae1,ae2 = st.columns([3,2])
    with ae1:
        section_label("Expense log")
        filter_cat = st.selectbox("Filter by category", ["All","General","Payroll","Supplies","Utilities","Rent","Equipment","Marketing","Subscription","Other"], key="acc_filter_cat")
        all_exp = sb_all("expenses", order="id", desc_order=True)
        if filter_cat != "All": all_exp = [e for e in all_exp if e.get("category") == filter_cat]
        if all_exp:
            st.dataframe(pd.DataFrame([{"id": e["id"], "Date": e["date"], "Category": e.get("category",""), "Description": e["description"], "Amount": float(e.get("amount") or 0), "Added By": e.get("added_by","")} for e in all_exp]), use_container_width=True, hide_index=True)
        else: st.info("No expenses recorded.")
    with ae2:
        section_label("Add expense")
        with st.form("expense_form"):
            e_desc = st.text_input("Description")
            e_cat  = st.selectbox("Category", ["General","Supplies","Utilities","Rent","Equipment","Marketing","Other"])
            e_amt  = st.number_input("Amount ($)", min_value=0.0, step=10.0)
            e_date = st.date_input("Date", value=date.today())
            if st.form_submit_button("Add Expense"):
                if e_desc and e_amt > 0:
                    sb_insert("expenses", {"description": e_desc, "category": e_cat, "amount": e_amt, "date": str(e_date), "added_by": username})
                    log_action(username, "Add Expense", f"{e_desc} | ${e_amt:.2f} | {e_cat}")
                    play_ding(); st.success("Expense added."); st.rerun()
                else: st.error("Description and amount are required.")

    st.markdown("---"); section_label("Delete expense")
    st.warning("⚠️ Use this to remove an expense added by mistake.")
    del_exp_list = sb_all("expenses", order="id", desc_order=True, limit=100)
    if del_exp_list:
        del_opts = {f"#{e['id']} · {e['date']} · {e['description']} · ${float(e.get('amount') or 0):.2f}": e["id"] for e in del_exp_list}
        chosen_del = st.selectbox("Select expense to delete", ["— select —"] + list(del_opts.keys()), key="del_exp_select")
        if st.button("Delete Expense", type="primary", key="btn_del_expense"):
            if chosen_del != "— select —":
                sb_delete("expenses", "id", del_opts[chosen_del])
                log_action(username, "Delete Expense", f"Deleted #{del_opts[chosen_del]}: {chosen_del}")
                play_ding(); st.success("Expense deleted."); st.rerun()
    else: st.info("No expenses to delete.")

    st.markdown("---"); section_label("Referral commissions owed this month")
    current_month = datetime.now().strftime("%Y-%m")
    all_refs = sb_all("referrers", order="name")
    if all_refs:
        all_v_month = [v for v in sb_all("visits") if (v.get("visit_date") or "")[:7] == current_month]
        ref_rows = []
        total_ref_comm = 0.0
        for ref in all_refs:
            v_via = [v for v in all_v_month if v.get("referred_by") == ref["name"]]
            rev = sum(float(v.get("net_paid") or 0) for v in v_via)
            comm = rev * (float(ref.get("commission_rate") or 0) / 100.0)
            total_ref_comm += comm
            ref_rows.append({"Referrer": ref["name"], "Rate": f"{ref.get('commission_rate')}%",
                             "Visits This Month": len(v_via), "Revenue Generated": f"${rev:,.2f}", "Commission Due": f"${comm:,.2f}"})
        st.dataframe(pd.DataFrame(ref_rows), use_container_width=True, hide_index=True)
        st.markdown(f"**Total referral commissions owed this month: ${total_ref_comm:,.2f}**")
        if st.button("Mark All Referral Commissions as Paid (add as expense)"):
            if total_ref_comm > 0:
                tag = f"Referral Commissions — {current_month}"
                if not sb_exists("expenses", "description", tag):
                    sb_insert("expenses", {"description": tag, "category": "Marketing", "amount": total_ref_comm, "date": f"{current_month}-01", "added_by": username})
                    log_action(username, "Referral Commission Paid", f"${total_ref_comm:.2f} for {current_month}")
                    play_ding(); st.success(f"Referral commissions of ${total_ref_comm:,.2f} recorded as expense."); st.rerun()
                else: st.warning("Already recorded for this month.")
            else: st.info("No referral commissions to record this month.")
    else: st.info("No referrers added yet. Add them in Settings → Referrers.")

# ─────────────────────────────────────────────
# ACCOUNTS (BOSS ONLY)
# ─────────────────────────────────────────────
elif selected == "👥  Accounts":
    page_header("Accounts", "Manage user access and review full activity logs.")
    accounts = sb_all("users")
    st.metric("Total user accounts", len(accounts))
    at1,at2 = st.tabs(["Profiles & Access","Activity Log"])
    with at1:
        section_label("All accounts")
        if accounts:
            st.dataframe(pd.DataFrame([{"id": u["id"], "username": u["username"], "role": u["role"]} for u in accounts]), use_container_width=True, hide_index=True)
            st.markdown("---"); section_label("Remove account")
            st.warning("⚠️ Removing an account immediately revokes access.")
            killable = ["— select —"] + [u["username"] for u in accounts if u["username"] != username]
            target_del = st.selectbox("Select account to remove", killable, key="burn_user_select")
            if st.button("Delete Account", type="primary", key="btn_del_account"):
                if target_del != "— select —":
                    sb_delete("users", "username", target_del)
                    log_action(username, "Delete Account", f"Removed: {target_del}")
                    play_ding(); st.success(f"Account '{target_del}' removed."); st.rerun()
        else: st.info("No accounts found.")
    with at2:
        section_label("Audit log by user")
        pf = ["All"] + [u["username"] for u in accounts]
        chosen_user = st.selectbox("Filter by user", pf, key="acc_audit_user_filter")
        audit_r = sb_all("audit_log", order="id", desc_order=True, limit=400)
        if chosen_user != "All": audit_r = [r for r in audit_r if r.get("username") == chosen_user]
        if audit_r:
            st.dataframe(pd.DataFrame([{"Time": r["timestamp"],"User": r["username"],"Action": r["action"],"Details": r.get("details","")} for r in audit_r]), use_container_width=True, hide_index=True)
        else: st.info("No activity recorded yet.")

# ─────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────
elif selected == "⚙️  Settings":
    page_header("Settings", "Configure doctors, staff, services, bundles, referrers, and subscriptions.")
    s1,s2,s3,s4,s5,s6 = st.tabs(["Doctors","Staff & Payroll","Services","Bundles","🎯 Referrers","🔄 Subscriptions"])

    with s1:
        section_label("Add doctor")
        c1,c2 = st.columns(2)
        with c1:
            d_name = st.text_input("Doctor name"); d_spec = st.text_input("Specialty (e.g. Dermatology)")
        with c2:
            c_mode = st.selectbox("Commission model", ["Tiered (3% at 10+ visits, 5% at 20+)","Fixed percentage"])
            f_rate = 0.0; comm_type = "tiered"
            if c_mode == "Fixed percentage":
                comm_type = "fixed"; f_rate = st.number_input("Fixed rate (%)", min_value=0.0, max_value=100.0, value=50.0)
        if st.button("Add Doctor"):
            if d_name.strip():
                if sb_exists("doctors","name",d_name.strip()): st.error("A doctor with that name already exists.")
                else:
                    sb_insert("doctors",{"name":d_name.strip(),"specialty":d_spec.strip(),"comm_type":comm_type,"fixed_rate":f_rate})
                    log_action(username,"Add Doctor",f"{d_name.strip()} | {comm_type}")
                    play_ding(); st.success(f"Doctor '{d_name}' added."); st.rerun()
            else: st.error("Doctor name is required.")
        st.markdown("---"); section_label("Current doctors")
        all_docs = sb_all("doctors", order="name")
        if all_docs:
            st.dataframe(pd.DataFrame(all_docs), use_container_width=True, hide_index=True)
            del_doc = st.selectbox("Remove doctor", ["— select —"]+[d["name"] for d in all_docs])
            if st.button("Remove Doctor", type="primary"):
                if del_doc != "— select —":
                    sb_delete("doctors","name",del_doc); log_action(username,"Remove Doctor",del_doc)
                    play_ding(); st.success(f"Doctor '{del_doc}' removed."); st.rerun()
        else: st.info("No doctors added yet.")

    with s2:
        section_label("Add staff member")
        c1,c2,c3 = st.columns(3)
        with c1: emp_name   = st.text_input("Full name")
        with c2: emp_role   = st.text_input("Role / title")
        with c3: emp_salary = st.number_input("Monthly salary ($)", min_value=0.0, step=100.0)
        st.info("💡 Staff salaries are automatically recorded as an expense on the 1st of each month.")
        if st.button("Add Staff Member"):
            if emp_name.strip() and emp_role.strip():
                if sb_exists("employees","name",emp_name.strip()): st.error("An employee with that name already exists.")
                else:
                    sb_insert("employees",{"name":emp_name.strip(),"role":emp_role.strip(),"salary":emp_salary})
                    log_action(username,"Add Staff",f"{emp_name.strip()} | ${emp_salary}")
                    play_ding(); st.success(f"{emp_name} added to payroll."); st.rerun()
            else: st.error("Name and role are required.")
        st.markdown("---"); section_label("Current staff")
        all_emp = sb_all("employees", order="name")
        if all_emp:
            st.dataframe(pd.DataFrame(all_emp), use_container_width=True, hide_index=True)
            st.markdown(f"**Monthly payroll total: ${sum(float(e.get('salary') or 0) for e in all_emp):,.2f}**")
            del_emp = st.selectbox("Remove employee", ["— select —"]+[e["name"] for e in all_emp])
            if st.button("Remove Employee", type="primary"):
                if del_emp != "— select —":
                    sb_delete("employees","name",del_emp); log_action(username,"Remove Staff",del_emp)
                    play_ding(); st.success(f"Removed {del_emp} from payroll."); st.rerun()
        else: st.info("No staff added yet.")

    with s3:
        section_label("Add service")
        c1,c2,c3 = st.columns(3)
        with c1: s_name = st.text_input("Service name")
        with c2: s_cat  = st.selectbox("Category", ["General","Consultation","Procedure","Therapy","Diagnostic","Other"])
        with c3: s_price = st.number_input("Price ($)", min_value=0.0, step=10.0)
        if st.button("Add Service"):
            if s_name.strip():
                if sb_exists("services","name",s_name.strip()): st.error("A service with that name already exists.")
                else:
                    sb_insert("services",{"name":s_name.strip(),"category":s_cat,"price":s_price,"active":1})
                    log_action(username,"Add Service",f"{s_name.strip()} | ${s_price}")
                    play_ding(); st.success(f"Service '{s_name}' added at ${s_price:.2f}."); st.rerun()
            else: st.error("Service name is required.")
        st.markdown("---"); section_label("Current services")
        all_svc = sb_all("services", order="name")
        if all_svc:
            st.dataframe(pd.DataFrame(all_svc), use_container_width=True, hide_index=True)
            del_svc = st.selectbox("Remove service", ["— select —"]+[s["name"] for s in all_svc])
            if st.button("Remove Service", type="primary"):
                if del_svc != "— select —":
                    sb_delete("services","name",del_svc); log_action(username,"Remove Service",del_svc)
                    play_ding(); st.success(f"Service '{del_svc}' removed."); st.rerun()
        else: st.info("No services added yet.")

    with s4:
        section_label("Create bundle")
        c1,c2 = st.columns(2)
        with c1:
            b_name  = st.text_input("Bundle name (e.g. Premium Care Package)")
            b_price = st.number_input("Bundle price ($)", min_value=0.0, step=25.0)
        with c2: b_desc = st.text_area("Description / included services", height=90)
        if st.button("Create Bundle"):
            if b_name.strip() and b_price > 0:
                if sb_exists("bundles","name",b_name.strip()): st.error("A bundle with that name already exists.")
                else:
                    sb_insert("bundles",{"name":b_name.strip(),"price":b_price,"description":b_desc.strip()})
                    log_action(username,"Create Bundle",f"{b_name.strip()} | ${b_price}")
                    play_ding(); st.success(f"Bundle '{b_name}' created at ${b_price:.2f}."); st.rerun()
            else: st.error("Name and price are required.")
        st.markdown("---"); section_label("Current bundles")
        all_bundles = sb_all("bundles", order="name")
        if all_bundles:
            st.dataframe(pd.DataFrame(all_bundles), use_container_width=True, hide_index=True)
            del_bnd = st.selectbox("Remove bundle", ["— select —"]+[b["name"] for b in all_bundles])
            if st.button("Remove Bundle", type="primary"):
                if del_bnd != "— select —":
                    sb_delete("bundles","name",del_bnd); log_action(username,"Remove Bundle",del_bnd)
                    play_ding(); st.success(f"Bundle '{del_bnd}' removed."); st.rerun()
        else: st.info("No bundles created yet.")

    with s5:
        section_label("Add referrer / influencer")
        st.info("💡 Add anyone who promotes the clinic. When a patient comes via them, select their name at checkout. Commission is calculated monthly in Accounting.")
        c1,c2 = st.columns(2)
        with c1:
            ref_name  = st.text_input("Referrer full name", key="ref_name_input")
            ref_phone = st.text_input("Phone / contact",    key="ref_phone_input")
        with c2:
            ref_rate  = st.number_input("Commission rate (%)", min_value=0.0, max_value=100.0, step=1.0, value=10.0, key="ref_rate_input")
            ref_notes = st.text_area("Notes (platform, content type, etc.)", height=80, key="ref_notes_input")
        if st.button("Add Referrer", key="btn_add_referrer"):
            if ref_name.strip():
                if sb_exists("referrers","name",ref_name.strip()): st.error("A referrer with that name already exists.")
                else:
                    sb_insert("referrers",{"name":ref_name.strip(),"phone":ref_phone.strip(),"commission_rate":ref_rate,"notes":ref_notes.strip(),"added_by":username,"created_at":today_str})
                    log_action(username,"Add Referrer",f"{ref_name} at {ref_rate}%")
                    play_ding(); st.success(f"Referrer '{ref_name}' added with {ref_rate}% commission."); st.rerun()
            else: st.error("Name is required.")
        st.markdown("---"); section_label("Current referrers")
        all_refs = sb_all("referrers", order="name")
        if all_refs:
            st.dataframe(pd.DataFrame(all_refs), use_container_width=True, hide_index=True)
            del_ref = st.selectbox("Remove referrer", ["— select —"]+[r["name"] for r in all_refs], key="del_ref_select")
            if st.button("Remove Referrer", type="primary", key="btn_del_referrer"):
                if del_ref != "— select —":
                    sb_delete("referrers","name",del_ref); log_action(username,"Remove Referrer",del_ref)
                    play_ding(); st.success(f"Referrer '{del_ref}' removed."); st.rerun()
        else: st.info("No referrers added yet.")

    with s6:
        section_label("Add monthly subscription")
        st.info("💡 Add recurring monthly costs. They are automatically recorded as an expense each month.")
        c1,c2,c3 = st.columns(3)
        with c1:
            sub_name = st.text_input("Subscription name", key="sub_name_input")
            sub_cat  = st.selectbox("Category", ["Subscription","Marketing","Software","Utilities","Other"], key="sub_cat_select")
        with c2:
            sub_amount = st.number_input("Monthly amount ($)", min_value=0.0, step=5.0, key="sub_amount_input")
            sub_day    = st.number_input("Billing day of month", min_value=1, max_value=28, step=1, value=1, key="sub_day_input")
        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("Subscriptions auto-post as expenses on the billing day each month.")
        if st.button("Add Subscription", key="btn_add_subscription"):
            if sub_name.strip() and sub_amount > 0:
                if sb_exists("subscriptions","name",sub_name.strip()): st.error("A subscription with that name already exists.")
                else:
                    sb_insert("subscriptions",{"name":sub_name.strip(),"amount":sub_amount,"billing_day":int(sub_day),"category":sub_cat,"active":1,"added_by":username,"created_at":today_str})
                    log_action(username,"Add Subscription",f"{sub_name} ${sub_amount}/mo")
                    play_ding(); st.success(f"Subscription '{sub_name}' added at ${sub_amount:.2f}/month."); st.rerun()
            else: st.error("Name and amount are required.")
        st.markdown("---"); section_label("Active subscriptions")
        all_subs = sb_all("subscriptions", order="name")
        if all_subs:
            st.dataframe(pd.DataFrame(all_subs), use_container_width=True, hide_index=True)
            st.markdown(f"**Total active monthly: ${sum(float(s.get('amount') or 0) for s in all_subs if s.get('active') == 1):,.2f}/month**")
            c1,c2 = st.columns(2)
            with c1:
                toggle_sub = st.selectbox("Pause / activate", ["— select —"]+[s["name"] for s in all_subs], key="toggle_sub_select")
                if st.button("Toggle Active/Paused", key="btn_toggle_sub"):
                    if toggle_sub != "— select —":
                        cur = next((s.get("active",1) for s in all_subs if s["name"]==toggle_sub), 1)
                        sb_update("subscriptions",{"active": 0 if cur else 1},"name",toggle_sub)
                        log_action(username,"Toggle Subscription",f"{toggle_sub} → {'Paused' if cur else 'Active'}")
                        play_ding(); st.success(f"'{toggle_sub}' is now {'paused' if cur else 'active'}."); st.rerun()
            with c2:
                del_sub = st.selectbox("Remove subscription", ["— select —"]+[s["name"] for s in all_subs], key="del_sub_select")
                if st.button("Remove Subscription", type="primary", key="btn_del_subscription"):
                    if del_sub != "— select —":
                        sb_delete("subscriptions","name",del_sub); log_action(username,"Remove Subscription",del_sub)
                        play_ding(); st.success(f"Subscription '{del_sub}' removed."); st.rerun()
        else: st.info("No subscriptions added yet.")
