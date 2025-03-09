import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting DNS")

    dns_options = {
        "Google DNS": "8.8.8.8,8.8.4.4",
        "Cloudflare": "1.1.1.1,1.0.0.1",
        "OpenDNS": "208.67.222.222,208.67.220.220",
        "Other": ""
    }

    selected_server = st.selectbox("Server:", list(dns_options.keys()))
    
    if selected_server == "Other":
        custom_dns = st.text_input("Enter custom DNS servers (comma-separated)")
    else:
        custom_dns = dns_options[selected_server]
    
    allow_remote_request = st.checkbox("allow remote request", True)
    
    if st.button("Apply Configuration"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None or client.get_transport() is None or not client.get_transport().is_active():
                st.error("Unable to connect to the router. Please reconnect.")
            else:
                command = f"/ip dns set servers={custom_dns} allow-remote-requests={'yes' if allow_remote_request else 'no'}"
                
                stdin, stdout, stderr = client.exec_command(command)
                stdout.channel.recv_exit_status()
                
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()

                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success(f"DNS applied: {custom_dns}")
                    if output:
                        st.text(f"Response: {output}")

        except Exception as e:
            st.error(f"Failed to change DNS: {e}")
