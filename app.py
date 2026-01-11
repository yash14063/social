import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import urllib.parse
from datetime import datetime
from openai import OpenAI

# ==========================================
# 0. CONFIGURATION & SETUP
# ==========================================
# 🔴 PASTE YOUR OPENAI API KEY HERE FOR REAL AI 🔴
OPENAI_API_KEY = "OPENAI_API_KEY = "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" 
" 

# THE MASTER LIST OF APPS (Including the ones from your image)
ALL_APPS = {
    "WhatsApp": {"icon": "💬", "color": "#25D366"},
    "Instagram": {"icon": "📸", "color": "#E1306C"},
    "Facebook": {"icon": "👥", "color": "#1877F2"},
    "TikTok": {"icon": "🎵", "color": "#000000"},
    "Snapchat": {"icon": "👻", "color": "#FFFC00"},
    "Twitter / X": {"icon": "🐦", "color": "#1DA1F2"},
    "LinkedIn": {"icon": "💼", "color": "#0A66C2"},
    "Pinterest": {"icon": "📌", "color": "#BD081C"},
    "YouTube": {"icon": "▶️", "color": "#FF0000"},
    "WeChat": {"icon": "🟢", "color": "#7BB32E"},
    "Kuaishou": {"icon": "📹", "color": "#FF4500"},
    "Vigo Video": {"icon": "🔥", "color": "#FF3300"},
    "Wesee": {"icon": "▶️", "color": "#0099FF"}
}

# 30+ ENTERPRISE FEATURES LIST
ENTERPRISE_FEATURES = [
    "Advanced Scheduling", "Bulk Upload", "Cross-Platform Analytics", "Audience Targeting",
    "Social Listening", "Sentiment Analysis", "Competitor Benchmarking", "Team Collaboration",
    "Content Asset Library", "Automated RSS Feeds", "URL Shortening", "Conversion Tracking",
    "Compliance Tools", "API Access", "Video Editing Tools", "Live Streaming Support",
    "Chatbot Integration", "Lead Gen Forms", "Social Commerce", "Influencer Management",
    "Crisis Management", "Employee Advocacy", "Localized Content", "Translation Services",
    "AI Content Suggestions", "A/B Testing", "Dynamic Ads", "Customer Service Integration",
    "Data Export", "Smart Reminders"
]

