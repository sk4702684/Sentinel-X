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