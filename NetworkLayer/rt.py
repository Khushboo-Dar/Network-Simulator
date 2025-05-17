import ipaddress
import time

class RIPProtocol:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {}  # neighbor_id -> cost
        self.routing_table = {router_id: (0, router_id)}  # destination -> (cost, next_hop)

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost
        self.routing_table[neighbor_id] = (cost, neighbor_id)

    def receive_vector(self, from_router, vector):
        updated = False
        cost_to_neighbor = self.neighbors.get(from_router, float('inf'))
        for dest, (neighbor_cost, _) in vector.items():
            new_cost = cost_to_neighbor + neighbor_cost
            if dest not in self.routing_table or new_cost < self.routing_table[dest][0]:
                self.routing_table[dest] = (new_cost, from_router)
                updated = True
        return updated

    def send_vector(self):
        return self.routing_table.copy()

    def get_next_hop(self, destination):
        return self.routing_table.get(destination, (float('inf'), None))[1]

    def print_routing_table(self):
        print(f"[RIP-{self.router_id}] Routing Table:")
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"  Destination: {dest}, Cost: {cost}, Next Hop: {next_hop}")
        print()



def get_network(ip_str, prefix):
    return str(ipaddress.IPv4Network(f"{ip_str}/{prefix}", strict=False).network_address)

class Host:
    def __init__(self, name, ip, mac, gateway_ip):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.gateway_ip = gateway_ip
        self.arp_table = {}
        self.connected_port = None
        self.connected_switch = None

    def connect(self, switch, port):
        self.connected_port = port
        self.connected_switch = switch
        switch.connect_device(self, port)

    def send_data(self, dest_ip):
        print(f"\n[{self.name}] wants to send data to {dest_ip}")
        self.print_arp_table()

        if self.gateway_ip not in self.arp_table:
            print(f"[{self.name}] doesn't know MAC of gateway {self.gateway_ip}, sending ARP Request")
            self.send_arp_request()
            return

        gw_mac = self.arp_table.get(self.gateway_ip)
        print(f"[{self.name}] prepares L2 header: src_mac={self.mac}, dst_mac={gw_mac}")
        print(f"[{self.name}] sends data to {dest_ip} via gateway MAC {gw_mac}")
        frame = {
            'type': 'DATA',
            'l2': {'src_mac': self.mac, 'dst_mac': gw_mac},
            'l3': {'src_ip': self.ip, 'dst_ip': dest_ip}
        }
        self.connected_switch.receive_frame(frame, self)

    def send_arp_request(self):
        frame = {
            'type': 'ARP_REQUEST',
            'sender_ip': self.ip,
            'sender_mac': self.mac,
            'target_ip': self.gateway_ip
        }
        self.connected_switch.receive_frame(frame, self)

    def receive_arp_reply(self, frame):
        print(f"[{self.name}] received ARP Reply: {frame['sender_ip']} is at {frame['sender_mac']}")
        self.arp_table[frame['sender_ip']] = frame['sender_mac']
        self.print_arp_table()
        self.send_data(frame['target_ip'])

    def receive_data(self, frame):
        print(f"[{self.name}] received DATA destined for IP {frame['l3']['dst_ip']}")
        print(f"[{self.name}] Message from {frame['l3']['src_ip']}: Payload received")

    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")


