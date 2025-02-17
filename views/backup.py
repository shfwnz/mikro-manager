import streamlit as st
import time
import os
import datetime

if 'ssh_connection' not in st.session_state or not st.session_state['ssh_connection']:
    st.warning("Please connect to the Router first")
else: 
    st.header("Backup Configuration")
    backup_name = st.text_input("Backup Name", "backup-configuration")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def download_backup(client, backup):
        sftp = client.open_sftp()
        remote_path = f"{backup}.backup"
        local_path = os.path.join("backup", f"{backup}.backup")
        
        try:
            os.makedirs("backup", exist_ok=True) 
            sftp.get(remote_path, local_path)
            sftp.close()
            st.success(f"Backup downloaded to: {local_path}")
            return local_path
        except FileNotFoundError:
            st.error(f"Backup file not found on MikroTik: {remote_path}")
            return None
        except Exception as e:
            st.error(f"Download failed: {e}")
            return None
    
    if st.button("Create Backup"):
        with st.spinner("Creating Backup..."):
            try:
                client = st.session_state.get('ssh_client', None)
                if client is None:
                    st.error("SSH client is not available. Please reconnect.")
                else:
                    backup_fullname = f"{backup_name}_{timestamp}"
                    command = f"/system backup save name={backup_fullname}"
                    
                    st.write(f"Executing: `{command}`")
                    
                    stdin, stdout, stderr = client.exec_command(command)
                    
                    time.sleep(4)
                    
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                        
                    if output:
                        st.success(f"Backup Created Successfully: {backup_fullname}.backup")

                        stdin, stdout, stderr = client.exec_command("/file print detail")
                        file_list = stdout.read().decode()
                        # st.text(f"File list from MikroTik:\n{file_list}")
                        
                        found_file = False
                        for line in file_list.split("\n"):
                            if backup_fullname in line and ".backup" in line:
                                found_file = True
                                break
                        
                        if found_file:
                            st.info(f"Backup file found on MikroTik: {backup_fullname}.backup")
                            local_file = download_backup(client, backup_fullname)

                            if local_file:
                                with open(local_file, "rb") as file:
                                    st.download_button(
                                        label="Download Backup",
                                        data=file,
                                        file_name=f"{backup_fullname}.backup",
                                        mime="application/octet-stream"
                                    )
                            else:
                                st.error("Failed to download backup file.")
                        else:
                            st.error(f"Backup file not found on MikroTik: {backup_fullname}.backup")
                    if error:
                        st.error(f"Error: {error}")
            except Exception as e:
                st.error(f"Failed: {e}")

    st.header("Upload Configuration")
    uploaded_file = st.file_uploader("Choose a file", type=["backup"])

    def upload_file(client, file, filename):
        sftp = client.open_sftp()
        remote_path = f"/{filename}"
        
        try:
            sftp.put(file, remote_path)
            sftp.close()
            st.success(f"File {filename} successfully uploaded to MikroTik.")
        except Exception as e:
            st.error(f"Upload failed: {e}")

    if uploaded_file is not None:
        save_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"File {uploaded_file.name} ready to upload.")
        
        if st.button("Upload to MikroTik"):
            client = st.session_state.get('ssh_client', None)
            if client is None:
                st.error("SSH client is not available. Please reconnect.")
            else:
                upload_file(client, save_path, uploaded_file.name)
