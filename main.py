import streamlit as st
import os

if 'ssh_connection' not in st.session_state:
    st.session_state['ssh_connection'] = None 
if 'ssh_client' not in st.session_state:
    st.session_state['ssh_client'] = None

pages = {
    "Connect": "./pages/auth/connect.py",
    "Change Router Name": "./pages/change_name_router.py",
    "Setting IP Address": "./pages/ip_address.py",
    "Setting Gateway": "./pages/gateway.py",
    "Setting DNS": "./pages/dns_server.py",
    "Setting NAT": "./pages/nat.py",
    "Backup Configuration": "./pages/backup.py",
    "Help": "./pages/help.py"
}

with st.sidebar:
    st.title("MikroManager")
    
    st.header("Connection Status")
    if st.session_state['ssh_client']:
        st.success("SSH Connected")
    else:
        st.warning("SSH Not Connected. Please go to 'Connect' and authenticate.")
    
    with st.expander("🔗 Connect", expanded=True):
        if st.button("Go to Connection Page"):
            st.session_state['current_page'] = "Connect"

    with st.expander("⚙️ Configuration", expanded=False):
        if st.button("Change Router Name"):
            st.session_state['current_page'] = "Change Router Name"
        if st.button("Setting IP Address"):
            st.session_state['current_page'] = "Setting IP Address"
        if st.button("Setting Gateway"):
            st.session_state['current_page'] = "Setting Gateway"
        if st.button("Setting DNS"):
            st.session_state['current_page'] = "Setting DNS"
        if st.button("Setting NAT"):
            st.session_state['current_page'] = "Setting NAT"
        if st.button("Backup Configuration"):
            st.session_state['current_page'] = "Backup Configuration"

    with st.expander("❓ Help", expanded=False):
        if st.button("Help Page"):
            st.session_state['current_page'] = "Help"

if 'current_page' in st.session_state and st.session_state['current_page'] in pages:
    file_path = pages[st.session_state['current_page']]
    
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            exec(file.read())
    else:
        st.error(f"File not found: {file_path}")
        
else:
    st.header("Welcome to MikroManager!\nPlease connect your router first.")