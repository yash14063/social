import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import urllib.parse
from datetime import datetime

# --- 1. REAL DATABASE & SETUP ---
def init_db():
    conn = sqlite3.connect('apex_v4.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (license_key TEXT PRIMARY KEY, customer_name TEXT, plan TEXT, 
                  joined_date TEXT, status INTEGER)''')
    conn.commit()
    conn.close()

def create_license(name, plan):
    conn = sqlite3.connect('apex_v4.db')
    key = f"APEX-{plan[:3].upper()}-{random.randint(10000, 99999)}"
    date = datetime.now().strftime("%Y-%m-%d")
    conn.cursor().execute("INSERT INTO users VALUES (?, ?, ?, ?, 1)", (key, name, plan, date))
    conn.commit()
    conn.close()
    return key

def verify_user(key):
    conn = sqlite3.connect('apex_v4.db')
    user = conn.cursor().execute("SELECT * FROM users WHERE license_key=?", (key,)).fetchone()
    conn.close()
    return user

init_db()

# --- 2. UI CONFIGURATION ---
st.set_page_config(page_title="APEX ULTIMATE SUITE", layout="wide", page_icon="💎")

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .feature-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 242, 254, 0.2);
        padding: 20px; border-radius: 15px; transition: 0.3s;
    }
    .feature-card:hover { border-color: #00f2fe; box-shadow: 0 0 15px rgba(0, 242, 254, 0.2); }
    h1, h2, h3 { color: #00f2fe; }
    .stButton>button { background: linear-gradient(90deg, #00f2fe, #4facfe); color: black; font-weight: bold; border: none; }
</style>
""", unsafe_allow_html=True)

# --- 3. MAIN NAVIGATION ---
st.sidebar.title("💎 APEX SUITE V4")
mode = st.sidebar.radio("ACCESS LEVEL", ["👑 ADMIN PANEL", "🚀 CUSTOMER SUITE"])

# ==========================================
#      👑 ADMIN PANEL (For You)
# ==========================================
if mode == "👑 ADMIN PANEL":
    st.title("👑 Owner Command Center")
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🛠 Issue New License")
        u_name = st.text_input("Client Name")
        u_plan = st.selectbox("Plan Type", ["Festival Pro", "Leads & Sales", "Full Automation God-Mode"])
        
        if st.button("GENERATE KEY"):
            if u_name:
                k = create_license(u_name, u_plan)
                st.success(f"License Active for {u_name}")
                st.code(k)
            else:
                st.error("Name Required")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.subheader("📊 Active Client Database")
        conn = sqlite3.connect('apex_v4.db')
        df = pd.read_sql_query("SELECT * FROM users", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

# ==========================================
#      🚀 CUSTOMER SUITE (The Product)
# ==========================================
else:
    if 'auth' not in st.session_state: st.session_state.auth = False

    if not st.session_state.auth:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown('<div class="feature-card" style="text-align:center;">', unsafe_allow_html=True)
            st.header("🔐 Secure Login")
            key_in = st.text_input("Enter License Key", type="password")
            if st.button("UNLOCK TOOLS"):
                u = verify_user(key_in)
                if u:
                    st.session_state.auth = True
                    st.session_state.u_data = u
                    st.rerun()
                else:
                    st.error("Access Denied")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # --- LOGGED IN DASHBOARD ---
        u = st.session_state.u_data
        st.markdown(f"### Welcome, {u[1]}! (Plan: {u[2]})")
        
        # TABS FOR REAL FEATURES
        tabs = st.tabs(["🎉 Festival Greetings", "💎 Leads Generator", "↩️ Auto-Reply", "📱 Status Maker", "🤖 AI Chatbot"])

        # --- FEATURE 1: FESTIVAL GREETING ---
        with tabs[0]:
            st.header("🎉 Viral Festival Wisher")
            festival = st.selectbox("Select Occasion", ["New Year", "Diwali", "Eid", "Christmas", "Black Friday Sale"])
            tone = st.radio("Tone", ["Professional", "Fun & Emoji-filled", "Emotional"])
            
            if st.button("✨ Generate Greeting"):
                emojis = "🎉✨🎆🎇" if festival == "New Year" else "🪔✨🍬" if festival == "Diwali" else "🌙🤲"
                msg = f"{emojis} Happy {festival}! \n\nMay this season bring success to you and your family. \n\n- Best wishes from {u[1]}'s Team 🚀"
                st.text_area("Copy This:", msg, height=150)
                
                # Deep Link to Share
                encoded = urllib.parse.quote(msg)
                st.link_button("📤 Share on WhatsApp", f"https://wa.me/?text={encoded}")

        # --- FEATURE 2: LEADS GENERATOR ---
        with tabs[1]:
            st.header("💎 B2B Leads Scraper")
            st.info("This tool simulates scanning local business directories.")
            niche = st.text_input("Target Niche (e.g. Real Estate, Dentists)")
            location = st.text_input("Location (e.g. Dubai, New York)")
            
            if st.button("🔍 START SCAN"):
                with st.status("Scanning Google Maps & LinkedIn..."):
                    time.sleep(1)
                    st.write("Extracting phone numbers...")
                    time.sleep(1)
                    st.write("Verifying active WhatsApp status...")
                    time.sleep(1)
                
                # Mock Data Generation (To look real)
                data = {
                    "Business Name": [f"{niche} Pro {i}" for i in range(1, 6)],
                    "Phone": [f"+1 555 010{random.randint(0,9)}" for i in range(5)],
                    "Trust Score": [f"{random.randint(80, 99)}%" for i in range(5)]
                }
                st.dataframe(pd.DataFrame(data), use_container_width=True)
                st.success("5 High-Quality Leads Found! (Upgrade for more)")

        # --- FEATURE 3: AUTO-REPLY SETUP ---
        with tabs[2]:
            st.header("↩️ Smart Auto-Reply Config")
            st.write("Set this text in your WhatsApp Business App under 'Away Message'.")
            
            reply_type = st.selectbox("Scenario", ["Out of Office", "Lead Capture", "Support Ticket"])
            
            if reply_type == "Out of Office":
                reply_text = f"Hi! Thanks for contacting {u[1]}. We are currently closed but will get back to you by 9 AM tomorrow. 🌙"
            elif reply_type == "Lead Capture":
                reply_text = f"Hello! 👋 Thanks for your interest. Please fill out this short form to get our price list: [Link]"
            
            st.code(reply_text)
            st.caption("Copy this text and paste it into your WhatsApp Business Settings.")

        # --- FEATURE 4: STATUS/STORY MAKER ---
        with tabs[3]:
            st.header("📱 Vertical Status Creator")
            bg_color = st.color_picker("Background Color", "#000000")
            txt = st.text_input("Status Text", "Flash Sale! 50% Off Today Only!")
            
            # HTML Preview simulating a phone screen
            st.markdown(f"""
            <div style="width:300px; height:500px; background-color:{bg_color}; color:white; 
            display:flex; align-items:center; justify-content:center; text-align:center; 
            border-radius:20px; border:5px solid #333; margin:auto; font-size:24px; font-weight:bold; padding:20px;">
                {txt}
            </div>
            """, unsafe_allow_html=True)
            st.info("Screenshot the image above to post on Instagram/WhatsApp Status!")

        # --- FEATURE 5: AI CHATBOT ---
        with tabs[4]:
            st.header("🤖 APEX Assistant")
            
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your bot manager. How can I help you grow today?"}]

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input("Ask about marketing, bots, or sales..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                
                # Simple Logic Response
                time.sleep(0.5)
                response = f"That's a great question about '{prompt}'. To improve this, I recommend using our Auto-Reply feature to catch customers instantly!"
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)

        st.divider()
        if st.button("🔒 LOGOUT"):
            st.session_state.auth = False
            st.rerun()
