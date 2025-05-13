# # File: models/router.py

# from models.device import Device
# from network.interface import Interface


# class Router(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.interfaces = []  # list of Interface objects
#         self.arp_table = {}   # IP -> MAC
#         self.routing_table = {}  # Static and dynamic entries
#         print(f"[INIT] Router {self.name} initialized")

#     def add_interface(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         iface.name = f"eth{len(self.interfaces)}"
#         iface.port = len(self.interfaces) + 1
#         self.interfaces.append(iface)
#         print(f"[CONFIG] Added interface {iface.name} to Router {self.name}: {ip} / {mac}")
#         return iface  # ✅ Return the interface

#     def show_interfaces(self):
#         print(f"\n[INTERFACES] Router {self.name}")
#         for iface in self.interfaces:
#             print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Router {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")

#     def receive_arp_request(self, incoming_iface, target_ip):
#         for iface in self.interfaces:
#             if target_ip == iface.ip:
#                 print(f"[Router {self.name}] ARP request matched on {iface.name} ({target_ip})")

#                 # ✅ Learn the sender (incoming interface's device IP+MAC)
#                 sender_ip = incoming_iface.ip
#                 sender_mac = incoming_iface.mac
#                 self.arp_table[sender_ip] = sender_mac
#                 print(f"[Router {self.name}] Learned ARP: {sender_ip} → {sender_mac}")

#                 # ✅ Send ARP reply to requestor
#                 incoming_iface.device.receive_arp_reply(
#                     iface.ip, iface.mac, iface
#                 )
#                 print(f"[Router {self.name}] ARP reply: {iface.ip} is at {iface.mac}")
#                 return

#         print(f"[Router {self.name}] ARP request not matched on any interface for {target_ip}")

#     def receive_arp_reply(self, sender_ip, sender_mac, _):
#         print(f"[Router {self.name}] ARP reply: {sender_ip} is at {sender_mac}")
#         self.arp_table[sender_ip] = sender_mac


# File: models/router.py

# from models.device import Device
# from network.interface import Interface

# class Router(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.interfaces = []
#         self.arp_table = {}

#     def add_interface(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         iface.name = f"eth{len(self.interfaces)}"
#         self.interfaces.append(iface)
#         print(f"[CONFIG] Added interface {iface.name} to Router {self.name}: {ip} / {mac}")
#         return iface

#     def receive_arp_request(self, incoming_iface, target_ip):
#         for iface in self.interfaces:
#             if iface.ip == target_ip:
#                 sender_ip = incoming_iface.ip
#                 sender_mac = incoming_iface.mac
#                 self.arp_table[sender_ip] = sender_mac
#                 print(f"[Router {self.name}] ARP request matched on {iface.name} ({iface.ip})")
#                 print(f"[Router {self.name}] Learned ARP: {sender_ip} → {sender_mac}")
#                 incoming_iface.device.receive_arp_reply(iface.ip, iface.mac, self)
#                 print(f"[Router {self.name}] ARP reply: {iface.ip} is at {iface.mac}")
#                 return
#         print(f"[Router {self.name}] ARP request for {target_ip} not matched")

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Router {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")


#File: models/router.py

from models.device import Device
from network.interface import Interface

class Router(Device):
    def __init__(self, name):
        super().__init__(name)
        self.interfaces = []
        self.arp_table = {}
        self.routing_table = {}
        print(f"[INIT] Router {self.name} initialized")

    def add_interface(self, ip, mac):
        iface = Interface(ip, mac, self)
        iface.name = f"eth{len(self.interfaces)}"
        self.interfaces.append(iface)
        print(f"[CONFIG] Added interface {iface.name} to Router {self.name}: {ip} / {mac}")
        return iface

    def receive_arp_request(self, incoming_iface, target_ip):
        for iface in self.interfaces:
            if iface.ip == target_ip:
                print(f"[Router {self.name}] ARP request matched on {iface.name} ({iface.ip})")
                self.arp_table[target_ip] = iface.mac
                print(f"[Router {self.name}] Learned ARP: {target_ip} → {iface.mac}")
                incoming_iface.device.receive_arp_reply(target_ip, iface.mac, incoming_iface)
                print(f"[Router {self.name}] ARP reply: {target_ip} is at {iface.mac}")
                return
        print(f"[Router {self.name}] ARP request for {target_ip} not matched")

    def show_arp_table(self):
        print(f"\n[ARP TABLE] Router {self.name}")
        if not self.arp_table:
            print("(empty)")
        for ip, mac in self.arp_table.items():
            print(f"{ip} → {mac}")

    def show_interfaces(self):
        print(f"\n[INTERFACES] Router {self.name}")
        if not self.interfaces:
            print("(no interfaces)")
        for iface in self.interfaces:
            print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")




