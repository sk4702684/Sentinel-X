import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import folium
from streamlit_folium import st_folium

# --- Elite UI Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        border-radius: 5px; box-shadow: 0 0 15px #00ff41; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; box-shadow: 0 0 25px #00ff41; }
    section[data-testid="stSidebar"] { background-color: rgba(10, 15, 20, 0.9); border-right: 1px solid #00ff41; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #050a0e; 
              color: #00ff41; text-align: center; padding: 10px; border-top: 1px solid #00ff41; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X: ELITE ENUMERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><code>v3.7.0 | OPERATOR: SATYAM | SYSTEM_LOCATION: DEHRADUN</code></p>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Deep Recon (Subdomains)", "Turbo Vuln Scanner"])

# --- Vuln DB ---
VULN_DB = {"21": "🚨 FTP: Unencrypted Risk", "23": "🚨 TELNET: Insecure Protocol", "80": "⚠️ HTTP: Missing Headers"}

# --- Mission Dashboard (Map Integration) ---
if option == "Mission Dashboard":
    st.subheader("🌐 Global Target Intelligence")
    target_ip = st.text_input("ENTER IP FOR GEOLOCATION", placeholder="8.8.8.8")
    
    if st.button("LOCATE TARGET"):
        with st.spinner("Fetching coordinates..."):
            try:
                res = requests.get(f"http://ip-api.com/json/{target_ip}").json()
                if res['status'] == 'success':
                    st.success(f"TARGET LOCATED: {res['city']}, {res['country']} | ISP: {res['isp']}")
                    m = folium.Map(location=[res['lat'], res['lon']], zoom_start=12, tiles="CartoDB dark_matter")
                    folium.Marker([res['lat'], res['lon']], popup=target_ip).add_to(m)
                    st_folium(m, width=1200, height=500)
                else: st.error("Invalid IP Address.")
            except Exception as e: st.error(f"Error: {e}")

# --- Subdomain Recon ---
elif option == "Deep Recon (Subdomains)":
    st.subheader("🔍 Subdomain Discovery")
    domain = st.text_input("ENTER ROOT DOMAIN", placeholder="example.com")
    if st.button("EXECUTE"):
        with st.spinner("Scanning..."):
            common = ['www', 'mail', 'ftp', 'dev', 'admin', 'api']
            found = []
            for s in common:
                try:
                    url = f"{s}.{domain}"
                    socket.gethostbyname(url)
                    found.append(url)
                except: pass
            if found: st.write(found)
            else: st.warning("No targets found.")

# --- Vuln Scanner ---
elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Port & Vulnerability Mapping")
    target = st.text_input("ENTER TARGET IP", placeholder="45.33.32.156")
    if st.button("INITIALIZE DEEP SCAN"):
        with st.spinner("🕵️ Enumerating..."):
            # Simple scan logic for stability
            ports = [21, 22, 80, 443]
            for p in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((target, p)) == 0:
                    vuln = VULN_DB.get(str(p), "✅ Service verified.")
                    with st.expander(f"🔹 PORT {p}"):
                        st.info(vuln)
                s.close()

# --- Footer ---
st.markdown("<div class='footer'>© 2026 SATYAM | SENTINEL-X | ALL RIGHTS RESERVED</div>", unsafe_allow_html=True)
