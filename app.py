import streamlit as st
import socket
import requests

# Page Config for Hacker Look
st.set_page_config(page_title="Sentinel-X", layout="wide")

# Custom CSS for Dark Theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; }
    .stButton>button { background-color: #00ff41; color: black; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Sentinel-X: Cyber Recon Tool")
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Select Module", ["Dashboard", "IP Scanner", "Port Scanner"])

if option == "Dashboard":
    st.subheader("System Status: Online")
    st.info("Sentinel-X is ready for reconnaissance. Choose a module from the sidebar.")

elif option == "IP Scanner":
    st.subheader("🌐 IP/Domain Reconnaissance")
    target = st.text_input("Enter Domain or IP (e.g., google.com)")
    
    if st.button("Scan Target"):
        try:
            ip_addr = socket.gethostbyname(target)
            st.success(f"Target IP: {ip_addr}")
            
            # API call for Geo-location (Free API)
            response = requests.get(f"http://ip-api.com/json/{ip_addr}").json()
            st.json(response)
        except Exception as e:
            st.error(f"Error: {e}")

elif option == "Port Scanner":
    st.subheader("🔌 Basic Port Scanner")
    target_ip = st.text_input("Target IP")
    port_range = st.slider("Select Port Range", 1, 1024, (20, 80))
    
    if st.button("Start Port Scan"):
        st.write(f"Scanning {target_ip}...")
        open_ports = []
        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((target_ip, port)) == 0:
                open_ports.append(port)
            s.close()
        
        if open_ports:
            st.success(f"Open Ports: {open_ports}")
        else:
            st.warning("No open ports found in this range.")
            # --- Footer / Copyright Section ---
st.markdown("---")
footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #00ff41;
        text-align: center;
        padding: 10px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 14px;
        border-top: 1px solid #00ff41;
    }
    </style>
    <div class="footer">
        <p>© 2026 Satyam | Sentinel-X Cyber Recon Tool | All Rights Reserved</p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
# Ye lines app.py ke upar imports mein daal dena
from fpdf import FPDF 

# Ye function scanning logic ke paas daal dena
def create_pdf(scan_results, target):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Sentinel-X: Recon Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Target: {target}", ln=True, align='L')
    pdf.cell(200, 10, txt="---------------------------------------", ln=True, align='L')
    
    for res in scan_results:
        text = f"Port: {res['Port']} | Status: {res['Status']} | Service: {res['Service Info']}"
        pdf.cell(200, 10, txt=text, ln=True, align='L')
    
    # Copyright line in PDF
    pdf.cell(200, 20, txt="© 2026 Satyam | Sentinel-X", ln=True, align='C')
    return pdf.output(dest='S').encode('latin-1')

# Scan results dikhane ke baad ye button dikhana
if found_ports:
    results_data = [{"Port": p[0], "Status": p[1], "Service Info": p[2]} for p in found_ports]
    st.table(results_data)
    
    pdf_bytes = create_pdf(results_data, target_ip)
    st.download_button(
        label="📥 Download Report",
        data=pdf_bytes,
        file_name="SentinelX_Report.pdf",
        mime="application/pdf"
    )
    
