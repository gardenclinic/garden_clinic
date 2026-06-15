"""Constants and configuration for Garden Clinic."""

# ═══════════════════════════════════════════════
# TABLE NAMES
# ═══════════════════════════════════════════════
TABLES = {
    "users": "users",
    "patients": "patients",
    "doctors": "doctors",
    "visits": "visits",
    "appointments": "appointments",
    "services": "services",
    "bundles": "bundles",
    "expenses": "expenses",
    "employees": "employees",
    "patient_sessions": "patient_sessions",
    "doctor_intake_form": "doctor_intake_form",
    "patient_subscriptions": "patient_subscriptions",
    "gym_checkins": "gym_checkins",
    "audit_log": "audit_log",
    "clinic_profile": "clinic_profile",
    "doctor_commission_tiers": "doctor_commission_tiers",
    "referrers": "referrers",
    "subscriptions": "subscriptions",
}

# ═══════════════════════════════════════════════
# USER ROLES & PERMISSIONS
# ═══════════════════════════════════════════════
ROLES = {
    "Boss": ["📈  Dashboard", "🖥️  Reception", "📊  Accounting", "📅  Appointments", "📑  Reports", "🔬  Research", "👥  Accounts", "⚙️  Settings"],
    "Reception & Accounting": ["🖥️  Reception", "📊  Accounting", "📅  Appointments", "📑  Reports"],
    "Accounting": ["📊  Accounting", "📑  Reports"],
    "Reception": ["🖥️  Reception", "📅  Appointments"],
    "Doctor": ["🩺  Clinical Workspace"],
}

VALID_ROLES = list(ROLES.keys())
ADMIN_CODE = "1011"

# ═══════════════════════════════════════════════
# DEFAULT VALUES
# ═══════════════════════════════════════════════
CLINIC_DEFAULTS = {
    "clinic_name": "Garden Clinic",
    "tagline": "Physical Therapy Center",
    "address": "",
    "phone": "",
    "email": "",
}

CURRENCY = "IQD"
CURRENCY_SYMBOL = "IQD"

# ═══════════════════════════════════════════════
# BODY AREAS
# ═══════════════════════════════════════════════
BODY_AREAS = [
    "— select —",
    "Neck / Cervical",
    "Upper back",
    "Lower back / Lumbar",
    "Shoulder",
    "Elbow",
    "Wrist / Hand",
    "Hip",
    "Knee",
    "Ankle / Foot",
    "Multiple areas",
    "Other",
]

# ═══════════════════════════════════════════════
# ASSESSMENT OUTCOMES
# ═══════════════════════════════════════════════
OUTCOME_OPTIONS = [
    "Pending",
    "Full Recovery Expected",
    "Partial Recovery Expected",
    "Long-term Management",
    "Successfully Relieved",
    "Partially Improved",
    "No Improvement",
    "Patient Discontinued",
    "Other",
]

OUTCOME_FINAL = [
    "Pending",
    "Successfully Relieved",
    "Partially Improved",
    "No Improvement",
    "Patient Discontinued",
    "Other",
]

# ═══════════════════════════════════════════════
# PAYMENT METHODS
# ═══════════════════════════════════════════════
PAYMENT_METHODS = ["Cash", "Card", "Insurance", "Transfer", "Subscription"]

# ═══════════════════════════════════════════════
# EXPENSE CATEGORIES
# ═══════════════════════════════════════════════
EXPENSE_CATEGORIES = [
    "General",
    "Payroll",
    "Supplies",
    "Utilities",
    "Rent",
    "Equipment",
    "Marketing",
    "Subscription",
    "Other",
]

EXPENSE_CATEGORIES_SHORT = [
    "General",
    "Supplies",
    "Utilities",
    "Rent",
    "Equipment",
    "Marketing",
    "Other",
]

# ═══════════════════════════════════════════════
# SERVICE CATEGORIES
# ═══════════════════════════════════════════════
SERVICE_CATEGORIES = [
    "General",
    "Consultation",
    "Procedure",
    "Therapy",
    "Diagnostic",
    "Other",
]

# ═══════════════════════════════════════════════
# SUBSCRIPTION TYPES
# ═══════════════════════════════════════════════
SUBSCRIPTION_TYPES = ["Monthly", "Weekly", "Custom (days)"]

SUBSCRIPTION_PLAN_TYPES = ["Monthly", "Weekly", "Custom (days)"]

# ═══════════════════════════════════════════════
# APPOINTMENT STATUSES
# ═══════════════════════════════════════════════
APPOINTMENT_STATUSES = ["Scheduled", "Completed", "Cancelled", "No-show"]

# ═══════════════════════════════════════════════
# REFERRAL OPTIONS
# ═══════════════════════════════════════════════
REFERRAL_OPTIONS_DEFAULT = [
    "Walk-in / Direct",
    "Instagram / Social Media",
    "Google Search",
    "Friend / Word of mouth",
]

# ═══════════════════════════════════════════════
# TREATMENT FREQUENCY
# ═══════════════════════════════════════════════
TREATMENT_FREQUENCIES = [
    "— select —",
    "Daily",
    "3x per week",
    "2x per week",
    "Weekly",
    "Every 2 weeks",
    "As needed",
]

# ═══════════════════════════════════════════════
# ONSET TYPES
# ═══════════════════════════════════════════════
ONSET_TYPES = [
    "— select —",
    "Sudden / Trauma",
    "Gradual",
    "Post-surgery",
    "Repetitive strain",
    "Unknown",
]

# ═══════════════════════════════════════════════
# PAIN SCALE RANGE
# ═══════════════════════════════════════════════
PAIN_MIN = 0
PAIN_MAX = 10
PAIN_DEFAULT = 5

# ═══════════════════════════════════════════════
# SESSION DEFAULTS
# ═══════════════════════════════════════════════
DEFAULT_SESSIONS = 10
MIN_SESSIONS = 1
MAX_SESSIONS = 200

# ═══════════════════════════════════════════════
# GENDER OPTIONS
# ═══════════════════════════════════════════════
GENDER_OPTIONS = ["Prefer not to say", "Male", "Female", "Other"]

# ═══════════════════════════════════════════════
# OVERDUE THRESHOLD (days)
# ═══════════════════════════════════════════════
OVERDUE_DAYS = 14

# ═══════════════════════════════════════════════
# APPOINTMENT SLOT COLORS
# ═══════════════════════════════════════════════
APPOINTMENT_COLORS = {
    "Scheduled": "#C47649",
    "Completed": "#4A6752",
    "Cancelled": "#B85C3A",
    "No-show": "#8A7E60",
}

# ═══════════════════════════════════════════════
# ICONS
# ═══════════════════════════════════════════════
PAYMENT_ICONS = {
    "Cash": "💵",
    "Card": "💳",
    "Insurance": "🏥",
    "Transfer": "🔁",
    "Subscription": "📋",
}

GENDER_ICONS = {
    "Male": "♂",
    "Female": "♀",
}

# ═══════════════════════════════════════════════
# VALIDATION PATTERNS
# ═══════════════════════════════════════════════
MIN_PASSWORD_LENGTH = 6
