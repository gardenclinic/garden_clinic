import streamlit as st
import pandas as pd
import hashlib
import io
from datetime import datetime, date, timedelta
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(page_title="Garden Clinic", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════
# LUXURY DARK CINEMATIC THEME
# ═══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: #0A0E0C !important; color: #E8EDE9 !important; font-family: 'Inter', system-ui, sans-serif !important; }
.stApp::before { content: ''; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at top right, rgba(255,140,60,0.08), transparent 50%), radial-gradient(ellipse at bottom left, rgba(30,150,90,0.06), transparent 50%); pointer-events: none; z-index: 0; }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0F1311 0%, #0A0E0C 100%) !important; border-right: 1px solid rgba(255,255,255,0.05) !important; min-width: 240px !important; }
[data-testid="stSidebar"] * { color: #E8EDE9 !important; }
section[data-testid="stSidebarNav"] { display: none; }
h1, h2, h3, h4 { font-family: 'Cormorant Garamond', serif !important; letter-spacing: -0.01em !important; }
.hero-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 500; color: #FFF; font-style: italic; letter-spacing: -0.02em; margin: 0 0 4px 0; line-height: 1.1; }
.hero-sub { font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #8A9690; letter-spacing: 0.04em; font-weight: 400; }
.pulse-bar { background: linear-gradient(135deg, rgba(20,28,24,0.9) 0%, rgba(15,22,19,0.9) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); border-radius: 18px; padding: 20px 28px; display: flex; gap: 36px; flex-wrap: wrap; align-items: center; margin-bottom: 28px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.pulse-stat { display: flex; flex-direction: column; }
.pulse-label { font-size: 0.68rem; color: #FF8C3C; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; }
.pulse-value { font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 500; color: #FFFFFF; margin-top: 4px; letter-spacing: -0.02em; }
.pulse-divider { width: 1px; background: linear-gradient(180deg, transparent, rgba(255,255,255,0.15), transparent); height: 40px; align-self: center; }
.page-header { margin-bottom: 32px; padding-top: 8px; }
.page-header h1 { font-family: 'Cormorant Garamond', serif !important; font-size: 2.6rem !important; font-weight: 500 !important; color: #FFFFFF !important; margin: 0 0 6px 0 !important; font-style: italic; letter-spacing: -0.02em; }
.page-header p { font-size: 0.9rem; color: #8A9690; margin: 0; font-weight: 400; letter-spacing: 0.02em; }
.card { background: linear-gradient(135deg, rgba(20,28,24,0.7) 0%, rgba(15,22,19,0.7) 100%); backdrop-filter: blur(20px); border-radius: 16px; padding: 24px 26px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 18px; transition: all 0.3s; }
.card:hover { border-color: rgba(255,140,60,0.2); transform: translateY(-2px); box-shadow: 0 10px 40px rgba(0,0,0,0.4); }
.card h3 { font-family: 'Inter', sans-serif !important; margin: 0 0 6px 0; font-size: 0.7rem; color: #FF8C3C; font-weight: 500; text-transform: uppercase; letter-spacing: 0.12em; }
.card .big-num { font-family: 'JetBrains Mono', monospace; font-size: 1.9rem; font-weight: 500; margin: 0; letter-spacing: -0.02em; }
.card .big-num.green { color: #6FE6A4; }
.card .big-num.red { color: #FF7B7B; }
.card .big-num.dark, .card .big-num.gold { color: #F0E0C0; }
.card .sub { font-size: 0.78rem; color: #6A766F; margin-top: 6px; font-weight: 400; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 6px !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important; padding-bottom: 0 !important; }
.stTabs button[data-baseweb="tab"] { background: transparent !important; border: none !important; color: #6A766F !important; font-size: 0.85rem !important; font-weight: 500 !important; padding: 10px 18px 12px !important; border-radius: 0 !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0.02em !important; }
.stTabs button[data-baseweb="tab"]:hover { color: #E8EDE9 !important; }
.stTabs button[aria-selected="true"] { color: #FF8C3C !important; font-weight: 600 !important; border-bottom: 2px solid #FF8C3C !important; margin-bottom: -1px !important; }
.stButton > button { background: linear-gradient(135deg, #FF8C3C, #E67528) !important; color: #FFFFFF !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 11px 22px !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0.02em !important; transition: all 0.2s !important; box-shadow: 0 4px 14px rgba(255,140,60,0.25) !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(255,140,60,0.4) !important; }
button[data-testid="baseButton-primary"] { background: linear-gradient(135deg, #C0392B, #A93226) !important; box-shadow: 0 4px 14px rgba(192,57,43,0.25) !important; }
button[data-testid="baseButton-primary"]:hover { box-shadow: 0 8px 24px rgba(192,57,43,0.4) !important; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input { background: rgba(255,255,255,0.04) !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important; font-family: 'Inter', sans-serif !important; font-size: 0.9rem !important; color: #E8EDE9 !important; padding: 11px 14px !important; transition: border-color 0.2s !important; }
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus { border-color: #FF8C3C !important; }
.stSelectbox > div > div > div, .stMultiSelect > div > div > div { background: rgba(255,255,255,0.04) !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important; color: #E8EDE9 !important; }
.stTextArea textarea { background: rgba(255,255,255,0.04) !important; border-radius: 10px !important; border: 1px solid rgba(255,255,255,0.08) !important; font-family: 'Inter', sans-serif !important; color: #E8EDE9 !important; }
.stRadio > div { gap: 10px !important; }
.stRadio label { color: #E8EDE9 !important; }
[data-testid="stDataFrame"] { border-radius: 14px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.05) !important; background: rgba(20,28,24,0.5) !important; }
[data-testid="stDataFrame"] * { color: #E8EDE9 !important; }
.stSuccess > div { background: rgba(111,230,164,0.1) !important; border: 1px solid rgba(111,230,164,0.3) !important; color: #6FE6A4 !important; border-radius: 10px !important; }
.stError > div { background: rgba(255,123,123,0.1) !important; border: 1px solid rgba(255,123,123,0.3) !important; color: #FF7B7B !important; border-radius: 10px !important; }
.stWarning > div { background: rgba(255,140,60,0.1) !important; border: 1px solid rgba(255,140,60,0.3) !important; color: #FF8C3C !important; border-radius: 10px !important; }
.stInfo > div { background: rgba(108,140,180,0.1) !important; border: 1px solid rgba(108,140,180,0.3) !important; color: #A6BDD9 !important; border-radius: 10px !important; }
.section-label { font-family: 'Inter', sans-serif !important; font-size: 0.7rem; font-weight: 600; color: #FF8C3C; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 14px; border-bottom: 1px solid rgba(255,140,60,0.15); padding-bottom: 10px; }
.receipt-wrap { background: linear-gradient(180deg, #FFFFFF 0%, #FAF7F2 100%); border-radius: 22px; padding: 0; max-width: 440px; font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #1A2E23; box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.2); overflow: hidden; border: 1px solid rgba(255,255,255,0.1); }
.receipt-header { background: linear-gradient(135deg, #0A0E0C 0%, #1A2622 60%, #0A0E0C 100%); padding: 36px 28px 26px; text-align: center; position: relative; }
.receipt-header::after { content: ''; position: absolute; bottom: -1px; left: 0; right: 0; height: 24px; background: #FFFFFF; border-radius: 24px 24px 0 0; }
.receipt-clinic-name { font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; font-weight: 500; color: #FFFFFF; font-style: italic; letter-spacing: -0.01em; margin: 0; }
.receipt-clinic-sub { font-size: 0.7rem; color: #FF8C3C; letter-spacing: 0.25em; text-transform: uppercase; margin-top: 6px; font-weight: 500; }
.receipt-gold-line { width: 50px; height: 1px; background: linear-gradient(90deg, transparent, #C9A84C, transparent); margin: 12px auto; }
.receipt-body { padding: 12px 32px 32px; }
.receipt-date-badge { background: linear-gradient(135deg, #FAF7F2, #F0EDE6); border-radius: 10px; padding: 8px 14px; text-align: center; font-size: 0.72rem; color: #5A7A65; font-weight: 600; letter-spacing: 0.06em; margin-bottom: 22px; border: 1px solid #EEE8DC; }
.receipt-section-title { font-family: 'Inter', sans-serif; font-size: 0.62rem; font-weight: 700; color: #8B7A5A; text-transform: uppercase; letter-spacing: 0.15em; margin: 18px 0 10px; }
.receipt-row { display: flex; justify-content: space-between; align-items: center; margin: 8px 0; font-size: 0.88rem; }
.receipt-row span:first-child { color: #5A7A65; } .receipt-row span:last-child { color: #1A2E23; font-weight: 600; }
.receipt-divider { border: none; border-top: 1px solid #EEE8DC; margin: 16px 0; }
.receipt-total-box { background: linear-gradient(135deg, #0A0E0C, #1A2622); border-radius: 14px; padding: 16px 20px; margin: 18px 0; }
.receipt-total-label { font-size: 0.7rem; color: #FF8C3C; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; }
.receipt-total-amount { font-family: 'JetBrains Mono', monospace; font-size: 1.7rem; font-weight: 600; color: #FFFFFF; margin-top: 4px; }
.receipt-discount { color: #C0392B !important; }
.receipt-footer-area { text-align: center; padding-top: 8px; border-top: 1px solid #EEE8DC; margin-top: 20px; }
.receipt-footer-text { font-size: 0.72rem; color: #8B7A5A; margin: 4px 0; }
.receipt-footer-clinic { font-size: 0.75rem; color: #5A7A65; font-weight: 600; margin-top: 8px; }
.login-card { background: linear-gradient(135deg, rgba(20,28,24,0.7) 0%, rgba(15,22,19,0.7) 100%); backdrop-filter: blur(30px); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 50px 44px; max-width: 460px; margin: 80px auto 0; box-shadow: 0 30px 80px rgba(0,0,0,0.5); }
.login-card h1 { font-family: 'Cormorant Garamond', serif; color: #FFFFFF; text-align: center; margin: 0 0 8px; font-weight: 500; font-style: italic; font-size: 2.4rem; letter-spacing: -0.02em; }
.login-card p { text-align: center; color: #FF8C3C; font-size: 0.72rem; margin-bottom: 28px; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 500; }
.stForm [data-testid="stFormSubmitButton"] button { width: 100%; }
[data-testid="stMetric"] { background: linear-gradient(135deg, rgba(20,28,24,0.7) 0%, rgba(15,22,19,0.7) 100%); border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px 22px; backdrop-filter: blur(20px); }
[data-testid="stMetricLabel"] { font-size: 0.7rem !important; color: #FF8C3C !important; text-transform: uppercase; letter-spacing: 0.12em; font-weight: 600 !important; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.6rem !important; color: #FFFFFF !important; font-weight: 500 !important; }
.session-bar-wrap { background: rgba(255,255,255,0.06); border-radius: 10px; height: 12px; width: 100%; margin-top: 8px; overflow: hidden; }
.session-bar-fill { height: 12px; border-radius: 10px; background: linear-gradient(90deg, #FF8C3C, #FFB060); box-shadow: 0 0 20px rgba(255,140,60,0.4); }
.profile-summary { background: linear-gradient(135deg, #0A0E0C 0%, #1A2622 100%); color: #FFF; padding: 28px 32px; border-radius: 18px; margin-bottom: 22px; border: 1px solid rgba(255,140,60,0.15); position: relative; overflow: hidden; }
.profile-summary::after { content: ''; position: absolute; top: 0; right: 0; width: 200px; height: 200px; background: radial-gradient(circle, rgba(255,140,60,0.15), transparent 70%); }
.profile-name { font-family: 'Cormorant Garamond', serif; font-size: 1.8rem; font-weight: 500; font-style: italic; margin: 0; color: #FFF; letter-spacing: -0.02em; }
.profile-meta { font-size: 0.85rem; color: #8A9690; margin-top: 6px; letter-spacing: 0.02em; }
.stMarkdown a { color: #FF8C3C !important; }
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; margin: 24px 0 !important; }
.stCheckbox label { color: #E8EDE9 !important; }
label, .stRadio label span { color: #E8EDE9 !important; }
[data-baseweb="select"] * { color: #E8EDE9 !important; }
[data-testid="stWidgetLabel"] p { color: #B8C3BD !important; font-size: 0.82rem !important; font-weight: 500 !important; }
@media print { [data-testid="stSidebar"], .stTabs [data-baseweb="tab-list"], .stButton, .pulse-bar { display: none !important; } }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# CURRENCY (IQD)
# ═══════════════════════════════════════════════
def fmt(amount):
    try: return f"{int(round(float(amount or 0))):,} IQD"
    except: return "0 IQD"

# ═══════════════════════════════════════════════
# SUPABASE
# ═══════════════════════════════════════════════
@st.cache_resource
def get_sb(): return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def sb_all(table, filters=None, order=None, desc_order=False, limit=None):
    try:
        q = get_sb().table(table).select("*")
        if filters:
            for k, v in filters.items(): q = q.eq(k, v)
        if order: q = q.order(order, desc=desc_order)
        if limit: q = q.limit(limit)
        return q.execute().data or []
    except: return []

def sb_one(table, filters):
    r = sb_all(table, filters=filters); return r[0] if r else None
def sb_insert(table, data):
    try: get_sb().table(table).insert(data).execute(); return True
    except: return False
def sb_delete(table, col, val):
    try: get_sb().table(table).delete().eq(col, val).execute(); return True
    except: return False
def sb_update(table, data, col, val):
    try: get_sb().table(table).update(data).eq(col, val).execute(); return True
    except: return False
def sb_exists(table, col, val):
    try: return len(get_sb().table(table).select("id").eq(col, val).execute().data) > 0
    except: return False
def sb_sum(table, col, filters=None): return sum(float(r.get(col) or 0) for r in sb_all(table, filters=filters))
def sb_count(table, filters=None): return len(sb_all(table, filters=filters))

# ═══════════════════════════════════════════════
# JOIN HELPERS
# ═══════════════════════════════════════════════
def get_visits_joined(limit=100, patient_id=None, start=None, end=None):
    visits = sb_all("visits", order="id", desc_order=True, limit=limit)
    if patient_id: visits = [v for v in visits if v.get("patient_id") == patient_id]
    if start and end: visits = [v for v in visits if start <= v.get("visit_date","") <= end]
    if not visits: return []
    patients = {p["id"]: p["name"] for p in sb_all("patients")}
    doctors  = {d["id"]: d["name"] for d in sb_all("doctors")}
    services = {s["id"]: s["name"] for s in sb_all("services")}
    bundles  = {b["id"]: b["name"] for b in sb_all("bundles")}
    result = []
    for v in visits:
        svc = services.get(v.get("service_id"),""); bnd = bundles.get(v.get("bundle_id"),"")
        result.append({"id": v["id"], "Date": v.get("visit_date",""), "Patient": patients.get(v.get("patient_id"),""),
            "Doctor": doctors.get(v.get("doctor_id"),""), "Item": svc if svc else (f"📦 {bnd}" if bnd else "—"),
            "Base": float(v.get("base_price") or 0), "Discount": float(v.get("discount_amount") or 0),
            "Paid": float(v.get("net_paid") or 0), "Method": v.get("payment_method",""), "Notes": v.get("notes","")})
    return result

def get_appointments_joined():
    appts = sb_all("appointments", order="appt_date", desc_order=True)
    if not appts: return []
    patients = {p["id"]: p["name"] for p in sb_all("patients")}
    doctors  = {d["id"]: d["name"] for d in sb_all("doctors")}
    return [{"id": a["id"], "Date": a.get("appt_date",""), "Time": a.get("appt_time",""),
             "Patient": patients.get(a.get("patient_id"),""), "Doctor": doctors.get(a.get("doctor_id"),""),
             "Reason": a.get("reason",""), "Status": a.get("status","")} for a in appts]

def get_doc_commission_rate(doctor_id, visit_count, all_tiers):
    tiers = sorted([t for t in all_tiers if t.get("doctor_id") == doctor_id], key=lambda x: int(x.get("min_visits") or 0), reverse=True)
    for t in tiers:
        if visit_count >= int(t.get("min_visits") or 0): return float(t.get("commission_rate") or 0) / 100.0
    return 0.0

def get_financials(start=None, end=None):
    visits = sb_all("visits")
    if start and end: visits = [v for v in visits if start <= v.get("visit_date","") <= end]
    doctors = sb_all("doctors")
    expenses_rows = sb_all("expenses")
    if start and end: expenses_rows = [e for e in expenses_rows if start <= e.get("date","") <= end]
    all_tiers = sb_all("doctor_commission_tiers")
    gross = sum(float(v.get("net_paid") or 0) for v in visits)
    total_exp = sum(float(e.get("amount") or 0) for e in expenses_rows)
    doc_map = {}
    for v in visits:
        did = v.get("doctor_id")
        if did: doc_map.setdefault(did, []).append(float(v.get("net_paid") or 0))
    commissions = 0.0; doc_visits = {}
    for d in doctors:
        paid_list = doc_map.get(d["id"], [])
        doc_visits[d["name"]] = {"visits": paid_list, "id": d["id"]}
        rate = get_doc_commission_rate(d["id"], len(paid_list), all_tiers)
        commissions += sum(paid_list) * rate
    total_out = total_exp + commissions
    return gross, total_exp, commissions, total_out, gross - total_out, doc_visits

def hash_password(pw): return hashlib.sha256(pw.encode()).hexdigest()
def log_action(uname, action, details=""):
    sb_insert("audit_log", {"username": uname, "action": action, "details": details, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
def play_ding():
    components.html("""<script>try{var c=new(window.AudioContext||window.webkitAudioContext)(),o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.setValueAtTime(1100,c.currentTime);g.gain.setValueAtTime(0.18,c.currentTime);g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+0.45);o.connect(g);g.connect(c.destination);o.start();o.stop(c.currentTime+0.45);}catch(e){}</script>""", height=0, width=0)
def get_clinic_profile():
    rows = sb_all("clinic_profile")
    return rows[0] if rows else {"clinic_name": "Garden Clinic", "address": "", "phone": "", "email": "", "tagline": "Physical Therapy Center"}
def to_excel(df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w: df.to_excel(w, index=False, sheet_name="Data")
    return out.getvalue()
def card(title, value, css_class="dark", subtitle=""):
    return f'<div class="card"><h3>{title}</h3><p class="big-num {css_class}">{value}</p>{f"<p class=sub>{subtitle}</p>" if subtitle else ""}</div>'
def section_label(text): st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)
def pulse_bar(stats):
    items = ""
    for i, (label, value) in enumerate(stats):
        if i > 0: items += '<div class="pulse-divider"></div>'
        items += f'<div class="pulse-stat"><span class="pulse-label">{label}</span><span class="pulse-value">{value}</span></div>'
    st.markdown(f'<div class="pulse-bar">{items}</div>', unsafe_allow_html=True)
def page_header(title, desc=""): st.markdown(f'<div class="page-header"><h1>{title}</h1><p>{desc}</p></div>', unsafe_allow_html=True)

def render_receipt(r, cp):
    st.markdown(f"""<div class="receipt-wrap">
        <div class="receipt-header"><div class="receipt-clinic-name">{cp.get('clinic_name','Garden Clinic')}</div>
            <div class="receipt-gold-line"></div><div class="receipt-clinic-sub">{cp.get('tagline','Physical Therapy Center')}</div></div>
        <div class="receipt-body">
            <div class="receipt-date-badge">OFFICIAL RECEIPT &nbsp;·&nbsp; {r['date']} &nbsp;·&nbsp; {datetime.now().strftime('%H:%M')}</div>
            <div class="receipt-section-title">Patient Information</div>
            <div class="receipt-row"><span>Patient Name</span><span>{r['patient']}</span></div>
            <div class="receipt-row"><span>Treating Doctor</span><span>{r['doctor']}</span></div>
            <hr class="receipt-divider">
            <div class="receipt-section-title">Service Details</div>
            <div class="receipt-row"><span>Service</span><span>{r['item']}</span></div>
            <div class="receipt-row"><span>Payment Method</span><span>{r['method']}</span></div>
            <hr class="receipt-divider">
            <div class="receipt-section-title">Payment Summary</div>
            <div class="receipt-row"><span>Base Price</span><span>{fmt(r['base'])}</span></div>
            <div class="receipt-row"><span class="receipt-discount">Discount Applied</span><span class="receipt-discount">− {fmt(r['disc'])}</span></div>
            <div class="receipt-total-box"><div class="receipt-total-label">Total Paid</div><div class="receipt-total-amount">{fmt(r['net'])}</div></div>
            <div class="receipt-footer-area">
                {'<div class="receipt-footer-clinic">📍 ' + cp.get('address','') + '</div>' if cp.get('address') else ''}
                {'<div class="receipt-footer-clinic">📞 ' + cp.get('phone','') + '</div>' if cp.get('phone') else ''}
                {'<div class="receipt-footer-clinic">✉️ ' + cp.get('email','') + '</div>' if cp.get('email') else ''}
                <div class="receipt-footer-text" style="margin-top:12px;">Thank you for choosing {cp.get('clinic_name','Garden Clinic')}</div>
                <div class="receipt-footer-text">We wish you a speedy recovery 🌿</div></div></div></div>""", unsafe_allow_html=True)

def auto_payroll():
    month = datetime.now().strftime("%Y-%m"); tag = f"Monthly Payroll — {month}"
    if not sb_exists("expenses", "description", tag):
        total = sb_sum("employees", "salary")
        if total > 0: sb_insert("expenses", {"description": tag, "category": "Payroll", "amount": total, "date": f"{month}-01", "added_by": "System"})
auto_payroll()

def auto_subscriptions():
    month = datetime.now().strftime("%Y-%m")
    for sub in sb_all("subscriptions", filters={"active": 1}):
        tag = f"Subscription: {sub['name']} — {month}"
        if not sb_exists("expenses", "description", tag):
            day = int(sub.get("billing_day") or 1)
            sb_insert("expenses", {"description": tag, "category": "Subscription", "amount": float(sub["amount"]), "date": f"{month}-{day:02d}", "added_by": "System"})
auto_subscriptions()

gross_income, base_expenses, total_commissions, total_outflows, net_profit, doc_visits = get_financials()
today_str = date.today().isoformat()
tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
today_visits_rows = sb_all("visits", filters={"visit_date": today_str})
today_revenue = sum(float(v.get("net_paid") or 0) for v in today_visits_rows)
today_visits_count = len(today_visits_rows)
patient_count = sb_count("patients")

# ═══════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown('<div class="login-card"><h1>Garden Clinic</h1><p>Management System</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.3,1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        lt, rt = st.tabs(["Sign In", "Create Account"])
        with lt:
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.button("Sign In →", use_container_width=True):
                users = sb_all("users", filters={"username": u.strip()})
                match = [x for x in users if x.get("password_hash") == hash_password(p)]
                if match:
                    st.session_state.logged_in = True
                    st.session_state.username = match[0]["username"]
                    st.session_state.role = match[0]["role"]
                    st.session_state.linked_doctor_id = match[0].get("linked_doctor_id")
                    st.rerun()
                else: st.error("Invalid username or password.")
        with rt:
            ru = st.text_input("New username"); rp = st.text_input("New password", type="password")
            rs = st.selectbox("Role", ["Boss","Accounting","Reception","Reception & Accounting","Doctor"])
            linked_doc_id = None
            if rs == "Doctor":
                all_doc_acc = sb_all("doctors", order="name")
                if all_doc_acc:
                    doc_map_acc = {d["name"]: d["id"] for d in all_doc_acc}
                    chosen_doc_acc = st.selectbox("Link to which doctor?", list(doc_map_acc.keys()))
                    linked_doc_id = doc_map_acc[chosen_doc_acc]
                else: st.warning("⚠️ Please add doctors in Settings first before creating a Doctor account.")
            code = st.text_input("Admin code", type="password")
            if st.button("Create Account", use_container_width=True):
                if code != "1011": st.error("Invalid admin code.")
                elif rs == "Doctor" and not linked_doc_id: st.error("Please add and link a doctor.")
                elif ru and rp:
                    if sb_exists("users","username",ru.strip()): st.error("Username already taken.")
                    else:
                        sb_insert("users",{"username":ru.strip(),"password_hash":hash_password(rp),"role":rs,"linked_doctor_id":linked_doc_id})
                        log_action("System","Create Account",f"User: {ru.strip()} | Role: {rs}")
                        st.success("Account created.")
    st.stop()

role = st.session_state.get("role","")
username = st.session_state.get("username","")
linked_doctor_id = st.session_state.get("linked_doctor_id")

st.sidebar.markdown(f"""
<div style="padding:24px 18px 20px;border-bottom:1px solid rgba(255,255,255,0.06);">
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:500;font-style:italic;color:#FFFFFF;letter-spacing:-0.02em;">Garden Clinic</div>
    <div style="font-size:0.65rem;color:#FF8C3C;margin-top:4px;font-weight:500;letter-spacing:0.15em;text-transform:uppercase;">Management System</div>
</div>
<div style="padding:18px 18px;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:10px;">
    <div style="font-size:0.62rem;color:#FF8C3C;text-transform:uppercase;letter-spacing:0.12em;font-weight:600;">Signed in as</div>
    <div style="font-size:1rem;color:#FFFFFF;font-weight:600;margin-top:4px;font-family:'Cormorant Garamond',serif;font-style:italic;">{username}</div>
    <div style="font-size:0.68rem;background:rgba(255,140,60,0.15);color:#FF8C3C;display:inline-block;padding:3px 10px;border-radius:20px;margin-top:6px;font-weight:600;letter-spacing:0.05em;">{role}</div>
</div>""", unsafe_allow_html=True)

menu_map = {
    "Boss": ["📈  Dashboard","🖥️  Reception","📊  Accounting","📅  Appointments","📑  Reports","🔬  Research","👥  Accounts","⚙️  Settings"],
    "Reception & Accounting": ["🖥️  Reception","📊  Accounting","📅  Appointments","📑  Reports"],
    "Accounting": ["📊  Accounting","📑  Reports"],
    "Reception": ["🖥️  Reception","📅  Appointments"],
    "Doctor": ["🩺  Doctor Form"],
}
menus = menu_map.get(role, [])
selected = st.sidebar.radio("Navigation", menus, label_visibility="collapsed")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Sign Out", use_container_width=True):
    st.session_state.logged_in = False; st.rerun()

# ═══════════════════════════════════════════════
# DOCTOR FORM (Doctor role only)
# ═══════════════════════════════════════════════
if selected == "🩺  Doctor Form":
    page_header("Doctor Intake Form", "Fill out the assessment for your patient.")
    if not linked_doctor_id:
        st.error("No doctor linked to this account. Contact admin.")
        st.stop()
    doc_info = sb_one("doctors", filters={"id": linked_doctor_id})
    if doc_info:
        st.markdown(f'<div class="profile-summary"><h2 class="profile-name">Dr. {doc_info["name"]}</h2><div class="profile-meta">{doc_info.get("specialty","")} · Welcome back</div></div>', unsafe_allow_html=True)

    df_tabs = st.tabs(["✍️ New Assessment","📋 My Past Assessments"])
    with df_tabs[0]:
        section_label("Find patient")
        ds_search = st.text_input("🔍 Search patient by name or phone", key="doc_search")
        all_p_doc = sb_all("patients", order="name")
        if ds_search: all_p_doc = [p for p in all_p_doc if ds_search.lower() in (p.get("name","")).lower() or ds_search in (p.get("phone","") or "")]
        if all_p_doc:
            sel_pat_doc = st.selectbox("Select patient", ["— select —"]+[p["name"] for p in all_p_doc], key="doc_pat_sel")
            if sel_pat_doc != "— select —":
                pat_doc = next(p for p in all_p_doc if p["name"]==sel_pat_doc)
                pid_doc = pat_doc["id"]
                # Show patient info (read-only)
                st.markdown(f'<div class="card"><h3>Patient Info (from reception)</h3><p style="color:#E8EDE9;margin:8px 0 0 0;font-size:0.95rem;"><strong>{pat_doc["name"]}</strong> · 📞 {pat_doc.get("phone","—")} · 🎂 {pat_doc.get("date_of_birth","—")} · {pat_doc.get("gender","—")}</p>{f"<p style=color:#8A9690;font-size:0.85rem;margin-top:8px;>📝 {pat_doc.get('notes','')}</p>" if pat_doc.get("notes") else ""}</div>', unsafe_allow_html=True)
                # Show previous assessments by any doctor
                prev_forms = sb_all("doctor_intake_form", filters={"patient_id": pid_doc}, order="id", desc_order=True)
                if prev_forms:
                    section_label("Previous assessments")
                    for f in prev_forms[:3]:
                        st.markdown(f'<div class="card" style="padding:14px 18px;"><div style="font-size:0.72rem;color:#FF8C3C;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">{f.get("filled_date","")} · Outcome: {f.get("outcome","Pending")}</div><div style="font-size:0.9rem;color:#E8EDE9;margin-top:6px;"><strong>Problem:</strong> {f.get("problem","—")}</div><div style="font-size:0.85rem;color:#B8C3BD;margin-top:4px;"><strong>Plan:</strong> {f.get("treatment_plan","—")}</div><div style="font-size:0.82rem;color:#8A9690;margin-top:4px;">Sessions: {f.get("sessions_needed",0)} · {f.get("notes","")}</div></div>', unsafe_allow_html=True)

                st.markdown("---"); section_label("✍️ New assessment")
                c1, c2 = st.columns(2)
                with c1:
                    form_problem = st.text_area("Problem / Diagnosis", height=100, placeholder="What is wrong with the patient?", key="df_problem")
                    form_plan = st.text_area("Treatment Plan / Expected Outcome", height=100, placeholder="What treatment will you provide? What is the expected outcome?", key="df_plan")
                with c2:
                    form_sessions = st.number_input("Sessions Needed", min_value=1, max_value=200, step=1, value=10, key="df_sessions")
                    form_notes = st.text_area("Additional Notes (private)", height=100, placeholder="Any extra notes...", key="df_notes")
                    form_outcome = st.selectbox("Expected Outcome", ["Pending","Full Recovery Expected","Partial Recovery Expected","Long-term Management","Other"], key="df_outcome")

                if st.button("Submit Assessment", use_container_width=True, key="btn_submit_assessment"):
                    if form_problem.strip() and form_plan.strip():
                        sb_insert("doctor_intake_form", {"patient_id": pid_doc, "doctor_id": linked_doctor_id,
                            "problem": form_problem.strip(), "treatment_plan": form_plan.strip(),
                            "sessions_needed": int(form_sessions), "notes": form_notes.strip(),
                            "outcome": form_outcome, "filled_date": today_str, "filled_by": username})
                        # Also create/update session plan
                        existing_sess = sb_one("patient_sessions", filters={"patient_id": pid_doc})
                        if existing_sess:
                            sb_update("patient_sessions", {"total_sessions": int(form_sessions)}, "id", existing_sess["id"])
                        else:
                            sb_insert("patient_sessions", {"patient_id": pid_doc, "total_sessions": int(form_sessions),
                                "sessions_done": 0, "notes": form_problem.strip(), "added_by": username, "created_at": today_str})
                        log_action(username, "Doctor Assessment", f"Patient: {sel_pat_doc} | Sessions: {form_sessions}")
                        play_ding(); st.success("✅ Assessment submitted! Reception can now see it and check out the patient.")
                    else: st.error("Problem and Treatment Plan are required.")
        else: st.info("No patients found.")

    with df_tabs[1]:
        section_label("My past assessments")
        my_forms = sb_all("doctor_intake_form", filters={"doctor_id": linked_doctor_id}, order="id", desc_order=True, limit=200)
        if my_forms:
            patients_map_df = {p["id"]: p["name"] for p in sb_all("patients")}
            rows_df = [{"Date": f.get("filled_date",""), "Patient": patients_map_df.get(f.get("patient_id"),""),
                "Problem": f.get("problem",""), "Plan": f.get("treatment_plan",""), "Sessions": f.get("sessions_needed",0),
                "Outcome": f.get("outcome","Pending"), "Notes": f.get("notes","")} for f in my_forms]
            # Outcome update
            section_label("Update outcome after treatment")
            opts_outcome = {f"#{f['id']} · {patients_map_df.get(f.get('patient_id'),'')} · {f.get('filled_date','')}": f["id"] for f in my_forms}
            sel_outcome = st.selectbox("Select assessment", ["— select —"]+list(opts_outcome.keys()), key="upd_outcome_sel")
            if sel_outcome != "— select —":
                fid = opts_outcome[sel_outcome]
                new_out = st.selectbox("Final Outcome", ["Pending","Successfully Relieved","Partially Improved","No Improvement","Patient Discontinued","Other"], key="new_out_sel")
                final_notes = st.text_area("Final notes / observations", key="final_notes")
                if st.button("Update Outcome", key="btn_upd_outcome"):
                    sb_update("doctor_intake_form", {"outcome": new_out, "outcome_notes": final_notes}, "id", fid)
                    log_action(username, "Update Outcome", f"#{fid} → {new_out}")
                    play_ding(); st.success("Outcome updated!"); st.rerun()
            st.markdown("---")
            st.dataframe(pd.DataFrame(rows_df), use_container_width=True, hide_index=True)
        else: st.info("You haven't filled any assessments yet.")

# ═══════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════
elif selected == "📈  Dashboard":
    page_header("Executive Dashboard", f"{date.today().strftime('%A, %B %d %Y')}")
    pulse_bar([("Today's Revenue",fmt(today_revenue)),("Visits Today",str(today_visits_count)),("Total Patients",str(patient_count)),("All-Time Revenue",fmt(gross_income)),("Net Profit",fmt(net_profit))])

    all_pt_subs = sb_all("patient_subscriptions")
    expiring = [s for s in all_pt_subs if s.get("status")=="Active" and s.get("end_date") in [today_str, tomorrow_str]]
    if expiring:
        patients_map = {p["id"]: p["name"] for p in sb_all("patients")}
        for s in expiring:
            pname = patients_map.get(s.get("patient_id"),"Unknown")
            st.warning(f"⚠️ **{pname}** — subscription **'{s.get('plan_name','')}' expires {'TODAY' if s.get('end_date')==today_str else 'TOMORROW'}!**")

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(card("Gross Revenue", fmt(gross_income), "green", "All collected payments"), unsafe_allow_html=True)
    with c2: st.markdown(card("Total Expenses", fmt(total_outflows), "red", "Bills + payroll + commissions"), unsafe_allow_html=True)
    with c3: st.markdown(card("Net Profit", fmt(net_profit), "gold", "Revenue minus all costs"), unsafe_allow_html=True)
    with c4: st.markdown(card("Doctor Commissions", fmt(total_commissions), "gold", "Total owed to doctors"), unsafe_allow_html=True)

    st.markdown("---"); section_label("📅 Today's appointments")
    today_appts = [a for a in get_appointments_joined() if a.get("Date")==today_str]
    if today_appts:
        cols = st.columns(min(len(today_appts),4))
        for i, a in enumerate(today_appts[:4]):
            with cols[i%4]:
                sc = {"Scheduled":"#FF8C3C","Completed":"#6FE6A4","Cancelled":"#FF7B7B","No-show":"#6A766F"}.get(a["Status"],"#FF8C3C")
                st.markdown(f'<div class="card" style="border-left:3px solid {sc};"><div style="font-size:0.7rem;color:#8A9690;font-weight:600;letter-spacing:0.08em;">{a["Time"]}</div><div style="font-family:Cormorant Garamond,serif;font-size:1.2rem;font-style:italic;color:#FFF;margin:6px 0;">{a["Patient"]}</div><div style="font-size:0.8rem;color:#B8C3BD;">{a["Doctor"]}</div><div style="font-size:0.75rem;color:#8A9690;margin-top:4px;">{a.get("Reason","")}</div><span style="background:{sc}20;color:{sc};font-size:0.65rem;font-weight:700;padding:3px 10px;border-radius:20px;display:inline-block;margin-top:8px;letter-spacing:0.05em;">{a["Status"]}</span></div>', unsafe_allow_html=True)
    else: st.info("No appointments scheduled for today.")

    st.markdown("---")
    ca,cb = st.columns([3,2])
    with ca:
        section_label("Revenue trend")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df = pd.DataFrame([{"Date":v["visit_date"],"Revenue":float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df.groupby("Date").sum(), y="Revenue", color="#FF8C3C", height=240)
        else: st.info("No visit data yet.")
    with cb:
        section_label("Doctor performance")
        all_tiers = sb_all("doctor_commission_tiers"); rows = []
        for d in sb_all("doctors", order="name"):
            info = doc_visits.get(d["name"],{"visits":[],"id":d["id"]})
            v = info["visits"]; vol = len(v); gen = sum(v)
            rate = get_doc_commission_rate(d["id"], vol, all_tiers)
            payout = gen * rate
            tiers_for_doc = sorted([t for t in all_tiers if t.get("doctor_id")==d["id"]], key=lambda x:x.get("min_visits",0))
            model = " / ".join([f"{t['min_visits']}+: {t['commission_rate']}%" for t in tiers_for_doc]) if tiers_for_doc else "No tiers"
            rows.append({"Doctor":d["name"],"Visits":vol,"Revenue":fmt(gen),"Commission":fmt(payout),"Tiers":model})
        if rows: st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else: st.info("No doctors added yet.")

    st.markdown("---"); section_label("Monthly revenue summary")
    all_v2 = sb_all("visits")
    if all_v2:
        df_m = pd.DataFrame([{"Month":v["visit_date"][:7],"Revenue":float(v.get("net_paid") or 0)} for v in all_v2])
        df_m_agg = df_m.groupby("Month").agg(Revenue=("Revenue","sum"),Visits=("Revenue","count")).reset_index().sort_values("Month",ascending=False)
        df_m_agg["Revenue"] = df_m_agg["Revenue"].apply(fmt)
        st.dataframe(df_m_agg, use_container_width=True, hide_index=True)
    else: st.info("No visit data yet.")

    st.markdown("---"); section_label("Activity audit log")
    af = st.selectbox("Filter by action",["All","New Visit","New Patient","Doctor Assessment","Update Outcome","Add Expense","Delete Expense","Remove Patient"], key="audit_filter")
    audit_rows = sb_all("audit_log", order="id", desc_order=True, limit=200)
    if af != "All": audit_rows = [r for r in audit_rows if r.get("action")==af]
    if audit_rows:
        st.dataframe(pd.DataFrame([{"Time":r["timestamp"],"User":r["username"],"Action":r["action"],"Details":r.get("details","")} for r in audit_rows]), use_container_width=True, hide_index=True)
    else: st.info("No activity yet.")

# ═══════════════════════════════════════════════
# RECEPTION
# ═══════════════════════════════════════════════
elif selected == "🖥️  Reception":
    page_header("Reception Desk", "Patient management and checkout.")
    pulse_bar([("Today's Revenue",fmt(today_revenue)),("Visits Today",str(today_visits_count)),("Total Patients",str(patient_count))])

    all_pt_subs = sb_all("patient_subscriptions")
    expiring_rec = [s for s in all_pt_subs if s.get("status")=="Active" and s.get("end_date") in [today_str, tomorrow_str]]
    if expiring_rec:
        patients_map_r = {p["id"]: p["name"] for p in sb_all("patients")}
        for s in expiring_rec:
            pname = patients_map_r.get(s.get("patient_id"),"Unknown")
            st.warning(f"⚠️ **{pname}** subscription **'{s.get('plan_name','')}'** expires {'TODAY' if s.get('end_date')==today_str else 'TOMORROW'}!")

    t1,t2,tD,tQ,t3,t4,t5,t6,t7,t8,t9 = st.tabs(["Checkout","Patient Records","🩺 Doctor Forms","👤 Quick View","Add Patient","Edit Patient","Sessions","Subscriptions","🏋️ Gym Check-in","Visit History","Delete/Edit Visit"])

    # ── CHECKOUT ──
    with t1:
        section_label("New checkout")
        patients_db = sb_all("patients", order="name"); docs_db = sb_all("doctors", order="name")
        services_db = [s for s in sb_all("services", order="name") if s.get("active")==1]
        bundles_db  = sb_all("bundles", order="name")
        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please add doctors and services in Settings before processing checkouts.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}; d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1:
                target_p = st.selectbox("Patient", ["— select —"]+list(p_map.keys()))
                chosen_doc = st.selectbox("Doctor", list(d_map.keys()))
                payment_method = st.selectbox("Payment method", ["Cash","Card","Insurance","Transfer"])
            with c2:
                item_type = st.radio("Item type", ["Service","Bundle"], horizontal=True)
                srv_id = bnd_id = None; base_price = 0.0; chosen_item_name = ""
                if item_type == "Service":
                    if services_db:
                        s_map = {f"{s['name']}  —  {fmt(s['price'])}": (s["id"],float(s["price"]),s["name"]) for s in services_db}
                        chosen = st.selectbox("Service", list(s_map.keys()))
                        srv_id, base_price, chosen_item_name = s_map[chosen]
                else:
                    if bundles_db:
                        b_map = {f"{b['name']}  —  {fmt(b['price'])}": (b["id"],float(b["price"]),b["name"]) for b in bundles_db}
                        chosen = st.selectbox("Bundle", list(b_map.keys()))
                        bnd_id, base_price, chosen_item_name = b_map[chosen]
                disc_type = st.radio("Discount", ["None","Fixed (IQD)","Percent (%)"], horizontal=True)
                disc_val  = st.number_input("Discount value", min_value=0.0, step=1000.0)

            # Show doctor's assessment for this patient if exists
            if target_p != "— select —":
                pid_chk = p_map[target_p]
                assessment = sb_one("doctor_intake_form", filters={"patient_id": pid_chk})
                sess_chk = sb_one("patient_sessions", filters={"patient_id": pid_chk})
                if assessment:
                    rem = max(0, int(sess_chk.get("total_sessions",0) or 0) - int(sess_chk.get("sessions_done",0) or 0)) if sess_chk else "—"
                    st.info(f"🩺 **Doctor's plan:** {assessment.get('problem','')} · Sessions: {sess_chk.get('sessions_done',0) if sess_chk else 0}/{assessment.get('sessions_needed',0)} (Remaining: {rem})")

            final_due = base_price
            if disc_type == "Fixed (IQD)": final_due = max(0.0, base_price-disc_val)
            elif disc_type == "Percent (%)": final_due = max(0.0, base_price*(1-disc_val/100))
            visit_notes = st.text_area("Visit notes (optional)", height=70)
            referrers_db = sb_all("referrers", order="name"); ref_names = [r["name"] for r in referrers_db]
            referral_options = ["Walk-in / Direct","Instagram / Social Media","Google Search","Friend / Word of mouth"]+ref_names
            how_found = st.selectbox("How did the patient find us?", referral_options)
            referred_by_val = how_found if how_found in ref_names else None
            st.markdown(f"### Total due: **{fmt(final_due)}**")
            if st.button("Save & Print Receipt", use_container_width=True):
                if target_p == "— select —": st.error("Please select a patient.")
                elif base_price == 0.0: st.error("Please select a service or bundle.")
                else:
                    disc_amt = base_price - final_due
                    sb_insert("visits",{"patient_id":p_map[target_p],"doctor_id":d_map[chosen_doc],"service_id":srv_id,"bundle_id":bnd_id,"visit_date":today_str,"base_price":base_price,"discount_amount":disc_amt,"net_paid":final_due,"payment_method":payment_method,"notes":visit_notes,"referred_by":referred_by_val,"added_by":username})
                    todays_appts = sb_all("appointments", filters={"patient_id": p_map[target_p], "appt_date": today_str, "status": "Scheduled"})
                    for ap in todays_appts: sb_update("appointments", {"status": "Completed"}, "id", ap["id"])
                    sess = sb_one("patient_sessions", filters={"patient_id": p_map[target_p]})
                    if sess:
                        new_done = int(sess.get("sessions_done") or 0) + 1
                        sb_update("patient_sessions", {"sessions_done": new_done}, "id", sess["id"])
                        total_s = int(sess.get("total_sessions") or 0)
                        if total_s > 0 and new_done >= total_s:
                            st.balloons(); st.success(f"🎉 {target_p} has completed all {total_s} sessions!")
                    log_action(username,"New Visit",f"Patient: {target_p} | Doctor: {chosen_doc} | Paid: {fmt(final_due)}")
                    play_ding(); st.success("Visit saved.")
                    st.session_state.rcpt = {"patient":target_p,"doctor":chosen_doc,"item":chosen_item_name,"base":base_price,"disc":disc_amt,"net":final_due,"method":payment_method,"date":today_str}
            if "rcpt" in st.session_state: render_receipt(st.session_state.rcpt, get_clinic_profile())

    # ── PATIENT RECORDS ──
    with t2:
        section_label("All patients")
        search = st.text_input("🔍 Search by name or phone", key="t2_search")
        all_p = sb_all("patients", order="name")
        if search: all_p = [p for p in all_p if search.lower() in (p.get("name","")).lower() or search in (p.get("phone","") or "")]
        if all_p:
            st.dataframe(pd.DataFrame(all_p), use_container_width=True, hide_index=True)
            st.markdown("---"); section_label("Remove patient")
            del_target = st.selectbox("Select patient", ["— select —"]+[p["name"] for p in all_p])
            if st.button("Remove Patient", type="primary"):
                if del_target != "— select —":
                    sb_delete("patients","name",del_target); log_action(username,"Remove Patient",del_target)
                    play_ding(); st.success(f"Removed."); st.rerun()
        else: st.info("No patients found.")

    # ── DOCTOR FORMS (READ-ONLY for reception) ──
    with tD:
        section_label("🩺 Doctor assessments — what the doctor wrote")
        st.info("💡 See what the doctor recommended after examining the patient.")
        df_search = st.text_input("🔍 Search by patient name", key="recep_df_search")
        all_forms = sb_all("doctor_intake_form", order="id", desc_order=True)
        patients_map_df = {p["id"]: p["name"] for p in sb_all("patients")}
        doctors_map_df = {d["id"]: d["name"] for d in sb_all("doctors")}
        if df_search:
            all_forms = [f for f in all_forms if df_search.lower() in (patients_map_df.get(f.get("patient_id"),"")).lower()]
        if all_forms:
            for f in all_forms[:20]:
                pname = patients_map_df.get(f.get("patient_id"),"")
                dname = doctors_map_df.get(f.get("doctor_id"),"")
                sess_f = sb_one("patient_sessions", filters={"patient_id": f.get("patient_id")})
                rem_text = ""
                if sess_f:
                    done_f = int(sess_f.get("sessions_done") or 0); total_f = int(sess_f.get("total_sessions") or 0)
                    rem_text = f" · Sessions: {done_f}/{total_f}"
                st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-family:Cormorant Garamond,serif;font-size:1.3rem;font-style:italic;color:#FFF;">{pname}</div><span style="font-size:0.7rem;background:rgba(255,140,60,0.15);color:#FF8C3C;padding:3px 10px;border-radius:20px;font-weight:600;">{f.get("outcome","Pending")}</span></div><div style="font-size:0.78rem;color:#8A9690;margin-top:4px;">Dr. {dname} · {f.get("filled_date","")}{rem_text}</div><div style="margin-top:10px;font-size:0.88rem;color:#E8EDE9;"><strong style="color:#FF8C3C;">Problem:</strong> {f.get("problem","—")}</div><div style="margin-top:6px;font-size:0.88rem;color:#E8EDE9;"><strong style="color:#FF8C3C;">Treatment Plan:</strong> {f.get("treatment_plan","—")}</div><div style="margin-top:6px;font-size:0.85rem;color:#B8C3BD;">Sessions Needed: {f.get("sessions_needed",0)}{" · " + f.get("notes","") if f.get("notes") else ""}</div></div>', unsafe_allow_html=True)
        else: st.info("No doctor assessments yet.")

    # ── QUICK VIEW ──
    with tQ:
        section_label("👤 Patient quick view")
        all_p_qv = sb_all("patients", order="name")
        if all_p_qv:
            qv_search = st.text_input("🔍 Search patient", key="qv_search")
            filtered = [p for p in all_p_qv if not qv_search or qv_search.lower() in (p.get("name","")).lower() or qv_search in (p.get("phone","") or "")]
            if filtered:
                qv_sel = st.selectbox("Select patient", [p["name"] for p in filtered], key="qv_sel")
                pat = next(p for p in filtered if p["name"]==qv_sel); pid = pat["id"]
                st.markdown(f'<div class="profile-summary"><h2 class="profile-name">{pat["name"]}</h2><div class="profile-meta">📞 {pat.get("phone","—")} · 🎂 {pat.get("date_of_birth","—")} · {pat.get("gender","—")}</div></div>', unsafe_allow_html=True)
                visits_p = get_visits_joined(limit=1000, patient_id=pid)
                total_spent = sum(v["Paid"] for v in visits_p)
                last_visit = visits_p[0]["Date"] if visits_p else "Never"
                sess_p = sb_one("patient_sessions", filters={"patient_id": pid})
                next_appt = next((a for a in get_appointments_joined() if a.get("Patient")==qv_sel and a.get("Status")=="Scheduled" and a.get("Date") >= today_str), None)
                sub_active = next((s for s in sb_all("patient_subscriptions", filters={"patient_id":pid, "status":"Active"})), None)
                m1,m2,m3,m4 = st.columns(4)
                m1.metric("Total Visits", len(visits_p))
                m2.metric("Total Spent", fmt(total_spent))
                m3.metric("Last Visit", last_visit)
                m4.metric("Next Appointment", next_appt["Date"] if next_appt else "—")
                # Doctor assessment
                assessment_q = sb_one("doctor_intake_form", filters={"patient_id": pid})
                if assessment_q:
                    section_label("Doctor's assessment")
                    st.markdown(f'<div class="card"><div style="font-size:0.88rem;color:#E8EDE9;"><strong style="color:#FF8C3C;">Problem:</strong> {assessment_q.get("problem","")}</div><div style="margin-top:8px;font-size:0.88rem;color:#E8EDE9;"><strong style="color:#FF8C3C;">Plan:</strong> {assessment_q.get("treatment_plan","")}</div><div style="margin-top:8px;font-size:0.85rem;color:#B8C3BD;">Outcome: {assessment_q.get("outcome","Pending")}</div></div>', unsafe_allow_html=True)
                if sess_p:
                    done = int(sess_p.get("sessions_done") or 0); total = int(sess_p.get("total_sessions") or 0)
                    rem = max(0, total-done); pct = int((done/total*100)) if total>0 else 0
                    section_label("Sessions progress")
                    st.markdown(f'**{done} of {total} done** · {rem} remaining')
                    st.markdown(f'<div class="session-bar-wrap"><div class="session-bar-fill" style="width:{pct}%;"></div></div>', unsafe_allow_html=True)
                if sub_active:
                    section_label("Active subscription")
                    st.info(f"📅 **{sub_active.get('plan_name','')}** · Expires {sub_active.get('end_date','')} · {sub_active.get('sessions_used',0)}/{sub_active.get('total_sessions','∞')} sessions")
                if visits_p:
                    section_label("Recent visits")
                    df_v_qv = pd.DataFrame(visits_p[:10])
                    for col in ["Base","Discount","Paid"]:
                        if col in df_v_qv.columns: df_v_qv[col] = df_v_qv[col].apply(fmt)
                    st.dataframe(df_v_qv, use_container_width=True, hide_index=True)
        else: st.info("No patients registered yet.")

    # ── ADD PATIENT ──
    with t3:
        section_label("Register new patient")
        c1,c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Full name *"); p_phone = st.text_input("Phone number")
            p_dob  = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1990-01-15")
        with c2:
            p_gender = st.selectbox("Gender", ["Prefer not to say","Male","Female","Other"])
            p_notes  = st.text_area("Notes / background", height=100)
        give_receipt = st.checkbox("📄 Print intake receipt (patient takes this to doctor)", value=True)
        if st.button("Register Patient"):
            if p_name.strip():
                if sb_exists("patients","name",p_name.strip()): st.error("Patient already exists.")
                else:
                    sb_insert("patients",{"name":p_name.strip(),"phone":p_phone.strip(),"date_of_birth":p_dob.strip(),"gender":p_gender,"notes":p_notes.strip(),"created_at":today_str})
                    log_action(username,"New Patient",f"{p_name.strip()} | {p_gender}")
                    play_ding(); st.success(f"Patient '{p_name}' registered.")
                    if give_receipt:
                        st.session_state.intake_rcpt = {"patient":p_name.strip(),"doctor":"To be assigned","item":"Initial Intake","base":0,"disc":0,"net":0,"method":"—","date":today_str}
            else: st.error("Name is required.")
        if "intake_rcpt" in st.session_state: render_receipt(st.session_state.intake_rcpt, get_clinic_profile())

    # ── EDIT PATIENT ──
    with t4:
        section_label("Edit patient profile")
        ep_search = st.text_input("🔍 Search", key="ep_search")
        all_p_edit = sb_all("patients", order="name")
        if ep_search: all_p_edit = [p for p in all_p_edit if ep_search.lower() in (p.get("name","")).lower()]
        if all_p_edit:
            edit_p_name = st.selectbox("Select", ["— select —"]+[p["name"] for p in all_p_edit], key="edit_p_sel")
            if edit_p_name != "— select —":
                pat = next(p for p in all_p_edit if p["name"]==edit_p_name)
                c1,c2 = st.columns(2)
                with c1:
                    new_name = st.text_input("Full name", value=pat.get("name",""), key="ep_name")
                    new_phone = st.text_input("Phone", value=pat.get("phone","") or "", key="ep_phone")
                    new_dob = st.text_input("DOB", value=pat.get("date_of_birth","") or "", key="ep_dob")
                with c2:
                    gopts = ["Prefer not to say","Male","Female","Other"]
                    cg = pat.get("gender","Prefer not to say") or "Prefer not to say"
                    new_gender = st.selectbox("Gender", gopts, index=gopts.index(cg) if cg in gopts else 0, key="ep_gender")
                    new_notes = st.text_area("Notes", value=pat.get("notes","") or "", height=100, key="ep_notes")
                if st.button("Save Changes", key="btn_edit_patient"):
                    sb_update("patients",{"name":new_name.strip(),"phone":new_phone.strip(),"date_of_birth":new_dob.strip(),"gender":new_gender,"notes":new_notes.strip()},"id",pat["id"])
                    log_action(username,"Edit Patient",f"Updated: {edit_p_name} → {new_name.strip()}")
                    play_ding(); st.success("Updated!"); st.rerun()
        else: st.info("No patients found.")

    # ── SESSIONS ──
    with t5:
        section_label("Patient session tracker")
        s_search = st.text_input("🔍 Search", key="sess_search")
        all_p_sess = sb_all("patients", order="name")
        if s_search: all_p_sess = [p for p in all_p_sess if s_search.lower() in (p.get("name","")).lower()]
        if all_p_sess:
            sel_p_sess = st.selectbox("Select", ["— select —"]+[p["name"] for p in all_p_sess], key="sess_p_sel")
            if sel_p_sess != "— select —":
                pid = next(p["id"] for p in all_p_sess if p["name"]==sel_p_sess)
                sess = sb_one("patient_sessions", filters={"patient_id": pid})
                if sess:
                    done = int(sess.get("sessions_done") or 0); total = int(sess.get("total_sessions") or 0)
                    rem = max(0, total-done); pct = int((done/total*100)) if total>0 else 0
                    cc1,cc2,cc3 = st.columns(3)
                    cc1.metric("Total Sessions", total); cc2.metric("Sessions Done", done); cc3.metric("Remaining", rem)
                    st.markdown(f'<div class="session-bar-wrap"><div class="session-bar-fill" style="width:{pct}%;"></div></div>', unsafe_allow_html=True)
                    if rem == 0 and total > 0: st.success(f"🎉 {sel_p_sess} has completed all {total} sessions!")
                    st.markdown("---"); section_label("Update")
                    c1,c2 = st.columns(2)
                    with c1:
                        new_total = st.number_input("Total sessions", min_value=0, step=1, value=total, key="sess_total")
                        new_done = st.number_input("Sessions done", min_value=0, step=1, value=done, key="sess_done")
                    with c2:
                        new_sess_notes = st.text_area("Notes", value=sess.get("notes","") or "", height=80, key="sess_notes")
                    if st.button("Update Session Plan", key="btn_update_sess"):
                        sb_update("patient_sessions",{"total_sessions":new_total,"sessions_done":new_done,"notes":new_sess_notes},"id",sess["id"])
                        play_ding(); st.success("Updated!"); st.rerun()
                    if st.button("Remove Session Plan", type="primary", key="btn_del_sess"):
                        sb_delete("patient_sessions","id",sess["id"]); st.rerun()
                else:
                    st.info(f"No session plan for {sel_p_sess}."); section_label("Create plan")
                    c1,c2 = st.columns(2)
                    with c1: new_total_s = st.number_input("Total sessions", min_value=1, step=1, value=10, key="new_sess_total")
                    with c2: new_sess_n = st.text_area("Notes", height=80, key="new_sess_notes")
                    if st.button("Create Session Plan", key="btn_create_sess"):
                        sb_insert("patient_sessions",{"patient_id":pid,"total_sessions":new_total_s,"sessions_done":0,"notes":new_sess_n,"added_by":username,"created_at":today_str})
                        play_ding(); st.success(f"Created!"); st.rerun()
        else: st.info("No patients found.")

    # ── SUBSCRIPTIONS ──
    with t6:
        section_label("Patient subscriptions")
        all_p_sub = sb_all("patients", order="name")
        if all_p_sub:
            sub_tabs = st.tabs(["Create","View & Manage"])
            with sub_tabs[0]:
                p_map_sub = {p["name"]: p["id"] for p in all_p_sub}
                c1,c2 = st.columns(2)
                with c1:
                    sub_patient = st.selectbox("Patient", list(p_map_sub.keys()), key="sub_pat_sel")
                    sub_plan = st.text_input("Plan name", key="sub_plan_name")
                    sub_type = st.selectbox("Type", ["Monthly","Weekly","Custom (days)"], key="sub_plan_type")
                with c2:
                    sub_price = st.number_input("Price (IQD)", min_value=0.0, step=5000.0, key="sub_price")
                    sub_sessions = st.number_input("Sessions included (0 = unlimited)", min_value=0, step=1, value=0, key="sub_sessions")
                    sub_start = st.date_input("Start date", value=date.today(), key="sub_start")
                    if sub_type == "Monthly": sub_end = sub_start + timedelta(days=30)
                    elif sub_type == "Weekly": sub_end = sub_start + timedelta(days=7)
                    else:
                        sub_days = st.number_input("Days", min_value=1, step=1, value=30, key="sub_days")
                        sub_end = sub_start + timedelta(days=int(sub_days))
                    st.info(f"Expires: **{sub_end}**")
                if st.button("Create Subscription & Print Receipt", key="btn_create_sub"):
                    if sub_plan.strip() and sub_price > 0:
                        sb_insert("patient_subscriptions",{"patient_id":p_map_sub[sub_patient],"plan_name":sub_plan.strip(),"plan_type":sub_type,"total_sessions":int(sub_sessions),"sessions_used":0,"price":sub_price,"start_date":str(sub_start),"end_date":str(sub_end),"status":"Active","added_by":username,"created_at":today_str})
                        docs_for_sub = sb_all("doctors", order="name")
                        doc_id_sub = docs_for_sub[0]["id"] if docs_for_sub else None
                        if doc_id_sub:
                            sb_insert("visits",{"patient_id":p_map_sub[sub_patient],"doctor_id":doc_id_sub,"service_id":None,"bundle_id":None,"visit_date":today_str,"base_price":sub_price,"discount_amount":0,"net_paid":sub_price,"payment_method":"Subscription","notes":f"Subscription: {sub_plan.strip()}","referred_by":None,"added_by":username})
                        log_action(username,"Create Subscription",f"{sub_patient} | {sub_plan} | {fmt(sub_price)}")
                        play_ding(); st.success(f"Subscription created!")
                        st.session_state.sub_rcpt = {"patient":sub_patient,"item":sub_plan,"base":sub_price,"disc":0.0,"net":sub_price,"method":"Subscription","date":today_str,"doctor":"—"}
                if "sub_rcpt" in st.session_state: render_receipt(st.session_state.sub_rcpt, get_clinic_profile())
            with sub_tabs[1]:
                sm_search = st.text_input("🔍 Search", key="sm_search")
                all_subs_pt = sb_all("patient_subscriptions", order="end_date")
                pmap2 = {p["id"]: p["name"] for p in all_p_sub}
                if sm_search: all_subs_pt = [s for s in all_subs_pt if sm_search.lower() in (pmap2.get(s.get("patient_id"),"")).lower()]
                if all_subs_pt:
                    rows_sub = []
                    for s in all_subs_pt:
                        pname = pmap2.get(s.get("patient_id"),"")
                        total_s = int(s.get("total_sessions") or 0); used_s = int(s.get("sessions_used") or 0)
                        rem_s = (total_s - used_s) if total_s>0 else "∞"
                        rows_sub.append({"Patient":pname,"Plan":s.get("plan_name",""),"Type":s.get("plan_type",""),"Price":fmt(s.get("price")),"Sessions":f"{used_s}/{total_s if total_s>0 else '∞'}","Remaining":rem_s,"Start":s.get("start_date",""),"Expires":s.get("end_date",""),"Status":s.get("status",""),"id":s["id"]})
                    st.dataframe(pd.DataFrame(rows_sub).drop(columns=["id"]), use_container_width=True, hide_index=True)
                    sub_opts = {f"{r['Patient']} — {r['Plan']} (exp {r['Expires']})": r["id"] for r in rows_sub}
                    chosen_sub = st.selectbox("Select", ["— select —"]+list(sub_opts.keys()), key="manage_sub_sel")
                    if chosen_sub != "— select —":
                        sid = sub_opts[chosen_sub]
                        c1,c2,c3 = st.columns(3)
                        with c1: new_sub_status = st.selectbox("Status",["Active","Expired","Cancelled"], key="sub_status_sel")
                        with c2: new_sub_end = st.text_input("Extend end date", key="sub_end_edit")
                        with c3: new_total_sub = st.number_input("Update total", min_value=0, step=1, key="sub_total_edit")
                        if st.button("Update", key="btn_upd_sub"):
                            upd = {"status": new_sub_status}
                            if new_sub_end.strip(): upd["end_date"] = new_sub_end.strip()
                            if new_total_sub > 0: upd["total_sessions"] = new_total_sub
                            sb_update("patient_subscriptions", upd, "id", sid)
                            play_ding(); st.success("Updated!"); st.rerun()
                        if st.button("Delete", type="primary", key="btn_del_sub"):
                            sb_delete("patient_subscriptions","id",sid); st.rerun()
                else: st.info("No subscriptions yet.")
        else: st.info("No patients yet.")

    # ── GYM CHECK-IN ──
    with t7:
        section_label("🏋️ Gym check-in")
        all_p_checkin = sb_all("patients", order="name")
        active_subs_map = {}
        for s in sb_all("patient_subscriptions", filters={"status":"Active"}):
            active_subs_map.setdefault(s["patient_id"], []).append(s)
        patients_with_sub = [p for p in all_p_checkin if p["id"] in active_subs_map]
        if patients_with_sub:
            ci_search = st.text_input("🔍 Search", key="ci_search")
            filtered_ci = [p for p in patients_with_sub if not ci_search or ci_search.lower() in (p.get("name","")).lower()]
            ci_patient = st.selectbox("Select", ["— select —"]+[p["name"] for p in filtered_ci], key="checkin_sel")
            if ci_patient != "— select —":
                pid_ci = next(p["id"] for p in filtered_ci if p["name"]==ci_patient)
                subs_for_pat = active_subs_map[pid_ci]
                for s in subs_for_pat:
                    total_s = int(s.get("total_sessions") or 0); used_s = int(s.get("sessions_used") or 0)
                    rem_s = (total_s - used_s) if total_s>0 else "∞"
                    st.markdown(f'<div class="card" style="border-left:3px solid #FF8C3C;"><strong>{s.get("plan_name","")}</strong> · Expires {s.get("end_date","")} · {used_s}/{total_s if total_s>0 else "∞"} · Remaining: {rem_s}</div>', unsafe_allow_html=True)
                if st.button(f"✅ Check In {ci_patient}", use_container_width=True, key="btn_checkin"):
                    sub_to_use = subs_for_pat[0]
                    new_used = int(sub_to_use.get("sessions_used") or 0) + 1
                    sb_update("patient_subscriptions",{"sessions_used":new_used},"id",sub_to_use["id"])
                    sb_insert("gym_checkins",{"subscription_id":sub_to_use["id"],"patient_id":pid_ci,"checkin_date":today_str,"added_by":username})
                    log_action(username,"Gym Check-in",f"{ci_patient}")
                    play_ding(); st.success(f"✅ Checked in!")
        else: st.info("No patients with active subscriptions.")

    # ── VISIT HISTORY ──
    with t8:
        section_label("Patient visit history")
        vh_search = st.text_input("🔍 Search", key="vh_search")
        patients_all = sb_all("patients", order="name")
        if vh_search: patients_all = [p for p in patients_all if vh_search.lower() in (p.get("name","")).lower()]
        if patients_all:
            lookup_p = st.selectbox("Select", ["— select —"]+[p["name"] for p in patients_all])
            if lookup_p != "— select —":
                pid = next(p["id"] for p in patients_all if p["name"]==lookup_p)
                hist = get_visits_joined(limit=500, patient_id=pid)
                if hist:
                    total_spent = sum(h["Paid"] for h in hist)
                    cc1,cc2 = st.columns(2); cc1.metric("Total visits", len(hist)); cc2.metric("Total spent", fmt(total_spent))
                    df_hist = pd.DataFrame(hist)
                    for col in ["Base","Discount","Paid"]:
                        if col in df_hist.columns: df_hist[col] = df_hist[col].apply(fmt)
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
                else: st.info("No visits recorded.")
        else: st.info("No patients found.")

    # ── DELETE / EDIT VISIT ──
    with t9:
        ed1, ed2 = st.tabs(["Delete","Edit"])
        with ed1:
            section_label("Delete visit"); st.warning("⚠️ For corrections only.")
            dv_search = st.text_input("🔍 Search", key="dv_search")
            all_visits_j = get_visits_joined(limit=200)
            if dv_search: all_visits_j = [v for v in all_visits_j if dv_search.lower() in v.get("Patient","").lower()]
            if all_visits_j:
                df_dv = pd.DataFrame(all_visits_j)
                for col in ["Base","Discount","Paid"]:
                    if col in df_dv.columns: df_dv[col] = df_dv[col].apply(fmt)
                st.dataframe(df_dv, use_container_width=True, hide_index=True)
                void_id = st.number_input("Visit ID to delete", min_value=1, step=1, key="void_id")
                if st.button("Delete Visit", type="primary", key="btn_del_visit"):
                    sb_delete("visits","id",void_id); log_action(username,"Delete Visit",f"#{void_id}")
                    play_ding(); st.success(f"Deleted."); st.rerun()
        with ed2:
            section_label("Edit visit")
            ev_search = st.text_input("🔍 Search", key="ev_search")
            all_visits_j2 = get_visits_joined(limit=200)
            if ev_search: all_visits_j2 = [v for v in all_visits_j2 if ev_search.lower() in v.get("Patient","").lower()]
            if all_visits_j2:
                visit_opts = {f"#{v['id']} · {v['Date']} · {v['Patient']} · {fmt(v['Paid'])}": v["id"] for v in all_visits_j2}
                chosen_v = st.selectbox("Select", ["— select —"]+list(visit_opts.keys()), key="edit_v_sel")
                if chosen_v != "— select —":
                    vid = visit_opts[chosen_v]; visit_rec = sb_one("visits", filters={"id": vid})
                    if visit_rec:
                        c1,c2 = st.columns(2)
                        with c1:
                            new_v_date = st.text_input("Date", value=visit_rec.get("visit_date",""), key="ev_date")
                            new_v_base = st.number_input("Base price", min_value=0.0, step=1000.0, value=float(visit_rec.get("base_price") or 0), key="ev_base")
                            new_v_disc = st.number_input("Discount", min_value=0.0, step=1000.0, value=float(visit_rec.get("discount_amount") or 0), key="ev_disc")
                        with c2:
                            new_v_paid = st.number_input("Net paid", min_value=0.0, step=1000.0, value=float(visit_rec.get("net_paid") or 0), key="ev_paid")
                            mopts = ["Cash","Card","Insurance","Transfer","Subscription"]
                            cm = visit_rec.get("payment_method","Cash") or "Cash"
                            new_v_method = st.selectbox("Payment", mopts, index=mopts.index(cm) if cm in mopts else 0, key="ev_method")
                            new_v_notes = st.text_area("Notes", value=visit_rec.get("notes","") or "", height=80, key="ev_notes")
                        if st.button("Save Changes", key="btn_edit_visit"):
                            sb_update("visits",{"visit_date":new_v_date,"base_price":new_v_base,"discount_amount":new_v_disc,"net_paid":new_v_paid,"payment_method":new_v_method,"notes":new_v_notes},"id",vid)
                            play_ding(); st.success(f"Updated!"); st.rerun()

# ═══════════════════════════════════════════════
# APPOINTMENTS
# ═══════════════════════════════════════════════
elif selected == "📅  Appointments":
    page_header("Appointments", "Schedule and manage appointments.")
    ta1,ta2,ta3 = st.tabs(["Schedule","View All","🖨️ Print Today"])
    with ta1:
        patients_db = sb_all("patients", order="name"); docs_db = sb_all("doctors", order="name")
        if not patients_db or not docs_db: st.warning("Need at least one patient and one doctor.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}; d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1: ap_patient = st.selectbox("Patient", list(p_map.keys())); ap_doctor = st.selectbox("Doctor", list(d_map.keys()))
            with c2: ap_date = st.date_input("Date", value=date.today()); ap_time = st.time_input("Time"); ap_reason = st.text_input("Reason / notes")
            if st.button("Book Appointment"):
                sb_insert("appointments",{"patient_id":p_map[ap_patient],"doctor_id":d_map[ap_doctor],"appt_date":str(ap_date),"appt_time":str(ap_time),"reason":ap_reason,"status":"Scheduled"})
                log_action(username,"Book Appointment",f"{ap_patient} with {ap_doctor}")
                play_ding(); st.success(f"Booked.")
    with ta2:
        ap_search = st.text_input("🔍 Search", key="ap_search")
        all_appts = get_appointments_joined()
        if ap_search: all_appts = [a for a in all_appts if ap_search.lower() in (a.get("Patient","")+" "+a.get("Doctor","")).lower()]
        if all_appts:
            st.dataframe(pd.DataFrame(all_appts), use_container_width=True, hide_index=True)
            c1,c2 = st.columns(2)
            with c1: upd_id = st.number_input("Appointment ID", min_value=1, step=1)
            with c2: new_status = st.selectbox("New status", ["Scheduled","Completed","Cancelled","No-show"])
            if st.button("Update Status"):
                sb_update("appointments",{"status":new_status},"id",upd_id); play_ding(); st.success("Updated."); st.rerun()
        else: st.info("No appointments yet.")
    with ta3:
        today_appts_p = [a for a in get_appointments_joined() if a.get("Date")==today_str]
        if today_appts_p:
            cp = get_clinic_profile()
            print_html = f'<div style="background:white;padding:30px;font-family:Inter,sans-serif;color:#1A2E23;max-width:800px;border-radius:14px;"><div style="text-align:center;border-bottom:3px solid #0A0E0C;padding-bottom:14px;margin-bottom:20px;"><h1 style="margin:0;font-family:Cormorant Garamond,serif;font-style:italic;color:#0A0E0C;">{cp.get("clinic_name","Garden Clinic")}</h1><p style="margin:4px 0 0 0;color:#FF8C3C;font-size:0.75rem;letter-spacing:0.2em;text-transform:uppercase;">Daily Appointments</p><p style="margin:8px 0 0 0;font-weight:700;color:#0A0E0C;">{date.today().strftime("%A, %B %d, %Y")}</p></div><table style="width:100%;border-collapse:collapse;font-size:0.95rem;"><thead><tr style="background:#0A0E0C;color:white;"><th style="padding:10px;text-align:left;">Time</th><th style="padding:10px;text-align:left;">Patient</th><th style="padding:10px;text-align:left;">Doctor</th><th style="padding:10px;text-align:left;">Reason</th><th style="padding:10px;text-align:left;">Status</th></tr></thead><tbody>'
            for a in today_appts_p:
                print_html += f'<tr style="border-bottom:1px solid #DDE8E1;"><td style="padding:10px;">{a["Time"]}</td><td style="padding:10px;font-weight:600;">{a["Patient"]}</td><td style="padding:10px;">{a["Doctor"]}</td><td style="padding:10px;">{a.get("Reason","—")}</td><td style="padding:10px;">{a["Status"]}</td></tr>'
            print_html += f'</tbody></table><p style="text-align:center;margin-top:20px;color:#8B7A5A;font-size:0.8rem;">Total: {len(today_appts_p)}</p></div>'
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("💡 Press **Ctrl+P** to print or save as PDF.")
        else: st.info("No appointments today.")

# ═══════════════════════════════════════════════
# ACCOUNTING
# ═══════════════════════════════════════════════
elif selected == "📊  Accounting":
    page_header("Accounting", "Revenue, expenses, and financial health.")
    section_label("📅 Date range filter")
    use_range = st.checkbox("Filter by date range", key="acc_use_range")
    if use_range:
        rc1,rc2 = st.columns(2)
        with rc1: start_d = st.date_input("From", value=date.today().replace(day=1), key="acc_start")
        with rc2: end_d = st.date_input("To", value=date.today(), key="acc_end")
        g_, e_, c_, o_, n_, _ = get_financials(start=str(start_d), end=str(end_d))
        st.info(f"📊 **{start_d}** → **{end_d}**")
    else:
        g_, e_, c_, o_, n_ = gross_income, base_expenses, total_commissions, total_outflows, net_profit
    pulse_bar([("Gross Revenue",fmt(g_)),("Total Expenses",fmt(o_)),("Net Profit",fmt(n_)),("Doctor Commissions",fmt(c_))])
    cc1,cc2,cc3 = st.columns(3)
    with cc1: st.markdown(card("Gross Revenue", fmt(g_),"green"), unsafe_allow_html=True)
    with cc2: st.markdown(card("Total Outflows", fmt(o_),"red"), unsafe_allow_html=True)
    with cc3: st.markdown(card("Net Profit", fmt(n_),"gold"), unsafe_allow_html=True)
    st.markdown("---")
    ac1,ac2 = st.columns(2)
    with ac1:
        section_label("Expenses breakdown")
        payroll_total = sum(float(e.get("amount") or 0) for e in sb_all("expenses") if e.get("category")=="Payroll")
        other_exp = e_ - payroll_total
        if o_ > 0:
            df_e = pd.DataFrame({"Category":["Other Expenses","Payroll","Doctor Commissions"],"Amount":[other_exp,payroll_total,c_]}).set_index("Category")
            st.bar_chart(df_e, y="Amount", color="#FF8C3C", height=240)
    with ac2:
        section_label("Daily revenue trend")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df_v = pd.DataFrame([{"Date":v["visit_date"],"Revenue":float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df_v.groupby("Date").sum(), y="Revenue", color="#6FE6A4", height=240)
    st.markdown("---")
    ae1,ae2 = st.columns([3,2])
    with ae1:
        section_label("Expense log")
        exp_search = st.text_input("🔍 Search expenses", key="exp_search")
        filter_cat = st.selectbox("Filter",["All","General","Payroll","Supplies","Utilities","Rent","Equipment","Marketing","Subscription","Other"], key="acc_filter_cat")
        all_exp = sb_all("expenses", order="id", desc_order=True)
        if filter_cat != "All": all_exp = [e for e in all_exp if e.get("category")==filter_cat]
        if exp_search: all_exp = [e for e in all_exp if exp_search.lower() in (e.get("description","")).lower()]
        if all_exp:
            df_exp = pd.DataFrame([{"id":e["id"],"Date":e["date"],"Category":e.get("category",""),"Description":e["description"],"Amount":fmt(e.get("amount") or 0),"Added By":e.get("added_by","")} for e in all_exp])
            st.dataframe(df_exp, use_container_width=True, hide_index=True)
    with ae2:
        section_label("Add expense")
        with st.form("expense_form"):
            e_desc = st.text_input("Description"); e_cat = st.selectbox("Category",["General","Supplies","Utilities","Rent","Equipment","Marketing","Other"])
            e_amt = st.number_input("Amount (IQD)", min_value=0.0, step=1000.0); e_date = st.date_input("Date", value=date.today())
            if st.form_submit_button("Add Expense"):
                if e_desc and e_amt > 0:
                    sb_insert("expenses",{"description":e_desc,"category":e_cat,"amount":e_amt,"date":str(e_date),"added_by":username})
                    log_action(username,"Add Expense",f"{e_desc} | {fmt(e_amt)}")
                    play_ding(); st.success("Added."); st.rerun()
    st.markdown("---"); section_label("Edit or delete expense")
    del_exp_list = sb_all("expenses", order="id", desc_order=True, limit=100)
    if del_exp_list:
        ed_exp_opts = {f"#{e['id']} · {e['date']} · {e['description']} · {fmt(e.get('amount') or 0)}": e["id"] for e in del_exp_list}
        chosen_ed_exp = st.selectbox("Select", ["— select —"]+list(ed_exp_opts.keys()), key="ed_exp_sel")
        if chosen_ed_exp != "— select —":
            eid = ed_exp_opts[chosen_ed_exp]; exp_rec = sb_one("expenses", filters={"id": eid})
            if exp_rec:
                c1,c2,c3 = st.columns(3)
                with c1: new_e_desc = st.text_input("Description", value=exp_rec.get("description",""), key="ee_desc")
                with c2:
                    cat_opts = ["General","Payroll","Supplies","Utilities","Rent","Equipment","Marketing","Subscription","Other"]
                    cur_cat = exp_rec.get("category","General") or "General"
                    new_e_cat = st.selectbox("Category", cat_opts, index=cat_opts.index(cur_cat) if cur_cat in cat_opts else 0, key="ee_cat")
                with c3: new_e_amt = st.number_input("Amount", min_value=0.0, step=1000.0, value=float(exp_rec.get("amount") or 0), key="ee_amt")
                cc1,cc2 = st.columns(2)
                with cc1:
                    if st.button("Save", key="btn_edit_exp"):
                        sb_update("expenses",{"description":new_e_desc,"category":new_e_cat,"amount":new_e_amt},"id",eid)
                        play_ding(); st.success("Updated."); st.rerun()
                with cc2:
                    if st.button("Delete", type="primary", key="btn_del_exp"):
                        sb_delete("expenses","id",eid); play_ding(); st.success("Deleted."); st.rerun()
    st.markdown("---"); section_label("Referral commissions this month")
    current_month = datetime.now().strftime("%Y-%m")
    all_refs = sb_all("referrers", order="name")
    if all_refs:
        all_v_month = [v for v in sb_all("visits") if (v.get("visit_date") or "")[:7]==current_month]
        ref_rows = []; total_ref_comm = 0.0
        for ref in all_refs:
            v_via = [v for v in all_v_month if v.get("referred_by")==ref["name"]]
            rev = sum(float(v.get("net_paid") or 0) for v in v_via)
            comm = rev*(float(ref.get("commission_rate") or 0)/100.0); total_ref_comm += comm
            ref_rows.append({"Referrer":ref["name"],"Rate":f"{ref.get('commission_rate')}%","Visits":len(v_via),"Revenue":fmt(rev),"Commission Due":fmt(comm)})
        st.dataframe(pd.DataFrame(ref_rows), use_container_width=True, hide_index=True)
        st.markdown(f"**Total: {fmt(total_ref_comm)}**")
        if st.button("Mark as Paid"):
            if total_ref_comm > 0:
                tag = f"Referral Commissions — {current_month}"
                if not sb_exists("expenses","description",tag):
                    sb_insert("expenses",{"description":tag,"category":"Marketing","amount":total_ref_comm,"date":f"{current_month}-01","added_by":username})
                    play_ding(); st.success(f"Recorded."); st.rerun()
    st.markdown("---"); section_label("📥 Export to Excel")
    ex1,ex2,ex3,ex4 = st.columns(4)
    with ex1:
        all_v_exp = sb_all("visits", order="visit_date", desc_order=True)
        if all_v_exp:
            df_ev = pd.DataFrame([{"ID":v["id"],"Date":v["visit_date"],"Net Paid (IQD)":v.get("net_paid",0),"Method":v.get("payment_method",""),"Added By":v.get("added_by","")} for v in all_v_exp])
            st.download_button("⬇️ All Visits", data=to_excel(df_ev), file_name=f"visits_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with ex2:
        all_e_exp = sb_all("expenses", order="date", desc_order=True)
        if all_e_exp:
            df_ee = pd.DataFrame([{"ID":e["id"],"Date":e["date"],"Description":e["description"],"Category":e.get("category",""),"Amount (IQD)":e.get("amount",0),"Added By":e.get("added_by","")} for e in all_e_exp])
            st.download_button("⬇️ All Expenses", data=to_excel(df_ee), file_name=f"expenses_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with ex3:
        all_p_exp = sb_all("patients", order="name")
        if all_p_exp:
            df_ep = pd.DataFrame([{"Name":p["name"],"Phone":p.get("phone",""),"Gender":p.get("gender",""),"DOB":p.get("date_of_birth",""),"Notes":p.get("notes",""),"Registered":p.get("created_at","")} for p in all_p_exp])
            st.download_button("⬇️ All Patients", data=to_excel(df_ep), file_name=f"patients_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
    with ex4:
        all_v_m = sb_all("visits")
        if all_v_m:
            df_em = pd.DataFrame([{"Month":v["visit_date"][:7],"Revenue":float(v.get("net_paid") or 0)} for v in all_v_m])
            df_em = df_em.groupby("Month").agg(Revenue=("Revenue","sum"),Visits=("Revenue","count")).reset_index().sort_values("Month",ascending=False)
            st.download_button("⬇️ Monthly", data=to_excel(df_em), file_name=f"monthly_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ═══════════════════════════════════════════════
# REPORTS
# ═══════════════════════════════════════════════
elif selected == "📑  Reports":
    page_header("Reports", "Daily summary, top patients, services, and doctor monthly.")
    rep_tabs = st.tabs(["📅 Daily Report","🏆 Top Patients","💎 Top Services","👨‍⚕️ Doctor Monthly"])
    with rep_tabs[0]:
        rep_date = st.date_input("Date", value=date.today(), key="dr_date")
        rep_date_str = str(rep_date)
        day_visits = [v for v in sb_all("visits") if v.get("visit_date")==rep_date_str]
        day_revenue = sum(float(v.get("net_paid") or 0) for v in day_visits)
        day_expenses = sum(float(e.get("amount") or 0) for e in sb_all("expenses") if e.get("date")==rep_date_str)
        unique_pat = len(set(v.get("patient_id") for v in day_visits))
        mc1,mc2,mc3,mc4 = st.columns(4)
        mc1.metric("Revenue", fmt(day_revenue))
        mc2.metric("Visits", len(day_visits))
        mc3.metric("Unique Patients", unique_pat)
        mc4.metric("Expenses", fmt(day_expenses))
        if day_visits:
            section_label("Visits that day")
            patients_dr = {p["id"]: p["name"] for p in sb_all("patients")}
            doctors_dr  = {d["id"]: d["name"] for d in sb_all("doctors")}
            services_dr = {s["id"]: s["name"] for s in sb_all("services")}
            bundles_dr  = {b["id"]: b["name"] for b in sb_all("bundles")}
            rows_dr = []
            for v in day_visits:
                svc_d = services_dr.get(v.get("service_id"),""); bnd_d = bundles_dr.get(v.get("bundle_id"),"")
                rows_dr.append({"Patient":patients_dr.get(v.get("patient_id"),""),"Doctor":doctors_dr.get(v.get("doctor_id"),""),"Item":svc_d if svc_d else (f"📦 {bnd_d}" if bnd_d else "—"),"Paid":fmt(v.get('net_paid') or 0),"Method":v.get("payment_method","")})
            st.dataframe(pd.DataFrame(rows_dr), use_container_width=True, hide_index=True)

    with rep_tabs[1]:
        tp_period = st.selectbox("Period", ["This month","This year","All time"], key="tp_period")
        all_v_tp = sb_all("visits")
        if tp_period == "This month": cm = datetime.now().strftime("%Y-%m"); all_v_tp = [v for v in all_v_tp if (v.get("visit_date") or "")[:7]==cm]
        elif tp_period == "This year": cy = datetime.now().strftime("%Y"); all_v_tp = [v for v in all_v_tp if (v.get("visit_date") or "")[:4]==cy]
        patient_totals = {}
        for v in all_v_tp:
            pid = v.get("patient_id")
            if pid:
                if pid not in patient_totals: patient_totals[pid] = {"visits":0,"spent":0.0}
                patient_totals[pid]["visits"] += 1
                patient_totals[pid]["spent"] += float(v.get("net_paid") or 0)
        patients_tp = {p["id"]: p["name"] for p in sb_all("patients")}
        rows_tp = sorted([{"Patient":patients_tp.get(pid,""),"Visits":info["visits"],"Total Spent":info["spent"]} for pid,info in patient_totals.items()], key=lambda x: x["Total Spent"], reverse=True)
        if rows_tp:
            df_tp = pd.DataFrame(rows_tp[:20])
            df_tp["Total Spent"] = df_tp["Total Spent"].apply(fmt)
            st.dataframe(df_tp, use_container_width=True, hide_index=True)

    with rep_tabs[2]:
        ts_period = st.selectbox("Period", ["This month","This year","All time"], key="ts_period")
        all_v_ts = sb_all("visits")
        if ts_period == "This month": cm2 = datetime.now().strftime("%Y-%m"); all_v_ts = [v for v in all_v_ts if (v.get("visit_date") or "")[:7]==cm2]
        elif ts_period == "This year": cy2 = datetime.now().strftime("%Y"); all_v_ts = [v for v in all_v_ts if (v.get("visit_date") or "")[:4]==cy2]
        services_ts = {s["id"]: s["name"] for s in sb_all("services")}
        bundles_ts  = {b["id"]: b["name"] for b in sb_all("bundles")}
        svc_totals = {}
        for v in all_v_ts:
            sid = v.get("service_id"); bid = v.get("bundle_id")
            item = services_ts.get(sid) if sid else (f"📦 {bundles_ts.get(bid,'')}" if bid else "Other")
            if item not in svc_totals: svc_totals[item] = {"count":0,"revenue":0.0}
            svc_totals[item]["count"] += 1
            svc_totals[item]["revenue"] += float(v.get("net_paid") or 0)
        rows_ts = sorted([{"Service / Bundle":k,"Times Sold":v["count"],"Total Revenue":v["revenue"]} for k,v in svc_totals.items()], key=lambda x: x["Total Revenue"], reverse=True)
        if rows_ts:
            df_ts = pd.DataFrame(rows_ts)
            df_ts["Total Revenue"] = df_ts["Total Revenue"].apply(fmt)
            st.dataframe(df_ts, use_container_width=True, hide_index=True)

    with rep_tabs[3]:
        dm_month = st.text_input("Month (YYYY-MM)", value=datetime.now().strftime("%Y-%m"), key="dm_month")
        all_v_dm = [v for v in sb_all("visits") if (v.get("visit_date") or "")[:7]==dm_month]
        doctors_dm = sb_all("doctors", order="name")
        all_tiers_dm = sb_all("doctor_commission_tiers")
        rows_dm = []
        for d in doctors_dm:
            doc_v = [v for v in all_v_dm if v.get("doctor_id")==d["id"]]
            rev = sum(float(v.get("net_paid") or 0) for v in doc_v)
            all_doc_v = [v for v in sb_all("visits") if v.get("doctor_id")==d["id"]]
            rate = get_doc_commission_rate(d["id"], len(all_doc_v), all_tiers_dm)
            comm = rev * rate
            rows_dm.append({"Doctor":d["name"],"Visits":len(doc_v),"Revenue":fmt(rev),"Rate":f"{rate*100:.1f}%","Commission":fmt(comm)})
        if rows_dm: st.dataframe(pd.DataFrame(rows_dm), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════
# RESEARCH (Boss only)
# ═══════════════════════════════════════════════
elif selected == "🔬  Research":
    page_header("Research & Outcomes", "Track patient outcomes for research and marketing.")
    all_forms_r = sb_all("doctor_intake_form")
    
    section_label("Filter by period")
    rp = st.selectbox("Period", ["All time","This year","This month","Custom range"], key="research_period")
    if rp == "All time": filtered_forms = all_forms_r
    elif rp == "This year":
        cy_r = datetime.now().strftime("%Y")
        filtered_forms = [f for f in all_forms_r if (f.get("filled_date") or "")[:4]==cy_r]
    elif rp == "This month":
        cm_r = datetime.now().strftime("%Y-%m")
        filtered_forms = [f for f in all_forms_r if (f.get("filled_date") or "")[:7]==cm_r]
    else:
        rc1,rc2 = st.columns(2)
        with rc1: r_start = st.date_input("From", value=date.today().replace(month=1, day=1), key="r_start")
        with rc2: r_end = st.date_input("To", value=date.today(), key="r_end")
        filtered_forms = [f for f in all_forms_r if str(r_start) <= (f.get("filled_date") or "") <= str(r_end)]

    total_treated = len(filtered_forms)
    relieved = len([f for f in filtered_forms if f.get("outcome") == "Successfully Relieved"])
    partial = len([f for f in filtered_forms if f.get("outcome") == "Partially Improved"])
    no_improv = len([f for f in filtered_forms if f.get("outcome") == "No Improvement"])
    discontinued = len([f for f in filtered_forms if f.get("outcome") == "Patient Discontinued"])
    pending = len([f for f in filtered_forms if f.get("outcome") in ["Pending", None, ""]])
    success_rate = (relieved/total_treated*100) if total_treated>0 else 0
    improvement_rate = ((relieved+partial)/total_treated*100) if total_treated>0 else 0

    pulse_bar([("Total Patients",str(total_treated)),("Successfully Relieved",str(relieved)),("Success Rate",f"{success_rate:.1f}%"),("Total Improvement Rate",f"{improvement_rate:.1f}%")])

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(card("Successfully Relieved", str(relieved), "green", f"{success_rate:.1f}% success rate"), unsafe_allow_html=True)
    with c2: st.markdown(card("Partially Improved", str(partial), "gold", "Some improvement"), unsafe_allow_html=True)
    with c3: st.markdown(card("No Improvement", str(no_improv), "red", "Need different approach"), unsafe_allow_html=True)
    with c4: st.markdown(card("Pending", str(pending), "dark", "Still in treatment"), unsafe_allow_html=True)

    st.markdown("---"); section_label("📢 Marketing narrative")
    narrative = ""
    if total_treated > 0:
        narrative = f"In this period, we successfully treated **{total_treated} patients**. Of those, **{relieved} ({success_rate:.1f}%)** experienced full pain relief, and **{relieved+partial} ({improvement_rate:.1f}%)** showed measurable improvement. This data reflects our commitment to evidence-based, results-driven physical therapy care."
    st.markdown(f'<div class="card" style="padding:24px 28px;"><div style="font-family:Cormorant Garamond,serif;font-size:1.2rem;font-style:italic;color:#FFF;line-height:1.7;">{narrative if narrative else "No data yet for this period."}</div></div>', unsafe_allow_html=True)

    st.markdown("---"); section_label("By doctor")
    doctors_r = sb_all("doctors", order="name")
    rows_dr = []
    for d in doctors_r:
        d_forms = [f for f in filtered_forms if f.get("doctor_id")==d["id"]]
        d_treated = len(d_forms)
        d_relieved = len([f for f in d_forms if f.get("outcome")=="Successfully Relieved"])
        d_rate = (d_relieved/d_treated*100) if d_treated>0 else 0
        rows_dr.append({"Doctor":d["name"],"Patients":d_treated,"Successfully Relieved":d_relieved,"Success Rate":f"{d_rate:.1f}%"})
    if rows_dr: st.dataframe(pd.DataFrame(rows_dr), use_container_width=True, hide_index=True)

    st.markdown("---"); section_label("By problem category")
    problem_stats = {}
    for f in filtered_forms:
        prob = (f.get("problem","") or "")[:50] or "Unknown"
        if prob not in problem_stats: problem_stats[prob] = {"total":0,"relieved":0}
        problem_stats[prob]["total"] += 1
        if f.get("outcome")=="Successfully Relieved": problem_stats[prob]["relieved"] += 1
    rows_ps = sorted([{"Problem":k,"Total Cases":v["total"],"Relieved":v["relieved"],"Success Rate":f"{(v['relieved']/v['total']*100) if v['total']>0 else 0:.1f}%"} for k,v in problem_stats.items()], key=lambda x: x["Total Cases"], reverse=True)
    if rows_ps: st.dataframe(pd.DataFrame(rows_ps[:20]), use_container_width=True, hide_index=True)

    st.markdown("---"); section_label("📥 Export research data")
    if filtered_forms:
        patients_r_map = {p["id"]: p["name"] for p in sb_all("patients")}
        doctors_r_map = {d["id"]: d["name"] for d in doctors_r}
        df_research = pd.DataFrame([{"Date":f.get("filled_date",""),"Patient":patients_r_map.get(f.get("patient_id"),""),"Doctor":doctors_r_map.get(f.get("doctor_id"),""),"Problem":f.get("problem",""),"Treatment Plan":f.get("treatment_plan",""),"Sessions Needed":f.get("sessions_needed",0),"Outcome":f.get("outcome","Pending"),"Outcome Notes":f.get("outcome_notes","")} for f in filtered_forms])
        st.download_button("⬇️ Export Research Data to Excel", data=to_excel(df_research), file_name=f"research_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

# ═══════════════════════════════════════════════
# ACCOUNTS
# ═══════════════════════════════════════════════
elif selected == "👥  Accounts":
    page_header("Accounts", "Manage users and activity logs.")
    accounts = sb_all("users"); st.metric("Total user accounts", len(accounts))
    at1,at2 = st.tabs(["Profiles & Access","Activity Log"])
    with at1:
        section_label("All accounts")
        doctors_acc_map = {d["id"]: d["name"] for d in sb_all("doctors")}
        if accounts:
            rows_acc = [{"id":u["id"],"username":u["username"],"role":u["role"],"Linked Doctor":doctors_acc_map.get(u.get("linked_doctor_id"),"—") if u.get("role")=="Doctor" else "—"} for u in accounts]
            st.dataframe(pd.DataFrame(rows_acc), use_container_width=True, hide_index=True)
            st.markdown("---"); section_label("Remove account")
            killable = ["— select —"]+[u["username"] for u in accounts if u["username"]!=username]
            target_del = st.selectbox("Select", killable, key="burn_user_select")
            if st.button("Delete Account", type="primary", key="btn_del_account"):
                if target_del != "— select —":
                    sb_delete("users","username",target_del); play_ding(); st.success("Removed."); st.rerun()
    with at2:
        al_search = st.text_input("🔍 Search", key="al_search")
        pf = ["All"]+[u["username"] for u in accounts]
        chosen_user = st.selectbox("Filter by user", pf, key="acc_audit_user_filter")
        audit_r = sb_all("audit_log", order="id", desc_order=True, limit=400)
        if chosen_user != "All": audit_r = [r for r in audit_r if r.get("username")==chosen_user]
        if al_search: audit_r = [r for r in audit_r if al_search.lower() in (r.get("action","")+" "+r.get("details","")).lower()]
        if audit_r:
            st.dataframe(pd.DataFrame([{"Time":r["timestamp"],"User":r["username"],"Action":r["action"],"Details":r.get("details","")} for r in audit_r]), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════
# SETTINGS
# ═══════════════════════════════════════════════
elif selected == "⚙️  Settings":
    page_header("Settings", "Configure doctors, commissions, staff, and more.")
    s1,s2,s3,s4,s5,s6,s7,s8 = st.tabs(["Doctors","💰 Commission","Staff & Payroll","Services","Bundles","🎯 Referrers","🔄 Subscriptions","🏥 Clinic Profile"])

    with s1:
        section_label("Add doctor")
        c1,c2 = st.columns(2)
        with c1: d_name = st.text_input("Doctor name"); d_spec = st.text_input("Specialty")
        if st.button("Add Doctor"):
            if d_name.strip():
                if sb_exists("doctors","name",d_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("doctors",{"name":d_name.strip(),"specialty":d_spec.strip(),"comm_type":"tiered","fixed_rate":0})
                    play_ding(); st.success("Added."); st.rerun()
        st.markdown("---"); section_label("Current doctors")
        all_docs = sb_all("doctors", order="name")
        if all_docs:
            st.dataframe(pd.DataFrame(all_docs), use_container_width=True, hide_index=True)
            del_doc = st.selectbox("Remove", ["— select —"]+[d["name"] for d in all_docs])
            if st.button("Remove Doctor", type="primary"):
                if del_doc != "— select —":
                    doc_id = next(d["id"] for d in all_docs if d["name"]==del_doc)
                    sb_delete("doctors","name",del_doc); sb_delete("doctor_commission_tiers","doctor_id",doc_id)
                    play_ding(); st.success("Removed."); st.rerun()

    with s2:
        section_label("💰 Commission tiers per doctor")
        st.info("💡 Highest qualifying tier applies. E.g. 3% at 5+ visits, 7% at 15+.")
        all_docs_t = sb_all("doctors", order="name")
        if all_docs_t:
            sel_doc_tier = st.selectbox("Select doctor", ["— select —"]+[d["name"] for d in all_docs_t], key="tier_doc_sel")
            if sel_doc_tier != "— select —":
                doc_id_t = next(d["id"] for d in all_docs_t if d["name"]==sel_doc_tier)
                existing_tiers = sorted(sb_all("doctor_commission_tiers", filters={"doctor_id": doc_id_t}), key=lambda x: int(x.get("min_visits") or 0))
                if existing_tiers:
                    st.dataframe(pd.DataFrame([{"id":t["id"],"Min Visits":t["min_visits"],"Rate (%)":t["commission_rate"]} for t in existing_tiers]), use_container_width=True, hide_index=True)
                    del_tier_id = st.number_input("Delete tier ID", min_value=1, step=1, key="del_tier_id")
                    if st.button("Delete Tier", type="primary", key="btn_del_tier"):
                        sb_delete("doctor_commission_tiers","id",del_tier_id); play_ding(); st.success("Deleted."); st.rerun()
                st.markdown("---"); section_label("Add tier")
                c1,c2 = st.columns(2)
                with c1: new_min = st.number_input("Min visits", min_value=1, step=1, value=10, key="tier_min")
                with c2: new_rate = st.number_input("Rate (%)", min_value=0.0, max_value=100.0, step=0.5, value=3.0, key="tier_rate")
                if st.button("Add Tier", key="btn_add_tier"):
                    sb_insert("doctor_commission_tiers",{"doctor_id":doc_id_t,"min_visits":int(new_min),"commission_rate":new_rate})
                    play_ding(); st.success("Added."); st.rerun()

    with s3:
        section_label("Add staff")
        c1,c2,c3 = st.columns(3)
        with c1: emp_name = st.text_input("Full name")
        with c2: emp_role = st.text_input("Role")
        with c3: emp_salary = st.number_input("Monthly salary (IQD)", min_value=0.0, step=50000.0)
        if st.button("Add Staff"):
            if emp_name.strip() and emp_role.strip():
                if sb_exists("employees","name",emp_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("employees",{"name":emp_name.strip(),"role":emp_role.strip(),"salary":emp_salary})
                    play_ding(); st.success("Added."); st.rerun()
        st.markdown("---"); section_label("Current staff")
        all_emp = sb_all("employees", order="name")
        if all_emp:
            df_emp = pd.DataFrame([{"id":e["id"],"name":e["name"],"role":e.get("role",""),"salary":fmt(e.get("salary"))} for e in all_emp])
            st.dataframe(df_emp, use_container_width=True, hide_index=True)
            st.markdown(f"**Monthly payroll: {fmt(sum(float(e.get('salary') or 0) for e in all_emp))}**")
            del_emp = st.selectbox("Remove", ["— select —"]+[e["name"] for e in all_emp])
            if st.button("Remove Employee", type="primary"):
                if del_emp != "— select —":
                    sb_delete("employees","name",del_emp); play_ding(); st.success("Removed."); st.rerun()

    with s4:
        section_label("Add service")
        c1,c2,c3 = st.columns(3)
        with c1: s_name = st.text_input("Service name")
        with c2: s_cat = st.selectbox("Category",["General","Consultation","Procedure","Therapy","Diagnostic","Other"])
        with c3: s_price = st.number_input("Price (IQD)", min_value=0.0, step=5000.0)
        if st.button("Add Service"):
            if s_name.strip():
                if sb_exists("services","name",s_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("services",{"name":s_name.strip(),"category":s_cat,"price":s_price,"active":1})
                    play_ding(); st.success("Added."); st.rerun()
        st.markdown("---"); section_label("Current services")
        all_svc = sb_all("services", order="name")
        if all_svc:
            df_svc = pd.DataFrame([{"id":s["id"],"name":s["name"],"category":s.get("category",""),"price":fmt(s.get("price")),"active":s.get("active",1)} for s in all_svc])
            st.dataframe(df_svc, use_container_width=True, hide_index=True)
            del_svc = st.selectbox("Remove", ["— select —"]+[s["name"] for s in all_svc])
            if st.button("Remove Service", type="primary"):
                if del_svc != "— select —":
                    sb_delete("services","name",del_svc); play_ding(); st.success("Removed."); st.rerun()

    with s5:
        section_label("Create bundle")
        c1,c2 = st.columns(2)
        with c1: b_name = st.text_input("Bundle name"); b_price = st.number_input("Price (IQD)", min_value=0.0, step=10000.0)
        with c2: b_desc = st.text_area("Description", height=90)
        if st.button("Create Bundle"):
            if b_name.strip() and b_price > 0:
                if sb_exists("bundles","name",b_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("bundles",{"name":b_name.strip(),"price":b_price,"description":b_desc.strip()})
                    play_ding(); st.success("Created."); st.rerun()
        st.markdown("---"); section_label("Current bundles")
        all_bundles = sb_all("bundles", order="name")
        if all_bundles:
            df_b = pd.DataFrame([{"id":b["id"],"name":b["name"],"price":fmt(b.get("price")),"description":b.get("description","")} for b in all_bundles])
            st.dataframe(df_b, use_container_width=True, hide_index=True)
            del_bnd = st.selectbox("Remove", ["— select —"]+[b["name"] for b in all_bundles])
            if st.button("Remove Bundle", type="primary"):
                if del_bnd != "— select —":
                    sb_delete("bundles","name",del_bnd); play_ding(); st.success("Removed."); st.rerun()

    with s6:
        section_label("Add referrer")
        c1,c2 = st.columns(2)
        with c1: ref_name = st.text_input("Name", key="ref_name_input"); ref_phone = st.text_input("Phone", key="ref_phone_input")
        with c2: ref_rate = st.number_input("Commission rate (%)", min_value=0.0, max_value=100.0, step=1.0, value=10.0, key="ref_rate_input"); ref_notes = st.text_area("Notes", height=80, key="ref_notes_input")
        if st.button("Add Referrer", key="btn_add_referrer"):
            if ref_name.strip():
                if sb_exists("referrers","name",ref_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("referrers",{"name":ref_name.strip(),"phone":ref_phone.strip(),"commission_rate":ref_rate,"notes":ref_notes.strip(),"added_by":username,"created_at":today_str})
                    play_ding(); st.success("Added."); st.rerun()
        st.markdown("---"); section_label("Current referrers")
        all_refs = sb_all("referrers", order="name")
        if all_refs:
            st.dataframe(pd.DataFrame(all_refs), use_container_width=True, hide_index=True)
            del_ref = st.selectbox("Remove", ["— select —"]+[r["name"] for r in all_refs], key="del_ref_select")
            if st.button("Remove Referrer", type="primary", key="btn_del_referrer"):
                if del_ref != "— select —":
                    sb_delete("referrers","name",del_ref); play_ding(); st.success("Removed."); st.rerun()

    with s7:
        section_label("Add monthly subscription (clinic expense)")
        c1,c2,c3 = st.columns(3)
        with c1: sub_name = st.text_input("Name", key="sub_name_input"); sub_cat = st.selectbox("Category",["Subscription","Marketing","Software","Utilities","Other"], key="sub_cat_select")
        with c2: sub_amount = st.number_input("Monthly amount (IQD)", min_value=0.0, step=5000.0, key="sub_amount_input"); sub_day = st.number_input("Billing day", min_value=1, max_value=28, step=1, value=1, key="sub_day_input")
        with c3: st.markdown("<br>", unsafe_allow_html=True); st.markdown("Auto-posts each month.")
        if st.button("Add Subscription", key="btn_add_subscription"):
            if sub_name.strip() and sub_amount > 0:
                if sb_exists("subscriptions","name",sub_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("subscriptions",{"name":sub_name.strip(),"amount":sub_amount,"billing_day":int(sub_day),"category":sub_cat,"active":1,"added_by":username,"created_at":today_str})
                    play_ding(); st.success("Added."); st.rerun()
        st.markdown("---"); section_label("Active subscriptions")
        all_subs = sb_all("subscriptions", order="name")
        if all_subs:
            df_s = pd.DataFrame([{"id":s["id"],"name":s["name"],"amount":fmt(s.get("amount")),"billing_day":s.get("billing_day",1),"category":s.get("category",""),"active":s.get("active",1)} for s in all_subs])
            st.dataframe(df_s, use_container_width=True, hide_index=True)
            st.markdown(f"**Total active: {fmt(sum(float(s.get('amount') or 0) for s in all_subs if s.get('active')==1))}/month**")
            c1,c2 = st.columns(2)
            with c1:
                toggle_sub = st.selectbox("Pause / activate", ["— select —"]+[s["name"] for s in all_subs], key="toggle_sub_select")
                if st.button("Toggle", key="btn_toggle_sub"):
                    if toggle_sub != "— select —":
                        cur = next((s.get("active",1) for s in all_subs if s["name"]==toggle_sub),1)
                        sb_update("subscriptions",{"active":0 if cur else 1},"name",toggle_sub)
                        play_ding(); st.success("Toggled."); st.rerun()
            with c2:
                del_sub = st.selectbox("Remove", ["— select —"]+[s["name"] for s in all_subs], key="del_sub_select")
                if st.button("Remove Subscription", type="primary", key="btn_del_subscription"):
                    if del_sub != "— select —":
                        sb_delete("subscriptions","name",del_sub); play_ding(); st.success("Removed."); st.rerun()

    with s8:
        section_label("Clinic profile")
        cp = get_clinic_profile()
        c1,c2 = st.columns(2)
        with c1:
            cp_name = st.text_input("Clinic name", value=cp.get("clinic_name","Garden Clinic"), key="cp_name")
            cp_tagline = st.text_input("Tagline", value=cp.get("tagline","Physical Therapy Center"), key="cp_tagline")
            cp_phone = st.text_input("Phone", value=cp.get("phone","") or "", key="cp_phone")
        with c2:
            cp_address = st.text_input("Address", value=cp.get("address","") or "", key="cp_address")
            cp_email = st.text_input("Email", value=cp.get("email","") or "", key="cp_email")
        if st.button("Save Clinic Profile", key="btn_save_clinic"):
            existing = sb_all("clinic_profile")
            data = {"clinic_name":cp_name,"tagline":cp_tagline,"phone":cp_phone,"address":cp_address,"email":cp_email}
            if existing: sb_update("clinic_profile",data,"id",existing[0]["id"])
            else: sb_insert("clinic_profile",data)
            play_ding(); st.success("Saved!"); st.rerun()
