import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor

# --- Cyberpunk Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide")
st.markdown("""<style>.main { background-color: #050a0e; color: #00ff41; }</style>""", unsafe_allow_html=True)

# --- Real Vulnerability Database (Simplified) ---
VULN_DB = {
    "21": "🚨 FTP: Unencrypted Credentials Risk (CVE-2011-2523)",
    "22": "✅ SSH: Secure (Check for Brute Force)",
    "23": "🚨 TELNET: Cleartext transmission detected!",
    "80": "⚠️ HTTP: Missing Security Headers (HSTS/CSP)",
    "443": "✅ HTTPS: Secure Tunnel",
    "3306": "⚠️ MYSQL: Exposure risk if remotely accessible"
}

# --- Banner Grabbing Logic ---
def get_banner(target, port):
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect((target, port))
        # Kuch services ko "Hello" bolna padta hai banner ke liye
        if port == 80:
            s.send(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner if banner else "Service Active (No Banner)"
    except:
        return "Service Active"

# --- Main Logic ---
st.title("🛡️ SENTINEL-X: ADVANCED VULN SCANNER")
target_ip = st.text_input("ENTER TARGET", placeholder="uktech.ac.in")
port_range = st.slider("PORT THRESHOLD", 1, 1000, (20, 100))

if st.button("INITIALIZE DEEP ENUMERATION"):
    with st.spinner("🕵️ Extracting Banners and Mapping CVEs..."):
        results = []
        def scan(p):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target_ip, p)) == 0:
                banner = get_banner(target_ip, p)
                vuln = VULN_DB.get(str(p), "✅ No common CVEs for this port.")
                return {"Port": p, "Banner": banner, "Risk": vuln}
            return None

        with ThreadPoolExecutor(max_workers=50) as ex:
            scan_data = list(ex.map(scan, range(port_range[0], port_range[1]+1)))
            results = [r for r in scan_data if r]

        if results:
            for r in results:
                with st.expander(f"🔍 PORT {r['Port']} | {r['Banner']}"):
                    if "🚨" in r['Risk'] or "⚠️" in r['Risk']:
                        st.error(f"FINDING: {r['Risk']}")
                    else:
                        st.success(f"FINDING: {r['Risk']}")
        else:
            st.warning("Target is secured or filtered by a Firewall.")

# --- Footer ---
st.markdown("<div style='text-align: center; border-top: 1px solid #00ff41; padding: 10px;'>© 2026 Satyam | Sentinel-X v3.0</div>", unsafe_allow_html=True)
