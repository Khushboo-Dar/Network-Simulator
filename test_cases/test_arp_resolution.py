# # File: test_cases/test_arp_resolution.py

# from models.router import Router
# from models.switch import Switch
# from models.device import Device
# from network.interface import Interface

# print("\n=== [ARP Resolution Demo: Host A → Router, Host D → Router] ===")

# class Host(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.arp_table = {}

#     def configure(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         self.interfaces.append(iface)
#         print(f"[INIT] Host {self.name} configured: IP={ip}, MAC={mac}")

#     def send_arp_request(self, target_ip, switch):
#         print(f"\n[Host {self.name}] Sending ARP request for {target_ip}")
#         switch.receive_arp_request(self.interfaces[0], target_ip)

#     def receive_arp_request(self, iface, target_ip):
#         if target_ip == iface.ip:
#             print(f"[Host {self.name}] Got ARP request for me ({target_ip}), replying with {iface.mac}")
#             iface.device.interfaces[0].device.receive_arp_reply(iface.ip, iface.mac, iface)
#         else:
#             print(f"[Host {self.name}] Ignored ARP request for {target_ip}")

#     def receive_arp_reply(self, sender_ip, sender_mac, _):
#         print(f"[Host {self.name}] Received ARP reply: {sender_ip} is at {sender_mac}")
#         self.arp_table[sender_ip] = sender_mac

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Host {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")

# # Instantiate hosts
# host_a = Host("A")
# host_a.configure("11.11.11.10", "aaaa")

# host_b = Host("B")
# host_b.configure("11.11.11.20", "bbbb")

# host_c = Host("C")
# host_c.configure("22.22.22.30", "cccc")

# host_d = Host("D")
# host_d.configure("22.22.22.40", "dddd")

# # Router with 2 interfaces
# router = Router("R")
# iface1 = router.add_interface("11.11.11.1", "ee01")  # eth0
# iface2 = router.add_interface("22.22.22.1", "ee02")  # eth1

# # Switches
# swX = Switch("X")
# swY = Switch("Y")

# # Add interfaces to Switch X (Subnet 1)
# swX.add_interface(host_b.interfaces[0]); swX.interfaces[-1].port = 1
# swX.add_interface(host_a.interfaces[0]); swX.interfaces[-1].port = 2
# swX.add_interface(iface1);                swX.interfaces[-1].port = 3

# # Add interfaces to Switch Y (Subnet 2)
# swY.add_interface(iface2);                swY.interfaces[-1].port = 4
# swY.add_interface(host_d.interfaces[0]); swY.interfaces[-1].port = 5
# swY.add_interface(host_c.interfaces[0]); swY.interfaces[-1].port = 6

# # Trigger ARP
# host_a.send_arp_request("11.11.11.1", swX)  # A → R
# host_d.send_arp_request("22.22.22.1", swY)  # D → R

# # Show Tables
# host_a.show_arp_table()
# host_d.show_arp_table()

# router.show_arp_table()
# swX.show_mac_table()
# swY.show_mac_table()


# File: test_cases/test_arp_resolution.py

from models.router import Router
from models.switch import Switch
from models.host import Host
from network.interface import Interface

print("\n=== [ARP Resolution Demo: Host A → Router, Host D → Router] ===")

# Hosts
host_a = Host("A")
host_a.configure("11.11.11.10", "aaaa")

host_b = Host("B")
host_b.configure("11.11.11.20", "bbbb")

host_c = Host("C")
host_c.configure("22.22.22.30", "cccc")

host_d = Host("D")
host_d.configure("22.22.22.40", "dddd")

# Router
router = Router("R")
iface1 = router.add_interface("11.11.11.1", "ee01")
iface2 = router.add_interface("22.22.22.1", "ee02")

# Switches
swX = Switch("X")
swY = Switch("Y")

# Connect interfaces to Switch X
host_b.interfaces[0].port = 1
swX.add_interface(host_b.interfaces[0])

host_a.interfaces[0].port = 2
swX.add_interface(host_a.interfaces[0])

iface1.port = 3
swX.add_interface(iface1)

# Connect interfaces to Switch Y
iface2.port = 4
swY.add_interface(iface2)

host_d.interfaces[0].port = 5
swY.add_interface(host_d.interfaces[0])

host_c.interfaces[0].port = 6
swY.add_interface(host_c.interfaces[0])

# Send ARP requests
host_a.send_arp_request("11.11.11.1", swX)  # A → R
host_d.send_arp_request("22.22.22.1", swY)  # D → R

# Show Tables
host_a.show_arp_table()
host_d.show_arp_table()

router.show_arp_table()
swX.show_mac_table()
swY.show_mac_table()

