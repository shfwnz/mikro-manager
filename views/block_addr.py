import streamlit as st
import time
import dns.resolver

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

def show_list(client):
    command = "/ip firewall address-list print terse"
    _, output, _ = execute_command(client, command)
    unique_lists = set()
    for line in output.split("\n"):
        if "list=" in line:
            parts = line.split("list=")
            if len(parts) > 1:
                list_name = parts[1].split()[0].strip(",.")
                unique_lists.add(list_name)
    return sorted(unique_lists) if unique_lists else ["No Categories Found"]

def blocking_sites(client, list_name):
    block_command = f"/ip firewall filter add action=drop chain=output dst-address-list={list_name}"
    _, _, error = execute_command(client, block_command)
    if error:
        st.error(f"Error: {error}")
    else:
        st.success(f"Blocking sites in `{list_name}`")

def add_to_list(client, url):
    clean_url = url.replace("https://", "").replace("http://", "").split('/')[0]
    try:
        answers = dns.resolver.resolve(clean_url, 'A')
        list_name = clean_url.split('.')[0]
        for ip in answers:
            ip_address = ip.to_text()  # Convert IP address to string format
            command = f"/ip firewall address-list add list=\"{list_name}\" address=\"{ip_address}\""
            loading(1, command)
            _, output, error = execute_command(client, command)
            if error:
                st.warning(f"Failed to add `{clean_url}` ({ip_address}) to `{list_name}`: {error}")
            else:
                st.success(f"Site `{clean_url}` ({ip_address}) added to `{list_name}`")
        return list_name  # Only return list_name
    except dns.resolver.NXDOMAIN:
        st.warning(f"Failed to resolve `{clean_url}`")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the router first")
else:
    st.header("Blocking Websites")
    try:
        client = st.session_state.get('ssh_client', None)
        if client is None or client.get_transport() is None or not client.get_transport().is_active():
            st.error("Unable to connect to the router. Please reconnect.")
        else:
            st.subheader("Add Site to Block List")
            url = st.text_input("Enter Website to Block", placeholder="facebook.com")
            if st.button("Add & Auto-Categorize"):
                if url:
                    list_name = add_to_list(client, url)
                    if list_name:
                        st.info(f"Category `{list_name}` created or updated.")
                        rerun_after(2)
                else:
                    st.warning("Please enter a valid website URL.")
            lists = show_list(client)
            if lists:
                selected_list = st.selectbox("Select Category to Block", options=lists)
                if st.button("Block Selected Category"):
                    blocking_sites(client, selected_list)
            else:
                st.info("No categories found. Add a site first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
