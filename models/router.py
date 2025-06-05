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

# from models.device import Device
# from network.interface import Interface

# class Router(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.interfaces = []
#         self.arp_table = {}
#         self.routing_table = {}
#         print(f"[INIT] Router {self.name} initialized")

#     def add_interface(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         iface.name = f"eth{len(self.interfaces)}"
#         self.interfaces.append(iface)
#         print(f"[CONFIG] Added interface {iface.name} to Router {self.name}: {ip} / {mac}")
#         return iface

#     def receive_arp_request(self, incoming_iface, target_ip):
#         for iface in self.interfaces:
#             if iface.ip == target_ip:
#                 print(f"[Router {self.name}] ARP request matched on {iface.name} ({iface.ip})")
#                 self.arp_table[target_ip] = iface.mac
#                 print(f"[Router {self.name}] Learned ARP: {target_ip} → {iface.mac}")
#                 incoming_iface.device.receive_arp_reply(target_ip, iface.mac, incoming_iface)
#                 print(f"[Router {self.name}] ARP reply: {target_ip} is at {iface.mac}")
#                 return
#         print(f"[Router {self.name}] ARP request for {target_ip} not matched")

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Router {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")

#     def show_interfaces(self):
#         print(f"\n[INTERFACES] Router {self.name}")
#         if not self.interfaces:
#             print("(no interfaces)")
#         for iface in self.interfaces:
#             print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")




# File: models/router.py

# from models.device import Device
# from network.interface import Interface
# from utils import longest_prefix_match

# class Router(Device):
#     def __init__(self, name):
#         super().__init__(name)
#         self.interfaces = []
#         self.arp_table = {}        # IP → MAC
#         self.routing_table = {}    # CIDR → (next_hop, interface)
#         print(f"[INIT] Router {self.name} initialized")

#     def add_interface(self, ip, mac):
#         iface = Interface(ip, mac, self)
#         iface.name = f"eth{len(self.interfaces)}"
#         self.interfaces.append(iface)
#         print(f"[CONFIG] Added interface {iface.name} to Router {self.name}: {ip} / {mac}")
#         return iface

#     def add_static_route(self, network, next_hop, interface):
#         self.routing_table[network] = (next_hop, interface)
#         nh_text = next_hop or "direct"
#         print(f"[ROUTER {self.name}] Static route added: {network} via {nh_text} → {interface.name} ({interface.ip})")

#     def receive_arp_request(self, incoming_iface, target_ip):
#         for iface in self.interfaces:
#             if iface.ip == target_ip:
#                 print(f"[Router {self.name}] ARP request matched on {iface.name} ({iface.ip})")
#                 self.arp_table[incoming_iface.ip] = incoming_iface.mac
#                 print(f"[Router {self.name}] Learned ARP: {incoming_iface.ip} → {incoming_iface.mac}")
#                 incoming_iface.device.receive_arp_reply(iface.ip, iface.mac, incoming_iface)
#                 print(f"[Router {self.name}] Sent ARP reply to {incoming_iface.device.name}")
#                 return
#         print(f"[Router {self.name}] No matching interface for ARP request to {target_ip}")

#     def receive_packet(self, dst_ip, payload, incoming_iface):
#         print(f"[Router {self.name}] Packet received: dst={dst_ip}, from {incoming_iface.device.name}")
#         match = longest_prefix_match(dst_ip, self.routing_table)
#         if not match:
#             print(f"[Router {self.name}] ❌ No matching route for {dst_ip}")
#             return

#         next_hop, out_iface = match[1]
#         next_hop_ip = next_hop or dst_ip

#         if next_hop_ip not in self.arp_table:
#             print(f"[Router {self.name}] ARP needed for {next_hop_ip}, sending request")
#             # Assume connected switch is calling back with response
#             return

#         dst_mac = self.arp_table[next_hop_ip]
#         print(f"[Router {self.name}] ✅ Forwarding to {dst_ip} via {out_iface.name} (MAC={dst_mac})")
#         for iface in out_iface.connections:
#             if iface.device != self:
#                 iface.device.receive_packet(dst_ip, payload, out_iface)

#     def show_arp_table(self):
#         print(f"\n[ARP TABLE] Router {self.name}")
#         if not self.arp_table:
#             print("(empty)")
#         for ip, mac in self.arp_table.items():
#             print(f"{ip} → {mac}")

#     def show_routing_table(self):
#         print(f"\n[ROUTING TABLE] Router {self.name}")
#         if not self.routing_table:
#             print("(empty)")
#         for network, (nexthop, iface) in self.routing_table.items():
#             nh = nexthop or "direct"
#             print(f"{network} via {nh} → {iface.name} ({iface.ip})")

#     def show_interfaces(self):
#         print(f"\n[INTERFACES] Router {self.name}")
#         if not self.interfaces:
#             print("(no interfaces)")
#         for iface in self.interfaces:
#             print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")
# File: models/router.py

from models.device import Device
from network.interface import Interface
from utils.longest_prefix_match import longest_prefix_match

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

    def add_static_route(self, subnet, next_hop, interface):
        self.routing_table[subnet] = (next_hop, interface)
        print(f"[ROUTER {self.name}] Static route added: {subnet} via {next_hop or 'direct'} → {interface.name} ({interface.ip})")

    def receive_arp_request(self, incoming_iface, target_ip):
        for iface in self.interfaces:
            if iface.ip == target_ip:
                print(f"[Router {self.name}] ARP request matched on {iface.name} ({iface.ip})")
                self.arp_table[incoming_iface.ip] = incoming_iface.mac
                print(f"[Router {self.name}] Learned ARP: {incoming_iface.ip} → {incoming_iface.mac}")
                incoming_iface.device.receive_arp_reply(iface.ip, iface.mac, incoming_iface)
                print(f"[Router {self.name}] Sent ARP reply to {incoming_iface.device.name}")
                return
        print(f"[Router {self.name}] ARP request for {target_ip} not matched")

    def receive_packet(self, dst_ip, payload, incoming_iface):
        print(f"\n[Router {self.name}] Packet received: dst={dst_ip}, src={incoming_iface.ip}")

    # Perform static route lookup
        match = longest_prefix_match(dst_ip, self.routing_table)
        if not match:
          print(f"[Router {self.name}] ❌ No route found for {dst_ip}")
        return

        network, (next_hop, out_iface) = match
        print(f"[Router {self.name}] Matched route {network}: next_hop={next_hop or 'direct'}, out_iface={out_iface.name}")

    # Check ARP resolution
        if dst_ip not in self.arp_table:
            print(f"[Router {self.name}] ARP entry for {dst_ip} not found. Cannot forward packet.")
            return

        dst_mac = self.arp_table[dst_ip]
        print(f"[Router {self.name}] Forwarding to next-hop MAC: {dst_mac}")
        for iface in out_iface.connections:
            iface.device.receive_packet(dst_ip, payload, out_iface)
 

    def show_arp_table(self):
        print(f"\n[ARP TABLE] Router {self.name}")
        if not self.arp_table:
            print("(empty)")
        for ip, mac in self.arp_table.items():
            print(f"{ip} → {mac}")

    def show_routing_table(self):
        print(f"\n[ROUTING TABLE] Router {self.name}")
        if not self.routing_table:
            print("(empty)")
        for subnet, (nexthop, iface) in self.routing_table.items():
            print(f"{subnet} via {nexthop or 'direct'} → {iface.name} ({iface.ip})")

    def show_interfaces(self):
        print(f"\n[INTERFACES] Router {self.name}")
        if not self.interfaces:
            print("(no interfaces)")
        for iface in self.interfaces:
            print(f"- {iface.name}: IP={iface.ip}, MAC={iface.mac}")
