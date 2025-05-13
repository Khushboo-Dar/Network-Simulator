# # File: network/interface.py

# class Interface:
#     def __init__(self, ip, mac, device=None):
#         """
#         Represents a network interface.

#         Args:
#             ip (str): IPv4 address.
#             mac (str): MAC address (hex-style string or dot notation).
#             device (Device): The device (Host, Router, Switch) this interface is attached to.
#         """
#         self.ip = ip
#         self.mac = mac
#         self.device = device      # Reference to parent device
#         self.name = None          # ethX, port label, etc.
#         self.port = None          # For Switch/Router physical port index
#         self.connections = []     # Interfaces this one is physically linked to

#     def connect_to(self, other_iface):
#         """
#         Bi-directionally connects this interface to another interface.
#         """
#         self.connections.append(other_iface)
#         other_iface.connections.append(self)
#         print(f"[LINK] {self} connected to {other_iface}")

#     def __repr__(self):
#         return f"<Interface {self.name or '?'} | IP={self.ip}, MAC={self.mac}>"



# File: network/interface.py

# class Interface:
#     def __init__(self, ip, mac, device=None):
#         self.ip = ip
#         self.mac = mac
#         self.device = device
#         self.name = None
#         self.port = None
#         self.connections = []

#     def connect_to(self, other_iface):
#         self.connections.append(other_iface)
#         other_iface.connections.append(self)

#     def __repr__(self):
#         return f"<Interface {self.name or ''} | IP={self.ip}, MAC={self.mac}>"

class Interface:
    def __init__(self, ip, mac, device=None):
        self.ip = ip
        self.mac = mac
        self.device = device   # Parent Device (Router, Host, Switch)
        self.name = None       # Name like eth0, eth1 (assigned by router/host)
        self.port = None       # Used when attached to switch
        self.connections = []  # Physical links (bi-directional)

    def connect_to(self, other_iface):
        if other_iface not in self.connections:
            self.connections.append(other_iface)
            other_iface.connections.append(self)
            print(f"[LINK] {self} ↔ {other_iface}")

    def get_connected_device(self):
        """Returns the device connected to this interface (if any)"""
        for conn in self.connections:
            if conn.device != self.device:
                return conn.device
        return None

    def __repr__(self):
        label = f"{self.name or 'iface'}"
        return f"<Interface {label} | IP={self.ip}, MAC={self.mac}>"
