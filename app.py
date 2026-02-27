import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF

# --- Elite Cyberpunk UI Config ---
st.set_page_config(page_title="Sentinel-X | Elite Recon", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        border-radius: 5px; box-shadow: 0 0 15px #00ff41; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; box-shadow: 0 0 25px #00ff41; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #050a0e; 
              color: #00ff41; text-align: center; padding: 10px; border-top: 1px solid #00ff41; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X: ELITE RECONNAISSANCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><code>SYSTEM v2.6.0 | OPERATOR: SATYAM</code></p>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Dashboard", "Deep Recon", "Turbo Vuln Scanner"])

# Vuln Logic
def check_vulns(port, banner):
    vulns = []
    if port == 21: vulns.append("🚨 FTP Backdoor Risk (CVE-2011-2523)")
    if port == 23: vulns.append("🚨 Insecure Telnet Detected")
    return vulns

if option == "Dashboard":
    st.markdown("<div style='border: 1px solid #00ff41; padding: 20px; background: rgba(0,255,65,0.05);'><h3>SYSTEM ONLINE</h3><p>Select a module to begin intelligence gathering.</p></div>", unsafe_allow_html=True)

elif option == "Deep Recon":
    st.subheader("🌐 Global Subdomain Discovery")
    # --- Yahan hai tera Input Box aur Button ---
    target_domain = st.text_input("ENTER DOMAIN (e.g. google.com)", placeholder="target.com")
    if st.button("EXECUTE SUBDOMAIN SCAN"):
        with st.spinner("Brute-forcing..."):
            common = ['www', 'mail', 'ftp', 'dev', 'admin']
            found = []
            for s in common:
                try:
                    url = f"{s}.{target_domain}"
                    socket.gethostbyname(url)
                    found.append(url)
                except: pass
            if found: st.success(f"ACTIVE TARGETS: {found}")
            else: st.warning("No common subdomains detected.")

elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Advanced Port & Vuln Scan")
    # --- Yahan hai IP Input aur Scan Button ---
    target_ip = st.text_input("ENTER TARGET IP", placeholder="45.33.32.156")
    port_range = st.slider("PORT RANGE", 1, 1000, (20, 443))
    
    if st.button("INITIALIZE DEEP SCAN"):
        with st.spinner("Scanning..."):
            found_ports = []
            def scan(p):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((target_ip, p)) == 0:
                    return {"Port": p, "Status": "OPEN", "Banner": "Active"}
                return None
            
            with ThreadPoolExecutor(max_workers=50) as ex:
                res = list(ex.map(scan, range(port_range[0], port_range[1]+1)))
                found_ports = [r for r in res if r]
            st.session_state['results'] = found_ports

    if 'results' in st.session_state and st.session_state['results']:
        for r in st.session_state['results']:
            v = check_vulns(r['Port'], r['Banner'])
            with st.expander(f"🔹 PORT {r['Port']}"):
                st.write(f"Service: {r['Banner']}")
                for msg in v: st.error(msg)

# --- Permanent Footer ---
st.markdown("<div class='footer'>© 2026 SATYAM | SENTINEL-X | ALL RIGHTS RESERVED</div>", unsafe_allow_html=True)
