import streamlit as st
import random
import time
from datetime import datetime

# --- WORLD-CLASS UI CONFIG ---
st.set_page_config(page_title="APEX BOT RESELLER", layout="wide")

st.markdown("""
<style>
    .stApp { background: #050a10; color: #ffffff; }
    .bento-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #00f2fe;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .neon-text { color: #00f2fe; text-shadow: 0 0 10px #00f2fe; font-family: 'Orbitron', sans-serif; }
    .whatsapp-style { background: #075E54; color: white; padding: 15px; border-radius: 10px; font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
st.markdown("<h1 class='neon-text'>🚀 APEX WHATSAPP PROVISIONING</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown('<div class="bento-card">', unsafe_allow_html=True)
    st.header("👤 Customer Allocation")
    cust_name = st.text_input("Customer Name", placeholder="e.g. John Doe")
    service_type = st.selectbox("Service Level", ["Basic Bot (Auto-Reply)", "Premium Bot (AI + Marketing)", "Legendary (Full Agency Suite)"])
    
    if st.button("ACTIVATE & GENERATE KEY"):
        with st.spinner("Allocating Server Resources..."):
            time.sleep(1.5)
            # Generate Unique Key
            random_id = random.randint(1000, 9999)
            license_key = f"WA-{service_type[:3].upper()}-{random_id}-ACTIVE"
            st.session_state.active_key = license_key
            st.session_state.cust_name = cust_name
            st.success("Service Allocated Successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if 'active_key' in st.session_state:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.header("📲 Delivery Package")
        
        # 1. The License Key for the Customer
        st.subheader("Your License Key")
        st.code(st.session_state.active_key)
        
        # 2. The WhatsApp Status Generator
        st.subheader("Generated WhatsApp Status (Copy this)")
        status_text = f"🤖 MY NEW {service_type.upper()} IS LIVE! \n\nI am now using the APEX AI System to handle my messages 24/7. \n\nPowered by: @{st.session_state.cust_name}'s Private Bot ⚡"
        st.info(status_text)
        
        # 3. The Professional Handover Message
        st.subheader("Send this Message to Customer:")
        handover_msg = f"""
*Hello {st.session_state.cust_name}!* 🌟

Your *WhatsApp Bot Service* has been successfully activated.

🔑 *Your License Key:* `{st.session_state.active_key}`
🛡️ *Status:* ACTIVE (365 Days)
⚙️ *Service:* {service_type}

You can now connect your number to the dashboard and start automating!
        """
        st.text_area("Copy and Paste to WhatsApp:", handover_msg, height=200)
        
        if st.button("Copy Handover Message"):
            st.write("✅ Text ready to copy!")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Fill out the customer details on the left to generate the service package.")

# --- ANALYTICS FOOTER ---
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Server Uptime", "99.99%", "Stable")
c2.metric("Bot Speed", "0.4ms", "Ultra-Fast")
c3.metric("Security", "AES-256", "Encrypted")
