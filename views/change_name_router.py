import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Change Router Name")
    new_name = st.text_input("Router Name:", "Mikrotik-New")
    if st.button("Change Name"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None:
                st.error("SSH client is not available. Please reconnect.")
            else:
                command = f"/system identity set name={new_name}"
                
                # st.write(f"Executing: `{command}`")
                    
                stdin, stdout, stderr = client.exec_command(command)
                
                stdout.channel.recv_exit_status()
                output = stdout.read().decode()
                error = stderr.read().decode()
                    
                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success(f"Router name changed: {new_name}")
        except Exception as e:
                st.error(f"Failed to change router name: {e}")
