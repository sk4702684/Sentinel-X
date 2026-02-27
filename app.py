import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import folium
from streamlit_folium import st_folium

# --- UI Config ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")

# --- Styling ---
st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        box-shadow: 0 0 15px #00ff41; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; }
    .operator-card { border: 1px solid #00ff41; padding: 15px; background: rgba(0,255,65,0.05); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Session State for Login ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- 1. Login Page ---
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X ACCESS CONTROL</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='operator-card'>", unsafe_allow_html=True)
        user_name = st.text_input("ENTER OPERATOR NAME", placeholder="Type your name...")
        access_key = st.text_input("ENTER ACCESS KEY", type="password", placeholder="Sentinel-X Private Key")
        
        if st.button("AUTHORIZE ACCESS"):
            if user_name and access_key == "SX-2026": # Secret key tune chuni hai
                st.session_state['authenticated'] = True
                st.session_state['operator'] = user_name
                st.rerun()
            else:
                st.error("Invalid Access Key or Identity.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. Main Dashboard (After Login) ---
else:
    op_name = st.session_state['operator']
    
    # Sidebar
    st.sidebar.markdown(f"### 👤 OPERATOR: {op_name.upper()}")
    option = st.sidebar.radio("COMMAND CENTER", ["Mission Dashboard", "Deep Recon", "Turbo Scanner", "Logout"])

    if option == "Logout":
        st.session_state['authenticated'] = False
        st.rerun()

    # Header with User Name
    st.markdown(f"<h1 style='text-shadow: 0 0 20px #00ff41;'>Welcome, Operator {op_name}</h1>", unsafe_allow_html=True)
    st.write(f"`Node Status: Active | Authorized Operator: {op_name} | Location: Dehradun`")

    # --- Modules Logic ---
    if option == "Mission Dashboard":
        st.subheader("🌐 Global Intelligence (Map)")
        target_ip = st.text_input("TARGET IP", placeholder="8.8.8.8")
        if st.button("LOCATE"):
            res = requests.get(f"http://ip-api.com/json/{target_ip}").json()
            if res['status'] == 'success':
                st.info(f"Target: {res['city']}, {res['country']}")
                m = folium.Map(location=[res['lat'], res['lon']], zoom_start=12, tiles="CartoDB dark_matter")
                folium.Marker([res['lat'], res['lon']]).add_to(m)
                st_folium(m, width=1000, height=400)

    elif option == "Deep Recon":
        st.subheader("🔍 Subdomain Discovery")
        domain = st.text_input("DOMAIN", placeholder="google.com")
        if st.button("EXECUTE"):
            common = ['www', 'mail', 'ftp', 'dev']
            for s in common:
                try:
                    socket.gethostbyname(f"{s}.{domain}")
                    st.success(f"Found: {s}.{domain}")
                except: pass

    elif option == "Turbo Scanner":
        st.subheader("🔌 Turbo Vuln Scanner")
        target = st.text_input("TARGET IP", placeholder="45.33.32.156")
        if st.button("START SCAN"):
            with st.spinner("Enumerating..."):
                ports = [21, 22, 80, 443]
                for p in ports:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    if s.connect_ex((target, p)) == 0:
                        st.write(f"🔹 Port {p}: OPEN")
                    s.close()

# --- Footer ---
st.markdown("<div style='text-align: center; color: #00ff41; padding: 20px; border-top: 1px solid #00ff41;'>© 2026 Satyam | Sentinel-X Cyber Suite</div>", unsafe_allow_html=True)
