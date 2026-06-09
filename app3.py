st.markdown("""
<style>

/* ==========================================
   PREMIUM CLINIC UI 2026
========================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main Background */
.stApp {
    background:
        radial-gradient(circle at top right, rgba(46,204,113,0.12), transparent 30%),
        radial-gradient(circle at bottom left, rgba(52,211,153,0.10), transparent 30%),
        #F7FAF8;
    color: #111827;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #071A12 0%,
        #0B291B 50%,
        #123524 100%
    ) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Headers */
h1 {
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #081C15 !important;
}

h2, h3, h4, h5, h6 {
    color: #0B291B !important;
    font-weight: 700 !important;
}

/* Glass Cards */
.feature-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border-radius: 22px;
    padding: 24px;

    border: 1px solid rgba(255,255,255,0.7);

    box-shadow:
        0 10px 30px rgba(0,0,0,0.08),
        inset 0 1px 0 rgba(255,255,255,0.8);

    transition: all .3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow:
        0 20px 40px rgba(0,0,0,0.12),
        inset 0 1px 0 rgba(255,255,255,0.9);
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 52px;

    background: linear-gradient(
        135deg,
        #2ECC71 0%,
        #27AE60 100%
    ) !important;

    border: none !important;

    color: white !important;

    border-radius: 14px !important;

    font-weight: 700 !important;

    box-shadow:
        0 8px 20px rgba(46,204,113,0.35);

    transition: all .25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow:
        0 12px 28px rgba(46,204,113,0.45);
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stSelectbox div[data-baseweb="select"] {

    background: white !important;

    border-radius: 12px !important;

    border: 1px solid #DCE5DD !important;

    transition: .2s ease !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border: 1px solid #2ECC71 !important;
    box-shadow: 0 0 0 4px rgba(46,204,113,0.15) !important;
}

/* DataFrames */
[data-testid="stDataFrame"] {
    border-radius: 18px !important;
    overflow: hidden !important;

    border: 1px solid #E5E7EB;

    box-shadow:
        0 10px 25px rgba(0,0,0,0.06);
}

/* Metrics */
[data-testid="metric-container"] {

    background: rgba(255,255,255,0.9);

    border-radius: 20px;

    padding: 18px;

    border: 1px solid #E5E7EB;

    box-shadow:
        0 8px 20px rgba(0,0,0,0.05);

    transition: .25s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-4px);
}

[data-testid="stMetricValue"] {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    color: #0B291B !important;
}

[data-testid="stMetricLabel"] {
    font-weight: 600 !important;
    color: #6B7280 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {

    background: white;

    border-radius: 12px;

    padding: 12px 20px;

    border: 1px solid #E5E7EB;
}

.stTabs [aria-selected="true"] {
    background: #2ECC71 !important;
    color: white !important;
}

/* Success Messages */
.stSuccess {
    border-radius: 14px;
    border-left: 5px solid #10B981;
}

/* Error Messages */
.stError {
    border-radius: 14px;
    border-left: 5px solid #EF4444;
}

/* Warning Messages */
.stWarning {
    border-radius: 14px;
    border-left: 5px solid #F59E0B;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: #F3F4F6;
}

::-webkit-scrollbar-thumb {
    background: #2ECC71;
    border-radius: 10px;
}

/* Smooth Animation */
@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.block-container {
    animation: fadeUp .4s ease;
}

/* Login Card */
.login-card {
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(15px);

    border-radius: 24px;

    padding: 35px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.08);

    border: 1px solid rgba(255,255,255,0.8);
}

/* Receipt */
#print-area {
    background: white;
    border-radius: 18px !important;
    border: 2px solid #2ECC71 !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

/* Radio Buttons */
.stRadio > div {
    background: white;
    padding: 10px;
    border-radius: 12px;
}

/* Forms */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.7);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #E5E7EB;
}

/* Hide Streamlit Footer */
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)