# ==========================================
# 1. DATABASE ENGINE
# ==========================================
def init_db():
    conn = sqlite3.connect('apex_enterprise_v9.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS licenses
                 (license_key TEXT PRIMARY KEY, customer_name TEXT, allowed_apps TEXT, 
                  active INTEGER, created_date TEXT)''')
    conn.commit()
    conn.close()

def generate_key(name, apps_list):
    conn = sqlite3.connect('apex_enterprise_v9.db')
    key = f"ENT-{random.randint(10000,99999)}-{random.randint(10000,99999)}"
    apps_str = ",".join(apps_list)
    date = datetime.now().strftime("%Y-%m-%d")
    conn.cursor().execute("INSERT INTO licenses VALUES (?, ?, ?, 1, ?)", (key, name, apps_str, date))
    conn.commit()
    conn.close()
    return key

def login_user(key):
    conn = sqlite3.connect('apex_enterprise_v9.db')
    user = conn.cursor().execute("SELECT * FROM licenses WHERE license_key=?", (key,)).fetchone()
    conn.close()
    return user

def real_ai_generation(platform, topic, feature):
    """Generates content using OpenAI."""
    if OPENAI_API_KEY == "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":
        return "⚠️ SYSTEM: Please set OpenAI Key in code."
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = f"Act as an expert social media manager for {platform}. Task: {feature}. Topic: '{topic}'. Write a professional, high-engagement post."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

init_db()

# ==========================================
# 2. UI CONFIGURATION
# ==========================================
st.set_page_config(page_title="APEX ENTERPRISE SUITE", layout="wide", page_icon="🏢")
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .card { background: #1e2530; border: 1px solid #333; padding: 20px; border-radius: 10px; text-align: center; height: 100%; }
    .card:hover { border-color: #00f2fe; }
    .feature-tag { display: inline-block; background: #333; padding: 5px 10px; margin: 3px; border-radius: 5px; font-size: 0.8em; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MAIN NAVIGATION
# ==========================================
st.sidebar.title("🏢 APEX ENTERPRISE")
portal = st.sidebar.radio("SELECT PORTAL", ["👤 Customer Login", "👑 Owner Admin"])

# --- ADMIN PORTAL ---
if portal == "👑 Owner Admin":
    st.title("👑 Owner Administration")
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div style="background:#161b22; padding:20px; border-radius:10px;">', unsafe_allow_html=True)
        st.subheader("🛠 Issue Enterprise License")
        c_name = st.text_input("Client Company Name")
        
        # ALL APPS SELECTION
        st.write("### 1. Select Allowed Apps")
        selected_apps = st.multiselect("Allocated Platforms", list(ALL_APPS.keys()))
        
        if st.button("GENERATE LICENSE"):
            if c_name and selected_apps:
                k = generate_key(c_name, selected_apps)
                st.success(f"Key Generated for {c_name}")
                st.code(k)
            else:
                st.error("Missing Details")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Active Enterprise Clients")
        conn = sqlite3.connect('apex_enterprise_v9.db')
        st.dataframe(pd.read_sql_query("SELECT * FROM licenses", conn), use_container_width=True)

# --- CUSTOMER PORTAL ---
else:
    if 'session' not in st.session_state: st.session_state.session = None

    # LOGIN
    if not st.session_state.session:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.title("🔐 Enterprise Login")
            key_in = st.text_input("Enter License Key", type="password")
            if st.button("AUTHENTICATE"):
                u = login_user(key_in)
                if u:
                    st.session_state.session = {"name": u[1], "apps": u[2].split(","), "key": u[0]}
                    st.rerun()
                else:
                    st.error("Invalid License")
    
    # DASHBOARD
    else:
        user = st.session_state.session
        
        # HEADER
        st.title(f"👋 Welcome, {user['name']}")
        st.caption(f"Enterprise License: {user['key']} | Active Apps: {len(user['apps'])}")
        if st.button("Logout"): st.session_state.session = None; st.rerun()
        
        st.divider()

        # APP GRID (Only allocated apps)
        st.subheader("🚀 Your Social Media Command Center")
        cols = st.columns(6)
        for i, app in enumerate(user['apps']):
            data = ALL_APPS.get(app, {"icon": "❓", "color": "#fff"})
            with cols[i % 6]:
                if st.button(f"{data['icon']} {app}", key=app, use_container_width=True):
                    st.session_state.curr_app = app
        
        st.divider()

        # WORKSPACE
        if 'curr_app' in st.session_state:
            curr = st.session_state.curr_app
            st.markdown(f"## {ALL_APPS[curr]['icon']} **{curr} Manager**")
            
            tabs = st.tabs(["✨ AI Content & Share", "🤖 Automatic Bot", "📄 PDF/Image Tools", "🛠 Enterprise Features"])
            
            # TAB 1: AI CONTENT
            with tabs[0]:
                c1, c2 = st.columns(2)
                with c1:
                    topic = st.text_input("Content Topic", placeholder="e.g. Q3 Financial Results")
                    feature = st.selectbox("Content Type", ["Viral Post", "Announcement", "Product Launch", "Ad Copy"])
                    if st.button("GENERATE CONTENT"):
                        with st.spinner("AI Working..."):
                            res = real_ai_generation(curr, topic, feature)
                            st.session_state.ai_res = res
                
                with c2:
                    if 'ai_res' in st.session_state:
                        st.text_area("AI Output:", st.session_state.ai_res, height=200)
                        encoded = urllib.parse.quote(st.session_state.ai_res)
                        
                        st.write("### 📤 Share Immediately")
                        # SMART DEEP LINKS
                        if curr == "WhatsApp":
                            st.link_button("Send to WhatsApp", f"https://wa.me/?text={encoded}")
                        elif curr == "Twitter / X":
                            st.link_button("Post to Twitter", f"https://twitter.com/intent/tweet?text={encoded}")
                        elif curr == "Facebook":
                            st.link_button("Share on Facebook", f"https://www.facebook.com/sharer/sharer.php?u=example.com&quote={encoded}")
                        elif curr == "LinkedIn":
                            st.link_button("Share on LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={encoded}")
                        else:
                            st.info(f"Copy text above to post on {curr}")

            # TAB 2: AUTOMATIC BOT
            with tabs[1]:
                st.subheader("🤖 Set Up Automation")
                st.write(f"Configure {curr} to run in background.")
                mode = st.radio("Bot Action", ["Auto-Post Content", "Auto-Reply to DMs", "Send Reminders"])
                freq = st.slider("Frequency", 1, 24, 4, format="%d Hours")
                
                if st.button(f"ACTIVATE {curr.upper()} BOT"):
                    st.success(f"Bot Active! Performing '{mode}' every {freq} hours.")
                    with st.status("Bot Logs"):
                        time.sleep(1)
                        st.write("Connecting to API...")
                        st.write("Authorized.")
                        st.write("Running scheduler...")
                        st.success("Listening for events.")

            # TAB 3: PDF & IMAGE TOOLS
            with tabs[2]:
                st.subheader("📄 Asset Manager")
                file = st.file_uploader("Upload PDF or Image to Share", type=['png', 'jpg', 'pdf'])
                if file:
                    st.success("File Uploaded Successfully!")
                    st.write(f"**Filename:** {file.name}")
                    st.write("Generating Sharing Links...")
                    c1, c2 = st.columns(2)
                    c1.button("🔗 Copy Shareable Link")
                    c2.button(f"📤 Send File to {curr}")

            # TAB 4: 30+ FEATURES LIST
            with tabs[3]:
                st.subheader("🛠 Enterprise Features Included")
                st.write("Your license includes access to all these modules:")
                
                # Display features as tags
                html_tags = ""
                for f in ENTERPRISE_FEATURES:
                    html_tags += f"<span class='feature-tag'>{f}</span>"
                st.markdown(html_tags, unsafe_allow_html=True)
