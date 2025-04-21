import streamlit as st
import paramiko as prm
import time

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    return stdout.channel.recv_exit_status(), stdout.read().decode().strip(), stderr.read().decode().strip()

def show(klien):
    st.title("DHCP Server Configuration")

    # Ambil interface dari IP address
    _, output, _ = execute_command(klien, "/ip address print")
    lines = output.strip().split("\n")[2:]  # Lewati header

    interfaces = []
    for line in lines:
        parts = line.split()
        if len(parts) > 1:
            interface_name = parts[-1]
            interfaces.append(interface_name)

    interfaces = sorted(list(set(interfaces)))  # Hapus duplikat dan urutkan

    if not interfaces:
        st.warning("Tidak ada interface yang ditemukan.")
        return

    # Input DHCP
    inter = st.selectbox("Pilih Interface", interfaces)
    range_user = st.number_input("Masukkan Jumlah User", min_value=2, max_value=250)
    st.caption("Maks : 250 User")
    start = st.text_input("Masukkan awal DHCP", "100")
    st.caption("Rekomendasi: Isi awal IP lebih tinggi dari gateway")

    # Ambil IP dan Network dari interface terpilih
    _, out_iface, _ = execute_command(klien, f"/ip address print where interface={inter}")
    iface_lines = out_iface.strip().split("\n")
    
    if len(iface_lines) < 3:
        st.error("Gagal membaca IP dari interface.")
        return

    ip_info_line = iface_lines[2]
    parts = ip_info_line.split()
    try:
        address_for_dhcp = parts[-3].split("/")[0]
        network_for_dhcp = parts[-2]
    except IndexError:
        st.error("Gagal memproses IP dan network.")
        return

    ipad = address_for_dhcp.split(".")
    if len(ipad) != 4:
        st.error("Format IP tidak valid.")
        return

    prefix = f"{ipad[0]}.{ipad[1]}.{ipad[2]}"
    try:
        range_start = f"{prefix}.{int(start)}"
        range_end = f"{prefix}.{int(start) + int(range_user) - 1}"
    except ValueError:
        st.error("Input awal DHCP harus berupa angka.")
        return

    # Tampilkan hasil
    st.write(f"Network : {network_for_dhcp}/24")
    st.write(f"Gateway : {address_for_dhcp}")
    st.write(f"DHCP Range IP : {range_start} - {range_end}")

    if st.button("Buat DHCP Server"):
        command = [
            f"/ip pool add name=dhcp_pool_{address_for_dhcp} ranges={range_start}-{range_end}",
            f"/ip dhcp-server add name=dhcp_server_{address_for_dhcp} interface={inter} lease-time=1d address-pool=dhcp_pool_{address_for_dhcp} disabled=no",
            f"/ip dhcp-server network add address={network_for_dhcp}/24 gateway={address_for_dhcp} dns-server=8.8.8.8,8.8.4.4"
        ]
        for coman in command:
            klien.exec_command(coman)
        
        st.success("Berhasil menambah DHCP Server")
        time.sleep(3)
        st.rerun()
