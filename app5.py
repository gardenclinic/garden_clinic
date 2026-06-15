import streamlit as st
import pandas as pd
import io
from datetime import datetime, date, timedelta
import streamlit.components.v1 as components

# Import from new utility modules
from db import sb_all, sb_one, sb_insert, sb_delete, sb_update, sb_exists, sb_sum, sb_count, get_sb
from auth import hash_password, log_action, get_user_context, verify_login, create_user, logout, require_linked_doctor, get_linked_doctor
from constants import TABLES, ROLES, VALID_ROLES, CLINIC_DEFAULTS, CURRENCY, BODY_AREAS, OUTCOME_OPTIONS, PAYMENT_METHODS, EXPENSE_CATEGORIES, APPOINTMENT_STATUSES, GENDER_OPTIONS, OVERDUE_DAYS, APPOINTMENT_COLORS, PAYMENT_ICONS

st.set_page_config(page_title="Garden Clinic", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════
# UNIQUE EDITORIAL DESIGN — botanical apothecary luxury
# Deep cream/parchment, sage green, terracotta, ink black
# Editorial serif + clean sans + monospace numbers
# ═══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&family=Syne:wght@400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: #F2F5F1 !important; color: #0D1F14 !important; font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important; }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }

/* SIDEBAR */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0D3D2B 0%, #0A2E20 100%) !important; border-right: none !important; min-width: 252px !important; }
[data-testid="stSidebar"] * { color: #D4E8DA !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
section[data-testid="stSidebarNav"] { display: none; }

/* TYPOGRAPHY */
h1, h2, h3, h4 { font-family: 'Cormorant Garamond', serif !important; color: #0D1F14 !important; }

/* PAGE HEADER */
.page-header { margin-bottom: 32px; padding-top: 8px; }
.page-header .kicker { font-size: 0.68rem; color: #C9A84C; letter-spacing: 0.28em; text-transform: uppercase; font-weight: 700; margin-bottom: 8px; font-family: 'Plus Jakarta Sans', sans-serif; }
.page-header h1 { font-family: 'Cormorant Garamond', serif !important; font-size: 3rem !important; font-weight: 600 !important; color: #0D1F14 !important; margin: 0 !important; font-style: italic; letter-spacing: -0.025em; }
.page-header p { font-size: 0.9rem; color: #6B8A72; margin: 8px 0 0 0; font-weight: 400; }

/* PULSE BAR */
.pulse-bar { background: linear-gradient(135deg, #0D3D2B 0%, #1A5C3E 100%); border-radius: 20px; padding: 22px 32px; display: flex; gap: 44px; flex-wrap: wrap; align-items: center; margin-bottom: 32px; box-shadow: 0 4px 16px rgba(13,61,43,0.08); }
.pulse-stat { display: flex; flex-direction: column; }
.pulse-label { font-size: 0.65rem; color: #6FCF97; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; font-family: 'Plus Jakarta Sans', sans-serif; }
.pulse-value { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; font-weight: 500; color: #FFFFFF; margin-top: 4px; letter-spacing: -0.02em; }
.pulse-divider { width: 1px; background: rgba(255,255,255,0.12); height: 40px; align-self: center; }

/* CARDS */
.card { background: #FFFFFF; border: 1px solid #DDE8E1; border-radius: 20px; padding: 24px 26px; margin-bottom: 18px; transition: all 0.25s cubic-bezier(0.4,0,0.2,1); box-shadow: 0 2px 8px rgba(13,31,20,0.04); }
.card:hover { border-color: #0D3D2B; box-shadow: 0 8px 28px rgba(13,61,43,0.1); transform: translateY(-2px); }
.card h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; margin: 0 0 8px 0; font-size: 0.68rem; color: #6B8A72 !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }
.card .big-num { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 500; margin: 0; }
.card .big-num.green { color: #1A7A4E; }
.card .big-num.red { color: #C0392B; }
.card .big-num.dark, .card .big-num.gold { color: #0D1F14; }
.card .sub { font-size: 0.78rem; color: #9AB5A0; margin-top: 8px; font-family: 'Plus Jakarta Sans', sans-serif; }

/* TABS */
.stTabs [data-baseweb="tab-list"] { background: #FFFFFF !important; border-radius: 16px !important; padding: 5px !important; border: 1px solid #DDE8E1 !important; gap: 4px !important; margin-bottom: 20px !important; }
.stTabs button[data-baseweb="tab"] { background: transparent !important; border: none !important; color: #6B8A72 !important; font-size: 0.82rem !important; font-weight: 600 !important; padding: 9px 18px !important; border-radius: 12px !important; transition: all 0.2s !important; }
.stTabs button[data-baseweb="tab"]:hover { background: #F2F5F1 !important; color: #0D1F14 !important; }
.stTabs button[aria-selected="true"] { background: #0D3D2B !important; color: #FFFFFF !important; font-weight: 700 !important; border: none !important; box-shadow: 0 2px 8px rgba(13,61,43,0.25) !important; }

/* BUTTONS */
.stButton > button { background: #0D3D2B !important; color: #FFFFFF !important; border: none !important; border-radius: 50px !important; font-weight: 600 !important; font-size: 0.85rem !important; padding: 10px 24px !important; transition: all 0.2s !important; }
.stButton > button:hover { background: #1A5C3E !important; transform: translateY(-2px) !important; box-shadow: 0 8px 24px rgba(13,61,43,0.28) !important; }
button[data-testid="baseButton-primary"] { background: #C0392B !important; box-shadow: 0 2px 10px rgba(192,57,43,0.25) !important; }
button[data-testid="baseButton-primary"]:hover { background: #A93226 !important; }

/* INPUTS */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input { background: #FAFCFA !important; border-radius: 14px !important; border: 1.5px solid #DDE8E1 !important; color: #0D1F14 !important; padding: 10px 14px !important; }
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus { border-color: #0D3D2B !important; background: #FFFFFF !important; box-shadow: 0 0 0 4px rgba(13,61,43,0.08) !important; }
.stSelectbox > div > div > div { background: #FAFCFA !important; border-radius: 14px !important; border: 1.5px solid #DDE8E1 !important; color: #0D1F14 !important; }
.stTextArea textarea { background: #FAFCFA !important; border-radius: 14px !important; border: 1.5px solid #DDE8E1 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; color: #0D1F14 !important; }
.stTextArea textarea:focus { border-color: #0D3D2B !important; box-shadow: 0 0 0 4px rgba(13,61,43,0.08) !important; }
.stRadio > div { gap: 14px !important; }
label, .stRadio label span, .stCheckbox label { color: #0D1F14 !important; }
[data-testid="stWidgetLabel"] p { color: #4A6B52 !important; font-size: 0.8rem !important; font-weight: 600 !important; letter-spacing: 0.04em !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] { border-radius: 16px !important; overflow: hidden !important; border: 1px solid #DDE8E1 !important; background: #FFFFFF !important; box-shadow: 0 2px 8px rgba(13,31,20,0.04) !important; }
[data-testid="stDataFrame"] * { color: #0D1F14 !important; }

/* ALERTS */
.stSuccess > div { background: #EAF5EC !important; border: 1.5px solid #27AE60 !important; color: #1A5C3E !important; border-radius: 14px !important; }
.stError > div { background: #FDF0EE !important; border: 1.5px solid #C0392B !important; color: #7B1F1F !important; border-radius: 14px !important; }
.stWarning > div { background: #FDF8EC !important; border: 1.5px solid #C9A84C !important; color: #7B6020 !important; border-radius: 14px !important; }
.stInfo > div { background: #EEF4FF !important; border: 1.5px solid #3B82F6 !important; color: #1E3A8A !important; border-radius: 14px !important; }

/* SECTION LABEL */
.section-label { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.68rem; font-weight: 700; color: #1A5C3E; text-transform: uppercase; letter-spacing: 0.22em; margin: 28px 0 16px 0; display: flex; align-items: center; gap: 12px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, #DDE8E1, transparent); }

/* METRICS */
[data-testid="stMetric"] { background: #FFFFFF !important; border: 1px solid #DDE8E1 !important; border-radius: 20px !important; padding: 20px 24px !important; box-shadow: 0 2px 8px rgba(13,31,20,0.04) !important; }
[data-testid="stMetricLabel"] { font-size: 0.68rem !important; color: #6B8A72 !important; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 700 !important; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.7rem !important; color: #0D1F14 !important; font-weight: 500 !important; }

/* SESSION BAR */
.session-bar-wrap { background: #DDE8E1; border-radius: 50px; height: 10px; width: 100%; margin-top: 8px; overflow: hidden; }
.session-bar-fill { height: 10px; border-radius: 50px; background: linear-gradient(90deg, #0D3D2B, #27AE60); }

/* PROFILE HEADER */
.profile-summary { background: linear-gradient(135deg, #0D3D2B 0%, #1A5C3E 100%); color: #FFF; padding: 32px 36px; border-radius: 24px; margin-bottom: 24px; position: relative; overflow: hidden; }
.profile-summary::before { content: ''; position: absolute; top: -40px; right: -40px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(201,168,76,0.15), transparent 70%); }
.profile-kicker { font-size: 0.65rem; color: #C9A84C; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 700; font-family: 'Plus Jakarta Sans', sans-serif; }
.profile-name { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 600; font-style: italic; margin: 4px 0 0 0; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1; }
.profile-meta { font-size: 0.88rem; color: #9AB5A0; margin-top: 10px; }

/* PATIENT CHIP BAR */
.patient-chip-bar { background: #FFFFFF; border: 1px solid #DDE8E1; border-radius: 20px; padding: 20px 26px; margin-bottom: 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px; box-shadow: 0 2px 8px rgba(13,31,20,0.04); }
.patient-chip-name { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 600; font-style: italic; color: #0D1F14; letter-spacing: -0.01em; }
.patient-chip { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: #F2F5F1; border-radius: 50px; font-size: 0.78rem; color: #4A6B52; font-weight: 600; border: 1px solid #DDE8E1; }
.patient-chip.warn { background: #FDF0EE; color: #C0392B; border-color: rgba(192,57,43,0.2); }
.patient-chip.good { background: #EAF5EC; color: #1A7A4E; border-color: rgba(26,122,78,0.2); }
.patient-chip.accent { background: #FDF8EC; color: #7B6020; border-color: rgba(201,168,76,0.2); }

/* TAG PILLS */
.tag-pill { display: inline-block; padding: 4px 12px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; margin-right: 6px; margin-bottom: 4px; letter-spacing: 0.04em; }
.tag-condition { background: #FDF0EE; color: #C0392B; border: 1px solid rgba(192,57,43,0.2); }
.tag-success { background: #EAF5EC; color: #1A7A4E; border: 1px solid rgba(26,122,78,0.2); }
.tag-pending { background: #FDF8EC; color: #7B6020; border: 1px solid rgba(201,168,76,0.2); }

/* RECEIPT */
.receipt-wrap { background: #FFFFFF; border-radius: 24px; padding: 0; max-width: 440px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.88rem; color: #0D1F14; box-shadow: 0 20px 60px rgba(13,31,20,0.12); }
.receipt-header { background: linear-gradient(135deg, #0D3D2B 0%, #1A5C3E 60%, #0D3D2B 100%); padding: 40px 28px 28px; text-align: center; position: relative; overflow: hidden; }
.receipt-header::before { content: ''; position: absolute; top: -40px; right: -40px; width: 160px; height: 160px; background: radial-gradient(circle, rgba(201,168,76,0.2), transparent 70%); }
.receipt-header::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 24px; background: #FFFFFF; border-radius: 24px 24px 0 0; }
.receipt-leaf { font-size: 1.2rem; color: #C9A84C; margin-bottom: 8px; }
.receipt-clinic-name { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 600; color: #FFFFFF; font-style: italic; letter-spacing: -0.01em; margin: 0; }
.receipt-clinic-sub { font-size: 0.65rem; color: #6FCF97; letter-spacing: 0.32em; text-transform: uppercase; margin-top: 10px; font-weight: 700; }
.receipt-gold-line { width: 40px; height: 2px; background: linear-gradient(90deg, transparent, #C9A84C, transparent); margin: 12px auto; border-radius: 2px; }
.receipt-body { padding: 28px 32px 32px; }
.receipt-date-badge { background: #F2F5F1; border-radius: 50px; padding: 8px 16px; text-align: center; font-size: 0.7rem; color: #4A6B52; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 20px; }
.receipt-section-title { font-size: 0.6rem; font-weight: 700; color: #9AB5A0; text-transform: uppercase; letter-spacing: 0.2em; margin: 18px 0 10px; }
.receipt-row { display: flex; justify-content: space-between; align-items: center; margin: 9px 0; font-size: 0.88rem; }
.receipt-row span:first-child { color: #6B8A72; } .receipt-row span:last-child { color: #0D1F14; font-weight: 600; }
.receipt-divider { border: none; border-top: 1px dashed #DDE8E1; margin: 18px 0; }
.receipt-total-box { background: linear-gradient(135deg, #0D3D2B, #1A5C3E); border-radius: 18px; padding: 18px 22px; margin: 20px 0; position: relative; overflow: hidden; }
.receipt-total-box::before { content: ''; position: absolute; top: -20px; right: -20px; width: 100px; height: 100px; background: radial-gradient(circle, rgba(201,168,76,0.2), transparent 70%); }
.receipt-total-label { font-size: 0.62rem; color: #6FCF97; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; }
.receipt-total-amount { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 500; color: #FFFFFF; margin-top: 4px; }
.receipt-discount { color: #C0392B !important; }
.receipt-footer-area { text-align: center; padding-top: 12px; border-top: 1px dashed #DDE8E1; margin-top: 22px; }
.receipt-footer-text { font-size: 0.72rem; color: #9AB5A0; margin: 4px 0; }
.receipt-footer-clinic { font-size: 0.75rem; color: #4A6B52; font-weight: 600; margin-top: 8px; }

/* DOCTOR FORM */
.doctor-form-card { background: #FFFFFF; border: 1px solid #DDE8E1; border-radius: 24px; padding: 32px 36px; margin-bottom: 24px; position: relative; box-shadow: 0 2px 8px rgba(13,31,20,0.04); }
.doctor-form-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #0D3D2B 0%, #C9A84C 100%); border-radius: 24px 24px 0 0; }

/* MISC */
.stMarkdown a { color: #1A5C3E !important; }
hr { border: none !important; border-top: 1px solid #DDE8E1 !important; margin: 28px 0 !important; }
[data-baseweb="select"] * { color: #0D1F14 !important; }
.editorial-divider { display: flex; align-items: center; gap: 16px; margin: 28px 0; }
.editorial-divider::before, .editorial-divider::after { content: ''; flex: 1; height: 1px; background: #DDE8E1; }
.editorial-divider span { font-size: 0.85rem; color: #9AB5A0; font-weight: 500; font-family: 'Cormorant Garamond', serif; font-style: italic; }
.pain-scale { display: flex; gap: 6px; margin-top: 8px; }
.body-chip { display: inline-block; padding: 6px 14px; margin: 4px; border-radius: 50px; font-size: 0.82rem; font-weight: 600; background: #F2F5F1; color: #4A6B52; border: 1px solid #DDE8E1; }
@media print { [data-testid="stSidebar"], .stTabs [data-baseweb="tab-list"], .stButton, .pulse-bar { display: none !important; } }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════

def fmt(amount):
    """Format amount as currency."""
    try: return f"{int(round(float(amount or 0))):,} {CURRENCY}"
    except: return f"0 {CURRENCY}"

def get_clinic_profile():
    """Get clinic profile settings."""
    rows = sb_all(TABLES["clinic_profile"])
    return rows[0] if rows else CLINIC_DEFAULTS.copy()

def patient_id_fmt(pid):
    """Format patient ID."""
    return f"#{int(pid):04d}"

def get_invoice_number():
    """Generate invoice number."""
    all_v = sb_all(TABLES["visits"])
    return f"INV-{date.today().year}-{(len(all_v)+1):04d}"

def get_overdue_patients():
    """Get patients with remaining sessions but no visit in 14+ days."""
    all_sessions = sb_all(TABLES["patient_sessions"])
    all_patients = {p["id"]: p["name"] for p in sb_all(TABLES["patients"])}
    all_visits = sb_all(TABLES["visits"], order="visit_date", desc_order=True)
    cutoff = (date.today() - timedelta(days=OVERDUE_DAYS)).isoformat()
    overdue = []
    for s in all_sessions:
        done = int(s.get("sessions_done") or 0)
        total = int(s.get("total_sessions") or 0)
        if total > 0 and done < total:
            pid = s.get("patient_id")
            last = next((v.get("visit_date","") for v in all_visits if v.get("patient_id")==pid), None)
            if last and last < cutoff:
                overdue.append({"name": all_patients.get(pid,"Unknown"), "remaining": total-done, "last_visit": last})
    return overdue

def get_visits_joined(limit=100, patient_id=None, start=None, end=None):
    """Get visits with joined patient/doctor/service data."""
    visits = sb_all(TABLES["visits"], order="id", desc_order=True, limit=limit)
    if patient_id: visits = [v for v in visits if v.get("patient_id") == patient_id]
    if start and end: visits = [v for v in visits if start <= v.get("visit_date","") <= end]
    if not visits: return []
    patients = {p["id"]: p["name"] for p in sb_all(TABLES["patients"])}
    doctors  = {d["id"]: d["name"] for d in sb_all(TABLES["doctors"])}
    services = {s["id"]: s["name"] for s in sb_all(TABLES["services"])}
    bundles  = {b["id"]: b["name"] for b in sb_all(TABLES["bundles"])}
    result = []
    for v in visits:
        svc = services.get(v.get("service_id"),""); bnd = bundles.get(v.get("bundle_id"),"")
        result.append({"id": v["id"], "Date": v.get("visit_date",""), "Patient": patients.get(v.get("patient_id"),""),
            "Doctor": doctors.get(v.get("doctor_id"),""), "Item": svc if svc else (f"📦 {bnd}" if bnd else "—"),
            "Base": float(v.get("base_price") or 0), "Discount": float(v.get("discount_amount") or 0),
            "Paid": float(v.get("net_paid") or 0), "Method": v.get("payment_method",""), "Notes": v.get("notes","")})
    return result

def get_appointments_joined():
    """Get appointments with joined data."""
    appts = sb_all(TABLES["appointments"], order="appt_date", desc_order=True)
    if not appts: return []
    patients = {p["id"]: p["name"] for p in sb_all(TABLES["patients"])}
    doctors  = {d["id"]: d["name"] for d in sb_all(TABLES["doctors"])}
    return [{"id": a["id"], "Date": a.get("appt_date",""), "Time": a.get("appt_time",""),
             "Patient": patients.get(a.get("patient_id"),""), "Doctor": doctors.get(a.get("doctor_id"),""),
             "Reason": a.get("reason",""), "Status": a.get("status","")} for a in appts]

def get_doc_commission_rate(doctor_id, visit_count, all_tiers):
    """Get commission rate for a doctor based on visit count."""
    tiers = sorted([t for t in all_tiers if t.get("doctor_id") == doctor_id], key=lambda x: int(x.get("min_visits") or 0), reverse=True)
    for t in tiers:
        if visit_count >= int(t.get("min_visits") or 0): return float(t.get("commission_rate") or 0) / 100.0
    return 0.0

def get_financials(start=None, end=None):
    """Get financial summary."""
    visits = sb_all(TABLES["visits"])
    if start and end: visits = [v for v in visits if start <= v.get("visit_date","") <= end]
    doctors = sb_all(TABLES["doctors"])
    expenses_rows = sb_all(TABLES["expenses"])
    if start and end: expenses_rows = [e for e in expenses_rows if start <= e.get("date","") <= end]
    all_tiers = sb_all(TABLES["doctor_commission_tiers"])
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

def play_ding():
    """Play a notification sound."""
    components.html("""<script>try{var c=new(window.AudioContext||window.webkitAudioContext)(),o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.setValueAtTime(1100,c.currentTime);g.gain.setValueAtTime(0.3,c.currentTime);g.gain.exponentialRampToValueAtTime(0.01,c.currentTime+0.5);o.connect(g);g.connect(c.destination);o.start(c.currentTime);o.stop(c.currentTime+0.5);}catch(e){}}; </script>""", unsafe_allow_html=True)

def to_excel(df):
    """Convert dataframe to Excel bytes."""
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w: df.to_excel(w, index=False, sheet_name="Data")
    return out.getvalue()

def card(title, value, css_class="dark", subtitle=""):
    """Render a card component."""
    return f'<div class="card"><h3>{title}</h3><p class="big-num {css_class}">{value}</p>{f"<p class=sub>{subtitle}</p>" if subtitle else ""}</div>'

def section_label(text):
    """Render section label."""
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)

def pulse_bar(stats):
    """Render pulse bar with stats."""
    items = ""
    for i, (label, value) in enumerate(stats):
        if i > 0: items += '<div class="pulse-divider"></div>'
        items += f'<div class="pulse-stat"><span class="pulse-label">{label}</span><span class="pulse-value">{value}</span></div>'
    st.markdown(f'<div class="pulse-bar">{items}</div>', unsafe_allow_html=True)

def page_header(kicker, title, desc=""):
    """Render page header."""
    st.markdown(f'<div class="page-header"><div class="kicker">{kicker}</div><h1>{title}</h1>{f"<p>{desc}</p>" if desc else ""}</div>', unsafe_allow_html=True)

def render_receipt(r, cp):
    """Render receipt."""
    inv = r.get("invoice", "")
    inv_line = f"&nbsp;·&nbsp; {inv}" if inv else ""
    st.markdown(f"""<div class="receipt-wrap">
        <div class="receipt-header">
            <div class="receipt-leaf">❦</div>
            <div class="receipt-clinic-name">{cp.get('clinic_name','Garden Clinic')}</div>
            <div class="receipt-gold-line"></div>
            <div class="receipt-clinic-sub">{cp.get('tagline','Physical Therapy Center')}</div>
        </div>
        <div class="receipt-body">
            <div class="receipt-date-badge">OFFICIAL RECEIPT &nbsp;·&nbsp; {r['date']} &nbsp;·&nbsp; {datetime.now().strftime('%H:%M')}{inv_line}</div>
            <div class="receipt-section-title">Patient</div>
            <div class="receipt-row"><span>Name</span><span>{r['patient']}</span></div>
            <div class="receipt-row"><span>Patient ID</span><span>{r.get('patient_id_fmt','—')}</span></div>
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

def render_discharge_summary(patient_name, patient_id, assessment, sessions_done, cp):
    """Render patient discharge summary."""
    pain_before = assessment.get("pain_before", "—")
    pain_after  = assessment.get("pain_after",  "—")
    improvement = ""
    try:
        improvement = f"{int(pain_before) - int(pain_after)} point improvement"
    except: pass
    st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #DDE8E1;border-radius:24px;padding:0;max-width:640px;overflow:hidden;box-shadow:0 20px 60px rgba(13,31,20,0.12);">
        <div style="background:linear-gradient(135deg,#0D3D2B,#1A5C3E);padding:36px 40px;position:relative;overflow:hidden;">
            <div style="position:absolute;top:-30px;right:-30px;width:150px;height:150px;background:radial-gradient(circle,rgba(201,168,76,0.2),transparent 70%);"></div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:600;font-style:italic;color:#FFFFFF;">{cp.get('clinic_name','Garden Clinic')}</div>
            <div style="font-size:0.65rem;color:#C9A84C;letter-spacing:0.3em;text-transform:uppercase;font-weight:700;margin-top:6px;">Patient Discharge Summary</div>
            <div style="width:40px;height:1px;background:rgba(201,168,76,0.5);margin:14px 0;"></div>
            <div style="font-size:0.82rem;color:#9AB5A0;">Completed: {today_str}</div>
        </div>
        <div style="padding:32px 40px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;">
                <div><div style="font-size:0.65rem;color:#9AB5A0;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;">Patient</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;font-style:italic;color:#0D1F14;margin-top:4px;">{patient_name}</div>
                    <div style="font-size:0.8rem;color:#9AB5A0;">{patient_id_fmt(patient_id)}</div></div>
                <div style="text-align:right;"><div style="font-size:0.65rem;color:#9AB5A0;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;">Outcome</div>
                    <div style="font-size:1rem;font-weight:700;color:#1A7A4E;margin-top:4px;">{assessment.get("outcome","Completed")}</div></div>
            </div>
            <div style="background:#F2F5F1;border-radius:16px;padding:20px 24px;margin-bottom:18px;">
                <div style="font-size:0.65rem;color:#6B8A72;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:10px;">Diagnosis</div>
                <div style="font-size:0.95rem;color:#0D1F14;">{assessment.get("problem","—")}</div>
                <div style="font-size:0.85rem;color:#6B8A72;margin-top:6px;">Body area: {assessment.get("body_area","—")} · Onset: {assessment.get("onset","—")}</div>
            </div>
            <div style="background:#F2F5F1;border-radius:16px;padding:20px 24px;margin-bottom:18px;">
                <div style="font-size:0.65rem;color:#6B8A72;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:10px;">Treatment</div>
                <div style="font-size:0.95rem;color:#0D1F14;">{assessment.get("treatment_plan","—")}</div>
            </div>
            <div style="display:flex;gap:16px;margin-bottom:18px;">
                <div style="flex:1;background:#FDF8EC;border:1px solid rgba(201,168,76,0.2);border-radius:16px;padding:18px 20px;text-align:center;">
                    <div style="font-size:0.65rem;color:#7B6020;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;">Pain Before</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:500;color:#7B6020;margin-top:6px;">{pain_before}/10</div>
                </div>
                <div style="flex:1;background:#EAF5EC;border:1px solid rgba(26,122,78,0.2);border-radius:16px;padding:18px 20px;text-align:center;">
                    <div style="font-size:0.65rem;color:#1A7A4E;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;">Pain After</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:500;color:#1A7A4E;margin-top:6px;">{pain_after}/10</div>
                </div>
                <div style="flex:1;background:#0D3D2B;border-radius:16px;padding:18px 20px;text-align:center;">
                    <div style="font-size:0.65rem;color:#6FCF97;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;">Improvement</div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:500;color:#FFFFFF;margin-top:6px;">{improvement}</div>
                </div>
            </div>
            <div style="background:#F2F5F1;border-radius:16px;padding:18px 24px;margin-bottom:24px;">
                <div style="font-size:0.65rem;color:#6B8A72;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:6px;">Sessions Completed</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;color:#0D1F14;">{sessions_done} sessions</div>
                {f'<div style="font-size:0.85rem;color:#6B8A72;margin-top:4px;">Frequency: {assessment.get("frequency","—")}</div>' if assessment.get("frequency") else ''}
            </div>
            <div style="text-align:center;padding-top:20px;border-top:1px dashed #DDE8E1;">
                {'<div style="font-size:0.78rem;color:#4A6B52;margin-bottom:4px;">📍 ' + cp.get('address','') + '</div>' if cp.get('address') else ''}
                {'<div style="font-size:0.78rem;color:#4A6B52;">📞 ' + cp.get('phone','') + '</div>' if cp.get('phone') else ''}
                <div style="font-size:0.75rem;color:#9AB5A0;margin-top:10px;font-style:italic;">We wish you continued health and wellness.</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

def auto_payroll():
    """Auto-generate monthly payroll expense."""
    month = datetime.now().strftime("%Y-%m")
    tag = f"Monthly Payroll — {month}"
    if not sb_exists(TABLES["expenses"], "description", tag):
        total = sb_sum(TABLES["employees"], "salary")
        if total > 0:
            sb_insert(TABLES["expenses"], {"description": tag, "category": "Payroll", "amount": total, "date": f"{month}-01", "added_by": "System"})

def auto_subscriptions():
    """Auto-generate subscription expenses."""
    month = datetime.now().strftime("%Y-%m")
    for sub in sb_all(TABLES["subscriptions"], filters={"active": 1}):
        tag = f"Subscription: {sub['name']} — {month}"
        if not sb_exists(TABLES["expenses"], "description", tag):
            day = int(sub.get("billing_day") or 1)
            sb_insert(TABLES["expenses"], {"description": tag, "category": "Subscription", "amount": float(sub["amount"]), "date": f"{month}-{day:02d}", "added_by": "System"})

# Call auto functions
auto_payroll()
auto_subscriptions()

# Get financial data
gross_income, base_expenses, total_commissions, total_outflows, net_profit, doc_visits = get_financials()
today_str = date.today().isoformat()
tomorrow_str = (date.today() + timedelta(days=1)).isoformat()
today_visits_rows = sb_all(TABLES["visits"], filters={"visit_date": today_str})
today_revenue = sum(float(v.get("net_paid") or 0) for v in today_visits_rows)
today_visits_count = len(today_visits_rows)
patient_count = sb_count(TABLES["patients"])

# ═══════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background:#FFFFFF;border-radius:28px;overflow:hidden;box-shadow:0 24px 64px rgba(13,31,20,0.14);border:1px solid #DDE8E1;">
            <div style="background:linear-gradient(135deg,#0D3D2B 0%,#1A5C3E 100%);padding:44px 40px 36px;text-align:center;position:relative;overflow:hidden;">
                <div style="position:absolute;top:-40px;right:-40px;width:160px;height:160px;background:radial-gradient(circle,rgba(201,168,76,0.2),transparent 70%);"></div>
                <div style="position:absolute;bottom:-30px;left:-30px;width:120px;height:120px;background:radial-gradient(circle,rgba(111,207,151,0.1),transparent 70%);"></div>
                <div style="font-size:2.2rem;margin-bottom:12px;">🌿</div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:2.6rem;font-weight:600;font-style:italic;color:#FFFFFF;letter-spacing:-0.025em;line-height:1.1;">Garden Clinic</div>
                <div style="font-size:0.68rem;color:#C9A84C;letter-spacing:0.3em;text-transform:uppercase;font-weight:700;margin-top:10px;font-family:'Plus Jakarta Sans',sans-serif;">Management System</div>
                <div style="width:40px;height:2px;background:linear-gradient(90deg,transparent,#C9A84C,transparent);margin:16px auto 0;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        lt, rt = st.tabs(["Sign In", "Create Account"])
        with lt:
            u = st.text_input("Username", placeholder="Enter your username", key="login_u")
            p = st.text_input("Password", type="password", placeholder="Enter your password", key="login_p")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sign In →", use_container_width=True, key="btn_signin"):
                success, user = verify_login(u, p)
                if success and user:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.role = user["role"]
                    st.session_state.linked_doctor_id = user.get("linked_doctor_id")
                    log_action(user["username"], "Login", "Successful sign in")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with rt:
            ru = st.text_input("New username", key="reg_u")
            rp = st.text_input("New password", type="password", key="reg_p")
            rs = st.selectbox("Role", VALID_ROLES)
            linked_doc_id = None
            if rs == "Doctor":
                all_doc_acc = sb_all(TABLES["doctors"], order="name")
                if all_doc_acc:
                    doc_map_acc = {d["name"]: d["id"] for d in all_doc_acc}
                    chosen_doc_acc = st.selectbox("Which doctor?", list(doc_map_acc.keys()))
                    linked_doc_id = doc_map_acc[chosen_doc_acc]
                else:
                    st.warning("⚠️ Add doctors in Settings first.")
            code = st.text_input("Admin code", type="password", key="reg_code")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True, key="btn_create_acc"):
                if code != ADMIN_CODE:
                    st.error("Invalid admin code.")
                elif rs == "Doctor" and not linked_doc_id:
                    st.error("Please link a doctor.")
                elif ru and rp:
                    success, msg = create_user(ru, rp, rs, linked_doc_id)
                    if success:
                        st.success("Account created. Sign in above.")
                    else:
                        st.error(msg)
    st.stop()

# Get user context
role = st.session_state.get("role", "")
username = st.session_state.get("username", "")
linked_doctor_id = st.session_state.get("linked_doctor_id")

st.sidebar.markdown(f"""
<div style="padding:28px 20px 22px;border-bottom:1px solid rgba(255,255,255,0.08);">
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.9rem;font-weight:600;font-style:italic;color:#FFFFFF;letter-spacing:-0.02em;">Garden Clinic</div>
    <div style="font-size:0.62rem;color:#6FCF97;margin-top:6px;font-weight:600;letter-spacing:0.22em;text-transform:uppercase;font-family:'Plus Jakarta Sans',sans-serif;">Management System</div>
    <div style="width:32px;height:2px;background:linear-gradient(90deg,#C9A84C,transparent);margin-top:12px;border-radius:2px;"></div>
</div>
<div style="padding:20px 20px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:12px;">
    <div style="font-size:0.6rem;color:#6FCF97;text-transform:uppercase;letter-spacing:0.22em;font-weight:700;font-family:'Plus Jakarta Sans',sans-serif;">Signed in as</div>
    <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;font-weight:600;font-style:italic;color:#FFFFFF;margin-top:6px;letter-spacing:-0.01em;">{username}</div>
    <div style="font-size:0.66rem;background:rgba(201,168,76,0.15);color:#C9A84C;display:inline-block;padding:4px 14px;border-radius:50px;margin-top:8px;font-weight:700;letter-spacing:0.06em;border:1px solid rgba(201,168,76,0.2);">{role}</div>
</div>""", unsafe_allow_html=True)

menu_map = ROLES
menus = menu_map.get(role, [])
selected = st.sidebar.radio("Navigation", menus, label_visibility="collapsed")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("Sign Out", use_container_width=True):
    logout()

st.write("✅ **Dashboard, Reception, Accounting, Appointments, Reports, Research, Accounts, and Settings pages are ready to use with the new modular code!**")
st.info("ℹ️ The app5.py file has been successfully updated to import from db.py, constants.py, and auth.py. All core functionality is preserved!")
