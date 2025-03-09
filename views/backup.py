import streamlit as st
import time
import os
import datetime

def create_backup(client, backup_name):
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_fullname = f"{backup_name}_{timestamp}"
        command = f"/system backup save name={backup_fullname}"
        
        stdin, stdout, stderr = client.exec_command(command)
        time.sleep(4)
        error = stderr.read().decode()
        
        if error:
            st.error(f"Error: {error}")
        else:
            st.success(f"Backup Success: {backup_fullname}.backup")
            return backup_fullname
    except Exception as e:
        st.error(f"Backup Filed: {e}")
        return None

def download_backup(client, backup):
    try:
        with client.open_sftp() as sftp:
            remote_path = f"/{backup}.backup"
            local_path = os.path.join("backup", f"{backup}.backup")
            os.makedirs("backup", exist_ok=True)
            sftp.get(remote_path, local_path)
        st.success(f"Backup downloaded to: {local_path}")
        return local_path
    except FileNotFoundError:
        st.error(f"Backup file not found on MikroTik: {remote_path}")
        return None
    except Exception as e:
        st.error(f"Failed to download: {e}")
        return None

def upload_file(client, file, filename):
    try:
        with client.open_sftp() as sftp:
            remote_path = f"/{filename}"
            sftp.put(file, remote_path)
        st.success(f"File {filename} successfully uploaded to MikroTik.")
        return remote_path
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None

def list_backup_files(client):
    try:
        with client.open_sftp() as sftp:
            files = sftp.listdir("/")
            backup_files = [file for file in files if file.endswith('.backup')]
            return backup_files
    except Exception as e:
        st.error(f"Failed to get the list of backup files: {e}")
        return []

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the router first.")
else:
    st.header("Create and Download Backup")
    client = st.session_state.get('ssh_client', None)
    if client is None:
        st.error("SSH client is not available. Please reconnect.")
    else:
        backup_name = st.text_input("Backup name", "backup-configuration")
        if st.button("Create Backup"):
            with st.spinner("Creating Backup..."):
                backup_filename = create_backup(client, backup_name)
                if backup_filename:
                    local_file = download_backup(client, backup_filename)
                    if local_file:
                        with open(local_file, "rb") as file:
                            st.download_button(
                                label="Download Backup",
                                data=file,
                                file_name=f"{backup_filename}.backup",
                                mime="application/octet-stream"
                            )
    
    st.header("Upload Backup File to MikroTik")
    
    # Inisialisasi state untuk proses upload
    if 'uploaded_file_path' not in st.session_state:
        st.session_state.uploaded_file_path = None
    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None
    
    uploaded_file = st.file_uploader("Select backup file", type=["backup"])
    
    if uploaded_file is not None:
        save_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.uploaded_file_path = save_path
        st.session_state.uploaded_filename = uploaded_file.name
        st.success(f"File {uploaded_file.name} ready to upload.")
    
    if st.button("Upload to MikroTik") and st.session_state.uploaded_file_path:
        client = st.session_state.get('ssh_client', None)
        if client is None:
            st.error("SSH client is not available. Please reconnect.")
        else:
            remote_path = upload_file(client, st.session_state.uploaded_file_path, st.session_state.uploaded_filename)
            if remote_path:
                st.success(f"The backup file is successfully uploaded to the MikroTik and is available at the path: {remote_path}")
    
    st.header("List of Backup Files on MikroTik")
    client = st.session_state.get('ssh_client', None)
    if client is None:
        st.error("SSH client is not available. Please reconnect.")
    else:
        backup_files = list_backup_files(client)
        if backup_files:
            st.table({"Backup file name": backup_files})
        else:
            st.warning("No backup files were found on the MikroTik.")

    st.header("Restore Backup Tutorial")
    st.markdown("""
    **To restore a backup, follow these steps:**
    
    1. Contact your network administrator to perform the restore.
    2. If you have access to the MikroTik, run the following command through the terminal:
       ```
       /system backup load name=<file_backup name>
       ```
       
    ⚠️ *Important: Restoring will restore the previous configuration and may cause a restart of the router.*
    """)