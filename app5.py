import streamlit as st

st.set_page_config(page_title="Garden Clinic", page_icon="🌿")

st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:80vh;text-align:center;">
    <div style="font-size:3rem;margin-bottom:16px;">🌿</div>
    <div style="font-family:Georgia,serif;font-size:2rem;font-weight:600;color:#0D3D2B;margin-bottom:12px;">Garden Clinic</div>
    <div style="font-size:1rem;color:#555;max-width:400px;line-height:1.7;">This application is currently unavailable.<br/>Please contact the clinic for assistance.</div>
</div>
""", unsafe_allow_html=True)
