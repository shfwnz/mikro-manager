import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting NAT")
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None:
            st.error("SSH client is not available. Please reconnect.")
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
            selected_chain = st.selectbox("Select Chain:", ("dstnat", "input", "output","srcnat"), index=3)
            selected_interface = st.selectbox("Select Interface:", interfaces, index=0)
            selected_action = st.selectbox("Select Action:", ("masquerade"))
            
            if st.button("Apply Configuration"):
                try:
                    set_firewall_command = f"/ip firewall nat add chain={selected_chain} out-interface={selected_interface} action={selected_action}"
                    
                    stdin, stdout, stderr = client.exec_command(set_firewall_command)
                    
                    stdout.channel.recv_exit_status()
                    output = stdout.read().decode().strip()
                    error = stderr.read().decode().strip()
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"NAT Configuration Applied")
                except Exception as e:
                    st.error(f"Failed: {e}")
    except Exception as e:
        st.error(f"Failed to change router name: {e}")