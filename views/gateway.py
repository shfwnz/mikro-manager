import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first.")
else:
    st.header("Gateway Configuration")

    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("SSH client is not available. Please reconnect.")
            st.stop()
        else:
            # Get interfaces
            get_interface = "/interface print terse"
            stdin, stdout, stderr = client.exec_command(get_interface)
            output = stdout.read().decode().strip()

            interfaces = [line.split("name=")[-1].split()[0] for line in output.split("\n") if "name=" in line]

            if not interfaces:
                st.error("No network interfaces found.")
                st.stop()

            selected_interface = st.selectbox("Select Interface:", interfaces)

            # Input for dst-address and gateway
            add_dstaddress = st.text_input("Enter IP address:", value="0.0.0.0/0", help="Example: 0.0.0.0/0")
            new_gateway = st.text_input("Gateway:", placeholder="Enter gateway", help="Example: 192.168.88.1")

            if st.button("Apply Gateway Configuration"):
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

            # # Show existing gateways
            # if st.button("Show Gateways"):
            #     try:
            #         show_command = "/ip route print"
            #         stdin, stdout, stderr = client.exec_command(show_command)
            #         output = stdout.read().decode().strip()
            #         if output:
            #             st.text_area("Existing Gateways:", value=output, height=300)
            #         else:
            #             st.info("No gateways configured.")
            #     except Exception as e:
            #         st.error(f"Failed to retrieve gateways: {e}")

            # Delete gateway
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

    except Exception as e:
        st.error(f"Unexpected error: {e}")
