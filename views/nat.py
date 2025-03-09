import streamlit as st
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def loading(timer, message):
    with st.spinner("wait"):  
        time.sleep(timer)
        st.write(f"Running Command: `{message}`")

def rerun_after(timer):
    time.sleep(timer)
    st.rerun()

def get_interface(client):
    get_interface_command = "/interface print terse"
    _, output, _ = execute_command(client, get_interface_command)
    
    interfaces = []
    for line in output.split("\n"):
        parts = line.split()
        if len(parts) >= 3:
            interfaces.append(parts[2].replace("name=", ""))
            
    if not output.strip():
        st.warning("No sharing rules found")
        return

    return interfaces
            
def enable_internet_sharing(client):
    st.subheader("Enable Internet Sharing")
    
    interfaces = get_interface(client)
    
    if not interfaces:
        st.warning("Interfaces not found")
        return
    
    selected_interface = st.selectbox("Choose Connection Source:", interfaces)
    if st.button("Enable Internet Sharing"):
        try:
            connect_internet_command = f"/ip firewall nat add chain=srcnat out-interface={selected_interface} action=masquerade"
            _, _, error = execute_command(client, connect_internet_command)
            
            if error:
                st.error(f"Error: {error}")
            else:
                loading(1, "Enabling Internet Sharing...")
                st.success(f"Internet sharing enabled via {selected_interface}.")
                rerun_after(4.5)
                
        except Exception as e:
            st.error(f"Failed: {e}")    

def reset_rules(client):
    st.subheader("Remove Sharing Settings")
    if st.button("Stop Internet Sharing"):
        try:
            remove_nat_command = "/ip firewall nat remove [find]"
            _, _, error = execute_command(client, remove_nat_command)
            
            if error:
                st.error(f"Error: {error}")
            else:
                loading(1, "Removing all rules...")
                st.success("All rules have been removed.")
                rerun_after(5)
                
        except Exception as e:
            st.error(f"Failed: {e}")

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first.")
else:
    st.header("Internet Sharing Settings")
    tab1, tab2 = st.tabs(["Connect Devices to Internet", "Remove Sharing Settings"])
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("Unable to connect to the router. Please reconnect.")
            st.stop()
        else:
            with tab1:
                enable_internet_sharing(client)
            with tab2:
                reset_rules(client)
                
    except Exception as e:
        st.error(f"Failed: {e}")