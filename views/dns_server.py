import streamlit as st

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting DNS")
    tab1, tab2 = st.tabs(["Server Provider", "Custome Name Server"])

    dns_options = {
        "Google DNS": "8.8.8.8,8.8.4.4",
        "Cloudflare": "1.1.1.1,1.0.0.1",
        "OpenDNS": "208.67.222.222,208.67.220.220",
    }
    
    with tab1:
        select_server = st.selectbox("Server Provider:", list(dns_options.keys()))
        selected_server = dns_options[select_server]
        
    with tab2:
        custom_dns_input = st.text_input("Enter custom name servers (comma-separated)", placeholder="1.1.1.1, 8.8.8.8")
    
    allow_remote_request = st.checkbox("allow remote request", True)
    
    if st.button("Save Settings"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None or client.get_transport() is None or not client.get_transport().is_active():
                st.error("Unable to connect to the router. Please reconnect.")
            else:
                command = f"/ip dns set servers={custom_dns_input} allow-remote-requests={'yes' if allow_remote_request else 'no'}"
                
                _, output, error = execute_command(client, command)

                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success(f"DNS applied: {custom_dns_input}")
                    if output:
                        st.text(f"Response: {output}")

        except Exception as e:
            st.error(f"Failed to change DNS: {e}")
