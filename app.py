import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import folium
from streamlit_folium import st_folium

# --- 1. UI Configuration & Cyber Styling (UNTOUCHED) ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        box-shadow: 0 0 15px #00ff41; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; box-shadow: 0 0 25px #00ff41; }
    section[data-testid="stSidebar"] { background-color: rgba(10, 15, 20, 0.9); border-right: 1px solid #00ff41; }
    .auth-box { border: 2px solid #00ff41; padding: 30px; border-radius: 15px; background: rgba(0,255,65,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Auth & Database Logic (UNTOUCHED) ---
if 'user_db' not in st.session_state:
    st.session_state['user_db'] = {"satyam": "password123"} 

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# --- 3. Authentication Screen (UNTOUCHED) ---
if not st.session_state['authenticated']:
    st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X ACCESS CONTROL</h1>", unsafe_allow_html=True)
    auth_tab = st.tabs(["🔐 Sign In", "📝 Sign Up"])
    with auth_tab[0]:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        login_user = st.text_input("Username")
        login_pass = st.text_input("Password", type="password")
        if st.button("SIGN IN"):
            if login_user in st.session_state['user_db'] and st.session_state['user_db'][login_user] == login_pass:
                st.session_state['authenticated'] = True
                st.session_state['operator'] = login_user
                st.rerun()
            else: st.error("Invalid Credentials")
        st.markdown("</div>", unsafe_allow_html=True)
    with auth_tab[1]:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")
        if st.button("CREATE ACCOUNT"):
            if new_user and new_pass:
                st.session_state['user_db'][new_user] = new_pass
                st.success("Account created! Go to Sign In.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. Operational Dashboard ---
else:
    op = st.session_state['operator']
    st.sidebar.markdown(f"### 🛡️ OPERATOR: {op.upper()}")
    option = st.sidebar.radio("COMMAND CENTER", ["Mission Dashboard", "Deep Recon", "Turbo Scanner", "Logout"])

    if option == "Logout":
        st.session_state['authenticated'] = False
        st.rerun()

    # --- Tool 1: Mission Dashboard (MAP FIX APPLIED HERE) ---
    if option == "Mission Dashboard":
        st.subheader("🌐 Global Target Intelligence")
        target_ip = st.text_input("ENTER IP", placeholder="8.8.8.8")
        if st.button("LOCATE"):
            try:
                res = requests.get(f"http://ip-api.com/json/{target_ip}").json()
                if res['status'] == 'success':
                    st.info(f"Target: {res['city']}, {res['country']} | ISP: {res['isp']}")
                    
                    # Fix: Added 'tiles' update and 'returned_objects' to stop blank screen
                    m = folium.Map(location=[res['lat'], res['lon']], zoom_start=12, tiles="OpenStreetMap")
                    folium.Marker([res['lat'], res['lon']], popup=target_ip).add_to(m)
                    
                    # Rendering with specific parameters to force display
                    st_folium(m, width=1000, height=450, key="sentinel_map", returned_objects=[])
                else: st.error("Invalid IP Address.")
            except Exception as e: st.error(f"Map Error: {e}")

    # --- Tool 2: Deep Recon (UNTOUCHED) ---
    elif option == "Deep Recon":
        st.subheader("🔍 Subdomain Discovery")
        domain = st.text_input("ENTER DOMAIN", placeholder="example.com")
        if st.button("EXECUTE RECON"):
            with st.spinner("Scanning..."):
                common = ['www', 'mail', 'ftp', 'dev', 'api', 'admin']
                for s in common:
                    try:
                        url = f"{s}.{domain}"
                        socket.gethostbyname(url)
                        st.success(f"✅ FOUND: {url}")
                    except: pass

    # --- Tool 3: Turbo Scanner (UNTOUCHED) ---
    elif option == "Turbo Scanner":
        st.subheader("🔌 Advanced Port & Vuln Mapping")
        target = st.text_input("TARGET IP", placeholder="45.33.32.156")
        p_start, p_end = st.slider("PORT RANGE", 1, 1000, (20, 100))
        if st.button("INITIALIZE SCAN"):
            with st.spinner("🕵️ Scanning..."):
                def scan_port(p):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.4)
                    if s.connect_ex((target, p)) == 0: return p
                    return None
                with ThreadPoolExecutor(max_workers=50) as ex:
                    found = list(ex.map(scan_port, range(p_start, p_end + 1)))
                    for p in found:
                        if p: st.write(f"🔹 PORT {p}: OPEN")

# --- Footer (UNTOUCHED) ---
st.markdown("<div style='text-align: center; color: #00ff41; padding: 20px; border-top: 1px solid #00ff41;'>© 2026 SATYAM | SENTINEL-X | DEHRADUN</div>", unsafe_allow_html=True)
