# File: models/device_host.py

from models.device import Device
from network.interface import Interface

class Host(Device):
    def __init__(self, name):
        super().__init__(name)
        self.arp_table = {}

    def configure_interface(self, ip, mac):
        self.interface = Interface(ip, mac, self)
        print(f"[INFO] Host {self.name} interface set to IP: {ip}, MAC: {mac}")

    def send_arp_request(self, target_ip, switch):
        print(f"[Host {self.name}] Broadcasting ARP request: Who has {target_ip}?")
        switch.receive_arp_request(self.interface, target_ip)

    def receive_arp_request(self, incoming_iface, target_ip):
        if self.interface.ip == target_ip:
            print(f"[Host {self.name}] ARP request matches IP {target_ip}, sending reply.")
            incoming_iface.device.receive_arp_reply(self.interface.ip, self.interface.mac, self.interface)
        else:
            print(f"[Host {self.name}] ARP request not for me.")

    def receive_arp_reply(self, ip, mac, _):
        print(f"[Host {self.name}] Received ARP reply: {ip} is at {mac}")
        self.arp_table[ip] = mac
