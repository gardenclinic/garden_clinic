import streamlit as st
import pandas as pd
from datetime import datetime

# Set page layout
st.set_page_config(page_title="Clinic Management System", layout="wide")

# ----------------------------------------------------
# 1. DATABASE EMULATION (Using Streamlit Session State)
# ----------------------------------------------------
if 'patients' not in st.session_state:
    st.session_state.patients = [
        {"id": 1, "name": "Alice Smith", "phone": "555-0192"},
        {"id": 2, "name": "Bob Jones", "phone": "555-0143"}
    ]

if 'services' not in st.session_state:
    st.session_state.services = {
        "Initial Assessment": 60,
        "Physical Therapy Session": 50,
        "Massage Therapy": 40,
        "Electrotherapy": 45
    }

if 'doctors' not in st.session_state:
    st.session_state.doctors = ["Dr. Adams", "Dr. Baker", "Dr. Clark"]

if 'visits' not in st.session_state:
    # Seed data so you can see the commission logic working instantly
    st.session_state.visits = []
    # Adding 12 visits to Dr. Adams to trigger 3% tier
    for _ in range(12):
        st.session_state.visits.append({"patient": "Alice Smith", "doctor": "Dr. Adams", "service": "Physical Therapy Session", "price": 50, "date": "2026-05-10"})
    # Adding 22 visits to Dr. Baker to trigger 5% tier
    for _ in range(22):
        st.session_state.visits.append({"patient": "Bob Jones", "doctor": "Dr. Baker", "service": "Initial Assessment", "price": 60, "date": "2026-05-12"})

# ----------------------------------------------------
# 2. NAVIGATION SIDEBAR
# ----------------------------------------------------
st.sidebar.title("🏥 Clinic System")
role = st.sidebar.radio("Select Dashboard:", ["👩‍💻 Reception desk", "💼 Boss Dashboard"])

# ----------------------------------------------------
# 3. RECEPTION DASHBOARD
# ----------------------------------------------------
if role == "👩‍💻 Reception desk":
    st.title("Receptionist Panel")
    
    tab1, tab2 = st.tabs(["📋 Register New Patient", "🚀 Check-In / New Visit"])
    
    with tab1:
        st.subheader("Register a New Patient")
        new_name = st.text_input("Full Name")
        new_phone = st.text_input("Phone Number")
        if st.button("Register Patient"):
            if new_name and new_phone:
                new_id = len(st.session_state.patients) + 1
                st.session_state.patients.append({"id": new_id, "name": new_name, "phone": new_phone})
                st.success(f"Success: Registered {new_name}!")
            else:
                st.error("Please fill in all fields.")

    with tab2:
        st.subheader("Record Patient Visit")
        
        # Patient list for selection
        patient_names = [p["name"] for p in st.session_state.patients]
        selected_patient = st.selectbox("Select Patient Name", [""] + patient_names)
        
        # SMART HISTORY LOOKUP
        if selected_patient != "":
            # Find past visits for this patient (reverse list to get newest first)
            past_visits = [v for v in st.session_state.visits if v["patient"] == selected_patient]
            
            if past_visits:
                last_visit = past_visits[-1] # Get the latest one
                st.info(f"📜 **Patient History Found!** \n* **Last Visit Date:** {last_visit['date']} \n* **Last Service Provided:** {last_visit['service']}")
            else:
                st.warning("🆕 This is the patient's first active visit record.")
        
        # Inputs for the new visit
        chosen_doc = st.selectbox("Assign Doctor", st.session_state.doctors)
        chosen_service = st.selectbox("Select Service Requested", list(st.session_state.services.keys()))
        visit_date = st.date_input("Visit Date", datetime.now())
        
        price = st.session_state.services[chosen_service]
        st.metric(label="Price to Collect", value=f"${price}")
        
        if st.button("Submit & Print Receipt"):
            if selected_patient == "":
                st.error("Please select a valid patient.")
            else:
                # Save visit
                st.session_state.visits.append({
                    "patient": selected_patient,
                    "doctor": chosen_doc,
                    "service": chosen_service,
                    "price": price,
                    "date": str(visit_date)
                })
                st.success(f"Visit logged successfully for {selected_patient} under {chosen_doc}!")

# ----------------------------------------------------
# 4. BOSS DASHBOARD
# ----------------------------------------------------
elif role == "💼 Boss Dashboard":
    st.title("Executive Financial Dashboard")
    
    if not st.session_state.visits:
        st.info("No clinic data recorded yet.")
    else:
        df_visits = pd.DataFrame(st.session_state.visits)
        
        # Global Metrics
        total_rev = df_visits["price"].sum()
        total_patients_seen = len(df_visits)
        
        col1, col2 = st.columns(2)
        col1.metric("💰 Total Revenue Earned", f"${total_rev:,}")
        col2.metric("👥 Total Consultations", f"{total_patients_seen}")
        
        st.markdown("---")
        st.subheader("🩺 Doctor Performance & Commission Breakdown")
        
        # Calculate Commissions
        doc_data = []
        for doc in st.session_state.doctors:
            doc_visits = df_visits[df_visits["doctor"] == doc]
            count = len(doc_visits)
            revenue = doc_visits["price"].sum()
            
            # Commission Tiers Logic
            if count >= 20:
                tier_pct = "5%"
                commission = revenue * 0.05
            elif count >= 10:
                tier_pct = "3%"
                commission = revenue * 0.03
            else:
                tier_pct = "0%"
                commission = 0.0
                
            doc_data.append({
                "Doctor Name": doc,
                "Patients Seen": count,
                "Total Revenue Generated": f"${revenue:,}",
                "Commission Tier": tier_pct,
                "Payout Amount": f"${commission:,.2f}"
            })
            
        df_commission = pd.DataFrame(doc_data)
        st.dataframe(df_commission, use_container_width=True)
        
        st.markdown("---")
        st.subheader("📋 All Live Diagnostic Logs")
        st.dataframe(df_visits[["date", "patient", "doctor", "service", "price"]], use_container_width=True)
