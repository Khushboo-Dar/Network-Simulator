# # # # File: models/host.py

# # # from models.device import Device
# # # from network.interface import Interface

# # # class Host(Device):
# # #     def __init__(self, name):
# # #         super().__init__(name)
# # #         self.arp_table = {}
# # #         print(f"[INIT] Host {self.name} initialized")

# # #     def configure_interface(self, ip, mac):
# # #         iface = Interface(ip, mac, self)
# # #         iface.name = "eth0"
# # #         self.interfaces.append(iface)
# # #         print(f"[CONFIG] {self.name} configured with IP: {ip}, MAC: {mac}")

# # #     def show_interfaces(self):
# # #         print(f"\n[INTERFACES] Host {self.name}")
# # #         for iface in self.interfaces:
# # #             print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")


# # # File: models/host.py

# # from models.device import Device
# # from network.interface import Interface

# # class Host(Device):
# #     def __init__(self, name):
# #         super().__init__(name)
# #         self.arp_table = {}

# #     def configure(self, ip, mac):
# #         iface = Interface(ip, mac, self)
# #         self.interfaces.append(iface)
# #         print(f"[INIT] Host {self.name} configured: IP={ip}, MAC={mac}")

# #     def send_arp_request(self, target_ip, switch):
# #         print(f"\n[Host {self.name}] Sending ARP request for {target_ip}")
# #         switch.receive_arp_request(self.interfaces[0], target_ip)

# #     def receive_arp_reply(self, sender_ip, sender_mac, _):
# #         print(f"[Host {self.name}] Received ARP reply: {sender_ip} is at {sender_mac}")
# #         self.arp_table[sender_ip] = sender_mac

# #     def show_arp_table(self):
# #         print(f"\n[ARP TABLE] Host {self.name}")
# #         if not self.arp_table:
# #             print("(empty)")
# #         for ip, mac in self.arp_table.items():
# #             print(f"{ip} → {mac}")


# # File: models/host.py

# from models.device import Device
# from network.interface import Interface

# class Host(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.arp_table = {}

#     def configure_interface(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         self.interfaces.append(iface)
#         print(f"[INIT] Host {self.name} configured: IP={ip}, MAC={mac}")

#     def send_arp_request(self, target_ip, switch):
#         print(f"\n[Host {self.name}] Sending ARP request for {target_ip}")
#         switch.receive_arp_request(self.interfaces[0], target_ip)

#     def receive_arp_reply(self, sender_ip, sender_mac, _):
#         print(f"[Host {self.name}] Received ARP reply: {sender_ip} is at {sender_mac}")
#         self.arp_table[sender_ip] = sender_mac

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Host {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")

# File: models/host.py

from models.device import Device
from network.interface import Interface

class Host(Device):
    def __init__(self, name):
        super().__init__(name)
        self.arp_table = {}

    def configure(self, ip, mac):
        """Alias for backward compatibility with test_arp_resolution"""
        self.configure_interface(ip, mac)

    def configure_interface(self, ip, mac):
        iface = Interface(ip, mac, self)
        self.interfaces.append(iface)
        print(f"[INIT] Host {self.name} configured: IP={ip}, MAC={mac}")

    def send_arp_request(self, target_ip, switch):
        print(f"\n[Host {self.name}] Sending ARP request for {target_ip}")
        switch.receive_arp_request(self.interfaces[0], target_ip)

    def receive_arp_reply(self, sender_ip, sender_mac, _):
        print(f"[Host {self.name}] Received ARP reply: {sender_ip} is at {sender_mac}")
        self.arp_table[sender_ip] = sender_mac

    def show_arp_table(self):
        print(f"\n[ARP TABLE] Host {self.name}")
        if not self.arp_table:
            print("(empty)")
        for ip, mac in self.arp_table.items():
            print(f"{ip} → {mac}")
