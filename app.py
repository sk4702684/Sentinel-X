import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF
import time

# --- Page Config ---
st.set_page_config(page_title="Sentinel-X | Elite Recon", layout="wide", page_icon="🛡️")

# --- Neon Glow & Glassmorphism CSS ---
st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    
    /* Neon Glow Buttons */
    div.stButton > button:first-child {
        background-color: transparent;
        color: #00ff41;
        border: 2px solid #00ff41;
        border-radius: 5px;
        box-shadow: 0 0 15px #00ff41;
        transition: 0.3s;
        font-family: 'Courier New', Courier, monospace;
    }
    div.stButton > button:hover {
        background-color: #00ff41;
        color: #050a0e;
        box-shadow: 0 0 25px #00ff41;
    }
    
    /* Glassmorphism Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 15, 20, 0.8);
        border-right: 1px solid #00ff41;
    }

    /* Status Box */
    .status-box {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #00ff41;
        background: rgba(0, 255, 65, 0.05);
        box-shadow: inset 0 0 10px #00ff41;
        margin-bottom: 20px;
    }

    /* Permanent Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(5, 10, 14, 0.9);
        color: #00ff41;
        text-align: center;
        padding: 8px;
        font-family: 'Courier New', Courier, monospace;
        border-top: 1px solid #00ff41;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF Logic ---
def create_pdf(scan_results, target):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="SENTINEL-X CLASSIFIED REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"TARGET: {target}", ln=True, align='L')
    for res in scan_results:
        text = f"PORT {res['Port']} [{res['Status']}] - {res['Banner']}"
        pdf.cell(200, 10, txt=text, ln=True, align='L')
    return pdf.output(dest='S').encode('latin-1')

# --- Header ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/564/564619.png", width=80)
with col2:
    st.markdown("<h1 style='text-shadow: 0 0 20px #00ff41;'>SENTINEL-X: ELITE RECON</h1>", unsafe_allow_html=True)

# --- Navigation & Logic ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Subdomain Recon", "Turbo Vuln Scanner"])

# Vulnerability Engine
def check_vulns(port, banner):
    vulns = []
    banner = banner.lower()
    if port == 21: vulns.append("🚨 FTP Backdoor Risk (CVE-2011-2523)")
    if "apache/2.4.41" in banner: vulns.append("⚠️ Path Traversal Vulnerability")
    if port == 23: vulns.append("🚨 Insecure Telnet Detected")
    return vulns

if option == "Mission Dashboard":
    st.markdown("<div class='status-box'><h3>SYSTEM ONLINE</h3><p>Sentinel-X ready. Pulse animation active. Choose a module to begin.</p></div>", unsafe_allow_html=True)
    # Pulse Animation Placeholder
    st.markdown("![Pulse](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJ6bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4bmZ4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxvK9vR8KEE/giphy.gif)")

elif option == "Subdomain Recon":
    st.subheader("🌐 Global Subdomain Discovery")
    target_domain = st.text_input("ENTER DOMAIN")
    if st.button("EXECUTE"):
        with st.spinner("Brute-forcing..."):
            subs = ['www', 'mail', 'ftp', 'dev', 'admin', 'api']
            found = []
            for s in subs:
                try: 
                    socket.gethostbyname(f"{s}.{target_domain}")
                    found.append(f"{s}.{target_domain}")
                except: pass
            st.success(f"Found: {found}")

elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Multi-Threaded Scanner")
    target_ip = st.text_input("TARGET IP", placeholder="45.33.32.156")
    if st.button("INITIALIZE SCAN"):
        with ThreadPoolExecutor(max_workers=50) as executor:
            found_ports = []
            # Port Scan Loop (Simplified for example)
            ports = [21, 22, 80, 443]
            for p in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.3)
                if s.connect_ex((target_ip, p)) == 0:
                    try: b = s.recv(1024).decode().strip()
                    except: b = "Active Service"
                    found_ports.append({"Port": p, "Status": "OPEN", "Banner": b})
            st.session_state['results'] = found_ports

    if 'results' in st.session_state:
        for r in st.session_state['results']:
            v = check_vulns(r['Port'], r['Banner'])
            with st.expander(f"🔹 PORT {r['Port']} - {r['Banner']}"):
                for msg in v: st.error(msg)
        
        pdf_bytes = create_pdf(st.session_state['results'], target_ip)
        st.download_button("📂 EXPORT PDF", data=pdf_bytes, file_name="Report.pdf")

# --- Footer ---
st.markdown("<div class='footer'>© 2026 SATYAM | SENTINEL-X | ALL RIGHTS RESERVED</div>", unsafe_allow_html=True)
