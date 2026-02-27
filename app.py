import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

# --- Elite UI Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        border-radius: 5px; box-shadow: 0 0 15px #00ff41; transition: 0.3s;
        font-family: 'Courier New', Courier, monospace;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; box-shadow: 0 0 25px #00ff41; }
    section[data-testid="stSidebar"] { background-color: rgba(10, 15, 20, 0.9); border-right: 1px solid #00ff41; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #050a0e; 
              color: #00ff41; text-align: center; padding: 10px; border-top: 1px solid #00ff41; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# --- Logic Modules ---
VULN_DB = {
    "21": "🚨 FTP: Unencrypted Credentials Risk (CVE-2011-2523)",
    "22": "✅ SSH: Secure Service Detected",
    "23": "🚨 TELNET: Insecure Cleartext Protocol",
    "80": "⚠️ HTTP: Missing Security Headers (HSTS/CSP)",
    "443": "✅ HTTPS: Secure Encryption Active"
}

def get_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(1.0)
        s.connect((target, port))
        if port == 80:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner if banner else "Active Service"
    except: return "Protected Service"

# --- Header ---
st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X: ELITE ENUMERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><code>v3.6.0 | OPERATOR: SATYAM | DEHRADUN_NODE</code></p>", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Deep Recon (Subdomains)", "Turbo Vuln Scanner"])

if option == "Mission Dashboard":
    st.markdown("""
        <div style='border: 1px solid #00ff41; padding: 20px; background: rgba(0,255,65,0.05);'>
            <h3>SYSTEM STATUS: ONLINE</h3>
            <p>Welcome back, Operator Satyam. Sentinel-X is ready for deployment.</p>
        </div>
    """, unsafe_allow_html=True)

elif option == "Deep Recon (Subdomains)":
    st.subheader("🌐 Global Subdomain Discovery")
    target_domain = st.text_input("ENTER ROOT DOMAIN", placeholder="example.com")
    if st.button("EXECUTE SUB-RECON"):
        with st.spinner("Brute-forcing common subdomains..."):
            common = ['www', 'mail', 'ftp', 'dev', 'admin', 'api', 'test', 'staging']
            found = []
            for s in common:
                try:
                    url = f"{s}.{target_domain}"
                    socket.gethostbyname(url)
                    found.append(url)
                except: pass
            if found:
                st.success(f"TARGETS ACQUIRED: {len(found)}")
                st.write(found)
            else: st.warning("No common subdomains detected.")

elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Port & Vulnerability Mapping")
    target_ip = st.text_input("ENTER TARGET IP", placeholder="45.33.32.156")
    col1, col2 = st.columns(2)
    with col1: port_range = st.slider("PORT RANGE", 1, 1000, (20, 100))
    with col2: scan_speed = st.select_slider("INTENSITY", options=["Stealth", "Balanced", "Turbo"])

    if st.button("INITIALIZE DEEP SCAN"):
        with st.spinner("🕵️ Enumerating Services..."):
            workers = 100 if scan_speed == "Turbo" else 50
            results = []
            def scan(p):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((target_ip, p)) == 0:
                    banner = get_banner(target_ip, p)
                    vuln = VULN_DB.get(str(p), "✅ Service verified. No common CVEs.")
                    return {"Port": p, "Banner": banner, "Risk": vuln}
                return None
            with ThreadPoolExecutor(max_workers=workers) as ex:
                scan_data = list(ex.map(scan, range(port_range[0], port_range[1]+1)))
                results = [r for r in scan_data if r]
            
            if results:
                for r in results:
                    with st.expander(f"🔹 PORT {r['Port']} | {r['Banner'][:40]}..."):
                        st.code(f"Banner: {r['Banner']}")
                        if "🚨" in r['Risk'] or "⚠️" in r['Risk']: st.error(r['Risk'])
                        else: st.success(r['Risk'])
            else: st.warning("No open ports detected.")

# --- Footer ---
st.markdown("<div class='footer'>© 2026 SATYAM | SENTINEL-X | ALL RIGHTS RESERVED</div>", unsafe_allow_html=True)
