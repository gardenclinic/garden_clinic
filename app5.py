import streamlit as st
import pandas as pd
import hashlib
import io
from datetime import datetime, date, timedelta
import streamlit.components.v1 as components
from supabase import create_client

st.set_page_config(page_title="Garden Clinic", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════
# UNIQUE EDITORIAL DESIGN — botanical apothecary luxury
# Deep cream/parchment, sage green, terracotta, ink black
# Editorial serif + clean sans + monospace numbers
# ═══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: #F4EFE6 !important; color: #1F2924 !important; font-family: 'Inter', system-ui, sans-serif !important; }
.stApp { position: relative; }
.stApp::before { content: ''; position: fixed; inset: 0; background-image: radial-gradient(circle at 20% 30%, rgba(196,118,73,0.05) 0%, transparent 40%), radial-gradient(circle at 80% 70%, rgba(74,103,82,0.05) 0%, transparent 40%); pointer-events: none; z-index: 0; }
.stApp::after { content: ''; position: fixed; inset: 0; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='6' height='6'%3E%3Ccircle cx='1' cy='1' r='0.4' fill='%23000' fill-opacity='0.025'/%3E%3C/svg%3E"); pointer-events: none; z-index: 0; }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }

/* Sidebar — botanical ink */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1F2924 0%, #15201B 100%) !important; border-right: none !important; min-width: 248px !important; }
[data-testid="stSidebar"] * { color: #E8E3D6 !important; font-family: 'Inter', sans-serif !important; }
section[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.88rem !important; padding: 4px 0 !important; transition: all 0.2s !important; }
[data-testid="stSidebar"] .stRadio label:hover { color: #C47649 !important; }

/* Typography — editorial */
h1, h2, h3, h4 { font-family: 'Fraunces', serif !important; letter-spacing: -0.015em !important; color: #1F2924 !important; }

/* Page header — magazine style */
.page-header { margin-bottom: 36px; padding-top: 12px; border-bottom: 1px solid #D8CFB8; padding-bottom: 24px; position: relative; }
.page-header::before { content: ''; position: absolute; bottom: -1px; left: 0; width: 60px; height: 2px; background: #C47649; }
.page-header .kicker { font-family: 'Inter', sans-serif; font-size: 0.7rem; color: #C47649; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 600; margin-bottom: 8px; }
.page-header h1 { font-family: 'Fraunces', serif !important; font-size: 3rem !important; font-weight: 400 !important; color: #1F2924 !important; margin: 0 !important; font-style: italic; letter-spacing: -0.03em !important; line-height: 1.05 !important; }
.page-header p { font-size: 0.92rem; color: #6B7A6F; margin: 8px 0 0 0; font-weight: 400; letter-spacing: 0.01em; }

/* Pulse bar — cream apothecary card */
.pulse-bar { background: #FBF8F1; border: 1px solid #D8CFB8; border-radius: 4px; padding: 24px 32px; display: flex; gap: 48px; flex-wrap: wrap; align-items: center; margin-bottom: 32px; box-shadow: 0 1px 0 #E8DFC8, 0 8px 24px rgba(31,41,36,0.04); position: relative; }
.pulse-bar::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(180deg, #C47649, #4A6752); }
.pulse-stat { display: flex; flex-direction: column; }
.pulse-label { font-family: 'Inter', sans-serif; font-size: 0.65rem; color: #C47649; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; }
.pulse-value { font-family: 'Fraunces', serif; font-size: 1.7rem; font-weight: 500; color: #1F2924; margin-top: 4px; letter-spacing: -0.02em; font-feature-settings: "tnum"; }
.pulse-divider { width: 1px; background: #D8CFB8; height: 44px; align-self: center; }

/* Cards — editorial paper */
.card { background: #FBF8F1; border: 1px solid #E5DCC4; border-radius: 4px; padding: 24px 28px; margin-bottom: 18px; transition: all 0.25s; position: relative; }
.card:hover { border-color: #C47649; box-shadow: 0 4px 24px rgba(196,118,73,0.08); transform: translateY(-1px); }
.card h3 { font-family: 'Inter', sans-serif !important; margin: 0 0 8px 0; font-size: 0.65rem; color: #C47649 !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.18em; }
.card .big-num { font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 500; margin: 0; letter-spacing: -0.02em; font-feature-settings: "tnum"; line-height: 1; }
.card .big-num.green { color: #4A6752; }
.card .big-num.red { color: #B85C3A; }
.card .big-num.dark, .card .big-num.gold { color: #1F2924; }
.card .sub { font-size: 0.78rem; color: #8A7E60; margin-top: 8px; font-weight: 400; font-style: italic; font-family: 'Fraunces', serif; }

/* Tabs — magazine tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; gap: 0 !important; border-bottom: 1px solid #D8CFB8 !important; padding-bottom: 0 !important; }
.stTabs button[data-baseweb="tab"] { background: transparent !important; border: none !important; color: #8A7E60 !important; font-size: 0.85rem !important; font-weight: 500 !important; padding: 12px 22px 14px !important; border-radius: 0 !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0.02em !important; transition: all 0.2s !important; }
.stTabs button[data-baseweb="tab"]:hover { color: #1F2924 !important; }
.stTabs button[aria-selected="true"] { color: #1F2924 !important; font-weight: 600 !important; border-bottom: 2px solid #C47649 !important; margin-bottom: -1px !important; }

/* Buttons — terracotta */
.stButton > button { background: #1F2924 !important; color: #FBF8F1 !important; border: 1px solid #1F2924 !important; border-radius: 2px !important; font-weight: 500 !important; font-size: 0.82rem !important; padding: 12px 26px !important; font-family: 'Inter', sans-serif !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #C47649 !important; border-color: #C47649 !important; transform: translateY(-1px) !important; box-shadow: 0 6px 16px rgba(196,118,73,0.25) !important; }
button[data-testid="baseButton-primary"] { background: #B85C3A !important; border-color: #B85C3A !important; }
button[data-testid="baseButton-primary"]:hover { background: #9A4A2A !important; border-color: #9A4A2A !important; }

/* Inputs — natural paper */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input { background: #FBF8F1 !important; border-radius: 2px !important; border: 1px solid #D8CFB8 !important; font-family: 'Inter', sans-serif !important; font-size: 0.92rem !important; color: #1F2924 !important; padding: 11px 14px !important; transition: all 0.2s !important; }
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus, .stDateInput > div > div > input:focus { border-color: #C47649 !important; box-shadow: 0 0 0 3px rgba(196,118,73,0.1) !important; outline: none !important; }
.stSelectbox > div > div > div, .stMultiSelect > div > div > div { background: #FBF8F1 !important; border-radius: 2px !important; border: 1px solid #D8CFB8 !important; color: #1F2924 !important; }
.stTextArea textarea { background: #FBF8F1 !important; border-radius: 2px !important; border: 1px solid #D8CFB8 !important; font-family: 'Inter', sans-serif !important; color: #1F2924 !important; }
.stTextArea textarea:focus { border-color: #C47649 !important; box-shadow: 0 0 0 3px rgba(196,118,73,0.1) !important; }
.stRadio > div { gap: 14px !important; }
.stRadio label { color: #1F2924 !important; }
label, .stRadio label span, .stCheckbox label { color: #1F2924 !important; }
[data-testid="stWidgetLabel"] p { color: #4A5A52 !important; font-size: 0.78rem !important; font-weight: 600 !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; }

/* Dataframes */
[data-testid="stDataFrame"] { border-radius: 4px !important; overflow: hidden !important; border: 1px solid #D8CFB8 !important; background: #FBF8F1 !important; }

/* Alerts */
.stSuccess > div { background: #E8EFE6 !important; border: 1px solid #4A6752 !important; color: #2D4636 !important; border-radius: 2px !important; }
.stError > div { background: #F5E2D8 !important; border: 1px solid #B85C3A !important; color: #6F2E15 !important; border-radius: 2px !important; }
.stWarning > div { background: #FAE8D0 !important; border: 1px solid #C47649 !important; color: #6F4520 !important; border-radius: 2px !important; }
.stInfo > div { background: #EFEAD9 !important; border: 1px solid #B89F6F !important; color: #5A4A28 !important; border-radius: 2px !important; }

/* Section label */
.section-label { font-family: 'Inter', sans-serif !important; font-size: 0.7rem; font-weight: 600; color: #C47649; text-transform: uppercase; letter-spacing: 0.22em; margin: 24px 0 14px; display: flex; align-items: center; gap: 12px; }
.section-label::before { content: ''; width: 24px; height: 1px; background: #C47649; }

/* Login */
.login-card { background: #FBF8F1; border: 1px solid #D8CFB8; border-radius: 4px; padding: 56px 48px; max-width: 480px; margin: 80px auto 0; box-shadow: 0 12px 48px rgba(31,41,36,0.08); position: relative; }
.login-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #C47649, #4A6752); }
.login-card .leaf { text-align: center; font-size: 1.5rem; color: #4A6752; margin-bottom: 8px; font-family: 'Fraunces', serif; }
.login-card h1 { font-family: 'Fraunces', serif; color: #1F2924; text-align: center; margin: 0 0 6px; font-weight: 500; font-style: italic; font-size: 2.6rem; letter-spacing: -0.03em; }
.login-card p { text-align: center; color: #C47649; font-size: 0.7rem; margin-bottom: 36px; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 600; }
.stForm [data-testid="stFormSubmitButton"] button { width: 100%; }

/* Metric */
[data-testid="stMetric"] { background: #FBF8F1 !important; border: 1px solid #E5DCC4 !important; border-radius: 4px !important; padding: 18px 22px !important; }
[data-testid="stMetricLabel"] { font-size: 0.65rem !important; color: #C47649 !important; text-transform: uppercase; letter-spacing: 0.18em; font-weight: 600 !important; }
[data-testid="stMetricValue"] { font-family: 'Fraunces', serif !important; font-size: 1.8rem !important; color: #1F2924 !important; font-weight: 500 !important; }

/* Session bar */
.session-bar-wrap { background: #E5DCC4; border-radius: 2px; height: 8px; width: 100%; margin-top: 8px; overflow: hidden; }
.session-bar-fill { height: 8px; border-radius: 2px; background: linear-gradient(90deg, #4A6752, #6B8B72); }

/* Patient profile header — apothecary style */
.profile-summary { background: linear-gradient(135deg, #1F2924 0%, #15201B 100%); color: #FBF8F1; padding: 32px 36px; border-radius: 4px; margin-bottom: 24px; position: relative; overflow: hidden; }
.profile-summary::before { content: ''; position: absolute; top: 0; right: 0; width: 240px; height: 240px; background: radial-gradient(circle, rgba(196,118,73,0.15), transparent 70%); }
.profile-summary::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #C47649 0%, #4A6752 100%); }
.profile-kicker { font-family: 'Inter', sans-serif; font-size: 0.65rem; color: #C47649; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 600; }
.profile-name { font-family: 'Fraunces', serif; font-size: 2.2rem; font-weight: 500; font-style: italic; margin: 4px 0 0 0; color: #FBF8F1; letter-spacing: -0.025em; line-height: 1.1; }
.profile-meta { font-size: 0.88rem; color: #B8AC92; margin-top: 10px; letter-spacing: 0.02em; }

/* Patient chip header (like reference inspiration) */
.patient-chip-bar { background: #FBF8F1; border: 1px solid #D8CFB8; border-radius: 4px; padding: 18px 24px; margin-bottom: 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 16px; font-family: 'Inter', sans-serif; }
.patient-chip-name { font-family: 'Fraunces', serif; font-size: 1.4rem; font-weight: 500; font-style: italic; color: #1F2924; letter-spacing: -0.01em; }
.patient-chip { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; background: #EFEAD9; border-radius: 20px; font-size: 0.78rem; color: #4A5A52; font-weight: 500; }
.patient-chip.warn { background: #F5E2D8; color: #B85C3A; }
.patient-chip.good { background: #E8EFE6; color: #4A6752; }
.patient-chip.accent { background: #FAE8D0; color: #6F4520; }

/* Tag pills */
.tag-pill { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.74rem; font-weight: 600; margin-right: 6px; margin-bottom: 4px; }
.tag-condition { background: #F5E2D8; color: #B85C3A; border: 1px solid rgba(184,92,58,0.2); }
.tag-success { background: #E8EFE6; color: #4A6752; border: 1px solid rgba(74,103,82,0.2); }
.tag-pending { background: #EFEAD9; color: #8A7E60; border: 1px solid rgba(138,126,96,0.2); }

/* RECEIPT — luxury apothecary */
.receipt-wrap { background: #FBF8F1; border-radius: 6px; padding: 0; max-width: 440px; font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #1F2924; box-shadow: 0 20px 60px rgba(31,41,36,0.25), 0 6px 20px rgba(31,41,36,0.1); overflow: hidden; border: 1px solid #D8CFB8; }
.receipt-header { background: linear-gradient(135deg, #1F2924 0%, #15201B 60%, #1F2924 100%); padding: 40px 28px 28px; text-align: center; position: relative; }
.receipt-header::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, #C47649 0%, #4A6752 100%); }
.receipt-leaf { font-size: 1.4rem; color: #C47649; margin-bottom: 6px; }
.receipt-clinic-name { font-family: 'Fraunces', serif; font-size: 1.9rem; font-weight: 500; color: #FBF8F1; font-style: italic; letter-spacing: -0.02em; margin: 0; }
.receipt-clinic-sub { font-size: 0.68rem; color: #C47649; letter-spacing: 0.32em; text-transform: uppercase; margin-top: 10px; font-weight: 500; }
.receipt-gold-line { width: 50px; height: 1px; background: linear-gradient(90deg, transparent, #C47649, transparent); margin: 14px auto; }
.receipt-body { padding: 28px 32px 32px; }
.receipt-date-badge { background: #EFEAD9; border-radius: 2px; padding: 9px 14px; text-align: center; font-size: 0.7rem; color: #8A7E60; font-weight: 600; letter-spacing: 0.15em; margin-bottom: 24px; border-left: 3px solid #C47649; }
.receipt-section-title { font-family: 'Inter', sans-serif; font-size: 0.6rem; font-weight: 700; color: #C47649; text-transform: uppercase; letter-spacing: 0.2em; margin: 18px 0 10px; }
.receipt-row { display: flex; justify-content: space-between; align-items: center; margin: 9px 0; font-size: 0.88rem; }
.receipt-row span:first-child { color: #6B7A6F; font-weight: 400; }
.receipt-row span:last-child { color: #1F2924; font-weight: 600; }
.receipt-divider { border: none; border-top: 1px dashed #D8CFB8; margin: 18px 0; }
.receipt-total-box { background: linear-gradient(135deg, #1F2924, #15201B); border-radius: 4px; padding: 18px 22px; margin: 20px 0; position: relative; overflow: hidden; }
.receipt-total-box::before { content: ''; position: absolute; top: 0; right: 0; width: 100px; height: 100px; background: radial-gradient(circle, rgba(196,118,73,0.2), transparent 70%); }
.receipt-total-label { font-size: 0.62rem; color: #C47649; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; }
.receipt-total-amount { font-family: 'Fraunces', serif; font-size: 2rem; font-weight: 500; color: #FBF8F1; margin-top: 4px; letter-spacing: -0.02em; }
.receipt-discount { color: #B85C3A !important; }
.receipt-footer-area { text-align: center; padding-top: 12px; border-top: 1px dashed #D8CFB8; margin-top: 22px; }
.receipt-footer-text { font-size: 0.72rem; color: #8A7E60; margin: 4px 0; font-family: 'Fraunces', serif; font-style: italic; }
.receipt-footer-clinic { font-size: 0.75rem; color: #4A5A52; font-weight: 500; margin-top: 8px; }

/* Doctor intake form — apothecary aesthetic */
.doctor-form-card { background: #FBF8F1; border: 1px solid #D8CFB8; border-radius: 4px; padding: 32px 36px; margin-bottom: 24px; position: relative; }
.doctor-form-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: linear-gradient(90deg, #C47649 0%, #4A6752 100%); }

/* Pain scale slider — visual */
.pain-scale { display: flex; gap: 6px; margin-top: 8px; }
.pain-dot { flex: 1; height: 32px; border-radius: 2px; display: flex; align-items: center; justify-content: center; font-family: 'Fraunces', serif; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; border: 1px solid #D8CFB8; background: #FBF8F1; color: #8A7E60; }

/* Body area chips */
.body-chip { display: inline-block; padding: 6px 14px; margin: 4px; border-radius: 20px; font-size: 0.82rem; font-weight: 500; background: #EFEAD9; color: #4A5A52; border: 1px solid #D8CFB8; }

/* Misc */
.stMarkdown a { color: #C47649 !important; }
hr { border: none !important; border-top: 1px solid #D8CFB8 !important; margin: 28px 0 !important; }
.stCheckbox { color: #1F2924 !important; }
[data-baseweb="select"] * { color: #1F2924 !important; }
[data-testid="stDataFrame"] * { color: #1F2924 !important; }

/* Editorial divider */
.editorial-divider { display: flex; align-items: center; gap: 16px; margin: 32px 0; }
.editorial-divider::before, .editorial-divider::after { content: ''; flex: 1; height: 1px; background: #D8CFB8; }
.editorial-divider span { font-family: 'Fraunces', serif; font-style: italic; color: #8A7E60; font-size: 0.95rem; }

@media print { [data-testid="stSidebar"], .stTabs [data-baseweb="tab-list"], .stButton, .pulse-bar { display: none !important; } }
</style>
""", unsafe_allow_html=True)

# Currency
def fmt(amount):
    try: return f"{int(round(float(amount or 0))):,} IQD"
    except: return "0 IQD"

# Supabase
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
def page_header(kicker, title, desc=""):
    st.markdown(f'<div class="page-header"><div class="kicker">{kicker}</div><h1>{title}</h1>{f"<p>{desc}</p>" if desc else ""}</div>', unsafe_allow_html=True)

def render_receipt(r, cp):
    st.markdown(f"""<div class="receipt-wrap">
        <div class="receipt-header">
            <div class="receipt-leaf">❦</div>
            <div class="receipt-clinic-name">{cp.get('clinic_name','Garden Clinic')}</div>
            <div class="receipt-gold-line"></div>
            <div class="receipt-clinic-sub">{cp.get('tagline','Physical Therapy Center')}</div>
        </div>
        <div class="receipt-body">
            <div class="receipt-date-badge">OFFICIAL RECEIPT &nbsp;·&nbsp; {r['date']} &nbsp;·&nbsp; {datetime.now().strftime('%H:%M')}</div>
            <div class="receipt-section-title">Patient</div>
            <div class="receipt-row"><span>Name</span><span>{r['patient']}</span></div>
            <div class="receipt-row"><span>Doctor</span><span>{r['doctor']}</span></div>
            <hr class="receipt-divider">
            <div class="receipt-section-title">Service</div>
            <div class="receipt-row"><span>Item</span><span>{r['item']}</span></div>
            <div class="receipt-row"><span>Payment</span><span>{r['method']}</span></div>
            <hr class="receipt-divider">
            <div class="receipt-section-title">Payment Summary</div>
            <div class="receipt-row"><span>Base Price</span><span>{fmt(r['base'])}</span></div>
            <div class="receipt-row"><span class="receipt-discount">Discount</span><span class="receipt-discount">− {fmt(r['disc'])}</span></div>
            <div class="receipt-total-box"><div class="receipt-total-label">Total Paid</div><div class="receipt-total-amount">{fmt(r['net'])}</div></div>
            <div class="receipt-footer-area">
                {'<div class="receipt-footer-clinic">📍 ' + cp.get('address','') + '</div>' if cp.get('address') else ''}
                {'<div class="receipt-footer-clinic">📞 ' + cp.get('phone','') + '</div>' if cp.get('phone') else ''}
                {'<div class="receipt-footer-clinic">✉ ' + cp.get('email','') + '</div>' if cp.get('email') else ''}
                <div class="receipt-footer-text" style="margin-top:14px;">Thank you for choosing {cp.get('clinic_name','Garden Clinic')}</div>
                <div class="receipt-footer-text">We wish you a speedy recovery</div></div></div></div>""", unsafe_allow_html=True)

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
    st.markdown('<div class="login-card"><div class="leaf">❦</div><h1>Garden Clinic</h1><p>Sanctuary of Care</p></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.3,1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        lt, rt = st.tabs(["Sign In", "Create Account"])
        with lt:
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.button("Sign In", use_container_width=True):
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
                    chosen_doc_acc = st.selectbox("Which doctor is this account for?", list(doc_map_acc.keys()))
                    linked_doc_id = doc_map_acc[chosen_doc_acc]
                else: st.warning("⚠️ Add doctors in Settings first.")
            code = st.text_input("Admin code", type="password")
            if st.button("Create Account", use_container_width=True):
                if code != "1011": st.error("ASK MR.HARYAD TO CRATE ACCOUNT FOR YOU.")
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
<div style="padding:28px 20px 22px;border-bottom:1px solid rgba(232,227,214,0.08);">
    <div style="font-family:'Fraunces',serif;font-size:1.8rem;font-weight:500;font-style:italic;color:#FBF8F1;letter-spacing:-0.025em;">Garden Clinic</div>
    <div style="font-size:0.62rem;color:#C47649;margin-top:6px;font-weight:600;letter-spacing:0.25em;text-transform:uppercase;">Management System</div>
    <div style="width:30px;height:1px;background:#C47649;margin-top:10px;"></div>
</div>
<div style="padding:20px 20px;border-bottom:1px solid rgba(232,227,214,0.08);margin-bottom:12px;">
    <div style="font-size:0.6rem;color:#C47649;text-transform:uppercase;letter-spacing:0.22em;font-weight:600;">Signed in as</div>
    <div style="font-size:1.1rem;color:#FBF8F1;font-weight:500;margin-top:6px;font-family:'Fraunces',serif;font-style:italic;letter-spacing:-0.01em;">{username}</div>
    <div style="font-size:0.66rem;background:rgba(196,118,73,0.15);color:#C47649;display:inline-block;padding:4px 12px;border-radius:20px;margin-top:8px;font-weight:600;letter-spacing:0.08em;border:1px solid rgba(196,118,73,0.3);">{role}</div>
</div>""", unsafe_allow_html=True)

menu_map = {
    "Boss": ["📈  Dashboard","🖥️  Reception","📊  Accounting","📅  Appointments","📑  Reports","🔬  Research","👥  Accounts","⚙️  Settings"],
    "Reception & Accounting": ["🖥️  Reception","📊  Accounting","📅  Appointments","📑  Reports"],
    "Accounting": ["📊  Accounting","📑  Reports"],
    "Reception": ["🖥️  Reception","📅  Appointments"],
    "Doctor": ["🩺  Clinical Workspace"],
}
menus = menu_map.get(role, [])
selected = st.sidebar.radio("Navigation", menus, label_visibility="collapsed")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Sign Out", use_container_width=True):
    st.session_state.logged_in = False; st.rerun()

# ═══════════════════════════════════════════════
# DOCTOR CLINICAL WORKSPACE
# ═══════════════════════════════════════════════
if selected == "🩺  Clinical Workspace":
    if not linked_doctor_id:
        st.error("No doctor linked to this account. Contact admin."); st.stop()
    doc_info = sb_one("doctors", filters={"id": linked_doctor_id})
    page_header("Clinical Workspace", f"Dr. {doc_info['name'] if doc_info else 'Unknown'}", doc_info.get("specialty","") if doc_info else "")

    df_tabs = st.tabs(["Patient Assessment","Past Assessments"])

    with df_tabs[0]:
        section_label("Find Patient")
        ds_search = st.text_input("Search by name or phone", key="doc_search", placeholder="Type to search...")
        all_p_doc = sb_all("patients", order="name")
        if ds_search: all_p_doc = [p for p in all_p_doc if ds_search.lower() in (p.get("name","")).lower() or ds_search in (p.get("phone","") or "")]
        if all_p_doc:
            sel_pat_doc = st.selectbox("Select patient", ["— select —"]+[p["name"] for p in all_p_doc], key="doc_pat_sel")
            if sel_pat_doc != "— select —":
                pat_doc = next(p for p in all_p_doc if p["name"]==sel_pat_doc)
                pid_doc = pat_doc["id"]

                # Patient chip header bar (like reference but cleaner)
                age_text = ""
                if pat_doc.get("date_of_birth"):
                    try:
                        dob_y = int(pat_doc["date_of_birth"][:4])
                        age_text = f"{date.today().year - dob_y} yrs"
                    except: age_text = pat_doc.get("date_of_birth","")
                gender_icon = "♀" if pat_doc.get("gender")=="Female" else ("♂" if pat_doc.get("gender")=="Male" else "•")
                visits_count = sb_count("visits", filters={"patient_id": pid_doc})
                st.markdown(f"""<div class="patient-chip-bar">
                    <div class="patient-chip-name">{pat_doc["name"]}</div>
                    <span class="patient-chip">{gender_icon} {pat_doc.get("gender","—")}</span>
                    <span class="patient-chip">{age_text}</span>
                    <span class="patient-chip">📞 {pat_doc.get("phone","—")}</span>
                    <span class="patient-chip accent">{visits_count} visits</span>
                </div>""", unsafe_allow_html=True)

                # Past assessments preview
                prev_forms = sb_all("doctor_intake_form", filters={"patient_id": pid_doc}, order="id", desc_order=True)
                if prev_forms:
                    section_label(f"Previous Assessments ({len(prev_forms)})")
                    for f in prev_forms[:3]:
                        outcome_class = "tag-success" if f.get("outcome")=="Successfully Relieved" else ("tag-condition" if f.get("outcome") in ["No Improvement","Patient Discontinued"] else "tag-pending")
                        st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><div style="font-family:Fraunces,serif;font-style:italic;font-size:1.1rem;color:#1F2924;">{f.get("filled_date","")}</div><span class="tag-pill {outcome_class}">{f.get("outcome","Pending")}</span></div><div style="font-size:0.88rem;color:#1F2924;margin-bottom:8px;"><strong style="color:#C47649;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Diagnosis</strong><br/>{f.get("problem","—")}</div><div style="font-size:0.88rem;color:#1F2924;margin-bottom:8px;"><strong style="color:#C47649;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Body Area</strong> <span style="color:#4A5A52;">{f.get("body_area","—")}</span> · <strong style="color:#C47649;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Pain</strong> <span style="color:#4A5A52;">{f.get("pain_before","—")}/10 → {f.get("pain_after","—")}/10</span></div><div style="font-size:0.85rem;color:#6B7A6F;"><strong style="color:#C47649;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Plan</strong><br/>{f.get("treatment_plan","—")}</div></div>', unsafe_allow_html=True)

                st.markdown('<div class="editorial-divider"><span>New Assessment</span></div>', unsafe_allow_html=True)
                st.markdown('<div class="doctor-form-card">', unsafe_allow_html=True)

                # Patient complaint section
                section_label("Chief Complaint & History")
                c1, c2 = st.columns(2)
                with c1:
                    form_complaint = st.text_input("Chief Complaint", placeholder="e.g. Lower back pain", key="df_complaint")
                    form_duration = st.text_input("Duration", placeholder="e.g. 3 months", key="df_duration")
                with c2:
                    form_body_area = st.selectbox("Affected Body Area", ["— select —","Neck / Cervical","Upper back","Lower back / Lumbar","Shoulder","Elbow","Wrist / Hand","Hip","Knee","Ankle / Foot","Multiple areas","Other"], key="df_body")
                    form_onset = st.selectbox("Onset", ["— select —","Sudden / Trauma","Gradual","Post-surgery","Repetitive strain","Unknown"], key="df_onset")
                form_history = st.text_area("History of present illness", height=80, placeholder="Describe what happened, how it started, what makes it better/worse...", key="df_history")

                # Pain assessment
                section_label("Pain Assessment")
                pc1, pc2 = st.columns(2)
                with pc1: form_pain_before = st.slider("Pain level on first visit (0-10)", 0, 10, 5, key="df_pain_before")
                with pc2: form_pain_after = st.slider("Pain level after sessions (0-10)", 0, 10, 5, key="df_pain_after", help="Update this later as treatment progresses")

                # Clinical findings
                section_label("Clinical Findings")
                cf1, cf2 = st.columns(2)
                with cf1:
                    form_rom = st.text_area("Range of Motion / Movement notes", height=80, placeholder="ROM limitations, stiffness, weakness...", key="df_rom")
                with cf2:
                    form_red_flags = st.text_area("⚠️ Red Flags (refer to MD if any)", height=80, placeholder="Numbness, weakness, bladder issues, severe pain at night...", key="df_red_flags")

                # Diagnosis & plan
                section_label("Diagnosis & Treatment Plan")
                dc1, dc2 = st.columns(2)
                with dc1:
                    form_problem = st.text_area("Diagnosis / Problem", height=100, placeholder="What is wrong with the patient?", key="df_problem")
                with dc2:
                    form_plan = st.text_area("Treatment Plan & Expected Outcome", height=100, placeholder="What treatment will you provide and what is the expected outcome?", key="df_plan")

                # Sessions & outcome
                section_label("Treatment Plan")
                sc1, sc2, sc3 = st.columns(3)
                with sc1: form_sessions = st.number_input("Sessions Needed", min_value=1, max_value=200, step=1, value=10, key="df_sessions")
                with sc2: form_frequency = st.selectbox("Frequency", ["— select —","Daily","3x per week","2x per week","Weekly","Every 2 weeks","As needed"], key="df_freq")
                with sc3: form_outcome = st.selectbox("Expected Outcome", ["Pending","Full Recovery Expected","Partial Recovery Expected","Long-term Management","Other"], key="df_outcome")

                # Notes
                form_prev_treatment = st.text_area("Previous treatments tried (if any)", height=70, placeholder="Medications, physiotherapy elsewhere, injections, surgery, home exercises...", key="df_prev")
                form_notes = st.text_area("Additional clinical notes", height=70, placeholder="Any extra observations...", key="df_notes")

                st.markdown("</div>", unsafe_allow_html=True)

                if st.button("Save Assessment", use_container_width=True, key="btn_submit_assessment"):
                    if form_problem.strip() and form_plan.strip():
                        sb_insert("doctor_intake_form", {
                            "patient_id": pid_doc, "doctor_id": linked_doctor_id,
                            "chief_complaint": form_complaint.strip(),
                            "duration": form_duration.strip(),
                            "body_area": form_body_area if form_body_area != "— select —" else "",
                            "onset": form_onset if form_onset != "— select —" else "",
                            "history": form_history.strip(),
                            "pain_before": int(form_pain_before),
                            "pain_after": int(form_pain_after),
                            "range_of_motion": form_rom.strip(),
                            "red_flags": form_red_flags.strip(),
                            "problem": form_problem.strip(),
                            "treatment_plan": form_plan.strip(),
                            "sessions_needed": int(form_sessions),
                            "frequency": form_frequency if form_frequency != "— select —" else "",
                            "previous_treatment": form_prev_treatment.strip(),
                            "notes": form_notes.strip(),
                            "outcome": form_outcome,
                            "filled_date": today_str, "filled_by": username
                        })
                        existing_sess = sb_one("patient_sessions", filters={"patient_id": pid_doc})
                        if existing_sess:
                            sb_update("patient_sessions", {"total_sessions": int(form_sessions)}, "id", existing_sess["id"])
                        else:
                            sb_insert("patient_sessions", {"patient_id": pid_doc, "total_sessions": int(form_sessions),
                                "sessions_done": 0, "notes": form_problem.strip(), "added_by": username, "created_at": today_str})
                        log_action(username, "Doctor Assessment", f"Patient: {sel_pat_doc} | Dx: {form_problem[:50]}")
                        play_ding(); st.success("✓ Assessment saved. Reception can now check out the patient.")
                    else: st.error("Diagnosis and Treatment Plan are required.")
        else: st.info("No patients found.")

    with df_tabs[1]:
        section_label("My Assessments")
        my_forms = sb_all("doctor_intake_form", filters={"doctor_id": linked_doctor_id}, order="id", desc_order=True, limit=200)
        if my_forms:
            patients_map_df = {p["id"]: p["name"] for p in sb_all("patients")}
            opts_outcome = {f"#{f['id']} · {patients_map_df.get(f.get('patient_id'),'')} · {f.get('filled_date','')}": f["id"] for f in my_forms}
            section_label("Update Final Outcome")
            sel_outcome = st.selectbox("Select assessment", ["— select —"]+list(opts_outcome.keys()), key="upd_outcome_sel")
            if sel_outcome != "— select —":
                fid = opts_outcome[sel_outcome]
                fc1, fc2 = st.columns(2)
                with fc1: new_out = st.selectbox("Final Outcome", ["Pending","Successfully Relieved","Partially Improved","No Improvement","Patient Discontinued","Other"], key="new_out_sel")
                with fc2: new_pain = st.slider("Final pain level (0-10)", 0, 10, 0, key="new_pain_lvl")
                final_notes = st.text_area("Final notes / observations", key="final_notes")
                if st.button("Update Outcome", key="btn_upd_outcome"):
                    sb_update("doctor_intake_form", {"outcome": new_out, "outcome_notes": final_notes, "pain_after": new_pain}, "id", fid)
                    play_ding(); st.success("Outcome updated."); st.rerun()
            st.markdown("---")
            rows_df = [{"Date": f.get("filled_date",""), "Patient": patients_map_df.get(f.get("patient_id"),""),
                "Body Area": f.get("body_area",""), "Diagnosis": (f.get("problem","") or "")[:50],
                "Pain": f"{f.get('pain_before','—')}/10 → {f.get('pain_after','—')}/10",
                "Sessions": f.get("sessions_needed",0), "Outcome": f.get("outcome","Pending")} for f in my_forms]
            st.dataframe(pd.DataFrame(rows_df), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════
elif selected == "📈  Dashboard":
    page_header("Executive", f"{date.today().strftime('%A')}", f"{date.today().strftime('%B %d, %Y')}")
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
    with c3: st.markdown(card("Net Profit", fmt(net_profit), "dark", "Revenue minus all costs"), unsafe_allow_html=True)
    with c4: st.markdown(card("Doctor Commissions", fmt(total_commissions), "dark", "Total owed to doctors"), unsafe_allow_html=True)

    section_label("Today's Appointments")
    today_appts = [a for a in get_appointments_joined() if a.get("Date")==today_str]
    if today_appts:
        cols = st.columns(min(len(today_appts),4))
        for i, a in enumerate(today_appts[:4]):
            with cols[i%4]:
                sc = {"Scheduled":"#C47649","Completed":"#4A6752","Cancelled":"#B85C3A","No-show":"#8A7E60"}.get(a["Status"],"#C47649")
                st.markdown(f'<div class="card" style="border-left:3px solid {sc};"><div style="font-family:Inter,sans-serif;font-size:0.65rem;color:#8A7E60;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;">{a["Time"]}</div><div style="font-family:Fraunces,serif;font-size:1.3rem;font-style:italic;color:#1F2924;margin:6px 0;letter-spacing:-0.01em;">{a["Patient"]}</div><div style="font-size:0.85rem;color:#4A5A52;">Dr. {a["Doctor"]}</div><div style="font-size:0.78rem;color:#8A7E60;margin-top:4px;font-style:italic;">{a.get("Reason","")}</div><span class="tag-pill" style="background:{sc}25;color:{sc};margin-top:8px;display:inline-block;">{a["Status"]}</span></div>', unsafe_allow_html=True)
    else: st.info("No appointments scheduled for today.")

    ca,cb = st.columns([3,2])
    with ca:
        section_label("Revenue Trend")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df = pd.DataFrame([{"Date":v["visit_date"],"Revenue":float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df.groupby("Date").sum(), y="Revenue", color="#C47649", height=260)
    with cb:
        section_label("Doctor Performance")
        all_tiers = sb_all("doctor_commission_tiers"); rows = []
        for d in sb_all("doctors", order="name"):
            info = doc_visits.get(d["name"],{"visits":[],"id":d["id"]})
            v = info["visits"]; vol = len(v); gen = sum(v)
            rate = get_doc_commission_rate(d["id"], vol, all_tiers)
            payout = gen * rate
            tiers_for_doc = sorted([t for t in all_tiers if t.get("doctor_id")==d["id"]], key=lambda x:x.get("min_visits",0))
            model = " / ".join([f"{t['min_visits']}+: {t['commission_rate']}%" for t in tiers_for_doc]) if tiers_for_doc else "—"
            rows.append({"Doctor":d["name"],"Visits":vol,"Revenue":fmt(gen),"Commission":fmt(payout),"Tiers":model})
        if rows: st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    section_label("Monthly Summary")
    all_v2 = sb_all("visits")
    if all_v2:
        df_m = pd.DataFrame([{"Month":v["visit_date"][:7],"Revenue":float(v.get("net_paid") or 0)} for v in all_v2])
        df_m_agg = df_m.groupby("Month").agg(Revenue=("Revenue","sum"),Visits=("Revenue","count")).reset_index().sort_values("Month",ascending=False)
        df_m_agg["Revenue"] = df_m_agg["Revenue"].apply(fmt)
        st.dataframe(df_m_agg, use_container_width=True, hide_index=True)

    section_label("Activity Log")
    af = st.selectbox("Filter",["All","New Visit","New Patient","Doctor Assessment","Add Expense","Delete Expense","Remove Patient"], key="audit_filter")
    audit_rows = sb_all("audit_log", order="id", desc_order=True, limit=200)
    if af != "All": audit_rows = [r for r in audit_rows if r.get("action")==af]
    if audit_rows:
        st.dataframe(pd.DataFrame([{"Time":r["timestamp"],"User":r["username"],"Action":r["action"],"Details":r.get("details","")} for r in audit_rows]), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════
# RECEPTION
# ═══════════════════════════════════════════════
elif selected == "🖥️  Reception":
    page_header("Front Desk", "Reception", "Patient intake, checkout, and management.")
    pulse_bar([("Today's Revenue",fmt(today_revenue)),("Visits Today",str(today_visits_count)),("Total Patients",str(patient_count))])

    all_pt_subs = sb_all("patient_subscriptions")
    expiring_rec = [s for s in all_pt_subs if s.get("status")=="Active" and s.get("end_date") in [today_str, tomorrow_str]]
    if expiring_rec:
        patients_map_r = {p["id"]: p["name"] for p in sb_all("patients")}
        for s in expiring_rec:
            pname = patients_map_r.get(s.get("patient_id"),"Unknown")
            st.warning(f"⚠️ **{pname}** subscription **'{s.get('plan_name','')}'** expires {'TODAY' if s.get('end_date')==today_str else 'TOMORROW'}!")

    t1,t2,tD,tQ,t3,t4,t5,t6,t7,t8,t9 = st.tabs(["Checkout","Patients","Doctor Notes","Quick View","Register","Edit","Sessions","Subscriptions","Check-in","History","Edit/Delete"])

    with t1:
        section_label("New Checkout")
        patients_db = sb_all("patients", order="name"); docs_db = sb_all("doctors", order="name")
        services_db = [s for s in sb_all("services", order="name") if s.get("active")==1]
        bundles_db  = sb_all("bundles", order="name")
        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please add doctors and services in Settings before checkout.")
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
                disc_val = st.number_input("Discount value", min_value=0.0, step=1000.0)

            if target_p != "— select —":
                pid_chk = p_map[target_p]
                assessment = sb_one("doctor_intake_form", filters={"patient_id": pid_chk})
                sess_chk = sb_one("patient_sessions", filters={"patient_id": pid_chk})
                if assessment:
                    rem = max(0, int(sess_chk.get("total_sessions",0) or 0) - int(sess_chk.get("sessions_done",0) or 0)) if sess_chk else "—"
                    done_count = sess_chk.get("sessions_done",0) if sess_chk else 0
                    total_count = assessment.get("sessions_needed",0)
                    st.markdown(f'<div class="card" style="border-left:3px solid #4A6752;"><div style="font-size:0.65rem;color:#4A6752;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;">Doctor\'s Plan</div><div style="margin-top:8px;font-family:Fraunces,serif;font-size:1.1rem;font-style:italic;color:#1F2924;">{assessment.get("problem","")}</div><div style="margin-top:6px;font-size:0.88rem;color:#4A5A52;">Sessions: <strong>{done_count}/{total_count}</strong> · Remaining: <strong>{rem}</strong> · Body area: {assessment.get("body_area","—")}</div></div>', unsafe_allow_html=True)

            final_due = base_price
            if disc_type == "Fixed (IQD)": final_due = max(0.0, base_price-disc_val)
            elif disc_type == "Percent (%)": final_due = max(0.0, base_price*(1-disc_val/100))
            visit_notes = st.text_area("Visit notes", height=70)
            referrers_db = sb_all("referrers", order="name"); ref_names = [r["name"] for r in referrers_db]
            referral_options = ["Walk-in / Direct","Instagram / Social Media","Google Search","Friend / Word of mouth"]+ref_names
            how_found = st.selectbox("How did the patient find us?", referral_options)
            referred_by_val = how_found if how_found in ref_names else None
            st.markdown(f'<div style="font-family:Fraunces,serif;font-size:1.8rem;font-style:italic;color:#1F2924;margin:20px 0;">Total due: <strong style="color:#C47649;">{fmt(final_due)}</strong></div>', unsafe_allow_html=True)
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

    with t2:
        section_label("All Patients")
        search = st.text_input("Search by name or phone", key="t2_search")
        all_p = sb_all("patients", order="name")
        if search: all_p = [p for p in all_p if search.lower() in (p.get("name","")).lower() or search in (p.get("phone","") or "")]
        if all_p:
            st.dataframe(pd.DataFrame(all_p), use_container_width=True, hide_index=True)
            del_target = st.selectbox("Remove patient", ["— select —"]+[p["name"] for p in all_p])
            if st.button("Remove Patient", type="primary"):
                if del_target != "— select —":
                    sb_delete("patients","name",del_target); log_action(username,"Remove Patient",del_target)
                    play_ding(); st.success(f"Removed."); st.rerun()

    with tD:
        section_label("Doctor's Assessments")
        df_search = st.text_input("Search by patient name", key="recep_df_search")
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
                    rem_text = f"{done_f} of {total_f} sessions"
                outcome_class = "tag-success" if f.get("outcome")=="Successfully Relieved" else ("tag-condition" if f.get("outcome") in ["No Improvement","Patient Discontinued"] else "tag-pending")
                st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-family:Fraunces,serif;font-size:1.4rem;font-style:italic;color:#1F2924;letter-spacing:-0.01em;">{pname}</div><span class="tag-pill {outcome_class}">{f.get("outcome","Pending")}</span></div><div style="font-size:0.75rem;color:#8A7E60;margin-top:6px;font-family:Inter,sans-serif;letter-spacing:0.04em;">Dr. {dname} · {f.get("filled_date","")} · {rem_text}</div><div style="margin-top:14px;display:flex;flex-wrap:wrap;gap:6px;">{f"<span class=patient-chip>{f.get('body_area','')}</span>" if f.get('body_area') else ''}{f"<span class=patient-chip>{f.get('duration','')}</span>" if f.get('duration') else ''}{f"<span class=patient-chip accent>Pain: {f.get('pain_before','—')}/10</span>"}</div><div style="margin-top:14px;font-size:0.9rem;color:#1F2924;"><strong style="color:#C47649;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Diagnosis</strong><br/>{f.get("problem","—")}</div><div style="margin-top:10px;font-size:0.88rem;color:#4A5A52;"><strong style="color:#C47649;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Treatment Plan</strong><br/>{f.get("treatment_plan","—")}</div>{f"<div style=margin-top:10px;font-size:0.85rem;color:#B85C3A;><strong style=color:#B85C3A;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;>Red Flags</strong><br/>{f.get('red_flags','')}</div>" if f.get("red_flags") else ""}</div>', unsafe_allow_html=True)
        else: st.info("No doctor assessments yet.")

    with tQ:
        section_label("Patient Quick View")
        all_p_qv = sb_all("patients", order="name")
        if all_p_qv:
            qv_search = st.text_input("Search patient", key="qv_search")
            filtered = [p for p in all_p_qv if not qv_search or qv_search.lower() in (p.get("name","")).lower() or qv_search in (p.get("phone","") or "")]
            if filtered:
                qv_sel = st.selectbox("Select patient", [p["name"] for p in filtered], key="qv_sel")
                pat = next(p for p in filtered if p["name"]==qv_sel); pid = pat["id"]
                st.markdown(f'<div class="profile-summary"><div class="profile-kicker">Patient Profile</div><div class="profile-name">{pat["name"]}</div><div class="profile-meta">📞 {pat.get("phone","—")} &nbsp;·&nbsp; 🎂 {pat.get("date_of_birth","—")} &nbsp;·&nbsp; {pat.get("gender","—")}</div></div>', unsafe_allow_html=True)
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
                assessment_q = sb_one("doctor_intake_form", filters={"patient_id": pid})
                if assessment_q:
                    section_label("Doctor's Assessment")
                    st.markdown(f'<div class="card"><div style="font-size:0.88rem;color:#1F2924;"><strong style="color:#C47649;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Problem</strong><br/>{assessment_q.get("problem","")}</div><div style="margin-top:10px;font-size:0.88rem;color:#1F2924;"><strong style="color:#C47649;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Plan</strong><br/>{assessment_q.get("treatment_plan","")}</div><div style="margin-top:10px;font-size:0.85rem;color:#4A5A52;">Outcome: {assessment_q.get("outcome","Pending")} · Pain: {assessment_q.get("pain_before","—")}/10 → {assessment_q.get("pain_after","—")}/10</div></div>', unsafe_allow_html=True)
                if sess_p:
                    done = int(sess_p.get("sessions_done") or 0); total = int(sess_p.get("total_sessions") or 0)
                    rem = max(0, total-done); pct = int((done/total*100)) if total>0 else 0
                    section_label("Sessions Progress")
                    st.markdown(f'**{done} of {total} done** · {rem} remaining')
                    st.markdown(f'<div class="session-bar-wrap"><div class="session-bar-fill" style="width:{pct}%;"></div></div>', unsafe_allow_html=True)
                if sub_active:
                    section_label("Active Subscription")
                    st.info(f"📅 **{sub_active.get('plan_name','')}** · Expires {sub_active.get('end_date','')} · {sub_active.get('sessions_used',0)}/{sub_active.get('total_sessions','∞')} sessions")
                if visits_p:
                    section_label("Recent Visits")
                    df_v_qv = pd.DataFrame(visits_p[:10])
                    for col in ["Base","Discount","Paid"]:
                        if col in df_v_qv.columns: df_v_qv[col] = df_v_qv[col].apply(fmt)
                    st.dataframe(df_v_qv, use_container_width=True, hide_index=True)

    with t3:
        section_label("Register New Patient")
        c1,c2 = st.columns(2)
        with c1:
            p_name = st.text_input("Full name *"); p_phone = st.text_input("Phone number")
            p_dob  = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1990-01-15")
        with c2:
            p_gender = st.selectbox("Gender", ["Prefer not to say","Male","Female","Other"])
            p_notes  = st.text_area("Notes", height=100)
        give_receipt = st.checkbox("📄 Print intake receipt", value=True)
        if st.button("Register Patient"):
            if p_name.strip():
                if sb_exists("patients","name",p_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("patients",{"name":p_name.strip(),"phone":p_phone.strip(),"date_of_birth":p_dob.strip(),"gender":p_gender,"notes":p_notes.strip(),"created_at":today_str})
                    log_action(username,"New Patient",f"{p_name.strip()} | {p_gender}")
                    play_ding(); st.success(f"Patient '{p_name}' registered.")
                    if give_receipt:
                        st.session_state.intake_rcpt = {"patient":p_name.strip(),"doctor":"To be assigned","item":"Initial Intake","base":0,"disc":0,"net":0,"method":"—","date":today_str}
        if "intake_rcpt" in st.session_state: render_receipt(st.session_state.intake_rcpt, get_clinic_profile())

    with t4:
        section_label("Edit Patient Profile")
        ep_search = st.text_input("Search", key="ep_search")
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
                    play_ding(); st.success("Updated."); st.rerun()

    with t5:
        section_label("Sessions Tracker")
        s_search = st.text_input("Search", key="sess_search")
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
                    cc1.metric("Total Sessions", total); cc2.metric("Done", done); cc3.metric("Remaining", rem)
                    st.markdown(f'<div class="session-bar-wrap"><div class="session-bar-fill" style="width:{pct}%;"></div></div>', unsafe_allow_html=True)
                    c1,c2 = st.columns(2)
                    with c1:
                        new_total = st.number_input("Total sessions", min_value=0, step=1, value=total, key="sess_total")
                        new_done = st.number_input("Sessions done", min_value=0, step=1, value=done, key="sess_done")
                    with c2:
                        new_sess_notes = st.text_area("Notes", value=sess.get("notes","") or "", height=80, key="sess_notes")
                    if st.button("Update", key="btn_update_sess"):
                        sb_update("patient_sessions",{"total_sessions":new_total,"sessions_done":new_done,"notes":new_sess_notes},"id",sess["id"])
                        play_ding(); st.success("Updated."); st.rerun()
                else:
                    st.info("No session plan yet.")
                    c1,c2 = st.columns(2)
                    with c1: new_total_s = st.number_input("Total sessions", min_value=1, step=1, value=10, key="new_sess_total")
                    with c2: new_sess_n = st.text_area("Notes", height=80, key="new_sess_notes")
                    if st.button("Create Plan", key="btn_create_sess"):
                        sb_insert("patient_sessions",{"patient_id":pid,"total_sessions":new_total_s,"sessions_done":0,"notes":new_sess_n,"added_by":username,"created_at":today_str})
                        play_ding(); st.success("Created."); st.rerun()

    with t6:
        section_label("Patient Subscriptions")
        all_p_sub = sb_all("patients", order="name")
        if all_p_sub:
            sub_tabs = st.tabs(["Create","Manage"])
            with sub_tabs[0]:
                p_map_sub = {p["name"]: p["id"] for p in all_p_sub}
                c1,c2 = st.columns(2)
                with c1:
                    sub_patient = st.selectbox("Patient", list(p_map_sub.keys()), key="sub_pat_sel")
                    sub_plan = st.text_input("Plan name", key="sub_plan_name")
                    sub_type = st.selectbox("Type", ["Monthly","Weekly","Custom (days)"], key="sub_plan_type")
                with c2:
                    sub_price = st.number_input("Price (IQD)", min_value=0.0, step=5000.0, key="sub_price")
                    sub_sessions = st.number_input("Sessions (0=unlimited)", min_value=0, step=1, value=0, key="sub_sessions")
                    sub_start = st.date_input("Start date", value=date.today(), key="sub_start")
                    if sub_type == "Monthly": sub_end = sub_start + timedelta(days=30)
                    elif sub_type == "Weekly": sub_end = sub_start + timedelta(days=7)
                    else:
                        sub_days = st.number_input("Days", min_value=1, step=1, value=30, key="sub_days")
                        sub_end = sub_start + timedelta(days=int(sub_days))
                    st.info(f"Expires: **{sub_end}**")
                if st.button("Create & Print Receipt", key="btn_create_sub"):
                    if sub_plan.strip() and sub_price > 0:
                        sb_insert("patient_subscriptions",{"patient_id":p_map_sub[sub_patient],"plan_name":sub_plan.strip(),"plan_type":sub_type,"total_sessions":int(sub_sessions),"sessions_used":0,"price":sub_price,"start_date":str(sub_start),"end_date":str(sub_end),"status":"Active","added_by":username,"created_at":today_str})
                        docs_for_sub = sb_all("doctors", order="name")
                        doc_id_sub = docs_for_sub[0]["id"] if docs_for_sub else None
                        if doc_id_sub:
                            sb_insert("visits",{"patient_id":p_map_sub[sub_patient],"doctor_id":doc_id_sub,"service_id":None,"bundle_id":None,"visit_date":today_str,"base_price":sub_price,"discount_amount":0,"net_paid":sub_price,"payment_method":"Subscription","notes":f"Subscription: {sub_plan.strip()}","referred_by":None,"added_by":username})
                        log_action(username,"Create Subscription",f"{sub_patient} | {fmt(sub_price)}")
                        play_ding(); st.success("Created!")
                        st.session_state.sub_rcpt = {"patient":sub_patient,"item":sub_plan,"base":sub_price,"disc":0.0,"net":sub_price,"method":"Subscription","date":today_str,"doctor":"—"}
                if "sub_rcpt" in st.session_state: render_receipt(st.session_state.sub_rcpt, get_clinic_profile())
            with sub_tabs[1]:
                sm_search = st.text_input("Search", key="sm_search")
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
                            play_ding(); st.success("Updated."); st.rerun()
                        if st.button("Delete", type="primary", key="btn_del_sub"):
                            sb_delete("patient_subscriptions","id",sid); st.rerun()

    with t7:
        section_label("Gym Check-in")
        all_p_checkin = sb_all("patients", order="name")
        active_subs_map = {}
        for s in sb_all("patient_subscriptions", filters={"status":"Active"}):
            active_subs_map.setdefault(s["patient_id"], []).append(s)
        patients_with_sub = [p for p in all_p_checkin if p["id"] in active_subs_map]
        if patients_with_sub:
            ci_search = st.text_input("Search", key="ci_search")
            filtered_ci = [p for p in patients_with_sub if not ci_search or ci_search.lower() in (p.get("name","")).lower()]
            ci_patient = st.selectbox("Select", ["— select —"]+[p["name"] for p in filtered_ci], key="checkin_sel")
            if ci_patient != "— select —":
                pid_ci = next(p["id"] for p in filtered_ci if p["name"]==ci_patient)
                subs_for_pat = active_subs_map[pid_ci]
                for s in subs_for_pat:
                    total_s = int(s.get("total_sessions") or 0); used_s = int(s.get("sessions_used") or 0)
                    rem_s = (total_s - used_s) if total_s>0 else "∞"
                    st.markdown(f'<div class="card" style="border-left:3px solid #C47649;"><strong>{s.get("plan_name","")}</strong> · Expires {s.get("end_date","")} · {used_s}/{total_s if total_s>0 else "∞"} · Remaining: {rem_s}</div>', unsafe_allow_html=True)
                if st.button(f"Check In {ci_patient}", use_container_width=True, key="btn_checkin"):
                    sub_to_use = subs_for_pat[0]
                    new_used = int(sub_to_use.get("sessions_used") or 0) + 1
                    sb_update("patient_subscriptions",{"sessions_used":new_used},"id",sub_to_use["id"])
                    sb_insert("gym_checkins",{"subscription_id":sub_to_use["id"],"patient_id":pid_ci,"checkin_date":today_str,"added_by":username})
                    log_action(username,"Gym Check-in",f"{ci_patient}")
                    play_ding(); st.success(f"✓ Checked in!")
        else: st.info("No patients with active subscriptions.")

    with t8:
        section_label("Visit History")
        vh_search = st.text_input("Search", key="vh_search")
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

    with t9:
        ed1, ed2 = st.tabs(["Delete","Edit"])
        with ed1:
            st.warning("⚠️ For corrections only.")
            dv_search = st.text_input("Search", key="dv_search")
            all_visits_j = get_visits_joined(limit=200)
            if dv_search: all_visits_j = [v for v in all_visits_j if dv_search.lower() in v.get("Patient","").lower()]
            if all_visits_j:
                df_dv = pd.DataFrame(all_visits_j)
                for col in ["Base","Discount","Paid"]:
                    if col in df_dv.columns: df_dv[col] = df_dv[col].apply(fmt)
                st.dataframe(df_dv, use_container_width=True, hide_index=True)
                void_id = st.number_input("Visit ID to delete", min_value=1, step=1, key="void_id")
                if st.button("Delete Visit", type="primary", key="btn_del_visit"):
                    sb_delete("visits","id",void_id); play_ding(); st.success("Deleted."); st.rerun()
        with ed2:
            ev_search = st.text_input("Search", key="ev_search")
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
                            new_v_base = st.number_input("Base", min_value=0.0, step=1000.0, value=float(visit_rec.get("base_price") or 0), key="ev_base")
                            new_v_disc = st.number_input("Discount", min_value=0.0, step=1000.0, value=float(visit_rec.get("discount_amount") or 0), key="ev_disc")
                        with c2:
                            new_v_paid = st.number_input("Paid", min_value=0.0, step=1000.0, value=float(visit_rec.get("net_paid") or 0), key="ev_paid")
                            mopts = ["Cash","Card","Insurance","Transfer","Subscription"]
                            cm = visit_rec.get("payment_method","Cash") or "Cash"
                            new_v_method = st.selectbox("Payment", mopts, index=mopts.index(cm) if cm in mopts else 0, key="ev_method")
                            new_v_notes = st.text_area("Notes", value=visit_rec.get("notes","") or "", height=80, key="ev_notes")
                        if st.button("Save", key="btn_edit_visit"):
                            sb_update("visits",{"visit_date":new_v_date,"base_price":new_v_base,"discount_amount":new_v_disc,"net_paid":new_v_paid,"payment_method":new_v_method,"notes":new_v_notes},"id",vid)
                            play_ding(); st.success("Updated."); st.rerun()
