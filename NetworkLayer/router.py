import ipaddress

def get_network(ip, prefix):
    return str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False).network_address)


class Router:
    def __init__(self, name, interfaces):
        self.name = name
        self.interfaces = interfaces
        self.arp_table = {}
        self.routing_table = {}
        self.interface_links = {}
        self.pending_packets = {}

        for iface, (ip, mac, prefix) in interfaces.items():
            network = get_network(ip, prefix)
            self.routing_table[(network, prefix)] = iface

        print(f"[{self.name}] Routing Table: {self.routing_table}")

    def connect_interface(self, iface, link, peer_iface=None):
        if peer_iface:
            self.interface_links[iface] = ('serial', link, peer_iface)
        else:
            self.interface_links[iface] = ('switch', link)

    def receive(self, frame, iface):
        if frame['type'] == 'DATA':
            self.receive_data(frame)
        elif frame['type'] == 'ARP_REQUEST':
            self.receive_arp_request(frame)
        elif frame['type'] == 'ARP_REPLY':
            self.receive_arp_reply(frame)

    def receive_arp_request(self, frame):
        target_ip = frame['target_ip']
        for iface, (ip, mac, _) in self.interfaces.items():
            if target_ip == ip:
                print(f"[{self.name}] received ARP Request for {target_ip} on {iface}, replying directly...")
                self.arp_table[frame['sender_ip']] = frame['sender_mac']
                self.print_arp_table()
                reply = {
                    'type': 'ARP_REPLY',
                    'sender_ip': ip,
                    'sender_mac': mac,
                    'target_ip': frame['sender_ip'],
                    'target_mac': frame['sender_mac']
                }
                link_type, *link_data = self.interface_links[iface]
                if link_type == 'switch':
                    link_data[0].receive_frame(reply, self)
                elif link_type == 'serial':
                    link_data[0].transmit(self, reply, iface)

    def receive_arp_reply(self, frame):
        print(f"[{self.name}] received ARP Reply: {frame['sender_ip']} is at {frame['sender_mac']}")
        self.arp_table[frame['sender_ip']] = frame['sender_mac']
        self.print_arp_table()
        if frame['sender_ip'] in self.pending_packets:
            pending_frame, out_iface = self.pending_packets.pop(frame['sender_ip'])
            out_ip, out_mac_self, _ = self.interfaces[out_iface]
            dst_mac = frame['sender_mac']
            pending_frame['l2'] = {'src_mac': out_mac_self, 'dst_mac': dst_mac}
            print(f"[{self.name}] prepares L2 header: src_mac={out_mac_self}, dst_mac={dst_mac}")
            print(f"[{self.name}] forwarding DATA to {pending_frame['l3']['dst_ip']} via MAC {dst_mac}")
            link_type, *link_data = self.interface_links[out_iface]
            if link_type == 'switch':
                link_data[0].receive_frame(pending_frame, self)

    def receive_data(self, frame):
        print(f"[{self.name}] received data frame. Stripping L2 and inspecting IP packet...")
        src_ip = frame['l3']['src_ip']
        dst_ip = frame['l3']['dst_ip']
        print(f"[{self.name}] IP Packet: src={src_ip}, dst={dst_ip}")

        best_match = None
        best_prefix = -1
        dst_ip_obj = ipaddress.IPv4Address(dst_ip)

        for (net_str, prefix), iface in self.routing_table.items():
            network = ipaddress.IPv4Network(f"{net_str}/{prefix}", strict=False)
            if dst_ip_obj in network and prefix > best_prefix:
                best_match = iface
                best_prefix = prefix

        if best_match:
            iface = best_match
            ip, mac, _ = self.interfaces[iface]
            link_type, *link_data = self.interface_links.get(iface, (None,))
            if link_type == 'switch':
                dst_mac = self.arp_table.get(dst_ip)
                if dst_mac is None:
                     print(f"[{self.name}] needs MAC of {dst_ip}, sending ARP Request on {iface}")
                     self.pending_packets[dst_ip] = (frame, iface)
                     arp_req = {
                         'type': 'ARP_REQUEST',
                         'sender_ip': ip,
                         'sender_mac': mac,
                         'target_ip': dst_ip
                     }
                     link_data[0].receive_frame(arp_req, self)
                else:
                    print(f"[{self.name}] MAC for {dst_ip} is {dst_mac}, forwarding data")
                    frame['l2'] = {'src_mac': mac, 'dst_mac': dst_mac}
                    print(f"[{self.name}] prepares L2 header: src_mac={mac}, dst_mac={dst_mac}")
                    print(f"[{self.name}] forwarding DATA to {dst_ip} via MAC {dst_mac}")
                    link_data[0].receive_frame(frame, self)

            elif link_type == 'serial':
                print(f"[{self.name}] forwarding frame over serial on {iface}")
                link_data[0].transmit(self, frame, iface)
        else:
            print(f"[{self.name}] No route to {dst_ip} found in routing table")

    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")
