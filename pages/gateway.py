import streamlit as st
import re

# Check if SSH connection is established
if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Gateway Configuration")

    try:
        client = st.session_state.get('ssh_client', None)
        if client is None:
            st.error("SSH client is not available. Please reconnect")
        else:
            # 🔍 1. Get list of interfaces
            get_interface = "/interface print terse"
            stdin, stdout, stderr = client.exec_command(get_interface)
            output = stdout.read().decode().strip()
            stderr_output = stderr.read().decode().strip()

            if stderr_output:
                st.error(f"Error fetching interfaces: {stderr_output}")
                st.stop()

            interfaces = []
            for line in output.split("\n"):
                match = re.search(r'name=(\S+)', line)
                if match:
                    interfaces.append(match.group(1))

            if not interfaces:
                st.error("No interfaces found on the router.")
                st.stop()

            selected_interface = st.selectbox("Select Interface:", interfaces)

            # 🔍 2. Get list of IPs on the selected interface
            get_ip = f"/ip address print where interface={selected_interface}"
            stdin, stdout, stderr = client.exec_command(get_ip)
            ip_output = stdout.read().decode().strip()
            stderr_output = stderr.read().decode().strip()

            if stderr_output:
                st.error(f"Error fetching IP addresses: {stderr_output}")
                st.stop()

            ip_list = []
            for line in ip_output.split("\n"):
                match = re.search(r'(\d+\.\d+\.\d+\.\d+/\d+)', line)
                if match:
                    ip_list.append(match.group(1))

            # 🔍 3. Get current gateway
            get_gateway = "/ip route print where dst-address=0.0.0.0/0"
            stdin, stdout, stderr = client.exec_command(get_gateway)
            gateway_output = stdout.read().decode().strip()
            stderr_output = stderr.read().decode().strip()

            if stderr_output:
                st.error(f"Error fetching gateways: {stderr_output}")
                st.stop()

            current_gateway = None
            match = re.search(r'gateway=(\d+\.\d+\.\d+\.\d+)', gateway_output)
            if match:
                current_gateway = match.group(1)

            # 📌 4. Display IP & Gateway info
            st.write(f"Current IPs on {selected_interface}:")
            st.table(ip_list if ip_list else ["No IP addresses found"])

            st.write(f"Current Gateway: {current_gateway if current_gateway else 'None'}")

            # 📌 5. Input for new gateway
            new_gateway = st.text_input("New Gateway:", "192.168.88.1")
            replace_old = st.checkbox("Replace existing gateway", False)

            # 📌 6. "Set Gateway" button
            if st.button("Set Gateway"):
                try:
                    # Remove old gateway if selected
                    if replace_old and current_gateway:
                        remove_command = f"/ip route remove [find gateway={current_gateway}]"
                        stdin, stdout, stderr = client.exec_command(remove_command)
                        stderr_output = stderr.read().decode().strip()
                        if stderr_output:
                            st.error(f"Error removing old gateway: {stderr_output}")
                        else:
                            st.warning(f"Removed old gateway: {current_gateway}")

                    # Add new gateway
                    add_gateway_command = f"/ip route add dst-address=0.0.0.0/0 gateway={new_gateway}"
                    stdin, stdout, stderr = client.exec_command(add_gateway_command)
                    stderr_output = stderr.read().decode().strip()
                    if stderr_output:
                        st.error(f"Error adding gateway: {stderr_output}")
                    else:
                        st.success(f"Gateway {new_gateway} applied successfully!")

                except Exception as e:
                    st.error(f"Failed: {e}")

    except Exception as e:
        st.error(f"Failed: {e}")
