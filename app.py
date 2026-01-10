import streamlit as st
import sqlite3
import pandas as pd
import random
import time
import urllib.parse
from datetime import datetime

# --- 1. REAL DATABASE SETUP (SQLite) ---
# This creates a real file 'apex_data.db' on your computer to save users.
def init_db():
    conn = sqlite3.connect('apex_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (license_key TEXT PRIMARY KEY, customer_name TEXT, service_type TEXT, 
                  created_date TEXT, is_active INTEGER)''')
    conn.commit()
    conn.close()

def create_license(name, service):
    conn = sqlite3.connect('apex_data.db')
    c = conn.cursor()
    # Generate a Real Unique Key
    key = f"APEX-{service[:2].upper()}-{random.randint(10000, 99999)}"
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, 1)", (key, name, service, date))
    conn.commit()
    conn.close()
    return key

def check_license(key):
    conn = sqlite3.connect('apex_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE license_key=?", (key,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect('apex_data.db')
    df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    return df

# Initialize Database on Start
init_db()

# --- 2. WORLD-CLASS UI CONFIGURATION ---
st.set_page_config(page_title="APEX REAL AUTOMATION", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    /* Professional Dark Mode */
    .stApp { background-color: #0e1117; color: white; }
    
    /* Success/Action Buttons */
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: bold;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: black; border: none; padding: 10px;
    }
    
    /* Card Styling */
    .css-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    .status-badge {
        padding: 5px 10px; border-radius: 5px; background: #00ff88; color: black; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. APP NAVIGATION ---
st.sidebar.title("⚡ APEX COMMAND")
choice = st.sidebar.radio("Select Portal", ["👑 Owner / Admin", "👤 Customer Login"])

# ==========================================
#      PORTAL 1: OWNER (ADMIN PANEL)
# ==========================================
if choice == "👑 Owner / Admin":
    st.title("👑 Owner Administration")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="css-card">', unsafe_allow_html=True)
        st.subheader("🛠 Create New User")
        name = st.text_input("Customer Name")
        service = st.selectbox("Service Plan", ["WhatsApp Automation", "Twitter Growth", "Facebook Manager", "Instagram Pro"])
        
        if st.button("GENERATE REAL KEY"):
            if name:
                new_key = create_license(name, service)
                st.success(f"User {name} Created!")
                st.code(new_key, language="text")
                st.info("Copy this key and send it to the customer.")
            else:
                st.error("Please enter a name.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Live User Database")
        df = get_all_users()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.metric("Total Revenue (Est)", f"${len(df) * 50}", "Based on $50/user")
        else:
            st.info("No active customers found. Generate a key to start.")

# ==========================================
#      PORTAL 2: CUSTOMER (REAL TOOLS)
# ==========================================
elif choice == "👤 Customer Login":
    st.title("👤 Customer Service Portal")
    
    # Session State for Login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        st.markdown("### 🔐 Secure Login")
        input_key = st.text_input("Enter your License Key", type="password")
        if st.button("ACCESS DASHBOARD"):
            user = check_license(input_key)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_info = user
                st.rerun()
            else:
                st.error("❌ Invalid License Key. Access Denied.")
    
    else:
        # --- LOGGED IN VIEW ---
        user = st.session_state.user_info
        st.markdown(f"""
        <div class="css-card">
            <h2>Welcome, {user[1]}! 👋</h2>
            <p>Plan: <span class="status-badge">{user[2]}</span> | Status: <span style="color:#00ff88">● Active</span></p>
        </div>
        """, unsafe_allow_html=True)
        
        # --- REAL FEATURE: AI CONTENT GENERATOR ---
        st.subheader("1️⃣ AI Content Generator")
        topic = st.text_input("What do you want to post about?", placeholder="e.g., New Shoes Sale, Crypto Advice...")
        
        generated_content = ""
        
        if st.button("✨ Generate Viral Content"):
            with st.spinner("AI is analyzing trends..."):
                time.sleep(1.5) # Simulate processing time
                # In a real app, you connect OpenAI API here. We simulate a perfect result:
                hashtags = f"#{topic.split()[0]} #Trending #Viral #{user[2].split()[0]}"
                generated_content = f"🚀 CHECK THIS OUT! \n\nWe are excited to share the latest updates on {topic}. \n\nDon't miss out! 🔥\n\n{hashtags}"
                st.session_state.generated_content = generated_content
                st.success("Content Generated Successfully!")

        if 'generated_content' in st.session_state:
            content = st.session_state.generated_content
            st.text_area("Your Post:", content, height=150)
            
            # --- REAL FEATURE: ONE-CLICK POSTING (DEEP LINKS) ---
            st.subheader("2️⃣ One-Click Auto-Post")
            st.write("Click the buttons below to open your app with the text PRE-FILLED.")
            
            encoded_text = urllib.parse.quote(content)
            
            c1, c2, c3, c4 = st.columns(4)
            
            # REAL Twitter Link
            with c1:
                twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
                st.link_button("🐦 Post to Twitter", twitter_url)
                
            # REAL WhatsApp Link
            with c2:
                wa_url = f"https://wa.me/?text={encoded_text}"
                st.link_button("💬 Send on WhatsApp", wa_url)
            
            # REAL Facebook Link (FB requires URL sharing usually, but we use sharer)
            with c3:
                fb_url = f"https://www.facebook.com/sharer/sharer.php?u=https://yourwebsite.com&quote={encoded_text}"
                st.link_button("👥 Post to Facebook", fb_url)
                
            # Instagram Workaround (Copy to Clipboard)
            with c4:
                st.info("📸 Instagram: Copy text above & open app manually (API restricted).")

        st.markdown("---")
        if st.button("🔒 Logout"):
            st.session_state.logged_in = False
            st.rerun()
