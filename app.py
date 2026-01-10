import streamlit as st
import random
import time
import urllib.parse

# --- PRE-CONFIGURED SERVICES ---
SERVICES = {
    "WhatsApp": {"color": "#25D366", "emoji": "💬", "feature": "AI Auto-Reply & Broadcast"},
    "Instagram": {"color": "#E1306C", "emoji": "📸", "feature": "AI Image & Reel Gen"},
    "Twitter/X": {"color": "#1DA1F2", "emoji": "🐦", "feature": "AI Trend Analysis & Tweeting"},
    "Facebook": {"color": "#4267B2", "emoji": "👥", "feature": "AI Group & Page Growth"}
}

# --- WORLD-CLASS STYLING ---
st.set_page_config(page_title="APEX UNIVERSAL ACTIVATOR", layout="wide")
st.markdown(f"""
    <style>
    .stApp {{ background: #000000; color: white; }}
    .service-card {{
        border-radius: 15px; padding: 20px; margin: 10px;
        border: 1px solid #333; transition: 0.3s;
    }}
    .service-card:hover {{ border-color: #00f2fe; box-shadow: 0 0 15px #00f2fe; }}
    .activation-link {{ 
        background: #1a1a1a; padding: 15px; border-radius: 10px; 
        color: #00f2fe; border: 1px dashed #00f2fe; font-family: monospace;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- RESELLER PANEL ---
st.title("🛡️ APEX UNIVERSAL ACTIVATION HUB")
st.write("Generate private service URLs for your high-ticket clients.")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("🛠️ Provision New Client")
    client_name = st.text_input("Client Name")
    selected_service = st.selectbox("Select Social Ecosystem", list(SERVICES.keys()))
    duration = st.select_slider("Access Level", options=["30 Days", "90 Days", "Lifetime"])
    
    if st.button("🔥 GENERATE ACTIVATION PACKAGE"):
        # 1. Generate Key
        key = f"APEX-{selected_service[:2].upper()}-{random.randint(1000,9999)}"
        
        # 2. Generate Private URL (Encoded for safety)
        # In a real scenario, this would point to your hosted app URL
        base_url = "https://apex-bot-service.streamlit.app/"
        params = {"user": client_name, "service": selected_service, "key": key}
        activation_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        
        st.session_state.pkg = {
            "key": key,
            "url": activation_url,
            "service": selected_service,
            "name": client_name
        }

with col2:
    if 'pkg' in st.session_state:
        pkg = st.session_state.pkg
        st.success(f"Successfully Allocated {pkg['service']} for {pkg['name']}")
        
        # Display the "Bento Grid" of Services
        cols = st.columns(2)
        for i, (name, info) in enumerate(SERVICES.items()):
            with cols[i % 2]:
                opacity = "1.0" if name == pkg['service'] else "0.3"
                st.markdown(f"""
                <div class="service-card" style="opacity: {opacity};">
                    <h3>{info['emoji']} {name}</h3>
                    <p style="font-size: 0.8em;">{info['feature']}</p>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.subheader("🔗 Private Activation URL")
        st.markdown(f'<div class="activation-link">{pkg["url"]}</div>', unsafe_allow_html=True)
        st.caption("Send this link to the customer. When they enter the key, AI will start posting.")

# --- THE "CLIENT SIDE" PREVIEW ---
# This simulates what the user sees when they open your link
st.divider()
if st.toggle("👁️ Preview Client View (What they see)"):
    st.markdown("### 🖥️ Client Portal: Service Activation")
    input_key = st.text_input("Enter your License Key to wake up the AI:")
    if input_key == st.session_state.pkg['key']:
        st.balloons()
        st.success(f"AI ENGINE ONLINE: Now managing {st.session_state.pkg['service']} for {st.session_state.pkg['name']}")
        
        # Simulated AI Posting Loop
        with st.status("AI content generation in progress..."):
            st.write("Analyzing niche trends...")
            time.sleep(1)
            st.write("Drafting high-engagement media content...")
            time.sleep(1)
            st.write("Optimizing hashtags for global reach...")
            st.success("First 5 posts scheduled. Posting 1 per day automatically.")
