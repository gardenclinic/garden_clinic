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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background: linear-gradient(135deg, #03100B 0%, #062018 35%, #010A07 65%, #052016 100%) !important; color: #EAF2EC !important; font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important; }
.stApp::before { content: ''; position: fixed; inset: -30%; z-index: 0; pointer-events: none; background:
    radial-gradient(circle 600px at 5% 10%, rgba(16,120,90,0.7) 0%, transparent 50%),
    radial-gradient(circle 520px at 95% 8%, rgba(201,168,76,0.32) 0%, transparent 48%),
    radial-gradient(circle 700px at 90% 92%, rgba(20,150,110,0.6) 0%, transparent 50%),
    radial-gradient(circle 540px at 12% 95%, rgba(12,90,68,0.6) 0%, transparent 50%),
    radial-gradient(circle 480px at 55% 50%, rgba(16,120,90,0.4) 0%, transparent 55%);
    filter: blur(60px); animation: floatOrbs 13s ease-in-out infinite alternate; }
@keyframes floatOrbs { 0% { transform: translate(-6%,-4%) scale(1) rotate(0deg); } 20% { transform: translate(7%,5%) scale(1.16) rotate(3deg); } 40% { transform: translate(8%,-6%) scale(1.1) rotate(-2deg); } 60% { transform: translate(-7%,6%) scale(1.18) rotate(2deg); } 80% { transform: translate(5%,-5%) scale(1.12) rotate(-1deg); } 100% { transform: translate(6%,4%) scale(1.08) rotate(1deg); } }
/* Flowing organic leaf veins — branching plant-like lines */
.stApp::after { content: ''; position: fixed; inset: -10%; z-index: 0; pointer-events: none; opacity: 0.72;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1200' height='800' viewBox='0 0 1200 800'%3E%3Cg fill='none' stroke='%23C9A84C' stroke-width='1.4' opacity='0.72'%3E%3Cpath d='M-50,200 C220,120 380,280 640,180 C880,90 1040,240 1300,150'/%3E%3Cpath d='M340,235 C400,180 440,150 500,140' stroke-width='0.6' opacity='0.5'/%3E%3Cpath d='M460,213 C520,260 560,290 620,300' stroke-width='0.6' opacity='0.5'/%3E%3Cpath d='M-50,420 C260,360 430,500 720,420 C960,350 1110,460 1300,400' stroke-width='1' opacity='0.55'/%3E%3Cpath d='M520,455 C570,410 610,385 660,378' stroke-width='0.5' opacity='0.4'/%3E%3Cpath d='M-50,600 C240,540 470,680 740,580 C1000,480 1130,640 1300,560' stroke-width='1.7'/%3E%3Cpath d='M600,613 C660,665 700,695 760,705' stroke-width='0.7' opacity='0.5'/%3E%3Cpath d='M380,576 C440,530 480,505 540,500' stroke-width='0.6' opacity='0.45'/%3E%3Cpath d='M180,-50 C240,200 140,400 280,650 C360,780 300,820 340,860' stroke-width='1' opacity='0.5'/%3E%3Cpath d='M850,-50 C910,220 790,420 930,680 C990,800 950,840 990,870' stroke-width='1.3' opacity='0.55'/%3E%3C/g%3E%3C/svg%3E");
    background-size: cover; background-position: center; filter: blur(0.5px) drop-shadow(0 0 7px rgba(201,168,76,0.55)); animation: veinDrift 20s ease-in-out infinite alternate; }
@keyframes veinDrift { 0% { transform: translate(0,0) scale(1.04) rotate(0deg); opacity:0.5; } 50% { transform: translate(-2.5%,1.5%) scale(1.1) rotate(1deg); opacity:0.82; } 100% { transform: translate(2.5%,-1.5%) scale(1.07) rotate(-0.8deg); opacity:0.64; } }
[data-testid="stAppViewContainer"] { position: relative; z-index: 1; }
.main .block-container { animation: pagefade 0.55s cubic-bezier(0.22,1,0.36,1); }
@keyframes pagefade { 0% { opacity: 0; transform: translateY(10px); } 100% { opacity: 1; transform: translateY(0); } }

/* SIDEBAR — deep frosted glass */
[data-testid="stSidebar"] { background: linear-gradient(180deg, rgba(13,61,43,0.55) 0%, rgba(10,46,32,0.62) 100%) !important; backdrop-filter: blur(60px) saturate(200%) !important; -webkit-backdrop-filter: blur(60px) saturate(200%) !important; border-right: 1px solid rgba(255,255,255,0.18) !important; min-width: 252px !important; box-shadow: inset -1px 0 1px rgba(255,255,255,0.1), 4px 0 40px rgba(13,61,43,0.15) !important; }
[data-testid="stSidebar"] * { color: #EAF5EE !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
section[data-testid="stSidebarNav"] { display: none; }
/* Sidebar nav items as glass buttons */
[data-testid="stSidebar"] [role="radiogroup"] { gap: 8px !important; display: flex; flex-direction: column; }
[data-testid="stSidebar"] [role="radiogroup"] label { background: linear-gradient(135deg, rgba(16,72,54,0.35), rgba(6,30,22,0.28)) !important; border: 1px solid rgba(201,168,76,0.18) !important; border-radius: 16px !important; padding: 11px 16px !important; margin: 0 !important; transition: all 0.3s cubic-bezier(0.34,1.5,0.64,1) !important; cursor: pointer !important; box-shadow: inset 0 1px 1px rgba(120,220,180,0.12) !important; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: linear-gradient(135deg, rgba(22,110,80,0.55), rgba(10,46,34,0.45)) !important; border-color: rgba(201,168,76,0.5) !important; transform: translateX(4px) scale(1.02) !important; box-shadow: 0 6px 18px rgba(0,0,0,0.3), 0 0 16px rgba(201,168,76,0.12) !important; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background: linear-gradient(135deg, rgba(26,130,95,0.7), rgba(12,56,42,0.6)) !important; border-color: rgba(201,168,76,0.7) !important; box-shadow: 0 6px 20px rgba(0,0,0,0.35), inset 0 1px 2px rgba(120,220,180,0.35), 0 0 18px rgba(201,168,76,0.2) !important; }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none !important; }
[data-testid="stSidebar"] [role="radiogroup"] label p, [data-testid="stSidebar"] [role="radiogroup"] label span { font-size: 0.92rem !important; font-weight: 600 !important; }
/* Hide broken Material icon text on sidebar collapse button */
[data-testid="stSidebarCollapseButton"] span, [data-testid="baseButton-headerNoPadding"] span, [data-testid="stSidebarCollapsedControl"] span { font-size: 0 !important; }
[data-testid="stSidebarCollapseButton"] span::before, [data-testid="baseButton-headerNoPadding"] span::before { font-family: 'Material Symbols Rounded','Material Symbols Outlined' !important; content: '\\00AB' !important; font-size: 1.2rem !important; color: #C9A84C !important; }

/* TYPOGRAPHY */
h1, h2, h3, h4 { font-family: 'Cormorant Garamond', serif !important; color: #EAF2EC !important; }

/* PAGE HEADER */
.page-header { margin-bottom: 32px; padding-top: 8px; }
.page-header .kicker { font-size: 0.68rem; color: #C9A84C; letter-spacing: 0.28em; text-transform: uppercase; font-weight: 700; margin-bottom: 8px; font-family: 'Plus Jakarta Sans', sans-serif; }
.page-header h1 { font-family: 'Cormorant Garamond', serif !important; font-size: 3rem !important; font-weight: 600 !important; color: #FFFFFF !important; margin: 0 !important; font-style: italic; letter-spacing: -0.02em !important; line-height: 1.05 !important; text-shadow: 0 2px 20px rgba(201,168,76,0.15); }
.page-header p { font-size: 0.9rem; color: #9DB5A6; margin: 8px 0 0 0; font-weight: 400; }

/* PULSE BAR — liquid glass */
.pulse-bar { background: linear-gradient(135deg, rgba(20,45,32,0.6) 0%, rgba(10,25,18,0.5) 100%); backdrop-filter: blur(50px) saturate(170%); -webkit-backdrop-filter: blur(50px) saturate(170%); border: 1px solid rgba(201,168,76,0.3); border-radius: 32px; padding: 24px 34px; display: flex; gap: 44px; flex-wrap: wrap; align-items: center; margin-bottom: 32px; box-shadow: 0 14px 44px rgba(0,0,0,0.4), inset 0 1px 2px rgba(255,255,255,0.4), inset 0 -12px 32px rgba(0,0,0,0.2); position: relative; overflow: hidden; }
.pulse-bar::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 55%; background: linear-gradient(180deg, rgba(255,255,255,0.18), transparent); pointer-events: none; border-radius: 32px 32px 50% 50%; }
.pulse-bar::after { content: ''; position: absolute; top: -80%; left: -60%; width: 55%; height: 260%; background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.28) 50%, rgba(201,168,76,0.18) 55%, transparent 80%); transform: rotate(8deg); pointer-events: none; animation: shimmer 5s ease-in-out infinite; }
@keyframes shimmer { 0% { left: -70%; } 55% { left: 150%; } 100% { left: 150%; } }
.pulse-stat { display: flex; flex-direction: column; position: relative; }
.pulse-label { font-size: 0.65rem; color: #C9A84C; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; font-family: 'Plus Jakarta Sans', sans-serif; }
.pulse-value { font-family: 'JetBrains Mono', monospace; font-size: 1.55rem; font-weight: 600; color: #FFFFFF; margin-top: 4px; letter-spacing: -0.02em; }
.pulse-divider { width: 1px; background: rgba(201,168,76,0.25); height: 40px; align-self: center; }

/* CARDS — liquid glass */
.card { background: linear-gradient(135deg, rgba(10,50,38,0.6), rgba(4,22,16,0.5)); backdrop-filter: blur(40px) saturate(170%); -webkit-backdrop-filter: blur(40px) saturate(170%); border: 1px solid rgba(201,168,76,0.28); border-radius: 28px; padding: 24px 28px; margin-bottom: 18px; transition: all 0.45s cubic-bezier(0.22,1,0.36,1); box-shadow: 0 4px 8px rgba(0,0,0,0.25), 0 14px 28px rgba(0,0,0,0.35), 0 32px 56px rgba(0,0,0,0.3), inset 0 1px 2px rgba(120,220,180,0.3), inset 0 -10px 30px rgba(0,0,0,0.25); position: relative; overflow: hidden; animation: cardRise 0.6s cubic-bezier(0.22,1,0.36,1) both; transform-style: preserve-3d; transform: perspective(900px) rotateX(0deg) rotateY(0deg) translateZ(0px); will-change: transform; }
@keyframes cardRise { 0% { opacity: 0; transform: perspective(900px) translateY(18px) translateZ(-40px) scale(0.98); } 100% { opacity: 1; transform: perspective(900px) translateY(0) translateZ(0) scale(1); } }
.card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 50%; background: linear-gradient(180deg, rgba(120,220,180,0.16), transparent); pointer-events: none; border-radius: 28px 28px 50% 50%; }
.card::after { content: ''; position: absolute; top: -80%; left: -60%; width: 60%; height: 260%; background: linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.28) 48%, rgba(201,168,76,0.35) 52%, transparent 78%); transform: rotate(8deg); pointer-events: none; animation: cardShine 7s ease-in-out infinite; }
@keyframes cardShine { 0% { left: -70%; } 55% { left: 150%; } 100% { left: 150%; } }
.card:hover { background: linear-gradient(135deg, rgba(16,72,54,0.72), rgba(6,30,22,0.62)); border-color: rgba(201,168,76,0.6); box-shadow: 0 6px 12px rgba(0,0,0,0.3), 0 20px 40px rgba(0,0,0,0.45), 0 48px 90px rgba(0,0,0,0.45), 0 0 50px rgba(201,168,76,0.25), inset 0 1px 2px rgba(120,220,180,0.4); transform: perspective(900px) rotateX(4deg) rotateY(-4deg) translateZ(28px) scale(1.02); }
.card h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; margin: 0 0 8px 0; font-size: 0.68rem; color: #D4B45C !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.18em; position: relative; }
.card .big-num { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 500; margin: 0; position: relative; }
.card .big-num.green { color: #2ECC8F; }
.card .big-num.red { color: #FF8A7A; }
.card .big-num.dark, .card .big-num.gold { color: #E8C870; }
.card .sub { font-size: 0.78rem; color: #8FB8A6; margin-top: 8px; font-family: 'Plus Jakarta Sans', sans-serif; position: relative; }
.card h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; margin: 0 0 8px 0; font-size: 0.68rem; color: #2D5740 !important; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; position: relative; }
.card .big-num { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 500; margin: 0; position: relative; }
.card .big-num.green { color: #167346; }
.card .big-num.red { color: #B83227; }
.card .big-num.dark, .card .big-num.gold { color: #08251A; }
.card .sub { font-size: 0.78rem; color: #4A6B52; margin-top: 8px; font-family: 'Plus Jakarta Sans', sans-serif; position: relative; }

/* TABS — liquid glass */
.stTabs [data-baseweb="tab-list"] { background: linear-gradient(135deg, rgba(10,50,38,0.45), rgba(4,22,16,0.4)) !important; backdrop-filter: blur(44px) saturate(180%) !important; -webkit-backdrop-filter: blur(44px) saturate(180%) !important; border-radius: 26px !important; padding: 7px !important; border: 1px solid rgba(201,168,76,0.22) !important; gap: 4px !important; margin-bottom: 24px !important; box-shadow: inset 0 1px 2px rgba(120,220,180,0.18), 0 8px 24px rgba(0,0,0,0.3) !important; }
.stTabs button[data-baseweb="tab"] { background: transparent !important; border: none !important; color: #9DB5A6 !important; font-size: 0.82rem !important; font-weight: 600 !important; padding: 9px 18px !important; border-radius: 16px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; transition: all 0.25s !important; }
.stTabs button[data-baseweb="tab"]:hover { background: rgba(255,255,255,0.12) !important; color: #FFFFFF !important; }
.stTabs button[aria-selected="true"] { background: linear-gradient(135deg, rgba(22,120,88,0.85), rgba(12,56,42,0.7)) !important; backdrop-filter: blur(20px) saturate(200%) !important; color: #F0E6C8 !important; font-weight: 700 !important; border: 1px solid rgba(201,168,76,0.6) !important; box-shadow: 0 4px 16px rgba(0,0,0,0.35), inset 0 1px 2px rgba(120,220,180,0.4), 0 0 18px rgba(201,168,76,0.18) !important; }

/* BUTTONS — emerald glass with rich motion */
.stButton > button { background: linear-gradient(135deg, rgba(16,90,66,0.7), rgba(8,40,30,0.6)) !important; backdrop-filter: blur(24px) saturate(180%) !important; -webkit-backdrop-filter: blur(24px) saturate(180%) !important; color: #F0E6C8 !important; border: 1px solid rgba(201,168,76,0.45) !important; border-radius: 50px !important; font-weight: 700 !important; font-size: 0.85rem !important; padding: 13px 30px !important; font-family: 'Plus Jakarta Sans', sans-serif !important; letter-spacing: 0.02em !important; transition: transform 0.25s cubic-bezier(0.34,1.8,0.5,1), background 0.3s, box-shadow 0.3s, border-color 0.3s !important; box-shadow: 0 2px 4px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.3), 0 16px 32px rgba(0,0,0,0.25), inset 0 1px 2px rgba(120,220,180,0.35), inset 0 -3px 10px rgba(0,0,0,0.2) !important; position: relative !important; overflow: hidden !important; animation: btnGlow 3.5s ease-in-out infinite !important; transform: perspective(600px) translateZ(0px) !important; }
@keyframes btnGlow { 0%,100% { box-shadow: 0 2px 4px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.3), 0 16px 32px rgba(0,0,0,0.25), inset 0 1px 2px rgba(120,220,180,0.35), inset 0 -3px 10px rgba(0,0,0,0.2), 0 0 0px rgba(201,168,76,0); } 50% { box-shadow: 0 2px 4px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.3), 0 16px 32px rgba(0,0,0,0.25), inset 0 1px 2px rgba(120,220,180,0.45), inset 0 -3px 10px rgba(0,0,0,0.2), 0 0 18px rgba(201,168,76,0.22); } }
.stButton > button::after { content: ''; position: absolute; top: -100%; left: -70%; width: 45%; height: 300%; background: linear-gradient(115deg, transparent, rgba(255,255,255,0.35), rgba(201,168,76,0.3), transparent); transform: rotate(10deg); pointer-events: none; animation: btnSweep 4.5s ease-in-out infinite; }
@keyframes btnSweep { 0% { left: -70%; } 45% { left: 160%; } 100% { left: 160%; } }
.stButton > button:hover { background: linear-gradient(135deg, rgba(24,135,98,0.9), rgba(14,64,48,0.78)) !important; color: #FFFFFF !important; border-color: rgba(201,168,76,0.9) !important; transform: perspective(600px) translateY(-5px) translateZ(20px) scale(1.045) rotateX(3deg) !important; box-shadow: 0 4px 8px rgba(0,0,0,0.35), 0 14px 28px rgba(0,0,0,0.4), 0 32px 56px rgba(0,0,0,0.35), inset 0 1px 2px rgba(120,220,180,0.6), 0 0 36px rgba(201,168,76,0.35) !important; animation: none !important; }
.stButton > button:hover::after { animation: btnSweepFast 0.7s ease forwards; }
@keyframes btnSweepFast { 0% { left: -70%; } 100% { left: 160%; } }
.stButton > button:active { transform: perspective(600px) translateZ(-6px) scale(0.92) translateY(0) rotateX(0deg) !important; transition: transform 0.08s !important; }
button[data-testid="baseButton-primary"] { background: linear-gradient(135deg, rgba(192,57,43,0.8), rgba(120,30,22,0.7)) !important; color: #FFEEEA !important; border: 1px solid rgba(255,180,160,0.4) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.3), 0 8px 16px rgba(192,57,43,0.3), 0 16px 32px rgba(192,57,43,0.15), inset 0 1px 2px rgba(255,255,255,0.4) !important; animation: none !important; }
button[data-testid="baseButton-primary"]:hover { background: linear-gradient(135deg, rgba(210,70,55,0.9), rgba(140,40,30,0.78)) !important; color: #FFFFFF !important; }

/* INPUTS — dark frosted glass */
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input { background: rgba(255,255,255,0.08) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important; border-radius: 16px !important; border: 1px solid rgba(201,168,76,0.3) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important; color: #EAF2EC !important; padding: 12px 16px !important; transition: all 0.25s !important; box-shadow: inset 0 1px 2px rgba(255,255,255,0.1) !important; }
.stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus { border-color: rgba(201,168,76,0.7) !important; background: rgba(255,255,255,0.12) !important; box-shadow: 0 0 0 4px rgba(201,168,76,0.15), inset 0 1px 2px rgba(255,255,255,0.15) !important; }
.stSelectbox > div > div > div { background: rgba(255,255,255,0.08) !important; backdrop-filter: blur(20px) !important; border-radius: 16px !important; border: 1px solid rgba(201,168,76,0.3) !important; color: #EAF2EC !important; }
.stTextArea textarea { background: rgba(255,255,255,0.08) !important; backdrop-filter: blur(20px) !important; border-radius: 16px !important; border: 1px solid rgba(201,168,76,0.3) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; color: #EAF2EC !important; }
.stTextArea textarea:focus { border-color: rgba(201,168,76,0.7) !important; box-shadow: 0 0 0 4px rgba(201,168,76,0.15) !important; }
.stRadio > div { gap: 14px !important; }
label, .stRadio label span, .stCheckbox label { color: #EAF2EC !important; }
[data-testid="stWidgetLabel"] p { color: #C9A84C !important; font-size: 0.8rem !important; font-weight: 600 !important; letter-spacing: 0.04em !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] { border-radius: 18px !important; overflow: hidden !important; border: 1px solid rgba(255,255,255,0.6) !important; background: rgba(255,255,255,0.55) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important; box-shadow: 0 4px 16px rgba(13,31,20,0.06) !important; }
[data-testid="stDataFrame"] * { color: #0D1F14 !important; }

/* ALERTS — frosted */
.stSuccess > div { background: rgba(234,245,236,0.7) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(39,174,96,0.4) !important; color: #145A38 !important; border-radius: 18px !important; }
.stError > div { background: rgba(253,240,238,0.7) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(192,57,43,0.4) !important; color: #7B1F1F !important; border-radius: 18px !important; }
.stWarning > div { background: rgba(253,248,236,0.7) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(201,168,76,0.5) !important; color: #6F5518 !important; border-radius: 18px !important; }
.stInfo > div { background: rgba(234,245,240,0.7) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(26,92,62,0.35) !important; color: #145A38 !important; border-radius: 18px !important; }

/* SECTION LABEL */
.section-label { font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.68rem; font-weight: 700; color: #D4B45C; text-transform: uppercase; letter-spacing: 0.22em; margin: 28px 0 16px; display: flex; align-items: center; gap: 10px; }
.section-label::after { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, rgba(201,168,76,0.4), transparent); }

/* METRICS — liquid glass */
[data-testid="stMetric"] { background: linear-gradient(135deg, rgba(20,40,30,0.55), rgba(10,25,18,0.45)) !important; backdrop-filter: blur(30px) saturate(160%) !important; -webkit-backdrop-filter: blur(30px) saturate(160%) !important; border: 1px solid rgba(201,168,76,0.3) !important; border-radius: 22px !important; padding: 20px 24px !important; box-shadow: 0 3px 6px rgba(0,0,0,0.25), 0 10px 20px rgba(0,0,0,0.3), 0 24px 40px rgba(0,0,0,0.25), inset 0 1px 2px rgba(255,255,255,0.35) !important; transition: transform 0.35s cubic-bezier(0.22,1,0.36,1), box-shadow 0.35s !important; }
[data-testid="stMetricLabel"] { font-size: 0.68rem !important; color: #C9A84C !important; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 700 !important; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 1.7rem !important; color: #FFFFFF !important; font-weight: 500 !important; }

/* SESSION BAR */
.session-bar-wrap { background: rgba(13,61,43,0.12); border-radius: 50px; height: 10px; width: 100%; margin-top: 8px; overflow: hidden; }
.session-bar-fill { height: 10px; border-radius: 50px; background: linear-gradient(90deg, #0D3D2B, #27AE60); box-shadow: 0 0 12px rgba(39,174,96,0.4); }

/* PROFILE HEADER — liquid glass */
.profile-summary { background: linear-gradient(135deg, rgba(13,61,43,0.85) 0%, rgba(26,92,62,0.78) 100%); backdrop-filter: blur(30px) saturate(160%); -webkit-backdrop-filter: blur(30px) saturate(160%); color: #FFF; padding: 32px 36px; border-radius: 28px; margin-bottom: 24px; position: relative; overflow: hidden; border: 1px solid rgba(255,255,255,0.18); box-shadow: 0 8px 32px rgba(13,61,43,0.25), inset 0 1px 1px rgba(255,255,255,0.25); }
.profile-summary::before { content: ''; position: absolute; top: -40px; right: -40px; width: 220px; height: 220px; background: radial-gradient(circle, rgba(201,168,76,0.22), transparent 70%); }
.profile-kicker { font-size: 0.65rem; color: #E8C870; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 700; font-family: 'Plus Jakarta Sans', sans-serif; position: relative; }
.profile-name { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 600; font-style: italic; margin: 4px 0 0 0; color: #FFFFFF; letter-spacing: -0.02em; line-height: 1.1; position: relative; }
.profile-meta { font-size: 0.88rem; color: #C5DDCB; margin-top: 10px; position: relative; }

/* PATIENT CHIP BAR — liquid glass */
.patient-chip-bar { background: linear-gradient(135deg, rgba(20,40,30,0.55), rgba(10,25,18,0.45)); backdrop-filter: blur(30px) saturate(160%); -webkit-backdrop-filter: blur(30px) saturate(160%); border: 1px solid rgba(201,168,76,0.3); border-radius: 24px; padding: 20px 26px; margin-bottom: 20px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px; box-shadow: 0 10px 32px rgba(0,0,0,0.35), inset 0 1px 2px rgba(255,255,255,0.3); }
.patient-chip-name { font-family: 'Cormorant Garamond', serif; font-size: 1.6rem; font-weight: 600; font-style: italic; color: #FFFFFF; letter-spacing: -0.01em; }
.patient-chip { display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; background: rgba(255,255,255,0.1); border-radius: 50px; font-size: 0.78rem; color: #C5D6CC; font-weight: 600; border: 1px solid rgba(201,168,76,0.25); }
.patient-chip.warn { background: rgba(253,240,238,0.7); color: #C0392B; border-color: rgba(192,57,43,0.2); }
.patient-chip.good { background: rgba(234,245,236,0.7); color: #1A7A4E; border-color: rgba(26,122,78,0.2); }
.patient-chip.accent { background: rgba(253,248,236,0.7); color: #7B6020; border-color: rgba(201,168,76,0.2); }

/* TAG PILLS */
.tag-pill { display: inline-block; padding: 4px 12px; border-radius: 50px; font-size: 0.72rem; font-weight: 700; margin-right: 6px; margin-bottom: 4px; letter-spacing: 0.04em; }
.tag-condition { background: #FDF0EE; color: #C0392B; border: 1px solid rgba(192,57,43,0.2); }
.tag-success { background: #EAF5EC; color: #1A7A4E; border: 1px solid rgba(26,122,78,0.2); }
.tag-pending { background: #FDF8EC; color: #7B6020; border: 1px solid rgba(201,168,76,0.2); }

/* RECEIPT */
.receipt-wrap { background: #FFFFFF; border-radius: 24px; padding: 0; max-width: 440px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.88rem; color: #0D1F14; box-shadow: 0 20px 60px rgba(13,31,20,0.15); overflow: hidden; border: 1px solid #DDE8E1; }
.receipt-header { background: #051811; padding: 40px 28px 28px; text-align: center; position: relative; overflow: hidden; }
.receipt-header::before { content: ''; display: none; }
.receipt-header::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 24px; background: #FFFFFF; border-radius: 24px 24px 0 0; }
.receipt-leaf { font-size: 1.2rem; color: #C9A84C; margin-bottom: 8px; }
.receipt-clinic-name { font-family: 'Cormorant Garamond', serif; font-size: 2rem; font-weight: 600; color: #FFFFFF; font-style: italic; letter-spacing: -0.01em; margin: 0; }
.receipt-clinic-sub { font-size: 0.65rem; color: #6FCF97; letter-spacing: 0.32em; text-transform: uppercase; margin-top: 10px; font-weight: 700; }
.receipt-gold-line { width: 40px; height: 2px; background: linear-gradient(90deg, transparent, #C9A84C, transparent); margin: 12px auto; border-radius: 2px; }
.receipt-body { padding: 28px 32px 32px; }
.receipt-date-badge { background: #F2F5F1; border-radius: 50px; padding: 8px 16px; text-align: center; font-size: 0.7rem; color: #1A5C3E !important; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 24px; border: 1px solid #DDE8E1; }
.receipt-section-title { font-size: 0.6rem; font-weight: 700; color: #6B8A72 !important; text-transform: uppercase; letter-spacing: 0.2em; margin: 18px 0 10px; }
.receipt-row { display: flex; justify-content: space-between; align-items: center; margin: 9px 0; font-size: 0.88rem; }
.receipt-row span:first-child { color: #4A6B52 !important; } .receipt-row span:last-child { color: #0D1F14 !important; font-weight: 700; }
.receipt-divider { border: none; border-top: 1px dashed #DDE8E1; margin: 18px 0; }
.receipt-total-box { background: #0D3D2B; border-radius: 18px; padding: 18px 22px; margin: 20px 0; position: relative; overflow: hidden; }
.receipt-total-box::before { content: ''; display: none; }
.receipt-total-label { font-size: 0.62rem; color: #6FCF97; font-weight: 700; text-transform: uppercase; letter-spacing: 0.2em; }
.receipt-total-amount { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 500; color: #FFFFFF; margin-top: 4px; }
.receipt-discount { color: #C0392B !important; }
.receipt-footer-area { text-align: center; padding-top: 12px; border-top: 1px dashed #DDE8E1; margin-top: 22px; }
.receipt-footer-text { font-size: 0.72rem; color: #6B8A72 !important; margin: 4px 0; }
.receipt-footer-clinic { font-size: 0.75rem; color: #1A5C3E !important; font-weight: 600; margin-top: 8px; }

/* DOCTOR FORM */
.doctor-form-card { background: #FFFFFF; border: 1px solid #DDE8E1; border-radius: 24px; padding: 32px 36px; margin-bottom: 24px; position: relative; box-shadow: 0 2px 8px rgba(13,31,20,0.04); }
.doctor-form-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, #0D3D2B 0%, #C9A84C 100%); border-radius: 24px 24px 0 0; }

/* MISC */
/* Universal soft hover-lift on interactive elements */
[data-testid="stMetric"], .stTextInput, .stNumberInput, .stDateInput, .stTextArea, .stSelectbox, [data-testid="stDataFrame"], .stExpander { transition: transform 0.3s cubic-bezier(0.34,1.4,0.64,1), box-shadow 0.3s !important; }
[data-testid="stMetric"]:hover, [data-testid="stDataFrame"]:hover { transform: perspective(700px) translateY(-7px) translateZ(16px) scale(1.03) rotateX(2deg) !important; box-shadow: 0 4px 8px rgba(0,0,0,0.3), 0 16px 32px rgba(0,0,0,0.4), 0 36px 64px rgba(0,0,0,0.35), 0 0 32px rgba(201,168,76,0.22) !important; }
.stTextInput:hover, .stNumberInput:hover, .stDateInput:hover, .stTextArea:hover, .stSelectbox:hover { transform: translateY(-2px) !important; }
.stExpander:hover { transform: translateY(-2px) !important; }
.tag-pill { transition: transform 0.25s cubic-bezier(0.34,1.6,0.64,1) !important; }
.patient-chip { transition: transform 0.25s cubic-bezier(0.34,1.6,0.64,1) !important; }
.patient-chip:hover { transform: translateY(-2px) scale(1.04) !important; }
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span, .stCaption, [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p { color: #C5D6CC !important; }
.stMarkdown a { color: #C9A84C !important; }
.stMarkdown strong { color: #EAF2EC !important; }
hr { border: none !important; border-top: 1px solid rgba(201,168,76,0.18) !important; margin: 28px 0 !important; }
[data-baseweb="select"] * { color: #EAF2EC !important; }
.editorial-divider { display: flex; align-items: center; gap: 16px; margin: 28px 0; }
.editorial-divider::before, .editorial-divider::after { content: ''; flex: 1; height: 1px; background: rgba(201,168,76,0.2); }
.editorial-divider span { font-size: 0.85rem; color: #C9A84C; font-weight: 500; font-family: 'Cormorant Garamond', serif; font-style: italic; }
.pain-scale { display: flex; gap: 6px; margin-top: 8px; }
.body-chip { display: inline-block; padding: 6px 14px; margin: 4px; border-radius: 50px; font-size: 0.82rem; font-weight: 600; background: rgba(255,255,255,0.08); color: #C5D6CC; border: 1px solid rgba(201,168,76,0.25); }
@media print { [data-testid="stSidebar"], .stTabs [data-baseweb="tab-list"], .stButton, .pulse-bar { display: none !important; } }

/* FLOATING BOTANICAL PARTICLES */
.leaf-field { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.leaf { position: absolute; opacity: 0; animation: leafFloat linear infinite; }
.leaf svg { display: block; filter: drop-shadow(0 2px 6px rgba(0,0,0,0.2)); }
@keyframes leafFloat {
    0%   { transform: translateY(110vh) translateX(0) rotate(0deg) scale(var(--s,1)); opacity: 0; }
    8%   { opacity: var(--o,0.5); }
    50%  { transform: translateY(45vh) translateX(40px) rotate(180deg) scale(var(--s,1)); }
    92%  { opacity: var(--o,0.5); }
    100% { transform: translateY(-15vh) translateX(-30px) rotate(360deg) scale(var(--s,1)); opacity: 0; }
}
@keyframes sporePulse { 0%,100% { opacity:0.15; transform: scale(1);} 50% { opacity:0.5; transform: scale(1.4);} }
.spore { position:absolute; width:5px; height:5px; border-radius:50%; background: radial-gradient(circle, rgba(201,168,76,0.9), rgba(201,168,76,0)); animation: sporePulse ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# Floating botanical layer (leaves + glowing spores drifting upward)
import random as _rnd
import urllib.parse as _urlp
_leaf_svgs_raw = [
    '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24"><path d="M12 2C7 6 4 11 4 16c0 4 3 6 8 6 0-6 2-11 8-15-3 0-6 0-8 2-1-3 0-5 0-7z" fill="#27AE60" fill-opacity="0.55"/><path d="M12 4C9 8 7 12 7 16" stroke="#C9A84C" stroke-width="0.8" fill="none" opacity="0.6"/></svg>',
    '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24"><ellipse cx="12" cy="12" rx="5" ry="10" fill="#1A7A4E" fill-opacity="0.5"/><line x1="12" y1="3" x2="12" y2="21" stroke="#C9A84C" stroke-width="0.7" opacity="0.6"/></svg>',
    '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24"><path d="M12 3c-4 3-6 7-6 11 0 3 2 5 6 6 4-1 6-3 6-6 0-4-2-8-6-11z" fill="#2ECC8F" fill-opacity="0.45"/><path d="M12 5v15" stroke="#D4B45C" stroke-width="0.7" opacity="0.55"/></svg>',
]
_leaf_svgs = ["data:image/svg+xml," + _urlp.quote(s) for s in _leaf_svgs_raw]
_particles = []
for _i in range(13):
    _left = _rnd.randint(2, 96); _dur = _rnd.randint(16, 34); _delay = _rnd.randint(0, 22)
    _scale = round(_rnd.uniform(0.5, 1.25), 2); _op = round(_rnd.uniform(0.25, 0.6), 2)
    _svg = _rnd.choice(_leaf_svgs)
    _particles.append(f'<div class="leaf" style="left:{_left}%;--s:{_scale};--o:{_op};animation-duration:{_dur}s;animation-delay:-{_delay}s;"><img src="{_svg}" width="{int(26*_scale)}"/></div>')
for _i in range(10):
    _left = _rnd.randint(3, 97); _top = _rnd.randint(5, 92); _dur = _rnd.randint(3, 7); _delay = _rnd.randint(0, 6)
    _particles.append(f'<div class="spore" style="left:{_left}%;top:{_top}%;animation-duration:{_dur}s;animation-delay:-{_delay}s;"></div>')
st.markdown(f'<div class="leaf-field">{"".join(_particles)}</div>', unsafe_allow_html=True)

# 3D mouse-tracking tilt for cards — reaches into the parent document since Streamlit renders this in an iframe
components.html("""
<script>
(function() {
    function attachTilt() {
        try {
            var doc = window.parent.document;
            var cards = doc.querySelectorAll('.card');
            cards.forEach(function(card) {
                if (card.dataset.tiltBound) return;
                card.dataset.tiltBound = "1";
                card.addEventListener('mousemove', function(e) {
                    var rect = card.getBoundingClientRect();
                    var x = e.clientX - rect.left;
                    var y = e.clientY - rect.top;
                    var cx = rect.width / 2;
                    var cy = rect.height / 2;
                    var rotateY = ((x - cx) / cx) * 7;
                    var rotateX = -((y - cy) / cy) * 7;
                    card.style.transform = 'perspective(900px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateZ(28px) scale(1.02)';
                });
                card.addEventListener('mouseleave', function() {
                    card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) translateZ(0px) scale(1)';
                });
            });
        } catch (e) {}
    }
    setInterval(attachTilt, 800);
    attachTilt();
})();
</script>
""", height=0, width=0)

# Currency
def fmt(amount):
    try: return f"{int(round(float(amount or 0))):,} IQD"
    except: return "0 IQD"

# Supabase
@st.cache_resource
def get_sb(): return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

@st.cache_data(ttl=60, show_spinner=False)
def _fetch_table(table):
    """Fetch a whole table once and cache it for 60 seconds. Repeated reads are instant."""
    try: return get_sb().table(table).select("*").execute().data or []
    except: return []

def sb_all(table, filters=None, order=None, desc_order=False, limit=None):
    rows = list(_fetch_table(table))
    if filters:
        for k, v in filters.items():
            rows = [r for r in rows if r.get(k) == v]
    if order:
        rows = sorted(rows, key=lambda r: (r.get(order) is None, r.get(order)), reverse=desc_order)
    if limit: rows = rows[:limit]
    return rows

def _clear_cache():
    try: _fetch_table.clear()
    except: pass

def sb_one(table, filters):
    r = sb_all(table, filters=filters); return r[0] if r else None
def sb_insert(table, data):
    try: get_sb().table(table).insert(data).execute(); _clear_cache(); return True
    except: return False
def sb_delete(table, col, val):
    try: get_sb().table(table).delete().eq(col, val).execute(); _clear_cache(); return True
    except: return False
def sb_update(table, data, col, val):
    try: get_sb().table(table).update(data).eq(col, val).execute(); _clear_cache(); return True
    except: return False
def sb_exists(table, col, val):
    return any(r.get(col) == val for r in sb_all(table))
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
    components.html("""<script>try{var c=new(window.AudioContext||window.webkitAudioContext)();function n(f,t,d){var o=c.createOscillator(),g=c.createGain();o.type='sine';o.frequency.setValueAtTime(f,c.currentTime+t);g.gain.setValueAtTime(0.0001,c.currentTime+t);g.gain.exponentialRampToValueAtTime(0.16,c.currentTime+t+0.02);g.gain.exponentialRampToValueAtTime(0.0001,c.currentTime+t+d);o.connect(g);g.connect(c.destination);o.start(c.currentTime+t);o.stop(c.currentTime+t+d);}n(880,0,0.5);n(1318.5,0.13,0.55);}catch(e){}</script>""", height=0, width=0)
def get_clinic_profile():
    rows = sb_all("clinic_profile")
    return rows[0] if rows else {"clinic_name": "Garden Clinic", "address": "", "phone": "", "email": "", "tagline": "Physical Therapy Center"}

def patient_id_fmt(pid): return f"#{int(pid):04d}"

def auto_cap_name(name):
    """Auto-capitalize each word of a name: 'ahmed ali' -> 'Ahmed Ali'."""
    if not name: return name
    return " ".join(w[:1].upper() + w[1:] if w else w for w in name.strip().split(" "))

def get_patient_loyalty(patient_id, created_at, visits_count):
    """Returns (tier_name, icon, color_hex, months_text) based on time since registration and visit count.
    Bronze: 3+ months OR 10+ visits. Silver: 6+ months OR 25+ visits. Gold: 12+ months OR 50+ visits."""
    months_since = 0
    if created_at:
        try:
            created_date = datetime.strptime(created_at[:10], "%Y-%m-%d").date()
            months_since = (date.today().year - created_date.year) * 12 + (date.today().month - created_date.month)
        except: months_since = 0
    if months_since >= 12 or visits_count >= 50:
        return ("Gold", "🥇", "#C9A84C", f"{months_since} mo · {visits_count} visits")
    elif months_since >= 6 or visits_count >= 25:
        return ("Silver", "🥈", "#C5C5C5", f"{months_since} mo · {visits_count} visits")
    elif months_since >= 3 or visits_count >= 10:
        return ("Bronze", "🥉", "#B87333", f"{months_since} mo · {visits_count} visits")
    return (None, None, None, None)

def get_invoice_number():
    all_v = sb_all("visits")
    return f"INV-{date.today().year}-{(len(all_v)+1):04d}"

def get_overdue_patients():
    """Patients with remaining sessions but no visit in 14+ days"""
    all_sessions = sb_all("patient_sessions")
    all_patients = {p["id"]: p["name"] for p in sb_all("patients")}
    all_visits = sb_all("visits", order="visit_date", desc_order=True)
    cutoff = (date.today() - timedelta(days=14)).isoformat()
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

def get_followup_patients(days_after=20):
    """Patients who COMPLETED all sessions and `days_after` days have passed since their last visit.
    Excludes those already marked as contacted for this completion."""
    all_sessions = sb_all("patient_sessions")
    all_patients = {p["id"]: p for p in sb_all("patients")}
    all_visits = sb_all("visits", order="visit_date", desc_order=True)
    contacted = sb_all("followup_log")
    cutoff = (date.today() - timedelta(days=days_after)).isoformat()
    followups = []
    for s in all_sessions:
        done = int(s.get("sessions_done") or 0)
        total = int(s.get("total_sessions") or 0)
        # completed all sessions
        if total > 0 and done >= total:
            pid = s.get("patient_id")
            last = next((v.get("visit_date","") for v in all_visits if v.get("patient_id")==pid), None)
            if last and last <= cutoff:
                # already contacted after this last visit?
                already = any(c.get("patient_id")==pid and c.get("last_visit")==last for c in contacted)
                if not already:
                    pat = all_patients.get(pid, {})
                    days_passed = (date.today() - date.fromisoformat(last)).days
                    followups.append({"patient_id": pid, "name": pat.get("name","Unknown"),
                        "phone": pat.get("phone",""), "last_visit": last, "days_passed": days_passed,
                        "total_sessions": total})
    return followups

def clean_phone(phone):
    """Convert phone to international format for WhatsApp. Iraq default 964."""
    if not phone: return ""
    p = "".join(c for c in str(phone) if c.isdigit())
    if p.startswith("00"): p = p[2:]
    elif p.startswith("0"): p = "964" + p[1:]   # Iraq: drop leading 0, add 964
    elif not p.startswith("964") and len(p) <= 10: p = "964" + p
    return p

def whatsapp_link(phone, message):
    import urllib.parse
    ph = clean_phone(phone)
    msg = urllib.parse.quote(message)
    return f"https://wa.me/{ph}?text={msg}"

def get_followup_template():
    rows = sb_all("clinic_settings", filters={"key": "followup_template"})
    if rows: return rows[0].get("value","")
    return "Hello {name}! 🌿 This is {clinic} checking in on you. It's been {days} days since you completed your treatment. We hope you're feeling great! If you need any follow-up care or have any concerns, we're here for you. Stay healthy! 💚"

def get_reminder_template():
    rows = sb_all("clinic_settings", filters={"key": "reminder_template"})
    if rows: return rows[0].get("value","")
    return "Hello {name}! 🌿 This is a friendly reminder from {clinic} that you have an appointment tomorrow, {date} at {time} with Dr. {doctor}. We look forward to seeing you! If you need to reschedule, please let us know."

def record_backup_download():
    """Records the timestamp of the most recent Excel export, used as a 'last backup' reminder."""
    existing_bk = sb_all("clinic_settings", filters={"key": "last_backup_at"})
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    if existing_bk: sb_update("clinic_settings", {"value": now_str}, "id", existing_bk[0]["id"])
    else: sb_insert("clinic_settings", {"key": "last_backup_at", "value": now_str})

def get_last_backup_info():
    """Returns (date_text, days_ago) for the last recorded backup, or (None, None) if never."""
    rows = sb_all("clinic_settings", filters={"key": "last_backup_at"})
    if not rows: return (None, None)
    val = rows[0].get("value","")
    try:
        dt = datetime.strptime(val[:10], "%Y-%m-%d")
        days_ago = (date.today() - dt.date()).days
        return (val, days_ago)
    except: return (val, None)

def get_tomorrow_appointments():
    """Appointments scheduled for tomorrow that are still 'Scheduled'."""
    tmrw = (date.today() + timedelta(days=1)).isoformat()
    appts = sb_all("appointments", filters={"appt_date": tmrw, "status": "Scheduled"})
    patients_map = {p["id"]: p for p in sb_all("patients")}
    doctors_map = {d["id"]: d["name"] for d in sb_all("doctors")}
    out = []
    for a in appts:
        pat = patients_map.get(a.get("patient_id"), {})
        out.append({"appt_id": a["id"], "name": pat.get("name","Unknown"), "phone": pat.get("phone",""),
            "date": a.get("appt_date",""), "time": a.get("appt_time",""), "doctor": doctors_map.get(a.get("doctor_id"),"—"),
            "reason": a.get("reason","")})
    return out

def get_doctor_noshows():
    """Patients whose doctor has a fixed schedule day that has already passed (today or before),
    who have remaining sessions, but have no visit logged on that scheduled day.
    Uses the patient's assigned_doctor_id when set (accurate, works even for brand-new patients);
    falls back to 'ever had a visit with this doctor' for older patients registered before assignment existed."""
    doctors_sched = sb_all("doctors")
    sessions_all = sb_all("patient_sessions")
    patients_all = sb_all("patients")
    patients_map = {p["id"]: p["name"] for p in patients_all}
    visits_all = sb_all("visits")
    weekday_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    today_name = weekday_names[date.today().weekday()]
    noshows = []
    for d in doctors_sched:
        sched_days = (d.get("schedule_days") or "").split(",")
        sched_days = [s.strip() for s in sched_days if s.strip()]
        if today_name not in sched_days: continue
        # Primary: patients explicitly assigned to this doctor
        assigned_ids = set(p["id"] for p in patients_all if p.get("assigned_doctor_id")==d["id"])
        # Fallback: older patients with no assignment but past visit history with this doctor
        unassigned_with_history = set(v.get("patient_id") for v in visits_all if v.get("doctor_id")==d["id"]) - set(p["id"] for p in patients_all if p.get("assigned_doctor_id"))
        candidate_ids = assigned_ids | unassigned_with_history
        for pid in candidate_ids:
            sess = next((s for s in sessions_all if s.get("patient_id")==pid), None)
            if not sess: continue
            done = int(sess.get("sessions_done") or 0); total = int(sess.get("total_sessions") or 0)
            if total <= 0 or done >= total: continue
            visited_today = any(v.get("patient_id")==pid and v.get("visit_date")==today_str and v.get("doctor_id")==d["id"] for v in visits_all)
            if not visited_today:
                noshows.append({"name": patients_map.get(pid,"Unknown"), "doctor": d["name"], "remaining": total-done})
    return noshows

def render_discharge_summary(patient_name, patient_id, assessment, sessions_done, cp):
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
                    <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;font-weight:600;font-style:italic;color:#EAF2EC;margin-top:4px;">{patient_name}</div>
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
                {f'<div style="font-size:0.85rem;color:#8FB8A6;margin-top:4px;">Frequency: {assessment.get("frequency","—")}</div>' if assessment.get("frequency") else ''}
            </div>
            <div style="text-align:center;padding-top:20px;border-top:1px dashed #DDE8E1;">
                {'<div style="font-size:0.78rem;color:#9DC2B0;margin-bottom:4px;">📍 ' + cp.get('address','') + '</div>' if cp.get('address') else ''}
                {'<div style="font-size:0.78rem;color:#9DC2B0;">📞 ' + cp.get('phone','') + '</div>' if cp.get('phone') else ''}
                <div style="font-size:0.75rem;color:#9AB5A0;margin-top:10px;font-style:italic;">We wish you continued health and wellness.</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_doctor_daily_sheet(doctor_name, rows, sheet_date):
    """Doctor's daily one-pager: today's patients, treatment stage, red flags. Print-only dark text on white."""
    row_html = ""
    for r in rows:
        flag_html = f'<div style="margin-top:4px;font-size:12px;color:#A3271F;font-weight:700;">⚠ RED FLAG: {r["red_flags"]}</div>' if r.get("red_flags") else ""
        time_html = r.get("time","") or "—"
        row_html += f"""
        <div style="border:1px solid #DDDDDD;border-radius:10px;padding:14px 18px;margin-bottom:12px;">
            <div style="display:flex;justify-content:space-between;align-items:baseline;">
                <div style="font-size:16px;font-weight:700;color:#1A1A1A;">{r['name']} <span style="font-size:12px;color:#777;font-weight:400;">({time_html})</span></div>
                <div style="font-size:12px;color:#0D3D2B;font-weight:700;background:#EAF3EC;padding:3px 10px;border-radius:20px;">Session {r['sessions_done']}/{r['sessions_total']}</div>
            </div>
            <div style="margin-top:6px;font-size:13px;color:#333;"><b>Diagnosis:</b> {r.get('problem','—')}</div>
            <div style="margin-top:2px;font-size:13px;color:#333;"><b>Body area:</b> {r.get('body_area','—')} &nbsp;·&nbsp; <b>Plan:</b> {r.get('treatment_plan','—')}</div>
            {flag_html}
        </div>"""
    if not rows:
        row_html = '<div style="text-align:center;color:#888;padding:30px 0;">No patients scheduled or in active treatment for today.</div>'

    sheet_html = f"""
    <div id="doctor-sheet" style="background:#FFFFFF;color:#1A1A1A;font-family:Arial,Helvetica,sans-serif;padding:24px 28px;border:1px solid #DDDDDD;border-radius:12px;max-width:720px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-end;border-bottom:3px solid #0D3D2B;padding-bottom:10px;margin-bottom:16px;">
            <div>
                <div style="font-size:11px;letter-spacing:2px;color:#C9A84C;font-weight:700;">DAILY PATIENT SHEET</div>
                <div style="font-size:22px;font-weight:800;color:#0D3D2B;">Dr. {doctor_name}</div>
            </div>
            <div style="font-size:13px;color:#555;">{sheet_date}</div>
        </div>
        {row_html}
    </div>"""
    st.markdown(sheet_html, unsafe_allow_html=True)

    components.html(f"""
    <style>
    .print-doc-sheet-btn {{ background:#0D3D2B; color:#FFF; border:none; border-radius:50px; font-weight:600; font-size:0.85rem; padding:12px 28px; font-family:'Plus Jakarta Sans',sans-serif; cursor:pointer; box-shadow:0 2px 10px rgba(13,61,43,0.2); margin-top:10px; }}
    .print-doc-sheet-btn:hover {{ background:#1A5C3E; }}
    </style>
    <button class="print-doc-sheet-btn" onclick="printDocSheet()">🖨️ Print Today's Sheet</button>
    <script>
    function printDocSheet() {{
        var content = `{sheet_html}`;
        var w = window.open('', '_blank', 'width=820,height=900');
        w.document.write('<html><head><title>Daily Sheet</title></head><body style="margin:24px;">' + content + '</body></html>');
        w.document.close();
        setTimeout(function() {{ w.focus(); w.print(); }}, 600);
    }}
    </script>
    """, height=70)

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
    inv = r.get("invoice", "")
    inv_line = f"&nbsp;·&nbsp; {inv}" if inv else ""
    receipt_html = f"""<div class="receipt-wrap" id="printable-receipt">
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
                <div class="receipt-footer-text">We wish you a speedy recovery</div></div></div></div>"""
    st.markdown(receipt_html, unsafe_allow_html=True)
    # Print button — opens a clean print window with ONLY the receipt
    receipt_js = receipt_html.replace("`", "\\`").replace("</div>", "</div>")
    components.html(f"""
    <style>
    .print-btn {{ background:#0D3D2B; color:#FFF; border:none; border-radius:50px; font-weight:600; font-size:0.85rem; padding:12px 28px; font-family:'Plus Jakarta Sans',sans-serif; letter-spacing:0.02em; cursor:pointer; box-shadow:0 2px 10px rgba(13,61,43,0.2); transition:all 0.2s; margin-top:12px; }}
    .print-btn:hover {{ background:#1A5C3E; transform:translateY(-2px); }}
    </style>
    <button class="print-btn" onclick="printReceipt()">🖨️ Print Receipt</button>
    <script>
    function printReceipt() {{
        var fonts = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">';
        var styles = `
        body {{ margin:0; padding:20px; display:flex; justify-content:center; background:#FFF; font-family:'Plus Jakarta Sans',sans-serif; }}
        .receipt-wrap {{ background:#FFFFFF; border-radius:24px; max-width:440px; font-size:0.88rem; color:#0D1F14; border:1px solid #DDE8E1; overflow:hidden; }}
        .receipt-header {{ background:#051811; padding:40px 28px 28px; text-align:center; }}
        .receipt-leaf {{ font-size:1.2rem; color:#C9A84C; margin-bottom:8px; }}
        .receipt-clinic-name {{ font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; color:#FFF; font-style:italic; margin:0; }}
        .receipt-clinic-sub {{ font-size:0.65rem; color:#6FCF97; letter-spacing:0.32em; text-transform:uppercase; margin-top:10px; font-weight:700; }}
        .receipt-gold-line {{ width:40px; height:2px; background:linear-gradient(90deg,transparent,#C9A84C,transparent); margin:12px auto; }}
        .receipt-body {{ padding:28px 32px 32px; }}
        .receipt-date-badge {{ background:#F2F5F1; border-radius:50px; padding:8px 16px; text-align:center; font-size:0.7rem; color:#1A5C3E; font-weight:700; letter-spacing:0.1em; margin-bottom:24px; border:1px solid #DDE8E1; }}
        .receipt-section-title {{ font-size:0.6rem; font-weight:700; color:#6B8A72; text-transform:uppercase; letter-spacing:0.2em; margin:18px 0 10px; }}
        .receipt-row {{ display:flex; justify-content:space-between; align-items:center; margin:9px 0; font-size:0.88rem; }}
        .receipt-row span:first-child {{ color:#4A6B52; }} .receipt-row span:last-child {{ color:#0D1F14; font-weight:700; }}
        .receipt-divider {{ border:none; border-top:1px dashed #DDE8E1; margin:18px 0; }}
        .receipt-total-box {{ background:#0D3D2B; border-radius:18px; padding:18px 22px; margin:20px 0; }}
        .receipt-total-label {{ font-size:0.62rem; color:#6FCF97; font-weight:700; text-transform:uppercase; letter-spacing:0.2em; }}
        .receipt-total-amount {{ font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:500; color:#FFF; margin-top:4px; }}
        .receipt-discount {{ color:#C0392B !important; }}
        .receipt-footer-area {{ text-align:center; padding-top:12px; border-top:1px dashed #DDE8E1; margin-top:22px; }}
        .receipt-footer-text {{ font-size:0.72rem; color:#6B8A72; margin:4px 0; }}
        .receipt-footer-clinic {{ font-size:0.75rem; color:#1A5C3E; font-weight:600; margin-top:8px; }}
        `;
        var content = `{receipt_js}`;
        var w = window.open('', '_blank', 'width=480,height=800');
        w.document.write('<html><head><title>Receipt</title>' + fonts + '<style>' + styles + '</style></head><body>' + content + '</body></html>');
        w.document.close();
        setTimeout(function() {{ w.focus(); w.print(); }}, 600);
    }}
    </script>
    """, height=70)



def auto_payroll():
    month = datetime.now().strftime("%Y-%m"); tag = f"Monthly Payroll — {month}"
    if not sb_exists("expenses", "description", tag):
        total = sb_sum("employees", "salary")
        if total > 0: sb_insert("expenses", {"description": tag, "category": "Payroll", "amount": total, "date": f"{month}-01", "added_by": "System"})

def auto_subscriptions():
    month = datetime.now().strftime("%Y-%m")
    for sub in sb_all("subscriptions", filters={"active": 1}):
        tag = f"Subscription: {sub['name']} — {month}"
        if not sb_exists("expenses", "description", tag):
            day = int(sub.get("billing_day") or 1)
            sb_insert("expenses", {"description": tag, "category": "Subscription", "amount": float(sub["amount"]), "date": f"{month}-{day:02d}", "added_by": "System"})

# Run monthly auto-tasks only once per session (not on every page load) — big speed gain
if "auto_tasks_done" not in st.session_state:
    auto_payroll()
    auto_subscriptions()
    st.session_state.auto_tasks_done = True

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
            with st.form("login_form", clear_on_submit=False):
                u = st.text_input("Username", placeholder="Enter your username", key="login_u")
                p = st.text_input("Password", type="password", placeholder="Enter your password", key="login_p")
                st.markdown("<br>", unsafe_allow_html=True)
                signin_clicked = st.form_submit_button("Sign In →", use_container_width=True)
            if signin_clicked:
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
            ru = st.text_input("New username", key="reg_u")
            rp = st.text_input("New password", type="password", key="reg_p")
            rs = st.selectbox("Role", ["Boss","Accounting","Reception","Reception & Accounting","Doctor"])
            linked_doc_id = None
            if rs == "Doctor":
                all_doc_acc = sb_all("doctors", order="name")
                if all_doc_acc:
                    doc_map_acc = {d["name"]: d["id"] for d in all_doc_acc}
                    chosen_doc_acc = st.selectbox("Which doctor?", list(doc_map_acc.keys()))
                    linked_doc_id = doc_map_acc[chosen_doc_acc]
                else: st.warning("⚠️ Add doctors in Settings first.")
            code = st.text_input("Admin code", type="password", key="reg_code")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create Account", use_container_width=True, key="btn_create_acc"):
                if code != "1011": st.error("Invalid admin code.")
                elif rs == "Doctor" and not linked_doc_id: st.error("Please link a doctor.")
                elif ru and rp:
                    if sb_exists("users","username",ru.strip()): st.error("Username already taken.")
                    else:
                        sb_insert("users",{"username":ru.strip(),"password_hash":hash_password(rp),"role":rs,"linked_doctor_id":linked_doc_id})
                        log_action("System","Create Account",f"User: {ru.strip()} | Role: {rs}")
                        st.success("Account created. Sign in above.")
    st.stop()

role = st.session_state.get("role","")
username = st.session_state.get("username","")
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
    <div style="font-size:0.66rem;background:rgba(201,168,76,0.15);color:#C9A84C;display:inline-block;padding:4px 14px;border-radius:50px;margin-top:8px;font-weight:700;letter-spacing:0.06em;border:1px solid rgba(201,168,76,0.25);font-family:'Plus Jakarta Sans',sans-serif;">{role}</div>
    <div style="margin-top:10px;font-size:0.72rem;color:#9DC2B0;font-family:'Plus Jakarta Sans',sans-serif;">👥 <span style="color:#FFFFFF;font-weight:700;">{sb_count("patients")}</span> total patients</div>
</div>""", unsafe_allow_html=True)

if role in ["Boss","Accounting","Reception & Accounting"]:
    backup_date, backup_days_ago = get_last_backup_info()
    if backup_date is None:
        backup_msg = "⚠️ No backup yet"; backup_color = "#FF8A7A"
    elif backup_days_ago is None:
        backup_msg = f"Backed up: {backup_date}"; backup_color = "#9DC2B0"
    elif backup_days_ago == 0:
        backup_msg = "✅ Backed up today"; backup_color = "#6FCF97"
    elif backup_days_ago <= 30:
        backup_msg = f"Backed up {backup_days_ago}d ago"; backup_color = "#9DC2B0"
    else:
        backup_msg = f"⚠️ Backup is {backup_days_ago}d old"; backup_color = "#FF8A7A"
    st.sidebar.markdown(f"""<div style="padding:0 20px 16px;margin-top:-6px;"><div style="font-size:0.68rem;color:{backup_color};font-family:'Plus Jakarta Sans',sans-serif;">💾 {backup_msg}</div></div>""", unsafe_allow_html=True)

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

    df_tabs = st.tabs(["Patient Assessment","Past Assessments","🩻 Imaging","📋 Today's Sheet"])

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
                tier_name, tier_icon, tier_color, tier_sub = get_patient_loyalty(pid_doc, pat_doc.get("created_at"), visits_count)
                tier_chip_html = f'<span class="patient-chip" style="border-color:{tier_color};color:{tier_color};font-weight:700;" title="{tier_sub}">{tier_icon} {tier_name}</span>' if tier_name else ""
                st.markdown(f"""<div class="patient-chip-bar">
                    <div class="patient-chip-name">{pat_doc["name"]}</div>
                    {tier_chip_html}
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
                        st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;"><div style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:1.1rem;color:#EAF2EC;">{f.get("filled_date","")}</div><span class="tag-pill {outcome_class}">{f.get("outcome","Pending")}</span></div><div style="font-size:0.88rem;color:#EAF2EC;margin-bottom:8px;"><strong style="color:#D4B45C;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Diagnosis</strong><br/>{f.get("problem","—")}</div><div style="font-size:0.88rem;color:#EAF2EC;margin-bottom:8px;"><strong style="color:#D4B45C;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Body Area</strong> <span style="color:#9DC2B0;">{f.get("body_area","—")}</span> · <strong style="color:#D4B45C;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Pain</strong> <span style="color:#9DC2B0;">{f.get("pain_before","—")}/10 → {f.get("pain_after","—")}/10</span></div><div style="font-size:0.85rem;color:#8FB8A6;"><strong style="color:#D4B45C;font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;">Plan</strong><br/>{f.get("treatment_plan","—")}</div></div>', unsafe_allow_html=True)
                        if st.button(f"✏️ Edit this assessment", key=f"edit_btn_{f['id']}"):
                            st.session_state[f"editing_form_{f['id']}"] = True
                        if st.session_state.get(f"editing_form_{f['id']}"):
                            with st.expander(f"✏️ Editing assessment from {f.get('filled_date','')}", expanded=True):
                                ec1, ec2 = st.columns(2)
                                with ec1:
                                    e_complaint = st.text_input("Chief Complaint", value=f.get("chief_complaint","") or "", key=f"e_complaint_{f['id']}")
                                    e_duration  = st.text_input("Duration", value=f.get("duration","") or "", key=f"e_duration_{f['id']}")
                                    body_opts = ["— select —","Neck / Cervical","Upper back","Lower back / Lumbar","Shoulder","Elbow","Wrist / Hand","Hip","Knee","Ankle / Foot","Multiple areas","Other"]
                                    cur_body = f.get("body_area","— select —") or "— select —"
                                    e_body = st.selectbox("Body Area", body_opts, index=body_opts.index(cur_body) if cur_body in body_opts else 0, key=f"e_body_{f['id']}")
                                    e_history = st.text_area("History", value=f.get("history","") or "", height=80, key=f"e_history_{f['id']}")
                                with ec2:
                                    e_problem  = st.text_area("Diagnosis", value=f.get("problem","") or "", height=80, key=f"e_problem_{f['id']}")
                                    e_plan     = st.text_area("Treatment Plan", value=f.get("treatment_plan","") or "", height=80, key=f"e_plan_{f['id']}")
                                    e_sessions = st.number_input("Sessions Needed", min_value=1, step=1, value=int(f.get("sessions_needed") or 10), key=f"e_sessions_{f['id']}")
                                ep1, ep2 = st.columns(2)
                                with ep1: e_pain_before = st.slider("Pain Before (0-10)", 0, 10, int(f.get("pain_before") or 0), key=f"e_pain_b_{f['id']}")
                                with ep2: e_pain_after  = st.slider("Pain After (0-10)",  0, 10, int(f.get("pain_after") or 0),  key=f"e_pain_a_{f['id']}")
                                outcome_opts = ["Pending","Full Recovery Expected","Partial Recovery Expected","Long-term Management","Successfully Relieved","Partially Improved","No Improvement","Patient Discontinued","Other"]
                                cur_out = f.get("outcome","Pending") or "Pending"
                                e_outcome = st.selectbox("Outcome", outcome_opts, index=outcome_opts.index(cur_out) if cur_out in outcome_opts else 0, key=f"e_outcome_{f['id']}")
                                e_notes = st.text_area("Notes", value=f.get("notes","") or "", height=60, key=f"e_notes_{f['id']}")
                                sc1, sc2 = st.columns(2)
                                with sc1:
                                    if st.button("💾 Save Changes", key=f"save_edit_{f['id']}", use_container_width=True):
                                        sb_update("doctor_intake_form", {
                                            "chief_complaint": e_complaint, "duration": e_duration,
                                            "body_area": e_body if e_body != "— select —" else "",
                                            "history": e_history, "problem": e_problem,
                                            "treatment_plan": e_plan, "sessions_needed": int(e_sessions),
                                            "pain_before": e_pain_before, "pain_after": e_pain_after,
                                            "outcome": e_outcome, "notes": e_notes
                                        }, "id", f["id"])
                                        # Update session plan if sessions changed
                                        existing_sess = sb_one("patient_sessions", filters={"patient_id": pid_doc})
                                        if existing_sess:
                                            sb_update("patient_sessions", {"total_sessions": int(e_sessions)}, "id", existing_sess["id"])
                                        log_action(username, "Edit Assessment", f"#{f['id']} for {sel_pat_doc}")
                                        del st.session_state[f"editing_form_{f['id']}"]
                                        play_ding(); st.success("Assessment updated!"); st.rerun()
                                with sc2:
                                    if st.button("Cancel", key=f"cancel_edit_{f['id']}", use_container_width=True):
                                        del st.session_state[f"editing_form_{f['id']}"]
                                        st.rerun()

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

    with df_tabs[2]:
        import os as _os
        section_label("🩻 X-Ray / CT / Imaging")
        st.caption("Upload images received from the imaging department (X-ray, CT scan, MRI, etc.) sent via WhatsApp. They'll be saved here under the patient's name.")
        img_search = st.text_input("Search patient by name or phone", key="img_search", placeholder="Type to search...")
        all_p_img = sb_all("patients", order="name")
        if img_search: all_p_img = [p for p in all_p_img if img_search.lower() in (p.get("name","")).lower() or img_search in (p.get("phone","") or "")]
        if all_p_img:
            sel_pat_img = st.selectbox("Select patient", ["— select —"]+[p["name"] for p in all_p_img], key="img_pat_sel")
            if sel_pat_img != "— select —":
                pat_img = next(p for p in all_p_img if p["name"]==sel_pat_img)
                pid_img = pat_img["id"]
                st.markdown(f'<div class="patient-chip-bar"><div class="patient-chip-name">{pat_img["name"]}</div><span class="patient-chip">{patient_id_fmt(pid_img)}</span></div>', unsafe_allow_html=True)

                with st.form("upload_image_form", clear_on_submit=True):
                    up_files = st.file_uploader("Drag & drop or browse image files", type=["png","jpg","jpeg","webp","pdf"], accept_multiple_files=True, key="img_uploader")
                    up_label = st.selectbox("Image type", ["X-Ray","CT Scan","MRI","Ultrasound","Lab Report","Other"], key="img_label_sel")
                    up_notes = st.text_input("Notes (optional)", placeholder="e.g. Lumbar spine, lateral view", key="img_notes_input")
                    submitted_img = st.form_submit_button("📤 Save to Patient Record", use_container_width=True)
                    if submitted_img:
                        if not up_files:
                            st.error("Please select at least one file.")
                        else:
                            save_dir = f"/mnt/user-data/outputs/patient_images/{pid_img}"
                            _os.makedirs(save_dir, exist_ok=True)
                            saved = 0
                            for uf in up_files:
                                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                                safe_name = f"{ts}_{uf.name}".replace(" ", "_")
                                fpath = f"{save_dir}/{safe_name}"
                                with open(fpath, "wb") as out_f: out_f.write(uf.getbuffer())
                                sb_insert("patient_images", {"patient_id": pid_img, "file_path": fpath, "file_name": uf.name, "image_type": up_label, "notes": up_notes.strip(), "uploaded_by": username, "uploaded_at": today_str})
                                saved += 1
                            log_action(username, "Upload Imaging", f"{saved} file(s) for {sel_pat_img}")
                            play_ding(); st.success(f"✅ Saved {saved} image(s) to {sel_pat_img}'s record."); st.rerun()

                st.markdown("---")
                section_label(f"Imaging History")
                patient_imgs = sb_all("patient_images", filters={"patient_id": pid_img}, order="id", desc_order=True)
                if patient_imgs:
                    for pi in patient_imgs:
                        ic1, ic2 = st.columns([4,1])
                        with ic1:
                            fpath_show = pi.get("file_path","")
                            is_image = fpath_show.lower().endswith((".png",".jpg",".jpeg",".webp"))
                            notes_line = pi.get("notes","") or ""
                            notes_html = f'<div style="margin-top:6px;font-size:0.85rem;color:#C5D6CC;">{notes_line}</div>' if notes_line else ""
                            st.markdown(f'<div class="card" style="padding:14px 20px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><span class="tag-pill tag-pending">{pi.get("image_type","")}</span> <span style="color:#EAF2EC;font-weight:600;margin-left:8px;">{pi.get("file_name","")}</span></div><div style="font-size:0.78rem;color:#9DC2B0;">{pi.get("uploaded_at","")} · by {pi.get("uploaded_by","")}</div></div>{notes_html}</div>', unsafe_allow_html=True)
                            if is_image and _os.path.exists(fpath_show):
                                st.image(fpath_show, width=280)
                        with ic2:
                            if st.button("🗑️ Delete", key=f"del_img_{pi['id']}"):
                                try:
                                    if _os.path.exists(fpath_show): _os.remove(fpath_show)
                                except: pass
                                sb_delete("patient_images", "id", pi["id"])
                                play_ding(); st.success("Deleted."); st.rerun()
                else:
                    st.info("No images uploaded yet for this patient.")
        else:
            st.info("No patients found.")

    with df_tabs[3]:
        section_label("📋 Today's Patient Sheet")
        st.caption("A quick one-page summary of today's patients and their treatment stage — for a glance each morning, separate from reception's appointment printout.")

        sheet_rows = []
        seen_pids = set()

        # 1) Today's scheduled appointments with this doctor
        todays_appts_doc = sb_all("appointments", filters={"doctor_id": linked_doctor_id, "appt_date": today_str})
        patients_map_sheet = {p["id"]: p for p in sb_all("patients")}
        intake_all_sheet = sb_all("doctor_intake_form", filters={"doctor_id": linked_doctor_id})
        sessions_all_sheet = sb_all("patient_sessions")

        def _latest_intake(pid):
            matches = [f for f in intake_all_sheet if f.get("patient_id")==pid]
            return sorted(matches, key=lambda x: x.get("id",0), reverse=True)[0] if matches else {}

        def _session_progress(pid):
            s = next((s for s in sessions_all_sheet if s.get("patient_id")==pid), None)
            if not s: return ("0","0")
            return (str(int(s.get("sessions_done") or 0)), str(int(s.get("total_sessions") or 0)))

        for a in todays_appts_doc:
            pid = a.get("patient_id")
            if pid in seen_pids: continue
            pat = patients_map_sheet.get(pid)
            if not pat: continue
            intake = _latest_intake(pid)
            done, total = _session_progress(pid)
            sheet_rows.append({"name": pat["name"], "time": a.get("appt_time",""), "sessions_done": done, "sessions_total": total,
                "problem": intake.get("problem",""), "body_area": intake.get("body_area",""), "treatment_plan": intake.get("treatment_plan",""),
                "red_flags": intake.get("red_flags","")})
            seen_pids.add(pid)

        # 2) Patients assigned to this doctor with sessions still remaining (not already listed above), in case no appointment was booked
        assigned_patients = [p for p in patients_map_sheet.values() if p.get("assigned_doctor_id")==linked_doctor_id]
        for pat in assigned_patients:
            pid = pat["id"]
            if pid in seen_pids: continue
            done, total = _session_progress(pid)
            if total and int(done) >= int(total): continue
            if not total or total == "0": continue
            intake = _latest_intake(pid)
            sheet_rows.append({"name": pat["name"], "time": "", "sessions_done": done, "sessions_total": total,
                "problem": intake.get("problem",""), "body_area": intake.get("body_area",""), "treatment_plan": intake.get("treatment_plan",""),
                "red_flags": intake.get("red_flags","")})
            seen_pids.add(pid)

        sheet_date_display = date.today().strftime("%A, %B %d, %Y")
        render_doctor_daily_sheet(doc_info['name'] if doc_info else 'Unknown', sheet_rows, sheet_date_display)

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
                st.markdown(f'<div class="card" style="border-left:3px solid {sc};"><div style="font-family:Inter,sans-serif;font-size:0.65rem;color:#9DC2B0;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;">{a["Time"]}</div><div style="font-family:Fraunces,serif;font-size:1.3rem;font-style:italic;color:#EAF2EC;margin:6px 0;letter-spacing:-0.01em;">{a["Patient"]}</div><div style="font-size:0.85rem;color:#C5D6CC;">Dr. {a["Doctor"]}</div><div style="font-size:0.78rem;color:#9DC2B0;margin-top:4px;font-style:italic;">{a.get("Reason","")}</div><span class="tag-pill" style="background:{sc}25;color:{sc};margin-top:8px;display:inline-block;">{a["Status"]}</span></div>', unsafe_allow_html=True)
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
    # ── Notification bell (top-right) ──
    followup_list_notif = get_followup_patients(days_after=20)
    overdue_notif = get_overdue_patients()
    expiring_notif = [s for s in sb_all("patient_subscriptions") if s.get("status")=="Active" and s.get("end_date") in [today_str, tomorrow_str]]
    tomorrow_appts_notif = get_tomorrow_appointments()
    noshow_notif = get_doctor_noshows()
    notif_count = len(followup_list_notif) + len(overdue_notif) + len(expiring_notif) + len(tomorrow_appts_notif) + len(noshow_notif)

    head_l, head_r = st.columns([4, 1])
    with head_l:
        page_header("Front Desk", "Reception", "Patient intake, checkout, and management.")
    with head_r:
        badge = f'<span style="position:absolute;top:-6px;right:-6px;background:#C0392B;color:#FFF;font-size:0.7rem;font-weight:700;min-width:20px;height:20px;border-radius:50px;display:flex;align-items:center;justify-content:center;padding:0 5px;border:2px solid #F2F5F1;">{notif_count}</span>' if notif_count > 0 else ''
        st.markdown(f'<div style="text-align:right;padding-top:18px;"><div style="position:relative;display:inline-block;background:#FFFFFF;border:1px solid #DDE8E1;border-radius:50px;padding:12px 16px;box-shadow:0 2px 8px rgba(13,31,20,0.05);"><span style="font-size:1.3rem;">🔔</span>{badge}</div></div>', unsafe_allow_html=True)
        if notif_count > 0:
            with st.expander(f"🔔 {notif_count} notifications", expanded=False):
                if tomorrow_appts_notif:
                    st.markdown(f"**📅 {len(tomorrow_appts_notif)} appointment{'s' if len(tomorrow_appts_notif)>1 else ''} tomorrow** — remind patients below")
                    for ta in tomorrow_appts_notif[:5]:
                        st.caption(f"• {ta['name']} — {ta['time']} with Dr. {ta['doctor']}")
                if noshow_notif:
                    st.markdown(f"**❗ {len(noshow_notif)} patient{'s' if len(noshow_notif)>1 else ''} didn't come today** (doctor's scheduled day)")
                    for ns in noshow_notif[:5]:
                        st.caption(f"• {ns['name']} — Dr. {ns['doctor']}, {ns['remaining']} sessions left")
                if followup_list_notif:
                    st.markdown(f"**💬 {len(followup_list_notif)} follow-up{'s' if len(followup_list_notif)>1 else ''} needed** — open the Follow-up tab")
                    for fu in followup_list_notif[:5]:
                        st.caption(f"• {fu['name']} — finished {fu['days_passed']} days ago")
                if overdue_notif:
                    st.markdown(f"**⏰ {len(overdue_notif)} overdue patient{'s' if len(overdue_notif)>1 else ''}**")
                    for od in overdue_notif[:5]:
                        st.caption(f"• {od['name']} — {od['remaining']} sessions left, last visit {od['last_visit']}")
                if expiring_notif:
                    pmap_notif = {p["id"]: p["name"] for p in sb_all("patients")}
                    st.markdown(f"**⚠️ {len(expiring_notif)} subscription{'s' if len(expiring_notif)>1 else ''} expiring**")
                    for s in expiring_notif[:5]:
                        st.caption(f"• {pmap_notif.get(s.get('patient_id'),'Unknown')} — '{s.get('plan_name','')}' expires {s.get('end_date','')}")

    pulse_bar([("Today's Revenue",fmt(today_revenue)),("Visits Today",str(today_visits_count)),("Total Patients",str(patient_count)),("Notifications",str(notif_count))])

    # ── No-show banner ──
    if noshow_notif:
        names_ns = ", ".join([f"{ns['name']} (Dr. {ns['doctor']})" for ns in noshow_notif[:4]])
        st.warning(f"❗ **{len(noshow_notif)} patient{'s' if len(noshow_notif)>1 else ''} didn't come in today** despite it being their doctor's scheduled day: {names_ns} — consider calling to ask why.")

    # ── Tomorrow's appointment reminders ──
    if tomorrow_appts_notif:
        with st.expander(f"📅 {len(tomorrow_appts_notif)} appointment{'s' if len(tomorrow_appts_notif)>1 else ''} tomorrow — send reminders", expanded=False):
            cp_rem = get_clinic_profile()
            rem_template = get_reminder_template()
            for ta in tomorrow_appts_notif:
                msg_rem = rem_template.replace("{name}", ta["name"]).replace("{clinic}", cp_rem.get("clinic_name","Garden Clinic")).replace("{date}", ta["date"]).replace("{time}", ta["time"]).replace("{doctor}", ta["doctor"])
                wa_url_rem = whatsapp_link(ta["phone"], msg_rem)
                rcol1, rcol2 = st.columns([3,1])
                with rcol1:
                    st.markdown(f'<div class="card" style="margin-bottom:8px;padding:14px 20px;"><div style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:1.15rem;color:#EAF2EC;">{ta["name"]}</div><div style="font-size:0.8rem;color:#9DC2B0;margin-top:2px;">📞 {ta["phone"] or "No phone"} · {ta["time"]} with Dr. {ta["doctor"]}{" · " + ta["reason"] if ta.get("reason") else ""}</div></div>', unsafe_allow_html=True)
                with rcol2:
                    if ta["phone"]:
                        st.markdown(f'<a href="{wa_url_rem}" target="_blank" style="display:inline-block;background:#25D366;color:#FFFFFF;padding:10px 18px;border-radius:50px;text-decoration:none;font-weight:600;font-size:0.82rem;text-align:center;width:100%;box-shadow:0 2px 10px rgba(37,211,102,0.3);">💬 Remind</a>', unsafe_allow_html=True)
                    else:
                        st.caption("⚠️ No phone")

    # ── Follow-up banner ──
    if followup_list_notif:
        names_fu = ", ".join([fu["name"] for fu in followup_list_notif[:4]])
        st.info(f"💬 **{len(followup_list_notif)} patient{'s' if len(followup_list_notif)>1 else ''} need follow-up:** {names_fu} — open the **💬 Follow-up** tab to send WhatsApp messages.")

    # ── Today's appointments banner ──
    today_appts_top = [a for a in get_appointments_joined() if a.get("Date")==today_str and a.get("Status")=="Scheduled"]
    if today_appts_top:
        names = " · ".join([f"**{a['Patient']}** @ {a['Time']}" for a in today_appts_top[:4]])
        st.info(f"📅 **{len(today_appts_top)} appointment{'s' if len(today_appts_top)>1 else ''} today:** {names}")

    # ── Overdue patients ──
    overdue_list = get_overdue_patients()
    for od in overdue_list:
        st.warning(f"⏰ **{od['name']}** hasn't visited in 14+ days — still has **{od['remaining']} sessions remaining** (last visit: {od['last_visit']})")

    # ── Expiring subscriptions ──
    all_pt_subs = sb_all("patient_subscriptions")
    expiring_rec = [s for s in all_pt_subs if s.get("status")=="Active" and s.get("end_date") in [today_str, tomorrow_str]]
    if expiring_rec:
        patients_map_r = {p["id"]: p["name"] for p in sb_all("patients")}
        for s in expiring_rec:
            pname = patients_map_r.get(s.get("patient_id"),"Unknown")
            st.warning(f"⚠️ **{pname}** subscription **'{s.get('plan_name','')}'** expires {'TODAY' if s.get('end_date')==today_str else 'TOMORROW'}!")

    # ── Quick phone search (auto-focused on load) ──
    quick_search = st.text_input("🔍 Quick search — name or phone number", placeholder="Type anything to find a patient instantly...", key="reception_quick_search")
    components.html("""<script>
    setTimeout(function(){
        try {
            var inputs = window.parent.document.querySelectorAll('input[aria-label*="Quick search"]');
            if (inputs.length) { inputs[0].focus(); }
        } catch(e) {}
    }, 300);
    </script>""", height=0, width=0)

    if quick_search:
        all_p_qs = sb_all("patients", order="name")
        found = [p for p in all_p_qs if quick_search.lower() in (p.get("name","")).lower() or quick_search in (p.get("phone","") or "")]
        if found:
            for p in found[:5]:
                visits_p = len([v for v in sb_all("visits", filters={"patient_id": p["id"]}) ])
                phone_disp = p.get("phone","—")
                st.markdown(f'<div class="card" style="padding:14px 20px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:1.2rem;color:#EAF2EC;">{p["name"]}</div><div style="font-size:0.8rem;color:#8FB8A6;margin-top:2px;">{patient_id_fmt(p["id"])} · 📞 {phone_disp} · {p.get("gender","—")} · {visits_p} visits</div></div></div></div>', unsafe_allow_html=True)
                if phone_disp != "—" and phone_disp:
                    components.html(f"""<button onclick="navigator.clipboard.writeText('{phone_disp}')" style="background:rgba(201,168,76,0.15);color:#D4B45C;border:1px solid rgba(201,168,76,0.4);border-radius:50px;padding:5px 14px;font-size:0.75rem;font-family:'Plus Jakarta Sans',sans-serif;cursor:pointer;margin-top:-8px;margin-bottom:8px;">📋 Copy phone</button>""", height=36)
                st.session_state.setdefault("recent_patients", [])
                if p["name"] not in st.session_state["recent_patients"]:
                    st.session_state["recent_patients"] = [p["name"]] + st.session_state["recent_patients"]
                    st.session_state["recent_patients"] = st.session_state["recent_patients"][:5]
        else:
            st.info("No patient found with that name or phone.")

    # ── Recently viewed patients shortcut ──
    if st.session_state.get("recent_patients"):
        with st.expander(f"🕘 Recently viewed ({len(st.session_state['recent_patients'])})", expanded=False):
            recent_cols = st.columns(len(st.session_state["recent_patients"]))
            for i, rname in enumerate(st.session_state["recent_patients"]):
                with recent_cols[i]:
                    st.markdown(f'<span class="patient-chip">{rname}</span>', unsafe_allow_html=True)

    t1,t3,t2,tD,tQ,tW,t4,t5,t6,t7,t8,t9 = st.tabs(["Checkout","Register","Patients","Doctor Notes","Quick View","💬 Follow-up","Edit","Sessions","Subscriptions","Check-in","History","Edit/Delete"])

    with t1:
        section_label("New Checkout")
        patients_db = sb_all("patients", order="name"); docs_db = sb_all("doctors", order="name")
        services_db = [s for s in sb_all("services", order="name") if s.get("active")==1]
        bundles_db  = sb_all("bundles", order="name")
        if not docs_db or (not services_db and not bundles_db):
            st.warning("Please add doctors and services in Settings before checkout.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}
            doc_visit_counts = {d["id"]: sb_count("visits", filters={"doctor_id": d["id"]}) for d in docs_db}
            doc_display_map = {f'{d["name"]} ({doc_visit_counts[d["id"]]} visits)': d["name"] for d in docs_db}
            d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1:
                target_p = st.selectbox("Patient", ["— select —"]+list(p_map.keys()))
                chosen_doc_display = st.selectbox("Doctor", list(doc_display_map.keys()))
                chosen_doc = doc_display_map[chosen_doc_display]
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
                    st.markdown(f'<div class="card" style="border-left:3px solid #4A6752;"><div style="font-size:0.65rem;color:#4A6752;font-weight:600;letter-spacing:0.18em;text-transform:uppercase;">Doctor\'s Plan</div><div style="margin-top:8px;font-family:Fraunces,serif;font-size:1.1rem;font-style:italic;color:#EAF2EC;">{assessment.get("problem","")}</div><div style="margin-top:6px;font-size:0.88rem;color:#C5D6CC;">Sessions: <strong>{done_count}/{total_count}</strong> · Remaining: <strong>{rem}</strong> · Body area: {assessment.get("body_area","—")}</div></div>', unsafe_allow_html=True)

            final_due = base_price
            if disc_type == "Fixed (IQD)": final_due = max(0.0, base_price-disc_val)
            elif disc_type == "Percent (%)": final_due = max(0.0, base_price*(1-disc_val/100))
            visit_notes = st.text_area("Visit notes", height=70)
            referrers_db = sb_all("referrers", order="name"); ref_names = [r["name"] for r in referrers_db]
            referral_options = ["Walk-in / Direct","Instagram / Social Media","Google Search","Friend / Word of mouth"]+ref_names
            how_found = st.selectbox("How did the patient find us?", referral_options)
            referred_by_val = how_found if how_found in ref_names else None
            st.markdown(f'<div style="font-family:Fraunces,serif;font-size:1.8rem;font-style:italic;color:#EAF2EC;margin:20px 0;">Total due: <strong style="color:#D4B45C;">{fmt(final_due)}</strong></div>', unsafe_allow_html=True)
            if st.button("Save & Print Receipt", use_container_width=True):
                if target_p == "— select —": st.error("Please select a patient.")
                elif base_price == 0.0: st.error("Please select a service or bundle.")
                else:
                    disc_amt = base_price - final_due
                    inv_num = get_invoice_number()
                    sb_insert("visits",{"patient_id":p_map[target_p],"doctor_id":d_map[chosen_doc],"service_id":srv_id,"bundle_id":bnd_id,"visit_date":today_str,"base_price":base_price,"discount_amount":disc_amt,"net_paid":final_due,"payment_method":payment_method,"notes":visit_notes,"referred_by":referred_by_val,"added_by":username})
                    todays_appts = sb_all("appointments", filters={"patient_id": p_map[target_p], "appt_date": today_str, "status": "Scheduled"})
                    for ap in todays_appts: sb_update("appointments", {"status": "Completed"}, "id", ap["id"])
                    sess = sb_one("patient_sessions", filters={"patient_id": p_map[target_p]})
                    completed_all = False
                    if sess:
                        new_done = int(sess.get("sessions_done") or 0) + 1
                        sb_update("patient_sessions", {"sessions_done": new_done}, "id", sess["id"])
                        total_s = int(sess.get("total_sessions") or 0)
                        if total_s > 0 and new_done >= total_s:
                            st.balloons(); st.success(f"🎉 {target_p} has completed all {total_s} sessions!")
                            completed_all = True
                            st.session_state["discharge_pid"] = p_map[target_p]
                            st.session_state["discharge_name"] = target_p
                            st.session_state["discharge_done"] = new_done
                    log_action(username,"New Visit",f"Patient: {target_p} | Doctor: {chosen_doc} | Paid: {fmt(final_due)} | {inv_num}")
                    play_ding(); st.success(f"Visit saved · {inv_num}")
                    st.session_state.rcpt = {"patient":target_p,"doctor":chosen_doc,"item":chosen_item_name,"base":base_price,"disc":disc_amt,"net":final_due,"method":payment_method,"date":today_str,"invoice":inv_num,"patient_id_fmt":patient_id_fmt(p_map[target_p])}
            if "rcpt" in st.session_state: render_receipt(st.session_state.rcpt, get_clinic_profile())

            # ── Discharge summary ──
            if "discharge_pid" in st.session_state:
                assessment_dc = sb_one("doctor_intake_form", filters={"patient_id": st.session_state["discharge_pid"]})
                if assessment_dc:
                    st.markdown("---")
                    section_label("🎓 Patient Discharge Summary")
                    st.info("💡 Press **Ctrl+P** to print this discharge summary for the patient.")
                    render_discharge_summary(st.session_state["discharge_name"], st.session_state["discharge_pid"], assessment_dc, st.session_state["discharge_done"], get_clinic_profile())

            # ── Daily cash summary ──
            st.markdown("---")
            section_label("💰 Today's Payment Breakdown")
            today_v = sb_all("visits", filters={"visit_date": today_str})
            if today_v:
                methods = {}
                for v in today_v:
                    m = v.get("payment_method","Cash") or "Cash"
                    if m not in methods: methods[m] = {"count": 0, "total": 0.0}
                    methods[m]["count"] += 1
                    methods[m]["total"] += float(v.get("net_paid") or 0)
                cols_cash = st.columns(len(methods))
                icons = {"Cash":"💵","Card":"💳","Insurance":"🏥","Transfer":"🔁","Subscription":"📋"}
                for i, (method, info) in enumerate(methods.items()):
                    with cols_cash[i]:
                        st.markdown(card(f"{icons.get(method,'💰')} {method}", fmt(info['total']), "dark", f"{info['count']} visit{'s' if info['count']>1 else ''}"), unsafe_allow_html=True)
            else:
                st.info("No visits yet today.")

    with t2:
        section_label("All Patients")
        search = st.text_input("Search by name or phone", key="t2_search")
        all_p = sb_all("patients", order="name")
        if search: all_p = [p for p in all_p if search.lower() in (p.get("name","")).lower() or search in (p.get("phone","") or "")]
        if all_p:
            all_visits_t2 = sb_all("visits", order="visit_date", desc_order=True)
            last_visit_map = {}
            for v in all_visits_t2:
                pid_v = v.get("patient_id")
                if pid_v not in last_visit_map:
                    last_visit_map[pid_v] = v.get("visit_date","")
            rows_t2 = []
            for p in all_p:
                row = dict(p)
                row["last_visit"] = last_visit_map.get(p["id"], "Never")
                rows_t2.append(row)
            st.dataframe(pd.DataFrame(rows_t2), use_container_width=True, hide_index=True)
            del_target = st.selectbox("Remove patient", ["— select —"]+[p["name"] for p in all_p])
            if del_target != "— select —":
                confirm_del_patient = st.checkbox(f"⚠️ Yes, I'm sure I want to permanently delete '{del_target}'", key="confirm_del_patient")
                if st.button("Remove Patient", type="primary"):
                    if not confirm_del_patient:
                        st.error("Please check the confirmation box above first.")
                    else:
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
                st.markdown(f'<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="font-family:Cormorant Garamond,serif;font-size:1.5rem;font-style:italic;color:#FFFFFF;letter-spacing:-0.01em;">{pname}</div><span class="tag-pill {outcome_class}">{f.get("outcome","Pending")}</span></div><div style="font-size:0.78rem;color:#9DC2B0;margin-top:6px;font-family:Inter,sans-serif;letter-spacing:0.04em;">Dr. {dname} · {f.get("filled_date","")} · {rem_text}</div><div style="margin-top:14px;display:flex;flex-wrap:wrap;gap:6px;">{f"<span class=patient-chip>{f.get('body_area','')}</span>" if f.get('body_area') else ''}{f"<span class=patient-chip>{f.get('duration','')}</span>" if f.get('duration') else ''}{f"<span class=patient-chip accent>Pain: {f.get('pain_before','—')}/10</span>"}</div><div style="margin-top:14px;font-size:0.9rem;color:#EAF2EC;"><strong style="color:#D4B45C;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Diagnosis</strong><br/>{f.get("problem","—")}</div><div style="margin-top:10px;font-size:0.88rem;color:#C5D6CC;"><strong style="color:#D4B45C;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Treatment Plan</strong><br/>{f.get("treatment_plan","—")}</div>{f"<div style=margin-top:10px;font-size:0.85rem;color:#FF8A7A;><strong style=color:#FF8A7A;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;>Red Flags</strong><br/>{f.get('red_flags','')}</div>" if f.get("red_flags") else ""}</div>', unsafe_allow_html=True)
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
                qv_visits_count = sb_count("visits", filters={"patient_id": pid})
                qv_tier_name, qv_tier_icon, qv_tier_color, qv_tier_sub = get_patient_loyalty(pid, pat.get("created_at"), qv_visits_count)
                qv_tier_badge = f' &nbsp;·&nbsp; <span style="color:{qv_tier_color};font-weight:700;">{qv_tier_icon} {qv_tier_name} Patient</span>' if qv_tier_name else ""
                st.markdown(f'<div class="profile-summary"><div class="profile-kicker">Patient Profile</div><div class="profile-name">{pat["name"]}</div><div class="profile-meta">📞 {pat.get("phone","—")} &nbsp;·&nbsp; 🎂 {pat.get("date_of_birth","—")} &nbsp;·&nbsp; {pat.get("gender","—")}{qv_tier_badge}</div></div>', unsafe_allow_html=True)
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
                    st.markdown(f'<div class="card"><div style="font-size:0.88rem;color:#EAF2EC;"><strong style="color:#D4B45C;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Problem</strong><br/>{assessment_q.get("problem","")}</div><div style="margin-top:10px;font-size:0.88rem;color:#EAF2EC;"><strong style="color:#D4B45C;font-size:0.66rem;letter-spacing:0.18em;text-transform:uppercase;">Plan</strong><br/>{assessment_q.get("treatment_plan","")}</div><div style="margin-top:10px;font-size:0.85rem;color:#C5D6CC;">Outcome: {assessment_q.get("outcome","Pending")} · Pain: {assessment_q.get("pain_before","—")}/10 → {assessment_q.get("pain_after","—")}/10</div></div>', unsafe_allow_html=True)
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

    with tW:
        section_label("💬 WhatsApp Follow-up")
        st.info("💡 Patients who completed all their sessions and haven't returned in 20+ days. Click the WhatsApp button to send them a check-in message.")
        cp_w = get_clinic_profile()
        followups = get_followup_patients(days_after=20)
        if followups:
            template = get_followup_template()
            for fu in followups:
                msg = template.replace("{name}", fu["name"]).replace("{clinic}", cp_w.get("clinic_name","Garden Clinic")).replace("{days}", str(fu["days_passed"]))
                wa_url = whatsapp_link(fu["phone"], msg)
                phone_display = fu["phone"] if fu["phone"] else "⚠️ No phone number"
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f'<div class="card" style="margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;"><div><div style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:1.3rem;color:#EAF2EC;">{fu["name"]}</div><div style="font-size:0.8rem;color:#8FB8A6;margin-top:4px;">📞 {phone_display} · Completed {fu["total_sessions"]} sessions · Last visit {fu["last_visit"]} ({fu["days_passed"]} days ago)</div></div></div></div>', unsafe_allow_html=True)
                with col_b:
                    if fu["phone"]:
                        st.markdown(f'<a href="{wa_url}" target="_blank" style="display:inline-block;background:#25D366;color:#FFFFFF;padding:12px 20px;border-radius:50px;text-decoration:none;font-weight:600;font-size:0.85rem;text-align:center;width:100%;box-shadow:0 2px 10px rgba(37,211,102,0.3);">💬 WhatsApp</a>', unsafe_allow_html=True)
                    if st.button("✓ Mark contacted", key=f"contacted_{fu['patient_id']}_{fu['last_visit']}"):
                        sb_insert("followup_log", {"patient_id": fu["patient_id"], "last_visit": fu["last_visit"], "contacted_date": today_str, "contacted_by": username})
                        log_action(username, "Follow-up Sent", f"{fu['name']} ({fu['days_passed']} days after completion)")
                        play_ding(); st.success(f"Marked {fu['name']} as contacted."); st.rerun()
            st.markdown("---")
            section_label("Message preview")
            st.markdown(f'<div class="card"><div style="font-size:0.9rem;color:#EAF2EC;line-height:1.7;">{get_followup_template().replace("{name}", "[Patient Name]").replace("{clinic}", cp_w.get("clinic_name","Garden Clinic")).replace("{days}", "20")}</div></div>', unsafe_allow_html=True)
            st.caption("You can customize this message in Settings → Clinic Profile.")
        else:
            st.success("✓ No follow-ups needed right now. All completed patients have been contacted or it hasn't been 20 days yet.")

    with t3:
        section_label("Register New Patient")
        with st.form("register_patient_form", clear_on_submit=True):
            c1,c2 = st.columns(2)
            with c1:
                p_name = st.text_input("Full name *")
                pc1, pc2 = st.columns([1, 2])
                with pc1: p_country_code = st.text_input("Code", value="964", key="p_country_code")
                with pc2: p_phone_local = st.text_input("Phone number", placeholder="7701234567", key="p_phone_local")
                p_dob  = st.text_input("Date of birth (YYYY-MM-DD)", placeholder="1990-01-15")
            with c2:
                p_gender = st.selectbox("Gender", ["Prefer not to say","Male","Female","Other"])
                all_docs_reg = sb_all("doctors", order="name")
                doc_names_reg = ["Not assigned yet"] + [d["name"] for d in all_docs_reg]
                p_assigned_doc = st.selectbox("Assigned Doctor", doc_names_reg, help="Which doctor will be treating this patient? Used for no-show tracking.")
                p_notes  = st.text_area("Notes", height=100)
            p_phone = (p_country_code.strip() + p_phone_local.strip()) if p_phone_local.strip() else ""
            give_receipt = st.checkbox("📄 Print intake receipt", value=True)
            submitted_reg = st.form_submit_button("Register Patient", use_container_width=True)
            if submitted_reg:
                if p_name.strip():
                    p_name_clean = auto_cap_name(p_name)
                    if sb_exists("patients","name",p_name_clean): st.error("Already exists.")
                    else:
                        assigned_doc_id = next((d["id"] for d in all_docs_reg if d["name"]==p_assigned_doc), None)
                        sb_insert("patients",{"name":p_name_clean,"phone":p_phone.strip(),"date_of_birth":p_dob.strip(),"gender":p_gender,"notes":p_notes.strip(),"created_at":today_str,"assigned_doctor_id":assigned_doc_id})
                        log_action(username,"New Patient",f"{p_name_clean} | {p_gender}")
                        new_pat = sb_one("patients", filters={"name": p_name_clean})
                        pid_new = new_pat["id"] if new_pat else 0
                        play_ding(); st.success(f"✅ Patient '{p_name_clean}' registered — ID: **{patient_id_fmt(pid_new)}**" + (f" · 📞 {p_phone}" if p_phone else ""))
                        if give_receipt:
                            st.session_state.intake_rcpt = {"patient":p_name_clean,"doctor":p_assigned_doc if p_assigned_doc!="Not assigned yet" else "To be assigned","item":"Initial Intake","base":0,"disc":0,"net":0,"method":"—","date":today_str,"invoice":"","patient_id_fmt":patient_id_fmt(pid_new)}
                else:
                    st.error("Name is required.")
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
                    all_docs_edit = sb_all("doctors", order="name")
                    doc_names_edit = ["Not assigned yet"] + [d["name"] for d in all_docs_edit]
                    cur_assigned_id = pat.get("assigned_doctor_id")
                    cur_assigned_name = next((d["name"] for d in all_docs_edit if d["id"]==cur_assigned_id), "Not assigned yet")
                    new_assigned_doc = st.selectbox("Assigned Doctor", doc_names_edit, index=doc_names_edit.index(cur_assigned_name) if cur_assigned_name in doc_names_edit else 0, key="ep_assigned_doc")
                    new_notes = st.text_area("Notes", value=pat.get("notes","") or "", height=100, key="ep_notes")
                if st.button("Save Changes", key="btn_edit_patient"):
                    new_assigned_id = next((d["id"] for d in all_docs_edit if d["name"]==new_assigned_doc), None)
                    sb_update("patients",{"name":auto_cap_name(new_name),"phone":new_phone.strip(),"date_of_birth":new_dob.strip(),"gender":new_gender,"notes":new_notes.strip(),"assigned_doctor_id":new_assigned_id},"id",pat["id"])
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

# ═══════════════════════════════════════════════
# APPOINTMENTS
# ═══════════════════════════════════════════════
elif selected == "📅  Appointments":
    page_header("Schedule", "Appointments", "Booking and management.")
    ta1,ta2,ta3 = st.tabs(["Book","View All","Print Today"])
    with ta1:
        patients_db = sb_all("patients", order="name"); docs_db = sb_all("doctors", order="name")
        if not patients_db or not docs_db: st.warning("Need at least one patient and one doctor.")
        else:
            p_map = {p["name"]: p["id"] for p in patients_db}; d_map = {d["name"]: d["id"] for d in docs_db}
            c1,c2 = st.columns(2)
            with c1: ap_patient = st.selectbox("Patient", list(p_map.keys())); ap_doctor = st.selectbox("Doctor", list(d_map.keys()))
            with c2: ap_date = st.date_input("Date", value=date.today()); ap_time = st.time_input("Time"); ap_reason = st.text_input("Reason")
            if st.button("Book Appointment"):
                sb_insert("appointments",{"patient_id":p_map[ap_patient],"doctor_id":d_map[ap_doctor],"appt_date":str(ap_date),"appt_time":str(ap_time),"reason":ap_reason,"status":"Scheduled"})
                log_action(username,"Book Appointment",f"{ap_patient} with {ap_doctor}")
                play_ding(); st.success("Booked.")
    with ta2:
        ap_search = st.text_input("Search", key="ap_search")
        all_appts = get_appointments_joined()
        if ap_search: all_appts = [a for a in all_appts if ap_search.lower() in (a.get("Patient","")+" "+a.get("Doctor","")).lower()]
        if all_appts:
            st.dataframe(pd.DataFrame(all_appts), use_container_width=True, hide_index=True)
            c1,c2 = st.columns(2)
            with c1: upd_id = st.number_input("Appointment ID", min_value=1, step=1)
            with c2: new_status = st.selectbox("Status", ["Scheduled","Completed","Cancelled","No-show"])
            if st.button("Update Status"):
                sb_update("appointments",{"status":new_status},"id",upd_id); play_ding(); st.success("Updated."); st.rerun()
    with ta3:
        today_appts_p = [a for a in get_appointments_joined() if a.get("Date")==today_str]
        if today_appts_p:
            cp = get_clinic_profile()
            print_html = f'<div style="background:#FBF8F1;padding:32px;font-family:Inter,sans-serif;color:#1F2924;max-width:800px;border-radius:4px;border:1px solid #D8CFB8;"><div style="text-align:center;border-bottom:2px solid #C47649;padding-bottom:16px;margin-bottom:22px;"><h1 style="margin:0;font-family:Fraunces,serif;font-style:italic;color:#1F2924;font-weight:500;">{cp.get("clinic_name","Garden Clinic")}</h1><p style="margin:6px 0 0 0;color:#C47649;font-size:0.72rem;letter-spacing:0.25em;text-transform:uppercase;font-weight:600;">Daily Appointments</p><p style="margin:10px 0 0 0;font-weight:600;color:#1F2924;">{date.today().strftime("%A, %B %d, %Y")}</p></div><table style="width:100%;border-collapse:collapse;font-size:0.95rem;"><thead><tr style="background:#1F2924;color:#FBF8F1;"><th style="padding:12px;text-align:left;">Time</th><th style="padding:12px;text-align:left;">Patient</th><th style="padding:12px;text-align:left;">Doctor</th><th style="padding:12px;text-align:left;">Reason</th><th style="padding:12px;text-align:left;">Status</th></tr></thead><tbody>'
            for a in today_appts_p:
                print_html += f'<tr style="border-bottom:1px solid #E5DCC4;"><td style="padding:12px;">{a["Time"]}</td><td style="padding:12px;font-weight:600;font-family:Fraunces,serif;font-style:italic;">{a["Patient"]}</td><td style="padding:12px;">{a["Doctor"]}</td><td style="padding:12px;">{a.get("Reason","—")}</td><td style="padding:12px;">{a["Status"]}</td></tr>'
            print_html += f'</tbody></table><p style="text-align:center;margin-top:22px;color:#8A7E60;font-size:0.8rem;font-style:italic;font-family:Fraunces,serif;">Total appointments: {len(today_appts_p)}</p></div>'
            st.markdown(print_html, unsafe_allow_html=True)
            st.info("💡 Press **Ctrl+P** to print or save as PDF.")
        else: st.info("No appointments today.")

# ═══════════════════════════════════════════════
# ACCOUNTING
# ═══════════════════════════════════════════════
elif selected == "📊  Accounting":
    page_header("Finance", "Accounting", "Revenue, expenses, and financial health.")
    section_label("Date Range")
    use_range = st.checkbox("Filter by date range", key="acc_use_range")
    if use_range:
        rc1,rc2 = st.columns(2)
        with rc1: start_d = st.date_input("From", value=date.today().replace(day=1), key="acc_start")
        with rc2: end_d = st.date_input("To", value=date.today(), key="acc_end")
        g_, e_, c_, o_, n_, _ = get_financials(start=str(start_d), end=str(end_d))
        st.info(f"**{start_d}** → **{end_d}**")
    else:
        g_, e_, c_, o_, n_ = gross_income, base_expenses, total_commissions, total_outflows, net_profit
    pulse_bar([("Gross Revenue",fmt(g_)),("Total Expenses",fmt(o_)),("Net Profit",fmt(n_)),("Doctor Commissions",fmt(c_))])
    cc1,cc2,cc3 = st.columns(3)
    with cc1: st.markdown(card("Gross Revenue", fmt(g_),"green"), unsafe_allow_html=True)
    with cc2: st.markdown(card("Total Outflows", fmt(o_),"red"), unsafe_allow_html=True)
    with cc3: st.markdown(card("Net Profit", fmt(n_),"dark"), unsafe_allow_html=True)
    ac1,ac2 = st.columns(2)
    with ac1:
        section_label("Expenses Breakdown")
        payroll_total = sum(float(e.get("amount") or 0) for e in sb_all("expenses") if e.get("category")=="Payroll")
        other_exp = e_ - payroll_total
        if o_ > 0:
            df_e = pd.DataFrame({"Category":["Other","Payroll","Commissions"],"Amount":[other_exp,payroll_total,c_]}).set_index("Category")
            st.bar_chart(df_e, y="Amount", color="#C47649", height=240)
    with ac2:
        section_label("Daily Revenue")
        all_v = sb_all("visits", order="visit_date")
        if all_v:
            df_v = pd.DataFrame([{"Date":v["visit_date"],"Revenue":float(v.get("net_paid") or 0)} for v in all_v])
            st.line_chart(df_v.groupby("Date").sum(), y="Revenue", color="#4A6752", height=240)
    ae1,ae2 = st.columns([3,2])
    with ae1:
        section_label("Expense Log")
        exp_search = st.text_input("Search", key="exp_search")
        filter_cat = st.selectbox("Category",["All","General","Payroll","Supplies","Utilities","Rent","Equipment","Marketing","Subscription","Other"], key="acc_filter_cat")
        all_exp = sb_all("expenses", order="id", desc_order=True)
        if filter_cat != "All": all_exp = [e for e in all_exp if e.get("category")==filter_cat]
        if exp_search: all_exp = [e for e in all_exp if exp_search.lower() in (e.get("description","")).lower()]
        if all_exp:
            df_exp = pd.DataFrame([{"id":e["id"],"Date":e["date"],"Category":e.get("category",""),"Description":e["description"],"Amount":fmt(e.get("amount") or 0),"Added By":e.get("added_by","")} for e in all_exp])
            st.dataframe(df_exp, use_container_width=True, hide_index=True)
    with ae2:
        section_label("Add Expense")
        with st.form("expense_form"):
            e_desc = st.text_input("Description"); e_cat = st.selectbox("Category",["General","Supplies","Utilities","Rent","Equipment","Marketing","Other"])
            e_amt = st.number_input("Amount (IQD)", min_value=0.0, step=1000.0); e_date = st.date_input("Date", value=date.today())
            if st.form_submit_button("Add Expense"):
                if e_desc and e_amt > 0:
                    sb_insert("expenses",{"description":e_desc,"category":e_cat,"amount":e_amt,"date":str(e_date),"added_by":username})
                    log_action(username,"Add Expense",f"{e_desc} | {fmt(e_amt)}")
                    play_ding(); st.success("Added."); st.rerun()
    section_label("Edit / Delete Expense")
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
    section_label("Referral Commissions This Month")
    current_month = datetime.now().strftime("%Y-%m")
    all_refs = sb_all("referrers", order="name")
    if all_refs:
        all_v_month = [v for v in sb_all("visits") if (v.get("visit_date") or "")[:7]==current_month]
        ref_rows = []; total_ref_comm = 0.0
        for ref in all_refs:
            v_via = [v for v in all_v_month if v.get("referred_by")==ref["name"]]
            rev = sum(float(v.get("net_paid") or 0) for v in v_via)
            comm = rev*(float(ref.get("commission_rate") or 0)/100.0); total_ref_comm += comm
            ref_rows.append({"Referrer":ref["name"],"Rate":f"{ref.get('commission_rate')}%","Visits":len(v_via),"Revenue":fmt(rev),"Due":fmt(comm)})
        st.dataframe(pd.DataFrame(ref_rows), use_container_width=True, hide_index=True)
        st.markdown(f"**Total: {fmt(total_ref_comm)}**")
        if st.button("Mark Paid"):
            if total_ref_comm > 0:
                tag = f"Referral Commissions — {current_month}"
                if not sb_exists("expenses","description",tag):
                    sb_insert("expenses",{"description":tag,"category":"Marketing","amount":total_ref_comm,"date":f"{current_month}-01","added_by":username})
                    play_ding(); st.success(f"Recorded."); st.rerun()
    section_label("Export to Excel")
    ex1,ex2,ex3,ex4 = st.columns(4)
    with ex1:
        all_v_exp = sb_all("visits", order="visit_date", desc_order=True)
        if all_v_exp:
            df_ev = pd.DataFrame([{"ID":v["id"],"Date":v["visit_date"],"Paid":v.get("net_paid",0),"Method":v.get("payment_method","")} for v in all_v_exp])
            st.download_button("Visits", data=to_excel(df_ev), file_name=f"visits_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, on_click=record_backup_download)
    with ex2:
        all_e_exp = sb_all("expenses", order="date", desc_order=True)
        if all_e_exp:
            df_ee = pd.DataFrame([{"ID":e["id"],"Date":e["date"],"Description":e["description"],"Category":e.get("category",""),"Amount":e.get("amount",0)} for e in all_e_exp])
            st.download_button("Expenses", data=to_excel(df_ee), file_name=f"expenses_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, on_click=record_backup_download)
    with ex3:
        all_p_exp = sb_all("patients", order="name")
        if all_p_exp:
            df_ep = pd.DataFrame([{"Name":p["name"],"Phone":p.get("phone",""),"Gender":p.get("gender",""),"DOB":p.get("date_of_birth","")} for p in all_p_exp])
            st.download_button("Patients", data=to_excel(df_ep), file_name=f"patients_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, on_click=record_backup_download)
    with ex4:
        all_v_m = sb_all("visits")
        if all_v_m:
            df_em = pd.DataFrame([{"Month":v["visit_date"][:7],"Revenue":float(v.get("net_paid") or 0)} for v in all_v_m])
            df_em = df_em.groupby("Month").agg(Revenue=("Revenue","sum"),Visits=("Revenue","count")).reset_index().sort_values("Month",ascending=False)
            st.download_button("Monthly", data=to_excel(df_em), file_name=f"monthly_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, on_click=record_backup_download)

# ═══════════════════════════════════════════════
# REPORTS
# ═══════════════════════════════════════════════
elif selected == "📑  Reports":
    page_header("Insights", "Reports", "Daily summary, top patients, services, and doctor monthly.")
    rep_tabs = st.tabs(["Daily Report","Top Patients","Top Services","Doctor Monthly","Machine Performance"])
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
            section_label("Visits That Day")
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
        rows_ts = sorted([{"Service":k,"Times Sold":v["count"],"Total Revenue":v["revenue"]} for k,v in svc_totals.items()], key=lambda x: x["Total Revenue"], reverse=True)
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

    with rep_tabs[4]:
        section_label("🖥️ Revenue by Machine")
        mp_month = st.text_input("Month (YYYY-MM)", value=datetime.now().strftime("%Y-%m"), key="mp_month")
        all_svc_mp = {s["id"]: s for s in sb_all("services")}
        all_v_mp = [v for v in sb_all("visits") if (v.get("visit_date") or "")[:7]==mp_month and v.get("service_id")]
        machine_rev = {}
        for v in all_v_mp:
            svc = all_svc_mp.get(v.get("service_id"))
            if svc and svc.get("delivery_type")=="Machine" and svc.get("machine_name"):
                mname = svc["machine_name"]
                if mname not in machine_rev: machine_rev[mname] = {"revenue":0.0,"visits":0,"services":set()}
                machine_rev[mname]["revenue"] += float(v.get("net_paid") or 0)
                machine_rev[mname]["visits"] += 1
                machine_rev[mname]["services"].add(svc["name"])
        if machine_rev:
            ranked = sorted(machine_rev.items(), key=lambda x: x[1]["revenue"], reverse=True)
            medals = ["🥇","🥈","🥉"]
            cols_mach = st.columns(min(len(ranked), 3))
            for idx, (mname, info) in enumerate(ranked[:3]):
                with cols_mach[idx]:
                    st.markdown(card(f"{medals[idx]} {mname}", fmt(info["revenue"]), "gold", f"{info['visits']} visits this month"), unsafe_allow_html=True)
            if len(ranked) > 3:
                st.markdown("---")
                section_label("All Machines")
            rows_mp = [{"Rank": medals[i] if i<3 else f"#{i+1}", "Machine": m, "Revenue": fmt(info["revenue"]), "Visits": info["visits"], "Services Used": ", ".join(info["services"])} for i,(m,info) in enumerate(ranked)]
            st.dataframe(pd.DataFrame(rows_mp), use_container_width=True, hide_index=True)
        else:
            st.info("No machine-based services recorded for this month yet. Mark services as 'Machine' in Settings → Services to track this.")

# ═══════════════════════════════════════════════
# RESEARCH
# ═══════════════════════════════════════════════
elif selected == "🔬  Research":
    page_header("Outcomes", "Research", "Track patient outcomes for research and marketing.")
    all_forms_r = sb_all("doctor_intake_form")
    rp = st.selectbox("Period", ["All time","This year","This month","Custom"], key="research_period")
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
    pending = len([f for f in filtered_forms if f.get("outcome") in ["Pending", None, ""]])
    success_rate = (relieved/total_treated*100) if total_treated>0 else 0
    improvement_rate = ((relieved+partial)/total_treated*100) if total_treated>0 else 0
    pulse_bar([("Total Patients",str(total_treated)),("Successfully Relieved",str(relieved)),("Success Rate",f"{success_rate:.1f}%"),("Improvement Rate",f"{improvement_rate:.1f}%")])
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(card("Relieved", str(relieved), "green", f"{success_rate:.1f}% success"), unsafe_allow_html=True)
    with c2: st.markdown(card("Improved", str(partial), "dark", "Partial recovery"), unsafe_allow_html=True)
    with c3: st.markdown(card("No Improvement", str(no_improv), "red", "Need different approach"), unsafe_allow_html=True)
    with c4: st.markdown(card("Pending", str(pending), "dark", "Still in treatment"), unsafe_allow_html=True)
    section_label("Marketing Narrative")
    narrative = ""
    if total_treated > 0:
        narrative = f"In this period, we successfully treated <strong>{total_treated} patients</strong>. Of those, <strong>{relieved} ({success_rate:.1f}%)</strong> experienced full pain relief, and <strong>{relieved+partial} ({improvement_rate:.1f}%)</strong> showed measurable improvement. This data reflects our commitment to evidence-based, results-driven physical therapy care."
    st.markdown(f'<div class="card" style="padding:28px 32px;"><div style="font-family:Fraunces,serif;font-size:1.2rem;font-style:italic;color:#EAF2EC;line-height:1.7;">{narrative if narrative else "No data yet for this period."}</div></div>', unsafe_allow_html=True)
    section_label("By Doctor")
    doctors_r = sb_all("doctors", order="name")
    rows_dr = []
    for d in doctors_r:
        d_forms = [f for f in filtered_forms if f.get("doctor_id")==d["id"]]
        d_treated = len(d_forms)
        d_relieved = len([f for f in d_forms if f.get("outcome")=="Successfully Relieved"])
        d_rate = (d_relieved/d_treated*100) if d_treated>0 else 0
        rows_dr.append({"Doctor":d["name"],"Patients":d_treated,"Relieved":d_relieved,"Success Rate":f"{d_rate:.1f}%"})
    if rows_dr: st.dataframe(pd.DataFrame(rows_dr), use_container_width=True, hide_index=True)
    section_label("By Body Area")
    body_stats = {}
    for f in filtered_forms:
        area = f.get("body_area","") or "Unknown"
        if area not in body_stats: body_stats[area] = {"total":0,"relieved":0,"pain_before":[],"pain_after":[]}
        body_stats[area]["total"] += 1
        if f.get("outcome")=="Successfully Relieved": body_stats[area]["relieved"] += 1
        if f.get("pain_before") is not None: body_stats[area]["pain_before"].append(f.get("pain_before",0))
        if f.get("pain_after") is not None: body_stats[area]["pain_after"].append(f.get("pain_after",0))
    rows_ba = []
    for k,v in body_stats.items():
        avg_before = sum(v["pain_before"])/len(v["pain_before"]) if v["pain_before"] else 0
        avg_after = sum(v["pain_after"])/len(v["pain_after"]) if v["pain_after"] else 0
        rows_ba.append({"Body Area":k,"Cases":v["total"],"Relieved":v["relieved"],"Success Rate":f"{(v['relieved']/v['total']*100) if v['total']>0 else 0:.1f}%","Avg Pain Before":f"{avg_before:.1f}/10","Avg Pain After":f"{avg_after:.1f}/10"})
    rows_ba = sorted(rows_ba, key=lambda x: x["Cases"], reverse=True)
    if rows_ba: st.dataframe(pd.DataFrame(rows_ba), use_container_width=True, hide_index=True)
    section_label("Export Research Data")
    if filtered_forms:
        patients_r_map = {p["id"]: p["name"] for p in sb_all("patients")}
        doctors_r_map = {d["id"]: d["name"] for d in doctors_r}
        df_research = pd.DataFrame([{"Date":f.get("filled_date",""),"Patient":patients_r_map.get(f.get("patient_id"),""),"Doctor":doctors_r_map.get(f.get("doctor_id"),""),"Body Area":f.get("body_area",""),"Problem":f.get("problem",""),"Pain Before":f.get("pain_before",0),"Pain After":f.get("pain_after",0),"Sessions":f.get("sessions_needed",0),"Outcome":f.get("outcome","Pending")} for f in filtered_forms])
        st.download_button("Export to Excel", data=to_excel(df_research), file_name=f"research_{today_str}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, on_click=record_backup_download)

# ═══════════════════════════════════════════════
# ACCOUNTS
# ═══════════════════════════════════════════════
elif selected == "👥  Accounts":
    page_header("Users", "Accounts", "Manage user access and review activity logs.")
    accounts = sb_all("users"); st.metric("Total accounts", len(accounts))
    at1,at2 = st.tabs(["Profiles","Activity Log"])
    with at1:
        section_label("All Accounts")
        doctors_acc_map = {d["id"]: d["name"] for d in sb_all("doctors")}
        if accounts:
            rows_acc = [{"id":u["id"],"username":u["username"],"role":u["role"],"Linked Doctor":doctors_acc_map.get(u.get("linked_doctor_id"),"—") if u.get("role")=="Doctor" else "—"} for u in accounts]
            st.dataframe(pd.DataFrame(rows_acc), use_container_width=True, hide_index=True)
            killable = ["— select —"]+[u["username"] for u in accounts if u["username"]!=username]
            target_del = st.selectbox("Remove", killable, key="burn_user_select")
            if target_del != "— select —":
                confirm_del_user = st.checkbox(f"⚠️ Yes, I'm sure I want to permanently delete the account '{target_del}'", key="confirm_del_user")
                if st.button("Delete Account", type="primary", key="btn_del_account"):
                    if not confirm_del_user:
                        st.error("Please check the confirmation box above first.")
                    else:
                        sb_delete("users","username",target_del); play_ding(); st.success("Removed."); st.rerun()
    with at2:
        al_search = st.text_input("Search", key="al_search")
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
    page_header("Configure", "Settings", "Doctors, commissions, staff, services, and more.")
    s1,s2,s3,s4,s5,s6,s7,s8 = st.tabs(["Doctors","Commission","Staff","Services","Bundles","Referrers","Subscriptions","Clinic Profile"])
    with s1:
        section_label("Add Doctor")
        c1,c2 = st.columns(2)
        with c1: d_name = st.text_input("Doctor name"); d_spec = st.text_input("Specialty")
        with c2: d_days = st.multiselect("Work days (for no-show tracking)", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], key="d_days_new")
        if st.button("Add Doctor"):
            if d_name.strip():
                if sb_exists("doctors","name",d_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("doctors",{"name":d_name.strip(),"specialty":d_spec.strip(),"comm_type":"tiered","fixed_rate":0,"schedule_days":",".join(d_days)})
                    play_ding(); st.success("Added."); st.rerun()
        section_label("Current Doctors")
        all_docs = sb_all("doctors", order="name")
        if all_docs:
            st.dataframe(pd.DataFrame([{"id":d["id"],"name":d["name"],"specialty":d.get("specialty",""),"work_days":d.get("schedule_days","") or "Not set"} for d in all_docs]), use_container_width=True, hide_index=True)
            section_label("Update Doctor's Work Days")
            sel_doc_days = st.selectbox("Select doctor", ["— select —"]+[d["name"] for d in all_docs], key="sel_doc_days_upd")
            if sel_doc_days != "— select —":
                doc_obj_days = next(d for d in all_docs if d["name"]==sel_doc_days)
                cur_days = [s.strip() for s in (doc_obj_days.get("schedule_days") or "").split(",") if s.strip()]
                new_days = st.multiselect("Work days", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], default=cur_days, key="upd_doc_days")
                if st.button("Save Work Days"):
                    sb_update("doctors", {"schedule_days": ",".join(new_days)}, "id", doc_obj_days["id"])
                    play_ding(); st.success("Updated."); st.rerun()
            del_doc = st.selectbox("Remove", ["— select —"]+[d["name"] for d in all_docs])
            if del_doc != "— select —":
                confirm_del_doc = st.checkbox(f"⚠️ Yes, I'm sure I want to permanently delete '{del_doc}'", key="confirm_del_doc")
                if st.button("Remove Doctor", type="primary"):
                    if not confirm_del_doc:
                        st.error("Please check the confirmation box above first.")
                    else:
                        doc_id = next(d["id"] for d in all_docs if d["name"]==del_doc)
                        sb_delete("doctors","name",del_doc); sb_delete("doctor_commission_tiers","doctor_id",doc_id)
                        play_ding(); st.success("Removed."); st.rerun()
    with s2:
        section_label("Commission Tiers Per Doctor")
        st.info("Highest qualifying tier applies. E.g. 3% at 5+ visits, 7% at 15+.")
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
                c1,c2 = st.columns(2)
                with c1: new_min = st.number_input("Min visits", min_value=1, step=1, value=10, key="tier_min")
                with c2: new_rate = st.number_input("Rate (%)", min_value=0.0, max_value=100.0, step=0.5, value=3.0, key="tier_rate")
                if st.button("Add Tier", key="btn_add_tier"):
                    sb_insert("doctor_commission_tiers",{"doctor_id":doc_id_t,"min_visits":int(new_min),"commission_rate":new_rate})
                    play_ding(); st.success("Added."); st.rerun()
    with s3:
        section_label("Add Staff")
        c1,c2,c3 = st.columns(3)
        with c1: emp_name = st.text_input("Name")
        with c2: emp_role = st.text_input("Role")
        with c3: emp_salary = st.number_input("Salary (IQD)", min_value=0.0, step=50000.0)
        if st.button("Add Staff"):
            if emp_name.strip() and emp_role.strip():
                if sb_exists("employees","name",emp_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("employees",{"name":emp_name.strip(),"role":emp_role.strip(),"salary":emp_salary})
                    play_ding(); st.success("Added."); st.rerun()
        section_label("Current Staff")
        all_emp = sb_all("employees", order="name")
        if all_emp:
            df_emp = pd.DataFrame([{"id":e["id"],"name":e["name"],"role":e.get("role",""),"salary":fmt(e.get("salary"))} for e in all_emp])
            st.dataframe(df_emp, use_container_width=True, hide_index=True)
            st.markdown(f"**Monthly payroll: {fmt(sum(float(e.get('salary') or 0) for e in all_emp))}**")
            del_emp = st.selectbox("Remove", ["— select —"]+[e["name"] for e in all_emp])
            if del_emp != "— select —":
                confirm_del_emp = st.checkbox(f"⚠️ Yes, I'm sure I want to permanently delete '{del_emp}'", key="confirm_del_emp")
                if st.button("Remove Employee", type="primary"):
                    if not confirm_del_emp:
                        st.error("Please check the confirmation box above first.")
                    else:
                        sb_delete("employees","name",del_emp); play_ding(); st.success("Removed."); st.rerun()
    with s4:
        section_label("Add Service")
        c1,c2,c3 = st.columns(3)
        with c1: s_name = st.text_input("Service name")
        with c2: s_cat = st.selectbox("Category",["General","Consultation","Procedure","Therapy","Diagnostic","Other"])
        with c3: s_price = st.number_input("Price (IQD)", min_value=0.0, step=5000.0)
        s_delivery = st.radio("How is this service performed?", ["Manual (by hand)","Machine"], horizontal=True, key="s_delivery")
        s_machine_name = ""
        if s_delivery == "Machine":
            s_machine_name = st.text_input("Machine name", placeholder="e.g. Laser Decompression Unit, Shockwave Device", key="s_machine_name")
        if st.button("Add Service"):
            if s_name.strip():
                if sb_exists("services","name",s_name.strip()): st.error("Already exists.")
                elif s_delivery == "Machine" and not s_machine_name.strip(): st.error("Please enter the machine name.")
                else:
                    sb_insert("services",{"name":s_name.strip(),"category":s_cat,"price":s_price,"active":1,"delivery_type":s_delivery,"machine_name":s_machine_name.strip() if s_delivery=="Machine" else ""})
                    play_ding(); st.success("Added."); st.rerun()
        section_label("Current Services")
        all_svc = sb_all("services", order="name")
        if all_svc:
            df_svc = pd.DataFrame([{"id":s["id"],"name":s["name"],"category":s.get("category",""),"price":fmt(s.get("price")),"type":s.get("delivery_type","Manual (by hand)"),"machine":s.get("machine_name","") or "—"} for s in all_svc])
            st.dataframe(df_svc, use_container_width=True, hide_index=True)
            del_svc = st.selectbox("Remove", ["— select —"]+[s["name"] for s in all_svc])
            if del_svc != "— select —":
                confirm_del_svc = st.checkbox(f"⚠️ Yes, I'm sure I want to permanently delete '{del_svc}'", key="confirm_del_svc")
                if st.button("Remove Service", type="primary"):
                    if not confirm_del_svc:
                        st.error("Please check the confirmation box above first.")
                    else:
                        sb_delete("services","name",del_svc); play_ding(); st.success("Removed."); st.rerun()
    with s5:
        section_label("Create Bundle")
        c1,c2 = st.columns(2)
        with c1: b_name = st.text_input("Bundle name"); b_price = st.number_input("Price (IQD)", min_value=0.0, step=10000.0)
        with c2: b_desc = st.text_area("Description", height=90)
        if st.button("Create Bundle"):
            if b_name.strip() and b_price > 0:
                if sb_exists("bundles","name",b_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("bundles",{"name":b_name.strip(),"price":b_price,"description":b_desc.strip()})
                    play_ding(); st.success("Created."); st.rerun()
        section_label("Current Bundles")
        all_bundles = sb_all("bundles", order="name")
        if all_bundles:
            df_b = pd.DataFrame([{"id":b["id"],"name":b["name"],"price":fmt(b.get("price")),"description":b.get("description","")} for b in all_bundles])
            st.dataframe(df_b, use_container_width=True, hide_index=True)
            del_bnd = st.selectbox("Remove", ["— select —"]+[b["name"] for b in all_bundles])
            if st.button("Remove Bundle", type="primary"):
                if del_bnd != "— select —":
                    sb_delete("bundles","name",del_bnd); play_ding(); st.success("Removed."); st.rerun()
    with s6:
        section_label("Add Referrer")
        c1,c2 = st.columns(2)
        with c1: ref_name = st.text_input("Name", key="ref_name_input"); ref_phone = st.text_input("Phone", key="ref_phone_input")
        with c2: ref_rate = st.number_input("Commission (%)", min_value=0.0, max_value=100.0, step=1.0, value=10.0, key="ref_rate_input"); ref_notes = st.text_area("Notes", height=80, key="ref_notes_input")
        if st.button("Add Referrer", key="btn_add_referrer"):
            if ref_name.strip():
                if sb_exists("referrers","name",ref_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("referrers",{"name":ref_name.strip(),"phone":ref_phone.strip(),"commission_rate":ref_rate,"notes":ref_notes.strip(),"added_by":username,"created_at":today_str})
                    play_ding(); st.success("Added."); st.rerun()
        section_label("Current Referrers")
        all_refs = sb_all("referrers", order="name")
        if all_refs:
            st.dataframe(pd.DataFrame(all_refs), use_container_width=True, hide_index=True)
            del_ref = st.selectbox("Remove", ["— select —"]+[r["name"] for r in all_refs], key="del_ref_select")
            if st.button("Remove Referrer", type="primary", key="btn_del_referrer"):
                if del_ref != "— select —":
                    sb_delete("referrers","name",del_ref); play_ding(); st.success("Removed."); st.rerun()
    with s7:
        section_label("Add Monthly Subscription (Clinic Expense)")
        c1,c2,c3 = st.columns(3)
        with c1: sub_name = st.text_input("Name", key="sub_name_input"); sub_cat = st.selectbox("Category",["Subscription","Marketing","Software","Utilities","Other"], key="sub_cat_select")
        with c2: sub_amount = st.number_input("Amount (IQD)", min_value=0.0, step=5000.0, key="sub_amount_input"); sub_day = st.number_input("Billing day", min_value=1, max_value=28, step=1, value=1, key="sub_day_input")
        with c3: st.markdown("<br>", unsafe_allow_html=True); st.markdown("Auto-posts monthly.")
        if st.button("Add Subscription", key="btn_add_subscription"):
            if sub_name.strip() and sub_amount > 0:
                if sb_exists("subscriptions","name",sub_name.strip()): st.error("Already exists.")
                else:
                    sb_insert("subscriptions",{"name":sub_name.strip(),"amount":sub_amount,"billing_day":int(sub_day),"category":sub_cat,"active":1,"added_by":username,"created_at":today_str})
                    play_ding(); st.success("Added."); st.rerun()
        section_label("Active Subscriptions")
        all_subs = sb_all("subscriptions", order="name")
        if all_subs:
            df_s = pd.DataFrame([{"id":s["id"],"name":s["name"],"amount":fmt(s.get("amount")),"billing_day":s.get("billing_day",1),"category":s.get("category",""),"active":s.get("active",1)} for s in all_subs])
            st.dataframe(df_s, use_container_width=True, hide_index=True)
            st.markdown(f"**Total: {fmt(sum(float(s.get('amount') or 0) for s in all_subs if s.get('active')==1))}/month**")
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
        section_label("Clinic Profile (Shown on Receipts)")
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

        st.markdown("---")
        section_label("💬 WhatsApp Follow-up Message")
        st.caption("This message is sent to patients 20+ days after they complete their sessions. Use {name} for patient name, {clinic} for clinic name, {days} for days passed.")
        current_template = get_followup_template()
        new_template = st.text_area("Message template", value=current_template, height=140, key="followup_template_input")
        if st.button("Save Message Template", key="btn_save_template"):
            existing_t = sb_all("clinic_settings", filters={"key": "followup_template"})
            if existing_t: sb_update("clinic_settings", {"value": new_template}, "id", existing_t[0]["id"])
            else: sb_insert("clinic_settings", {"key": "followup_template", "value": new_template})
            play_ding(); st.success("Message template saved!"); st.rerun()
        st.markdown("**Preview:**")
        preview = new_template.replace("{name}", "Ahmed").replace("{clinic}", cp.get("clinic_name","Garden Clinic")).replace("{days}", "20")
        st.markdown(f'<div class="card"><div style="font-size:0.9rem;color:#EAF2EC;line-height:1.7;">{preview}</div></div>', unsafe_allow_html=True)

        st.markdown("---")
        section_label("📅 Appointment Reminder Message")
        st.caption("This message is used for tomorrow's appointment reminders. Use {name}, {clinic}, {date}, {time}, {doctor}.")
        current_rem_template = get_reminder_template()
        new_rem_template = st.text_area("Reminder message", value=current_rem_template, height=120, key="reminder_template_input")
        if st.button("Save Reminder Template", key="btn_save_reminder_template"):
            existing_rt = sb_all("clinic_settings", filters={"key": "reminder_template"})
            if existing_rt: sb_update("clinic_settings", {"value": new_rem_template}, "id", existing_rt[0]["id"])
            else: sb_insert("clinic_settings", {"key": "reminder_template", "value": new_rem_template})
            play_ding(); st.success("Reminder template saved!"); st.rerun()
        st.markdown("**Preview:**")
        preview_rem = new_rem_template.replace("{name}", "Ahmed").replace("{clinic}", cp.get("clinic_name","Garden Clinic")).replace("{date}", "2026-06-19").replace("{time}", "10:30 AM").replace("{doctor}", "Haryad")
        st.markdown(f'<div class="card"><div style="font-size:0.9rem;color:#EAF2EC;line-height:1.7;">{preview_rem}</div></div>', unsafe_allow_html=True)
        
