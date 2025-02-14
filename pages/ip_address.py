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
            # Get interfaces
            get_interface = f"/interface print terse"
            stdin, stdout, stderr = client.exec_command(get_interface)
            output = stdout.read().decode().strip()
            
            interfaces = []
            for line in output.split("\n"):
                parts = line.split()
                if len(parts) >= 3:  
                    interfaces.append(parts[2].replace("name=", "")) 
                    
            # Show dropdown
            selected_interface = st.selectbox("Select Interface:", interfaces)
            st.write(f"Selected Interface: {selected_interface}")
            
            # Get IP addresses
            list_ip = f"/ip address print detail"
            stdin, stdout, stderr = client.exec_command(list_ip)
            
            output = stdout.read().decode()
            error = stderr.read().decode()
            
            st.text(f"Your IP Addresses:\n{output}")
            
    except Exception as e:
        st.error(f"Failed: {e}")