class Switch:
    def __init__(self, name):
        self.name = name
        self.ports = {}
        self.mac_table = {}

    def connect_device(self, device, port):
        self.ports[port] = device
        print(f"[{self.name}] connected {device.name if hasattr(device, 'name') else 'Router'} at port {port}")

    def receive_frame(self, frame, sender):
        sender_port = self.find_port(sender)

        if 'sender_mac' in frame:
            self.mac_table[frame['sender_mac']] = sender_port
        elif 'l2' in frame:
            self.mac_table[frame['l2']['src_mac']] = sender_port

        self.print_mac_table()

        if frame['type'] == 'ARP_REQUEST':
            for port, device in self.ports.items():
                if device != sender:
                    print(f"[{self.name}] flooding ARP Request to {getattr(device, 'name', 'Router')}")
                    device.receive_arp_request(frame)

        elif frame['type'] == 'ARP_REPLY':
            dst_mac = frame['target_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] unicasting ARP Reply to {getattr(dest_device, 'name', 'Router')}")
                dest_device.receive_arp_reply(frame)

        elif frame['type'] == 'DATA':
            dst_mac = frame['l2']['dst_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] forwarding DATA frame to {getattr(dest_device, 'name', 'Router')}")
                dest_device.receive_data(frame)
            else:
                print(f"[{self.name}] unknown destination MAC {dst_mac}, flooding not implemented for DATA")

    def find_port(self, device):
        for port, dev in self.ports.items():
            if dev == device:
                return port
        return None

    def print_mac_table(self):
        print(f"[{self.name}] MAC Table: {self.mac_table}")


class Router:
    def __init__(self, name, interfaces):
        self.name = name
        self.interfaces = interfaces  # iface -> (ip, mac, prefix)
        self.arp_table = {}
        self.routing_table = {}  # (network, prefix) -> iface
        self.switch_links = {}

        for iface, (ip, mac, prefix) in interfaces.items():
            network = get_network(ip, prefix)
            self.routing_table[(network, prefix)] = iface


        self.rip = RIPProtocol(name)
        print(f"[{self.name}] Routing Table: {self.routing_table}")

    def connect_interface(self, iface, switch):
        self.switch_links[iface] = switch

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
                self.switch_links[iface].receive_frame(reply, self)

    def receive_arp_reply(self, frame):
        print(f"[{self.name}] received ARP Reply: {frame['sender_ip']} is at {frame['sender_mac']}")
        self.arp_table[frame['sender_ip']] = frame['sender_mac']
        self.print_arp_table()

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
            dst_mac = self.arp_table.get(dst_ip)
            if dst_mac is None:
                print(f"[{self.name}] needs MAC of {dst_ip}, sending ARP Request on {iface}")
                arp_req = {
                    'type': 'ARP_REQUEST',
                    'sender_ip': self.interfaces[iface][0],
                    'sender_mac': self.interfaces[iface][1],
                    'target_ip': dst_ip
                }
                self.switch_links[iface].receive_frame(arp_req, self)
            else:
                print(f"[{self.name}] MAC for {dst_ip} is {dst_mac}, forwarding data")
                frame['l2']['src_mac'] = self.interfaces[iface][1]
                frame['l2']['dst_mac'] = dst_mac
                self.switch_links[iface].receive_frame(frame, self)
        else:
            print(f"[{self.name}] No route to {dst_ip} found in routing table")

    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")

    def add_rip_neighbor(self, neighbor_router, cost):
        self.rip.add_neighbor(neighbor_router.name, cost)

    def exchange_routing_info(self, neighbor_router):
        updated = neighbor_router.rip.receive_vector(self.name, self.rip.send_vector())
        return updated

    def print_rip_table(self):
        self.rip.print_routing_table()

def run_rip_simulation(routers):
    changed = True
    while changed:
        changed = False
        for r1 in routers:
            for r2 in routers:
                if r1 != r2:
                    changed |= r1.exchange_routing_info(r2)
    
    for router in routers:
        router.print_rip_table()


# --------- SIMULATION ---------
s1 = Switch("Switch1")
s2 = Switch("Switch2")

# Define routers
r1 = Router("Router1", {
    "eth1": ("11.11.11.1", "AA:BB:CC:DD:EE:01", 24),
    "eth2": ("22.22.22.1", "AA:BB:CC:DD:EE:02", 24)
})

r2 = Router("Router2", {
    "eth1": ("33.33.33.1", "AA:BB:CC:DD:EE:03", 24)
})

r3 = Router("Router3", {
    "eth1": ("44.44.44.1", "AA:BB:CC:DD:EE:04", 24)
})

# Connect interfaces (you may need switches or direct connections here)
# For now, only connecting r1
r1.connect_interface("eth1", s1)
r1.connect_interface("eth2", s2)

# Setup RIP neighbors
r1.add_rip_neighbor(r2, 1)
r2.add_rip_neighbor(r1, 1)
r2.add_rip_neighbor(r3, 2)
r3.add_rip_neighbor(r2, 2)

# Run RIP simulation after setting neighbors
run_rip_simulation([r1, r2, r3])

# Setup Hosts
h1 = Host("PC-A", "11.11.11.10", "AA:AA:AA:AA:AA:01", "11.11.11.1")
h2 = Host("PC-B", "22.22.22.40", "AA:AA:AA:AA:AA:02", "22.22.22.1")

# Connect hosts and router to switches
h1.connect(s1, 2)
s1.connect_device(r1, 3)

h2.connect(s2, 5)
s2.connect_device(r1, 4)

# Trigger communication
h1.send_data("22.22.22.40")

# Print RIP tables
r1.print_rip_table()
r2.print_rip_table()
r3.print_rip_table()

