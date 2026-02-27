import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import folium
from streamlit_folium import st_folium

# --- UI Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")
st.markdown("""<style>.main { background-color: #050a0e; color: #00ff41; }</style>""", unsafe_allow_html=True)

# --- Header & Sidebar ---
st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X: ELITE ENUMERATOR</h1>", unsafe_allow_html=True)
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Deep Recon (Subdomains)", "Turbo Vuln Scanner"])

# --- Vuln Database ---
VULN_DB = {"21": "🚨 FTP: Unencrypted", "22": "✅ SSH: Secure", "23": "🚨 TELNET: Risk", "80": "⚠️ HTTP: No HSTS"}

# --- 1. Mission Dashboard (Map) ---
if option == "Mission Dashboard":
    st.subheader("🌐 Global Target Intelligence")
    target_ip = st.text_input("ENTER IP", placeholder="8.8.8.8")
    if st.button("LOCATE"):
        res = requests.get(f"http://ip-api.com/json/{target_ip}").json()
        if res['status'] == 'success':
            st.success(f"LOCATED: {res['city']}, {res['country']}")
            m = folium.Map(location=[res['lat'], res['lon']], zoom_start=12, tiles="CartoDB dark_matter")
            folium.Marker([res['lat'], res['lon']]).add_to(m)
            st_folium(m, width=1000, height=400)

# --- 2. Deep Recon ---
elif option == "Deep Recon (Subdomains)":
    st.subheader("🔍 Subdomain Discovery")
    domain = st.text_input("ROOT DOMAIN", placeholder="google.com")
    if st.button("EXECUTE"):
        common = ['www', 'mail', 'ftp', 'dev']
        for s in common:
            try:
                url = f"{s}.{domain}"
                socket.gethostbyname(url)
                st.write(f"✅ FOUND: {url}")
            except: pass

# --- 3. Turbo Vuln Scanner (FIXED LOGIC) ---
elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Advanced Port & Vulnerability Mapping")
    target = st.text_input("ENTER TARGET IP", placeholder="47.15.117.3")
    # Slider range use karenge ab
    p_start, p_end = st.slider("PORT RANGE", 1, 1000, (20, 100))
    
    if st.button("INITIALIZE DEEP SCAN"):
        results_found = False
        with st.spinner("🕵️ Scanning all ports in range..."):
            def scan(p):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.4)
                if s.connect_ex((target, p)) == 0:
                    return p
                return None

            # Multi-threading taaki scan fast ho
            with ThreadPoolExecutor(max_workers=50) as ex:
                ports = range(p_start, p_end + 1)
                found = list(ex.map(scan, ports))
                
                for p in found:
                    if p:
                        results_found = True
                        vuln = VULN_DB.get(str(p), "✅ Service active. No common CVEs.")
                        with st.expander(f"🔹 PORT {p} - OPEN"):
                            st.info(f"FINDING: {vuln}")
            
            if not results_found:
                st.warning("No open ports found in this range. Try increasing the range or checking a different IP.")

# --- Footer ---
st.markdown("<div style='text-align: center; color: #00ff41; padding: 20px;'>© 2026 SATYAM | SENTINEL-X | DEHRADUN</div>", unsafe_allow_html=True)
