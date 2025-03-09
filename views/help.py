import streamlit as st

st.title("Help Page - Network Configuration Guide")

st.markdown("""
## 🔹 What is an Interface?
An interface is a network port on a router used to connect devices to a network.

### **Common Interfaces in MikroTik**
- **ether1 (WAN - Internet)** → Connects to the Internet Service Provider (ISP).
- **ether2 - ether5 (LAN - Local Network)** → Used for devices like computers, switches, or IoT devices.
- **wlan1 (WiFi)** → Wireless connection for laptops, smartphones, and other wireless devices.

📌 **For more details, visit:** [MikroTik Documentation](https://wiki.mikrotik.com/wiki/Main_Page)

---

## 🔹 What is an IP Address?
An IP Address is a unique identifier assigned to each device in a network to allow communication.

### **Examples of IP Addresses**
- **192.168.1.1** → Default IP for many routers.
- **192.168.88.1** → Default IP for MikroTik.

**Types of IP Addresses:**
- **Static IP** → Manually assigned, does not change.
- **Dynamic IP** → Automatically assigned by a DHCP server.

📌 **Learn more:** [IP Address Wiki](https://en.wikipedia.org/wiki/IP_address)

---

## 🔹 What is a Subnet Mask?
A subnet mask defines which portion of an IP address represents the network and which represents the devices.

### **Examples of Subnet Masks & CIDR**
| Subnet Mask   | CIDR | Maximum Devices |
|--------------|------|----------------|
| 255.255.255.0 | /24  | 254 |
| 255.255.0.0   | /16  | 65,534 |
| 255.0.0.0     | /8   | 16,777,214 |

**Functions of a Subnet Mask:**
- **Divides a network into smaller subnetworks.**
- **Defines the number of available devices in a network.**

📌 **Learn more:** [Subnetting Guide](https://www.practicalnetworking.net/stand-alone/subnetting/)

---

## 🔹 What is a Gateway?
A gateway acts as the access point between different networks, typically between a **local network** and the **internet**.

### **Common Gateway Configurations**
- **Default Gateway** → The IP address of the router within a network.
- **Example:** If your IP address is `192.168.1.100`, your gateway is often `192.168.1.1`.

📌 **Learn more:** [Gateway Configuration](https://en.wikipedia.org/wiki/Gateway_(telecommunications))

---

## 🔹 What is DNS Configuration?
The **Domain Name System (DNS)** translates domain names into IP addresses.

### **Common DNS Servers**
| Provider  | Primary DNS | Secondary DNS |
|-----------|------------|--------------|
| Google    | 8.8.8.8    | 8.8.4.4      |
| Cloudflare| 1.1.1.1    | 1.0.0.1      |
| OpenDNS   | 208.67.222.222 | 208.67.220.220 |

**How to Configure DNS on MikroTik?**
1. Open WinBox or MikroManager.
2. Go to **IP** → **DNS**.
3. Enter the preferred DNS server (e.g., `8.8.8.8` for Google).
4. Apply the changes.

📌 **Learn more:** [DNS Configuration](https://wiki.mikrotik.com/wiki/Manual:IP/DNS)

---

## 🔹 What is NAT (Network Address Translation)?
**NAT** allows multiple devices in a local network to share a single public IP address.

### **Types of NAT**
- **Masquerade NAT** → Automatically assigns an external IP for devices in a private network.
- **Static NAT** → Maps a specific private IP to a public IP.

**Example: Configuring NAT on MikroTik**
1. Open WinBox.
2. Go to **IP** → **Firewall** → **NAT**.
3. Add a new rule with:
   - **Chain:** `srcnat`
   - **Out Interface:** `ether1`
   - **Action:** `masquerade`
4. Click **OK** and apply.

📌 **Learn more:** [MikroTik NAT Guide](https://wiki.mikrotik.com/wiki/NAT_Tutorial)

---

## 🔹 How to Backup and Restore Configuration?
Backing up your router settings ensures that you can quickly restore your configuration if needed.

### **How to Create a Backup**
1. Open **MikroManager** or **WinBox**.
2. Go to **System** → **Backup**.
3. Click **Save** to create a backup file.

### **How to Restore a Backup**
1. Open **System** → **Backup**.
2. Click **Restore** and select the backup file.
3. Restart the router.

📌 **Learn more:** [Backup and Restore MikroTik](https://wiki.mikrotik.com/wiki/Manual:Configuration_Management)

---

## ❓ Need More Help?   
If you have further questions, please contact your network administrator or check the official MikroTik documentation.

""")
if st.button("🔙 Back to Main Page"):
    st.switch_page("main.py")