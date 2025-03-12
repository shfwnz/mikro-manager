import streamlit as st
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def loading(timer, message):
    with st.spinner("Processing..."):  
        time.sleep(timer)
        st.write(f"Running Command: `{message}`")

def rerun_after(timer):
    time.sleep(timer)
    st.rerun()

def apply_configuration(client, custom_dns_input, allow_remote_request):
    command = f"/ip dns set servers={custom_dns_input} allow-remote-requests={allow_remote_request}"
    
    loading(1, "Applying DNS settings...")
    _, output, error = execute_command(client, command)

    if error:
        st.error(f"Error: {error}")
    else:
        st.success(f"DNS applied: {custom_dns_input}")
        rerun_after(4.5)
        if output:
            st.text(f"Response: {output}")

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting DNS")
    tab1, tab2 = st.tabs(["Server Provider", "Custom Name Server"])
    
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("Unable to connect to the router. Please reconnect.")
        else:
            dns_options = {
                "Google DNS": "8.8.8.8,8.8.4.4",
                "Cloudflare": "1.1.1.1,1.0.0.1",
                "OpenDNS": "208.67.222.222,208.67.220.220",
            }
            
            with tab1:
                select_server = st.selectbox("Server Provider:", list(dns_options.keys()))
                selected_dns = dns_options[select_server]
            
            if 'custom_dns_input' not in st.session_state:
                st.session_state['custom_dns_input'] = ""
            
            with tab2:
                custom_dns_input = st.text_input(
                    "Enter custom DNS servers (comma-separated):", 
                    placeholder="1.1.1.1,8.8.8.8", 
                    key='custom_dns_input'
                ).strip()
            
            allow_remote_request = st.checkbox("Allow remote request", True)
            
            if st.button("Apply DNS Settings"):
                remote_request_value = 'yes' if allow_remote_request else 'no'
                apply_configuration(client, custom_dns_input if custom_dns_input else selected_dns, remote_request_value)
                
                st.session_state['custom_dns_input'] = ""
                st.rerun()
    
    except Exception as e:
        st.error(f"Failed to change DNS: {e}")
