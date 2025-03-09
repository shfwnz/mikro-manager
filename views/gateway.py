import streamlit as st

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

def apply_configuration(client, add_dstaddress, new_gateway):  
    try:
        add_gateway_command = f"/ip route add dst-address={add_dstaddress} gateway={new_gateway}"
        stdin, stdout, stderr = client.exec_command(add_gateway_command)
        stderr_output = stderr.read().decode().strip()

        if stderr_output:
            st.error(f"Error adding new gateway: {stderr_output}")
        else:
            st.success(f"New gateway `{new_gateway}` applied successfully!")

    except Exception as e:
        st.error(f"Failed: {e}")  
        
def list_gateway(client):
    try:
        get_routes_command = "/ip route print terse"
        stdin, stdout, stderr = client.exec_command(get_routes_command)
        output = stdout.read().decode().strip()

        if not output:
            st.warning("No gateway routes found.")
            return

        routes = []
        for line in output.split("\n"):
            parts = line.split()
            if len(parts) >= 3:  # Pastikan ada cukup data dalam setiap baris
                dst_address = next((p.replace("dst-address=", "") for p in parts if p.startswith("dst-address=")), "Unknown")
                gateway = next((p.replace("gateway=", "") for p in parts if p.startswith("gateway=")), "Unknown")
                routes.append({"Destination": dst_address, "Gateway": gateway})

        if routes:
            st.table(routes)
        else:
            st.warning("No gateway routes found.")

    except Exception as e:
        st.error(f"Failed to list gateways: {e}")

        
def add_gateway(client):
    interfaces = get_interface(client)

    if not interfaces:
        st.error("No network interfaces found.")
        st.stop()

    # selected_interface = st.selectbox("Select Interface:", interfaces)

    add_dstaddress = st.text_input("Enter IP address:", value="0.0.0.0/0", help="Example: 0.0.0.0/0")
    new_gateway = st.text_input("Gateway:", placeholder="Enter gateway", help="Example: 192.168.88.1")
    
    if st.button("Apply Configuration"):
        apply_configuration(client, add_dstaddress, new_gateway)
        
def delete_gateway(client):
    gateway_to_delete = st.text_input("Enter Gateway IP to Delete:", placeholder="e.g., 192.168.88.1")
    if st.button("Delete Gateway"):
        try:
            delete_command = f"/ip route remove [find gateway={gateway_to_delete}]"
            stdin, stdout, stderr = client.exec_command(delete_command)
            stderr_output = stderr.read().decode().strip()

            if stderr_output:
                st.error(f"Error deleting gateway: {stderr_output}")
            else:
                st.success(f"Gateway `{gateway_to_delete}` deleted successfully!")
        except Exception as e:
            st.error(f"Failed to delete gateway: {e}")

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first.")
else:
    st.header("Gateway Configuration")
    tab1, tab2, tab3 = st.tabs(["List Gateway", "Add Gateway", "Delete Gateway"])
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("SSH client is not available. Please reconnect.")
            st.stop()
        else:
            with tab1: 
                list_gateway(client)
            with tab2:
                add_gateway(client)
            with tab3:
                delete_gateway(client)

    except Exception as e:
        st.error(f"Unexpected error: {e}")
