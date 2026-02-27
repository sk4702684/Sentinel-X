import streamlit as st
import socket
import requests
from concurrent.futures import ThreadPoolExecutor
import folium
from streamlit_folium import st_folium

# --- Elite UI Styling ---
st.set_page_config(page_title="Sentinel-X Pro", layout="wide", page_icon="🛡️")
st.markdown("""<style>.main { background-color: #050a0e; color: #00ff41; }</style>""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("### 🛠️ COMMAND CENTER")
option = st.sidebar.radio("CHOOSE MODULE", ["Mission Dashboard", "Deep Recon (Subdomains)", "Turbo Vuln Scanner"])

# --- 1. Mission Dashboard (Stable Map Logic) ---
if option == "Mission Dashboard":
    st.subheader("🌐 Global Target Intelligence")
    target_ip = st.text_input("ENTER IP FOR GEOLOCATION", placeholder="47.15.117.3")
    
    if st.button("LOCATE TARGET"):
        with st.spinner("Fetching coordinates from satellite..."):
            try:
                res = requests.get(f"http://ip-api.com/json/{target_ip}").json()
                if res['status'] == 'success':
                    st.success(f"TARGET LOCATED: {res['city']}, {res['country']} | ISP: {res['isp']}")
                    
                    # Map configuration with Dark Mode
                    m = folium.Map(location=[res['lat'], res['lon']], zoom_start=12, tiles="CartoDB dark_matter")
                    folium.Marker(
                        [res['lat'], res['lon']], 
                        popup=f"Target: {target_ip}", 
                        icon=folium.Icon(color='green', icon='info-sign')
                    ).add_to(m)
                    
                    # Stable rendering call
                    st_folium(m, width=1100, height=500, returned_objects=[])
                else: 
                    st.error("Invalid IP or Private Network detected.")
            except Exception as e: 
                st.error(f"Map Rendering Error: {e}")

# --- Baaki modules ka code same rahega ---
elif option == "Deep Recon (Subdomains)":
    st.subheader("🔍 Subdomain Discovery")
    # ... (Pura purana logic) ...

elif option == "Turbo Vuln Scanner":
    st.subheader("🔌 Port & Vulnerability Mapping")
    # ... (Pura purana logic) ...

# --- Footer ---
st.markdown("<div style='text-align: center; color: #00ff41; padding: 20px; border-top: 1px solid #00ff41;'>© 2026 SATYAM | SENTINEL-X | DEHRADUN</div>", unsafe_allow_html=True)
