import streamlit as st

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else:
    st.header("Setting DNS")
    dns_server = st.text_input("Server:", "8.8.8.8, 1.1.1.1")
    allow_remote_request = st.checkbox("allow remote request", True)
    st.markdown("[What is Allow Remote Request?](./pages/help.py)")

    if st.button("Set DNS"):
        try:
            client = st.session_state.get('ssh_client', None)
            if client is None or client.get_transport() is None or not client.get_transport().is_active():
                st.error("SSH client is not available. Please reconnect.")
            else:
                # Gabungkan semua DNS dalam satu perintah
                dns_list = ",".join([dns.strip() for dns in dns_server.split(",")])
                command = f"/ip dns set servers={dns_list} allow-remote-requests={'yes' if allow_remote_request else 'no'}"

                st.write(f"Executing: `{command}`")

                stdin, stdout, stderr = client.exec_command(command)
                stdout.channel.recv_exit_status()
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()

                if error:
                    st.error(f"Error: {error}")
                else:
                    st.success(f"DNS applied: {dns_list}")

        except Exception as e:
            st.error(f"Failed to change DNS: {e}")
