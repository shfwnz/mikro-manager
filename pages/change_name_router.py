import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Change Router Name")
    new_name = st.text_input("New Router Name", "Mikrotik-NeW")
    if st.button("Change Name"):
        with st.spinner("Changing Name..."):
            try:
                client = st.session_state.get('ssh_client', None)
                if client is None:
                    st.error("SSH client is not available. Please reconnect.")
                else:
                    command = f"/system identity set name={new_name}"
                    stdin, stdout, stderr = client.exec_command(command)
                        
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                        
                    if output:
                        st.success(f"New Router name applied: {new_name}")
                    if error:
                        st.error(f"Error: {error}")
            except Exception as e:
                    st.error(f"Failed to change router name: {e}")
