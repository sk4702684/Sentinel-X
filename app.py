import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF
import time

# --- Page Config ---
st.set_page_config(page_title="Sentinel-X | Elite Recon", layout="wide", page_icon="🛡️")

# --- Advanced Cyberpunk CSS ---
st.markdown("""
    <style>
    .main { background-color: #050a0e; color: #00ff41; }
    
    /* Neon Border and Glow for Containers */
    div.stButton > button:first-child {
        background-color: transparent;
        color: #00ff41;
        border: 2px solid #00ff41;
        border-radius: 5px;
        box-shadow: 0 0 10px #00ff41;
        transition: 0.3s;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #00ff41;
        color: #050a0e;
        box-shadow: 0 0 20px #00ff41;
    }
    
    /* Footer Styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(10, 15, 20, 0.9);
        color: #00ff41;
        text-align: center;
        padding: 5px;
        font-family: 'Courier New', Courier, monospace;
        border-top: 1px solid #00ff41;
        z-index: 100;
    }

    /* Input Box Styling */
    .stTextInput > div > div > input {
        background-color: #0a0f14;
        color: #00ff41;
        border: 1px solid #00ff41;
    }

    /* Metrics and Status */
    .status-box {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00ff41;
        background: rgba(0, 255, 65, 0.05);
        margin-bottom: 20px;
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
    pdf.cell(200, 10, txt=f"TARGET ENUMERATED: {target}", ln=True, align='L')
    pdf.cell(200, 10, txt="---------------------------------------", ln=True, align='L')
    for res in scan_results:
        text = f"PORT {res['Port']} [{res['Status']}] - SERVICE: {res['Service Info']}"
        pdf.cell(200, 10, txt=text, ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt="© 2026 SATYAM | SENTINEL-X INTERNAL", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- Header Section ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/564/564619.png", width=100)
with col2:
    st.markdown("<h1 style='text-shadow: 0 0 15px #00ff41;'>SENTINEL-X: ELITE RECONNAISSANCE</h1>", unsafe_allow_html=True)
    st.write("`System v2.1.0 | Status: Authorized`")

# --- Navigation ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Network Recon", "Turbo Scanner"])

if option == "Mission Dashboard":
    st.markdown("<div class='status-box'><h3>SITUATION REPORT</h3><p>Waiting for target input. Sentinel-X is idle and ready for deployment.</p></div>", unsafe_allow_html=True)
    st.info("Select a module to begin intelligence gathering.")

elif option == "Network Recon":
    st.subheader("🌐 Global IP Intelligence")
    target = st.text_input("ENTER TARGET DOMAIN/IP", placeholder="example.com")
    if st.button("EXECUTE WHOIS"):
        with st.spinner("Decrypting metadata..."):
            try:
                ip_addr = socket.gethostbyname(target)
                st.success(f"TARGET ACQUIRED: {ip_addr}")
                res = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
                st.json(res)
            except Exception as e:
                st.error(f"SCAN FAILED: {e}")

elif option == "Turbo Scanner":
    st.subheader("🔌 Advanced Port Enumeration")
    target_ip = st.text_input("TARGET IP", placeholder="127.0.0.1")
    port_range = st.select_slider("SELECT PORT THRESHOLD", options=[20, 80, 443, 1000, 5000, 8080], value=(20, 443))
    
    def scan_port(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
                return (port, "OPEN", banner if banner else "Banner-less")
            except:
                return (port, "OPEN", "Active Service")
        s.close()
        return None

    if st.button("INITIALIZE TURBO SCAN"):
        progress_bar = st.progress(0)
        found_ports = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            ports = range(port_range[0], port_range[1] + 1)
            results = list(executor.map(scan_port, ports))
            for i, res in enumerate(results):
                if res: found_ports.append(res)
                progress_bar.progress((i + 1) / len(results))
        st.session_state['scan_results'] = found_ports

    if 'scan_results' in st.session_state and st.session_state['scan_results']:
        results_data = [{"Port": p[0], "Status": p[1], "Service Info": p[2]} for p in st.session_state['scan_results']]
        st.dataframe(results_data, use_container_width=True)
        
        pdf_bytes = create_pdf(results_data, target_ip)
        st.download_button("📂 EXPORT CLASSIFIED PDF", data=pdf_bytes, file_name=f"Recon_{target_ip}.pdf")

# --- Footer ---
st.markdown("""
    <div class="footer">
        <p>TERMINAL: SENTINEL-X | © 2026 SATYAM | CLASSIFIED PROJECT</p>
    </div>
    """, unsafe_allow_html=True)
