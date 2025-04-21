import streamlit as st
import paramiko as pmk
import time

#Check connection
if 'ssh_connection' not in st.session_state:
    st.session_state['ssh_connection'] = False
if 'ssh_client' not in st.session_state:
    st.session_state['ssh_client'] = None

st.title("Connect router using SSH")

col1, col2 = st.columns(2)
with col1:
    hostname = st.text_input("Input IP Address")
    username = st.text_input("Input Username")
with col2:
    port = st.text_input("Input Port", value="22")
    password = st.text_input("Input Password", type="password")

def connect_to_ssh(hostname, port, username, password):
    try:
        client = pmk.SSHClient()
        client.set_missing_host_key_policy(pmk.AutoAddPolicy())

        client.connect(
            hostname,
            port=int(port),
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False
        )

        st.session_state['ssh_client'] = client
        st.session_state['ssh_connection'] = True
        st.success("Connected successfully!")

        st.rerun()

    except pmk.AuthenticationException:
        st.error("Authentication failed. Please check your username and password.")
        st.session_state['ssh_connection'] = False
    except pmk.SSHException as e:
        st.error(f"SSH connection failed: {e}")
        st.session_state['ssh_connection'] = False
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state['ssh_connection'] = False

if st.button("Connect"):
    if hostname and port and username and password:
        st.write(f"Executing: `Connecting to SSH`")
        time.sleep(0.5)
        connect_to_ssh(hostname, port, username, password)
    else:
        st.warning("Please fill in all fields.")
