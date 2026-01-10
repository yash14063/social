import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import urllib.parse
from datetime import datetime

# --- 1. DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('apex_v5.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (license_key TEXT PRIMARY KEY, customer_name TEXT, plan TEXT, 
                  joined_date TEXT, status INTEGER)''')
    conn.commit()
    conn.close()

def create_license(name, plan):
    conn = sqlite3.connect('apex_v5.db')
    key = f"APEX-{plan[:3].upper()}-{random.randint(10000, 99999)}"
    date = datetime.now().strftime("%Y-%m-%d")
    conn.cursor().execute("INSERT INTO users VALUES (?, ?, ?, ?, 1)", (key, name, plan, date))
    conn.commit()
    conn.close()
    return key

def verify_user(key):
    conn = sqlite3.connect('apex_v5.db')
    user = conn.cursor().execute("SELECT * FROM users WHERE license_key=?", (key,)).fetchone()
    conn.close()
    return user

init_db()

# --- 2. WORLD-CLASS UI CONFIG ---
st.set_page_config(page_title="APEX GLOBAL COMMAND", layout="wide", page_icon="🌐")

st.markdown("""
<style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    
    /* Social App Cards */
    .app-card {
        background: linear-gradient(145deg, #1e1e1e, #121212);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        cursor: pointer;
        height: 150px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .app-card:hover {
        border-color: #00f2fe;
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0, 242, 254, 0.2);
    }
    .icon { font-size: 40px; margin-bottom: 10px; }
    
    /* Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: bold;
        background: #00f2fe; color: black; border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. APP DICTIONARY (Data for all apps) ---
APPS = {
    "WhatsApp": {"icon": "💬", "color": "#25D366", "action": "Auto-Reply & Status"},
    "Instagram": {"icon": "📸", "color": "#E1306C", "action": "Caption & Hashtag Gen"},
    "Facebook": {"icon": "👥", "color": "#1877F2", "action": "Group Post & Ads"},
    "Twitter / X": {"icon": "❌", "color": "#1DA1F2", "action": "Thread Writer & Sniper"},
    "LinkedIn": {"icon": "💼", "color": "#0A66C2", "action": "Professional Article Gen"},
    "YouTube": {"icon": "▶️", "color": "#FF0000", "action": "Title & SEO Tag Gen"},
    "TikTok": {"icon": "🎵", "color": "#000000", "action": "Viral Script Writer"},
    "Telegram": {"icon": "✈️", "color": "#0088cc", "action": "Channel Broadcaster"},
    "Snapchat": {"icon": "👻", "color": "#FFFC00", "action": "Streak & Spotlight Gen"},
    "Pinterest": {"icon": "📌", "color": "#BD081C", "action": "Pin Description Gen"}
}

# --- 4. MAIN LOGIC ---
st.sidebar.title("🌐 APEX COMMAND")
mode = st.sidebar.radio("PORTAL SELECTOR", ["👑 ADMIN / OWNER", "🚀 CUSTOMER SUITE"])

# ==========================================
#      👑 ADMIN PANEL
# ==========================================
if mode == "👑 ADMIN / OWNER":
    st.title("👑 Owner Administration")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown('<div style="background:#111; padding:20px; border-radius:10px;">', unsafe_allow_html=True)
        st.subheader("🛠 Issue License")
        u_name = st.text_input("Customer Name")
        u_plan = st.selectbox("Plan", ["Starter (3 Apps)", "Pro (All Apps)", "Agency (White Label)"])
        if st.button("CREATE KEY"):
            if u_name:
                k = create_license(u_name, u_plan)
                st.success("License Created!")
                st.code(k)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.subheader("📊 Active Users")
        conn = sqlite3.connect('apex_v5.db')
        df = pd.read_sql_query("SELECT * FROM users", conn)
        st.dataframe(df, use_container_width=True)
        conn.close()

# ==========================================
#      🚀 CUSTOMER SUITE
# ==========================================
else:
    if 'auth' not in st.session_state: st.session_state.auth = False

    # LOGIN SCREEN
    if not st.session_state.auth:
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.title("🔐 Login")
            key_in = st.text_input("Enter License Key", type="password")
            if st.button("UNLOCK COMMAND CENTER"):
                u = verify_user(key_in)
                if u:
                    st.session_state.auth = True
                    st.session_state.u_data = u
                    st.rerun()
                else:
                    st.error("Invalid Key")

    # DASHBOARD SCREEN
    else:
        user = st.session_state.u_data
        st.markdown(f"### 👋 Welcome, {user[1]}")
        
        # --- APP SELECTION GRID ---
        st.markdown("---")
        st.subheader("📱 Select Platform to Automate")
        
        # Create a grid layout for apps
        app_list = list(APPS.keys())
        rows = [st.columns(5), st.columns(5)] # 2 rows of 5
        
        selected_app = None
        
        # Render Buttons as a Grid
        for i, app_name in enumerate(app_list):
            row_idx = 0 if i < 5 else 1
            col_idx = i % 5
            with rows[row_idx][col_idx]:
                if st.button(f"{APPS[app_name]['icon']}\n{app_name}", key=app_name, use_container_width=True):
                    st.session_state.active_app = app_name

        st.markdown("---")

        # --- THE WORKSTATION (Shows tools for the selected app) ---
        if 'active_app' in st.session_state:
            app = st.session_state.active_app
            data = APPS[app]
            
            st.markdown(f"<h1 style='color:{data['color']}'>{data['icon']} {app} Automation Hub</h1>", unsafe_allow_html=True)
            
            # SPLIT INTO TABS FOR FUNCTIONALITY
            t1, t2, t3 = st.tabs(["⚡ AI Content Generator", "🔗 One-Click Poster", "📈 Growth Tools"])
            
            # TAB 1: GENERATE CONTENT
            with t1:
                topic = st.text_input(f"What is your {app} post about?", placeholder="e.g. New Product Launch")
                tone = st.select_slider("Select Tone", options=["Professional", "Casual", "Viral/Hype", "Emotional"])
                
                if st.button(f"✨ Generate {app} Content"):
                    with st.spinner("AI is crafting the perfect message..."):
                        time.sleep(1.5)
                        
                        # SMART SIMULATION LOGIC
                        if app == "LinkedIn":
                            content = f"🚀 Excited to announce: {topic}!\n\nIn today's fast-paced world, innovation is key. That's why we are launching {topic}.\n\n👇 Let me know your thoughts in the comments!\n\n#Innovation #Business #Growth"
                        elif app == "Instagram":
                            content = f"{topic} Vibes! ✨\n.\n.\nDon't miss out on this. Double tap if you agree! ❤️\n.\n#Explore #Trending #{topic.replace(' ', '')}"
                        elif app == "Twitter / X":
                            content = f"🧵 1/5: Let's talk about {topic}.\n\nA lot of people get this wrong, but here is the truth...\n\n(Thread) 👇 #{topic.replace(' ', '')}"
                        elif app == "YouTube":
                            content = f"TITLE: {topic} - Ultimate Guide 2026\n\nDESCRIPTION:\nIn this video, I reveal the secrets of {topic}. Make sure to SUBSCRIBE for more!\n\nTAGS: {topic}, viral, how-to, guide"
                        else:
                            content = f"🔥 CHECK THIS OUT: {topic}!\n\nThis is going to change everything. Send me a DM for info! 💬"
                        
                        st.session_state.gen_text = content
                        st.text_area("AI Output:", content, height=200)

            # TAB 2: POSTING LINKS
            with t2:
                if 'gen_text' in st.session_state:
                    encoded = urllib.parse.quote(st.session_state.gen_text)
                    st.write("Click below to open the app with text pre-filled:")
                    
                    # DYNAMIC DEEP LINKS
                    if app == "Twitter / X":
                        st.link_button("🐦 Tweet Now", f"https://twitter.com/intent/tweet?text={encoded}")
                    elif app == "WhatsApp":
                        st.link_button("💬 Send to WhatsApp", f"https://wa.me/?text={encoded}")
                    elif app == "Telegram":
                        st.link_button("✈️ Broadcast on Telegram", f"https://t.me/share/url?url={encoded}")
                    elif app == "LinkedIn":
                        st.link_button("💼 Post to LinkedIn", f"https://www.linkedin.com/sharing/share-offsite/?url={encoded}") # Note: LI strictly limits text pre-fill via web
                    elif app == "Facebook":
                        st.link_button("👥 Share on Facebook", f"https://www.facebook.com/sharer/sharer.php?u=example.com&quote={encoded}")
                    else:
                        st.info(f"📸 For {app}, auto-posting via web is restricted by API.")
                        st.code(st.session_state.gen_text, language="text")
                        st.caption("Copy the text above and paste it into the app!")
                else:
                    st.warning("Generate content in Tab 1 first!")

            # TAB 3: SPECIFIC GROWTH TOOLS
            with t3:
                if app == "YouTube":
                    st.subheader("🏷️ SEO Tag Generator")
                    if st.button("Generate Tags"):
                        st.write("`#viral` `#trending` `#subscribe` `#newvideo` `#fyp`")
                elif app == "Instagram":
                    st.subheader("#️⃣ Hashtag Ladder")
                    st.write("**High Volume:** #Love #InstaGood\n**Mid Volume:** #TechLife #Startup\n**Niche:** #MyBusinessJourney")
                elif app == "WhatsApp":
                    st.subheader("📢 Bulk Broadcaster (Simulated)")
                    st.info("Upload CSV to send to 1000 contacts (Enterprise Plan Only)")
                else:
                    st.info(f"Advanced Analytics for {app} coming in Pro Version.")

        else:
            st.info("👈 Select an App from the grid above to start automating.")
            
        st.markdown("---")
        if st.button("🔒 LOGOUT"):
            st.session_state.auth = False
            st.rerun()
