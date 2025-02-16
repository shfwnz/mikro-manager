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

## ❓ Need More Help?
If you have further questions, please contact your network administrator or check the official MikroTik documentation.

🔙 [Back to IP Configuration](./main.py)
""")
