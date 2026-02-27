import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF

# --- Layout & Styling (Cyberpunk) ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    .stButton>button { background-color: transparent; color: #00ff41; border: 1px solid #00ff41; box-shadow: 0 0 10px #00ff41; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #050a0e; color: #00ff41; text-align: center; border-top: 1px solid #00ff41; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. Subdomain Scanner Module ---
def scan_subdomains(domain):
    common_subs = ['www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'staging', 'api', 'test']
    found_subs = []
    for sub in common_subs:
        url = f"{sub}.{domain}"
        try:
            socket.gethostbyname(url)
            found_subs.append(url)
        except:
            pass
    return found_subs

# --- 2. Basic Vuln Scanner Module ---
def check_vulnerabilities(port, service_info):
    # Simple Logic: Checking for outdated/dangerous services
    vulnerabilities = []
    service_info = service_info.lower()
    if "apache/2.4.41" in service_info:
        vulnerabilities.append("⚠️ Potential CVE-2021-41773 (Path Traversal)")
    if port == 21:
        vulnerabilities.append("⚠️ FTP is often unencrypted. Risk of Sniffing.")
    if port == 23:
        vulnerabilities.append("🚨 Telnet detected! Extremely insecure.")
    return vulnerabilities if vulnerabilities else ["✅ No common vulnerabilities found."]

# --- Main App ---
st.title("🛡️ Sentinel-X: Elite Recon & Vuln Scanner")
option = st.sidebar.selectbox("COMMANDS", ["Dashboard", "Deep Subdomain Recon", "Port & Vuln Scanner"])

if option == "Dashboard":
    st.info("Sentinel-X v2.5.0: Enhanced with Deep Recon and CVE Mapping.")

elif option == "Deep Subdomain Recon":
    st.subheader("🔍 Subdomain Discovery")
    domain = st.text_input("Enter Root Domain (e.g., google.com)")
    if st.button("Start Discovery"):
        with st.spinner("Brute-forcing common subdomains..."):
            subs = scan_subdomains(domain)
            if subs:
                st.success(f"Found {len(subs)} active subdomains:")
                st.write(subs)
            else:
                st.warning("No common subdomains found.")

elif option == "Port & Vuln Scanner":
    st.subheader("🔌 Port Scanning & Vuln Mapping")
    target_ip = st.text_input("Target IP/Domain")
    if st.button("Initialize Deep Scan"):
        # Port Scan Logic (Reuse your fast threader)
        found_ports = [] # Assume list of (port, status, banner)
        # ... (Scan Logic here) ...
        
        # Display with Vuln Data
        st.markdown("### Scan Results & Risk Assessment")
        # Example output for testing
        test_port = 21
        test_banner = "Vsftpd 2.3.4"
        vulns = check_vulnerabilities(test_port, test_banner)
        st.write(f"**Port {test_port}**: {test_banner}")
        for v in vulns:
            st.error(v)

# --- Footer ---
st.markdown('<div class="footer">© 2026 Satyam | Sentinel-X All Rights Reserved</div>', unsafe_allow_html=True)
