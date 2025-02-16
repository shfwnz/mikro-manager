import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting DNS")

    dns_options = {
        "Google DNS": "8.8.8.8,8.8.4.4",
        "Cloudflare": "1.1.1.1,1.0.0.1",
        "OpenDNS": "208.67.222.222,208.67.220.220"
    }

    selected_server = st.selectbox("Server:", list(dns_options.keys()))
    allow_remote_request = st.checkbox("allow remote request", True)
    # st.markdown("[What is Allow Remote Request?](./pages/help.py)")

    if st.button("Apply Configuration"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None or client.get_transport() is None or not client.get_transport().is_active():
                st.error("SSH client is not available. Please reconnect.")
            else:
                dns_servers = dns_options[selected_server]
                command = f"/ip dns set servers={dns_servers} allow-remote-requests={'yes' if allow_remote_request else 'no'}"
                
                stdin, stdout, stderr = client.exec_command(command)
                stdout.channel.recv_exit_status()
                
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()

                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success(f"DNS applied: {selected_server}")
                    if output:
                        st.text(f"Response: {output}")

        except Exception as e:
            st.error(f"Failed to change DNS: {e}")
