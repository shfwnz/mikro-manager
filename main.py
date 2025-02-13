import streamlit as st

if 'ssh_connection' not in st.session_state:
    st.session_state['ssh_connection'] = None 
if 'ssh_client' not in st.session_state:
    st.session_state['ssh_client'] = None

pages = {
    "Connect": [
        st.Page("./pages/auth/connect.py", title="Connection")
    ],
    "Config": [
        st.Page("./pages/change_name_router.py", title="Change Router Name"),
        st.Page("./pages/ip_address.py", title="Setting IP Address"),
        st.Page("./pages/backup.py", title="Backup Configuration")
    ]
}

pg = st.navigation(pages)
pg.run()

with st.sidebar:
    st.header("Connection Status")

    if st.session_state['ssh_client']:
        st.success("SSH Connected")
    else:
        st.warning("SSH Not Connected. Please go to 'Connect' and authenticate.")
