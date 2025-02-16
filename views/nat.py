import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first.")
else:
    st.header("NAT Configuration")
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("SSH client is not available. Please reconnect.")
            st.stop()
        else:
            get_interface = "/interface print terse"
            stdin, stdout, stderr = client.exec_command(get_interface)
            output = stdout.read().decode().strip()
            
            interfaces = []
            for line in output.split("\n"):
                parts = line.split()
                if len(parts) >= 3:
                    interfaces.append(parts[2].replace("name=", ""))
            
            st.subheader("Enable Internet Sharing")
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
                except Exception as e:
                    st.error(f"Failed: {e}")

            st.subheader("Port Forwarding")
            st.write("Allow external access to a local device (e.g., web server, CCTV, or game server).")
            
            public_port = st.text_input("Public Port (External):", placeholder="8080")
            local_ip = st.text_input("Local Device IP:", placeholder="192.168.1.100")
            local_port = st.text_input("Local Port (Internal):", placeholder="80")

            if st.button("Apply Port Forwarding"):
                try:
                    port_forwarding = f"/ip firewall nat add chain=dstnat dst-port={public_port} protocol=tcp action=dst-nat to-addresses={local_ip} to-ports={local_port}"
                    stdin, stdout, stderr = client.exec_command(port_forwarding)
                    stdout.channel.recv_exit_status()
                    error = stderr.read().decode().strip()

                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.success(f"Port Forwarding applied: {public_port} → {local_ip}:{local_port}")
                except Exception as e:
                    st.error(f"Failed: {e}")

            # st.subheader("View Active NAT Rules")
            # if st.button("Show NAT Rules"):
            #     with st.spinner("Fetching NAT rules..."):
            #         try:
            #             get_nat_rules = "/ip firewall nat print"
            #             stdin, stdout, stderr = client.exec_command(get_nat_rules)
            #             stdout.channel.recv_exit_status()
            #             output = stdout.read().decode().strip()
            #             error = stderr.read().decode().strip()

            #             if error:
            #                 st.error(f"Error: {error}")
            #             else:
            #                 if output:
            #                     with st.expander("NAT Rules (Click to expand)", expanded=True):
            #                         st.code(output, language="bash")
            #                 else:
            #                     st.warning("No NAT rules configured.")

            #         except Exception as e:
            #             st.error(f"Failed: {e}")

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
                except Exception as e:
                    st.error(f"Failed: {e}")

    except Exception as e:
        st.error(f"Failed: {e}")
