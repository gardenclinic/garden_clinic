"""Authentication and utility functions for Garden Clinic."""
import streamlit as st
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from db import sb_all, sb_one, sb_insert, sb_sum
from constants import ROLES, VALID_ROLES, ADMIN_CODE


def hash_password(pw: str) -> str:
    """Hash a password using SHA256."""
    return hashlib.sha256(pw.encode()).hexdigest()


def log_action(username: str, action: str, details: str = "") -> None:
    """Log an action to the audit log."""
    sb_insert(
        "audit_log",
        {
            "username": username,
            "action": action,
            "details": details,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
    )


def get_user_context() -> Dict[str, Any]:
    """Get current user context from session state."""
    return {
        "role": st.session_state.get("role", ""),
        "username": st.session_state.get("username", ""),
        "linked_doctor_id": st.session_state.get("linked_doctor_id"),
        "logged_in": st.session_state.get("logged_in", False),
    }


def verify_login(username: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
    """Verify user credentials and return user data if valid."""
    try:
        users = sb_all("users", filters={"username": username.strip()})
        match = [x for x in users if x.get("password_hash") == hash_password(password)]
        if match:
            return True, match[0]
        return False, None
    except Exception as e:
        st.error(f"Login error: {str(e)}")
        return False, None


def create_user(
    username: str,
    password: str,
    role: str,
    linked_doctor_id: Optional[int] = None,
) -> Tuple[bool, str]:
    """Create a new user account."""
    try:
        if not username.strip():
            return False, "Username is required."
        if not password.strip():
            return False, "Password is required."
        if role not in VALID_ROLES:
            return False, f"Invalid role. Must be one of: {', '.join(VALID_ROLES)}"
        if role == "Doctor" and not linked_doctor_id:
            return False, "Doctor role requires linked doctor account."

        # Check if username already exists
        existing = sb_all("users", filters={"username": username.strip()})
        if existing:
            return False, "Username already taken."

        # Insert new user
        sb_insert(
            "users",
            {
                "username": username.strip(),
                "password_hash": hash_password(password),
                "role": role,
                "linked_doctor_id": linked_doctor_id,
            },
        )
        log_action("System", "Create Account", f"User: {username.strip()} | Role: {role}")
        return True, "Account created successfully."

    except Exception as e:
        return False, f"Error creating account: {str(e)}"


def get_user_menu(role: str) -> list:
    """Get menu items for a user role."""
    return ROLES.get(role, [])


def require_auth():
    """Check if user is authenticated, redirect to login if not."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.error("Please log in to continue.")
        st.stop()


def require_role(*allowed_roles: str):
    """Check if current user has one of the allowed roles."""
    user_role = st.session_state.get("role", "")
    if user_role not in allowed_roles:
        st.error(f"Access denied. Required role: {', '.join(allowed_roles)}")
        st.stop()


def logout():
    """Log out the current user."""
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.linked_doctor_id = None
    st.rerun()


def get_linked_doctor() -> Optional[Dict[str, Any]]:
    """Get the doctor linked to the current user (for Doctor role)."""
    doctor_id = st.session_state.get("linked_doctor_id")
    if doctor_id:
        return sb_one("doctors", filters={"id": doctor_id})
    return None


def require_linked_doctor() -> Dict[str, Any]:
    """Require that current user has a linked doctor (for Doctor role)."""
    doctor = get_linked_doctor()
    if not doctor:
        st.error("No doctor linked to this account. Contact admin.")
        st.stop()
    return doctor
