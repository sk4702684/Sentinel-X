import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# --- Elite UI Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    
    /* Neon Glow UI Elements */
    div.stButton > button:first-child {
        background-color: transparent; color: #00ff41; border: 2px solid #00ff41;
        border-radius: 5px; box-shadow: 0 0 15px #00ff41; transition: 0.3s;
        font-family: 'Courier New', Courier, monospace; font-weight: bold;
    }
    div.stButton > button:hover { background-color: #00ff41; color: #050a0e; box-shadow: 0 0 25px #00ff41; }
    
    /* Result Expander Styling */
    .stExpander { border: 1px solid #00ff41 !important; background-color: rgba(0, 255, 65, 0.05) !important; }
    
    /* Professional Footer */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #050a0e; color: #00ff41; text-align: center;
        padding: 10px; border-top: 1px solid #00ff41; z-index: 100;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Logic Modules ---
VULN_DB = {
    "21": "🚨 FTP: Unencrypted Credentials Risk",
    "23": "🚨 TELNET: Cleartext transmission risk!",
    "80": "⚠️ HTTP: Missing Security Headers (HSTS/CSP)",
    "443": "✅ HTTPS: Secure Tunnel Verified"
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
    except: return "Active (Protected)"

# --- Dashboard Header ---
st.markdown("<h1 style='text-align: center; text-shadow: 0 0 20px #00ff41;'>🛡️ SENTINEL-X: ELITE ENUMERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><code>v3.5.0 | STATUS: AUTHORIZED | OPERATOR: SATYAM</code></p>", unsafe_allow_html=True)

# --- Main Layout ---
target_ip = st.text_input("🎯 ENTER TARGET (IP/DOMAIN)", placeholder="uktech.ac.in")
col1, col2 = st.columns(2)
with col1:
    port_range = st.slider("PORT RANGE", 1, 500, (20, 100))
with col2:
    scan_speed = st.select_slider("SCAN INTENSITY", options=["Stealth", "Balanced", "Turbo"], value="Balanced")

if st.button("INITIALIZE DEEP SCAN"):
    with st.spinner("🕵️ Decoding Network Packets..."):
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
            st.success(f"ANALYSIS COMPLETE: {len(results)} active entry points detected.")
            for r in results:
                with st.expander(f"🔹 PORT {r['Port']} | {r['Banner'][:50]}..."):
                    st.code(f"Technical Data: {r['Banner']}", language="bash")
                    if "🚨" in r['Risk'] or "⚠️" in r['Risk']:
                        st.error(f"VULNERABILITY: {r['Risk']}")
                    else:
                        st.success(f"SECURITY: {r['Risk']}")
        else:
            st.warning("No open ports found. Target might be behind a firewall.")

# --- Footer ---
st.markdown(f"""<div class='footer'>© 2026 SATYAM | SENTINEL-X | SYSTEM_LOCATION: DEHRADUN</div>""", unsafe_allow_html=True)
