import streamlit as st
from pathlib import Path

def load_css():
    with open("./assets/style/styles.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

load_css()

if 'ssh_connection' not in st.session_state:
    st.session_state['ssh_connection'] = False 
if 'ssh_client' not in st.session_state:
    st.session_state['ssh_client'] = None
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = None

pages = {
    "Connect": "./views/auth/connect.py",
    "Change Router Name": "./views/change_name_router.py",
    "IP Address Configuration": "./views/ip_address.py",
    "Gateway Configuration": "./views/gateway.py",
    "DNS Configuration": "./views/dns_server.py",
    "NAT Configuration": "./views/nat.py",
    "Backup Configuration": "./views/backup.py",
    "Help": "./views/help.py"
}

with st.sidebar:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("assets/img/logo-mikromanager.png", width=42)
    with col2:
        st.title("MikroManager")
    
    st.header("Connection Status")
    if st.session_state['ssh_client']:
        st.success("SSH Connected")
        
        if st.button("Disconnect", key="disconnect_button", help="Click to disconnect from the router."):
            try:
                if st.session_state['ssh_client']:
                    st.session_state['ssh_client'].close() 
                st.session_state['ssh_client'] = None
                st.session_state['ssh_connection'] = False
                st.success("Successfully disconnected from the router.")
                
                st.rerun()
            except Exception as e:
                st.error(f"Error disconnecting: {e}")
    else:
        st.warning("SSH Not Connected. Please go to 'Connect' and authenticate.")
    
    with st.expander("🔗 Connect", expanded=True):
        if st.button("Go to Connection Page", use_container_width=True):
            st.session_state['current_page'] = "Connect"

    with st.expander("⚙️ Configuration", expanded=False):
        if st.button("Change Router Name", use_container_width=True):
            st.session_state['current_page'] = "Change Router Name"
        if st.button("IP Address Configuration", use_container_width=True):
            st.session_state['current_page'] = "IP Address Configuration"
        if st.button("Gateway Configuration", use_container_width=True):
            st.session_state['current_page'] = "Gateway Configuration"
        if st.button("DNS Configuration", use_container_width=True):
            st.session_state['current_page'] = "DNS Configuration"
        if st.button("Nat Configuration", use_container_width=True):
            st.session_state['current_page'] = "NAT Configuration"
        if st.button("Backup Configuration", use_container_width=True):
            st.session_state['current_page'] = "Backup Configuration"

    with st.expander("❓ Help", expanded=False):
        if st.button("Help Page", use_container_width=True):
            st.session_state['current_page'] = "Help"

if 'current_page' in st.session_state and st.session_state['current_page'] in pages:
    file_path = Path(pages[st.session_state['current_page']])
    
    if file_path.exists():
        with file_path.open("r", encoding="utf-8") as file:
            exec(file.read())
    else:
        st.error(f"File not found: {file_path}")
else:
    st.header("Welcome to MikroManager!\nPlease connect your router first.")