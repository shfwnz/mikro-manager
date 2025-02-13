import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else: 
    st.header("Setting IP Address")
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None:
            st.error("SSH client is not available. Please reconnect")
        else:
            list_ip = f"/ip address print detail"
            stdin, stdout, stderr = client.exec_command(list_ip)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            st.text(f"Your IP Addresses:\n{output}")
            
    except Exception as e:
        st.error(f"Failed: {e}")