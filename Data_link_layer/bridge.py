class Bridge:
    """Simulates a network bridge that connects two segments and filters traffic using MAC addresses."""
    
    def __init__(self): #Constructor
        self.mac_table = {}  #empty dictionary to store Mapping of MAC addresses to ports {mac -> port}
        self.ports = {}  #Port to device mapping {port->device}

    def connect_device(self, device, port):
        """Connects an end device to a specific port."""
        self.ports[port] = device
        device.port = port
        print(f"Connected {device} to port {port}")

    def receive_frame(self, src_mac, dest_mac, data):
        """Processes incoming frames and forwards them intelligently."""
        if src_mac not in self.mac_table:
            print(f"Learning MAC {src_mac} on port {self.ports[src_mac].port}")
            self.mac_table[src_mac] = self.ports[src_mac].port
        
        if dest_mac in self.mac_table:
            # Known destination, unicast forwarding
            dest_port = self.mac_table[dest_mac]
            print(f"Forwarding frame to port {dest_port}")
            self.ports[dest_port].data = data
            print(f"Message delivered to {dest_mac}: {data}")
        else:
            # Unknown destination, broadcast to all except the sender
            print(f"MAC {dest_mac} not in table, broadcasting...")
            for port, device in self.ports.items():
                if device.mac != src_mac:
                    device.data = data
                    print(f"Message broadcasted to {device.mac}")

    def display_mac_table(self):
        """Displays the MAC address table."""
        print("\nBridge MAC Table:")
        for mac, port in self.mac_table.items():
            print(f"MAC: {mac} -> Port: {port}")


# Example Usage
bridge = Bridge()