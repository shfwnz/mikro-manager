import streamlit as st
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def loading(timer, message):
    with st.spinner("Processing..."):  
        time.sleep(timer)
        st.write(f"Executing: `{message}`")

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the router first")
else:
    st.header("Change Router Name")
    new_name = st.text_input("Router Name:", "Mikrotik-New")
    if st.button("Change Name"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None:
                st.error("Unable to connect to the router. Please reconnect.")
            else:
                change_router_name_command = f"/system identity set name={new_name}"
                
                _, _, error = execute_command(client, change_router_name_command)
                    
                if error:
                    st.error(f"Error: {error}")
                else:
                    loading(1, "changing router name...")
                    st.success(f"Router name changed to: `{new_name}`")
                    
                    time.sleep(4)
                    st.rerun()

        except Exception as e:
            st.error(f"Failed to change router name: {e}")
