import streamlit as st

def subnet_mask_to_cidr(subnet_mask):
    return sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("IP Address Configuration")
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None:
            st.error("SSH client is not available. Please reconnect")
        else:
            if st.button("Show IP"):
                st.subheader("IP Addresses")
                
                stdin, stdout, stderr = client.exec_command("/ip address print")
                output = stdout.read().decode()
                
                col_headers = st.columns([3,2,1.5,1,1])
                with col_headers[0]: st.markdown("**Address**")
                with col_headers[1]: st.markdown("**Network**")
                with col_headers[2]: st.markdown("**Interface**")
                with col_headers[3]: st.markdown("**Status**")
                with col_headers[4]: st.markdown("**Action**")
                
                found_ips = False
                for line in output.split("\n")[2:]:
                    if not line.strip():
                        continue
                        
                    found_ips = True
                    parts = line.split()
                    if len(parts) >= 4:
                        index = parts[0]
                        
                        if len(parts) >= 5 and parts[1] in ['D', 'X', 'I']:
                            status_code = parts[1]
                            address = parts[2]
                            network = parts[3]
                            interface = parts[-1]
                        else:
                            status_code = ""
                            address = parts[1]
                            network = parts[2]
                            interface = parts[-1]
                        
                        status_text = {
                            "": "Active",
                            "D": "Dynamic",
                            "X": "Disabled",
                            "I": "Invalid"
                        }.get(status_code, "Unknown")
                        
                        cols = st.columns([3,2,1.5,1,1])
                        with cols[0]: st.write(address)
                        with cols[1]: st.write(network)
                        with cols[2]: st.write(interface)
                        with cols[3]: st.write(status_text)
                        with cols[4]:
                            if st.button("Delete", key=f"del_{index}", use_container_width=True):
                                client.exec_command(f"/ip address remove numbers={index}")
                                st.success(f"Deleted IP {address}")
                                st.rerun()
                
                if not found_ips:
                    st.info("No IP addresses found")
                                    
            get_interface = f"/interface print terse"
            stdin, stdout, stderr = client.exec_command(get_interface)
            output = stdout.read().decode().strip()
            
            interfaces = []
            for line in output.split("\n"):
                parts = line.split()
                if len(parts) >= 3:
                    interfaces.append(parts[2].replace("name=", "")) 
                    
            selected_interface = st.selectbox("Select Interface:", interfaces, placeholder="choose an interfaces", index=None)
            
            #Disable/Enable Interface
            message_success = ""
            message_error = ""
            
            col1, spacer, col2 = st.columns([1,2.5,1])
            with col1:
                if st.button("Enable Interface"):
                    enable_command = f"/interface enable {selected_interface}"
                    stdin, stdout, stderr = client.exec_command(enable_command)
                    output = stdout.read().decode().strip()
                    error = stderr.read().decode().strip()
                    if error:
                        message_error = f"Unable to enable {selected_interface}: {error}"
                    else:
                        message_success = f"Enabled {selected_interface}"
            with col2:
                if st.button("Disable Interface"):
                    disable_command = f"/interface disable {selected_interface}"
                    stdin, stdout, stderr = client.exec_command(disable_command)
                    output = stdout.read().decode().strip()
                    error = stderr.read().decode().strip()
                    if error:
                        message_error = f"Unable to disable {selected_interface}: {error}"
                    else:
                        message_success = f"Disabled {selected_interface}"
            
            if message_error:
                st.error(message_error)    
            elif message_success:
                st.success(message_success) 
            
            ip_address = st.text_input("IP Address:", placeholder="Enter the IP address of the device", help="Example: 192.168.88.1")
            subnet_mask = st.text_input("Subnet:", placeholder="Enter a subnet mask for the device", help="Example: 255.255.255.0")
            remove_old = st.checkbox("Remove old IP before applying", False)
            
            st.subheader("Apply Configuration")
            if st.button("Apply Configuration"):
                try:
                    cidr = subnet_mask_to_cidr(subnet_mask)
                    ip_with_subnet = f"{ip_address}/{cidr}"
                    
                    if remove_old:
                        remove_command = f"/ip address remove [find interface={selected_interface}]"
                        client.exec_command(remove_command)
                        st.warning(f"Removing old IPs on {selected_interface}...")
                    
                    command = f"/ip address add address={ip_with_subnet} interface={selected_interface}"
                    stdin, stdout, stderr = client.exec_command(command)
                    stdout.channel.recv_exit_status()
                    output = stdout.read().decode().strip()
                    error = stderr.read().decode().strip()
                    
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"New IP {ip_with_subnet} applied to {selected_interface}")
                    
                except Exception as e:
                    st.error(f"Failed to Set IP: {e}")
            
            
    
    except Exception as e:
        st.error(f"Failed: {e}")
