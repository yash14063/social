import streamlit as st
import random
import time
import pandas as pd

# --- THEME & UI SETUP ---
st.set_page_config(page_title="APEX CLOUD: Dual Portal", layout="wide")

st.markdown("""
<style>
    .stApp { background: #0b0e14; color: #ffffff; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; }
    .owner-box { border: 2px solid #00f2fe; padding: 20px; border-radius: 15px; background: rgba(0, 242, 254, 0.05); }
    .customer-box { border: 2px solid #a29bfe; padding: 20px; border-radius: 15px; background: rgba(162, 155, 254, 0.05); }
    .neon-button { background: linear-gradient(45deg, #00f2fe, #4facfe); color: black; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- DATABASE (Simulated) ---
if 'db_keys' not in st.session_state:
    st.session_state.db_keys = {} # Format: { "KEY-123": {"user": "John", "service": "Instagram"} }

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🚀 APEX NAVIGATION")
role = st.sidebar.selectbox("SWITCH PORTAL", ["Owner / Admin", "Customer / Client"])

# --- SECTION 1: OWNER / ADMIN ---
if role == "Owner / Admin":
    st.markdown("<h1 style='color:#00f2fe;'>👑 OWNER COMMAND CENTER</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown('<div class="owner-box">', unsafe_allow_html=True)
        st.subheader("Generate New License")
        c_name = st.text_input("Customer Name")
        c_service = st.selectbox("Assign Service", ["WhatsApp Bot", "Instagram AI", "Twitter Sniper", "Facebook LeadGen"])
        
        if st.button("CREATE ACCESS KEY"):
            new_key = f"APEX-{c_service[:2].upper()}-{random.randint(1000, 9999)}"
            st.session_state.db_keys[new_key] = {"name": c_name, "service": c_service}
            st.success(f"Key Created for {c_name}")
            st.code(new_key)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Active Licenses")
        if st.session_state.db_keys:
            df = pd.DataFrame.from_dict(st.session_state.db_keys, orient='index')
            st.table(df)
        else:
            st.info("No active licenses yet.")

# --- SECTION 2: CUSTOMER / CLIENT ---
else:
    st.markdown("<h1 style='color:#a29bfe;'>📱 CUSTOMER CLIENT SUITE</h1>", unsafe_allow_html=True)
    
    # LOCK MECHANISM
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown('<div class="customer-box">', unsafe_allow_html=True)
        st.subheader("🔐 Enter Your License Key to Activate")
        input_key = st.text_input("License Key", type="password")
        
        if st.button("ACTIVATE SERVICES"):
            if input_key in st.session_state.db_keys:
                st.session_state.authenticated = True
                st.session_state.current_user = st.session_state.db_keys[input_key]
                st.rerun()
            else:
                st.error("Invalid Key. Please contact the owner.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ACTIVATED CUSTOMER INTERFACE
    else:
        user_data = st.session_state.current_user
        st.success(f"Welcome Back, {user_data['name']}! Your {user_data['service']} is ACTIVE.")
        
        tab1, tab2 = st.tabs(["🤖 AI Content Engine", "📈 Growth Analytics"])
        
        with tab1:
            st.subheader("Generate & Post Automatically")
            topic = st.text_input("What is your niche today?", placeholder="e.g. Real Estate in Dubai")
            
            if st.button("START AI AUTOMATION"):
                with st.status("AI is drafting content..."):
                    time.sleep(1)
                    st.write("Optimizing for algorithm...")
                    time.sleep(1)
                    st.write(f"Posting to {user_data['service']}...")
                st.success("Post Successfully Published!")
                
                # Show AI Generated Preview
                st.info(f"**AI Content Preview:** 'Discover the best {topic} tips! 🚀 #Success #{user_data['service'].split()[0]}'")

        with tab2:
            st.subheader("Performance Tracking")
            chart_data = pd.DataFrame(np.random.randn(10, 1), columns=['Engagement'])
            st.line_chart(chart_data)

        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()
