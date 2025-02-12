import streamlit as st
import paramiko
from datetime import datetime

if 'ssh_connection' not in st.session_state:
    st.session_state.ssh_connection = None
if 'connected' not in st.session_state:
    st.session_state.connected = False
if 'router_identity' not in st.session_state:
    st.session_state.router_identity = "Tidak Terhubung"

def get_router_identity():
    if st.session_state.connected:
        try:
            stdin, stdout, stderr = st.session_state.ssh_connection.exec_command("/system identity print")
            output = stdout.read().decode().strip()
            if output:
                identity_line = output.split("\n")[0]
                identity = identity_line.split(":")[-1].strip()
                return identity
        except Exception as e:
            st.error(f"Gagal mendapatkan identitas router: {str(e)}")
    return "Tidak Terhubung"

# Judul Aplikasi
st.title("MikroManager - Tool Konfigurasi Mikrotik")
st.write("Aplikasi sederhana untuk mengatur router MikroTik Anda")

# Sidebar
with st.sidebar:
    st.header("Router Identity")
    st.write(f"🔹 **{st.session_state.router_identity}**")  # Menampilkan identitas router

    st.header("Menu")
    menu = st.radio(
        "Pilih Menu:",
        ["Koneksi Router", "Ganti Nama Router", "Konfigurasi Dasar", "Backup"]
    )

# Halaman berdasarkan menu yang dipilih
if menu == "Koneksi Router":
    st.header("Koneksi ke Router")
    ip = st.text_input("IP Router", "192.168.88.1")
    username = st.text_input("Username", "admin")
    password = st.text_input("Password", type="password")

    if st.button("Hubungkan"):
        try:
            # Membuat koneksi SSH baru
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(ip, username=username, password=password)
            st.session_state.ssh_connection = ssh_client
            st.session_state.connected = True

            # Perbarui Identity Router
            st.session_state.router_identity = get_router_identity()
            st.success(f"Berhasil terhubung ke router: {st.session_state.router_identity}")

        except Exception as e:
            st.error(f"Gagal koneksi: {str(e)}")
            st.session_state.connected = False

elif menu == "Ganti Nama Router":
    if not st.session_state.connected:
        st.warning("Silakan hubungkan ke router terlebih dahulu!")
    else:
        st.header("Ganti Nama Router")
        nama_baru = st.text_input("Nama Router Baru", "MikroTik-Baru")
        if st.button("Ganti Nama"):
            with st.spinner("Sedang mengganti nama..."):
                # Menjalankan perintah untuk mengganti nama router
                command = f"/system identity set name={nama_baru}"
                stdin, stdout, stderr = st.session_state.ssh_connection.exec_command(command)
                
                # Perbarui Identity Router setelah perubahan
                st.session_state.router_identity = nama_baru
                st.success(f"Nama router berhasil diganti menjadi: {nama_baru}")

elif menu == "Konfigurasi Dasar":
    if not st.session_state.connected:
        st.warning("Silakan hubungkan ke router terlebih dahulu!")
    else:
        st.header("Konfigurasi Dasar")
        ip_wan = st.text_input("Ether 1", "192.168.1.2/24")
        ip_lan = st.text_input("Ether 2", "192.168.88.1/24")
        dns = st.text_input("DNS Server", "8.8.8.8,8.8.4.4")
        # default_gateway = st.text_input("Default Gateway", "192.168.1.1")

        if st.button("Terapkan Konfigurasi"):
            with st.spinner("Sedang mengatur konfigurasi..."):
                commands = [
                    # f"/ip address add address={ip_wan} interface=ether1",
                    f"/ip address add address={ip_lan} interface=ether2",
                    f"/ip dns set servers={dns}",
                    # f"/ip route add gateway={default_gateway}",
                    "/ip firewall nat add chain=srcnat out-interface=ether1 action=masquerade"
                ]
                # Eksekusi setiap perintah
                for cmd in commands:
                    st.session_state.ssh_connection.exec_command(cmd)
                st.success("Konfigurasi berhasil diterapkan!")

elif menu == "Backup":
    if not st.session_state.connected:
        st.warning("Silakan hubungkan ke router terlebih dahulu!")
    else:
        st.header("Backup Konfigurasi")
        if st.button("Buat Backup"):
            with st.spinner("Sedang membuat backup..."):
                waktu = datetime.now().strftime("%Y%m%d_%H%M%S")
                nama_backup = f"backup_{waktu}"
                command = f"/system backup save name={nama_backup}"
                st.session_state.ssh_connection.exec_command(command)
                st.success("Backup berhasil dibuat!")

# Status koneksi di sidebar
st.sidebar.markdown("---")
if st.session_state.connected:
    st.sidebar.success("Status: Terhubung")
    if st.sidebar.button("Putus Koneksi"):
        st.session_state.ssh_connection.close()
        st.session_state.connected = False
        st.session_state.router_identity = "Tidak Terhubung"
        st.experimental_rerun()
else:
    st.sidebar.error("Status: Tidak Terhubung")
