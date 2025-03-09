import streamlit as st
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def rerun_after(timer):
    time.sleep(timer)
    st.rerun()

def get_interface(client):
    get_interface = "/interface print terse"
    stdin, stdout, stderr = client.exec_command(get_interface)
    output = stdout.read().decode().strip()
    
    interfaces = []
    for line in output.split("\n"):
        parts = line.split()
        if len(parts) >= 3:
            interfaces.append(parts[2].replace("name=", ""))
            
    return interfaces
            
def enable_internet_sharing(client):
    st.subheader("Enable Internet Sharing")
    
    interfaces = get_interface(client)
    
    if not interfaces:
        st.warning("Interfaces not found")
        return
    
    selected_interface = st.selectbox("Select Interface:", interfaces)
    if st.button("Enable Internet Sharing"):
        try:
            connect_internet = f"/ip firewall nat add chain=srcnat out-interface={selected_interface} action=masquerade"
            stdin, stdout, stderr = client.exec_command(connect_internet)
            stdout.channel.recv_exit_status()
            error = stderr.read().decode().strip()
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.success(f"Internet sharing enabled via {selected_interface}.")
                rerun_after(3)
                
        except Exception as e:
            st.error(f"Failed: {e}")    

def reset_rules(client):
    st.subheader("Reset NAT Rules")
    if st.button("Remove NAT Rules"):
        try:
            remove_nat = "/ip firewall nat remove [find]"
            stdin, stdout, stderr = client.exec_command(remove_nat)
            stdout.channel.recv_exit_status()
            error = stderr.read().decode().strip()
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.success("All NAT rules have been removed.")
                rerun_after(3)
                
        except Exception as e:
            st.error(f"Failed: {e}")

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first.")
else:
    st.header("NAT Configuration")
    tab1, tab2 = st.tabs(["Share Internet", "Reset Rules"])
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("SSH client is not available. Please reconnect.")
            st.stop()
        else:
            with tab1:
                enable_internet_sharing(client)
            with tab2:
                reset_rules(client)
                
    except Exception as e:
        st.error(f"Failed: {e}")