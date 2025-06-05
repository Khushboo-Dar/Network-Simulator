# File: models/switch.py

from models.device import Device

class Switch(Device):
    def __init__(self, name):
        super().__init__(name)
        self.mac_table = {}
        print(f"[INIT] Switch {self.name} initialized")

    def add_interface(self, interface):
        self.interfaces.append(interface)
        print(f"[CONFIG] Interface added to Switch {self.name}: MAC={interface.mac}, Port={interface.port}")

    def receive_arp_request(self, incoming_iface, target_ip):
        src_mac = incoming_iface.mac
        self.learn_mac(src_mac, incoming_iface.port)
        print(f"[Switch {self.name}] Flooding ARP request for {target_ip}")

        for iface in self.interfaces:
            if iface == incoming_iface:
                continue
            if not hasattr(iface, 'device') or iface.device is None:
                continue
            if not hasattr(iface.device, 'interfaces'):
                continue

            matched = False
            for dev_iface in iface.device.interfaces:
                if dev_iface.ip == target_ip:
                    iface.device.receive_arp_request(incoming_iface, target_ip)
                    matched = True
                    break
            if not matched:
                print(f"[{iface.device.name}] Ignored ARP request for {target_ip}")

    def receive_arp_reply(self, sender_ip, sender_mac, incoming_iface):
        self.learn_mac(sender_mac, incoming_iface.port)
        print(f"[Switch {self.name}] Received ARP reply: {sender_ip} → {sender_mac}, learned on Port {incoming_iface.port}")

        for iface in self.interfaces:
            if iface.device.name != incoming_iface.device.name:
                iface.device.receive_arp_reply(sender_ip, sender_mac, iface)

    def learn_mac(self, mac, port):
        if mac not in self.mac_table:
            self.mac_table[mac] = port
            print(f"[Switch {self.name}] Learning: {mac} → Port {port}")

    def show_mac_table(self):
        print(f"\n[MAC TABLE] Switch {self.name}")
        if not self.mac_table:
            print("(empty)")
        for mac, port in self.mac_table.items():
            print(f"Port {port} → {mac}")
    def receive_packet(self, incoming_iface, dst_ip, payload):
        print(f"[Switch {self.name}] Received packet for {dst_ip} from {incoming_iface.mac}")
    # Learn source MAC (if not already)
        self.learn_mac(incoming_iface.mac, incoming_iface.port)

    # Find destination MAC from routing decision — simulated for now
        dst_mac = None
        for iface in self.interfaces:
            if iface.device.name != incoming_iface.device.name:
               dst_mac = iface.mac
               print(f"[Switch {self.name}] Forwarding packet to MAC={dst_mac} on Port {iface.port}")
               iface.device.receive_packet(dst_ip, payload, incoming_iface)
               return

        print(f"[Switch {self.name}] No known destination MAC. Packet dropped.")
