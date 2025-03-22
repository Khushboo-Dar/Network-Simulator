class Device:
    """Represents a network device with a MAC address."""
    def __init__(self, mac):
        self.mac = mac
        self.port = None
        self.data = None  # Stores received data

    def __repr__(self):
        return f"Device({self.mac})"


class Bridge:
    """Simulates a network bridge that connects two segments and filters traffic using MAC addresses."""
    
    def __init__(self):  # Constructor
        self.mac_table = {}  # {MAC -> Port}
        self.ports = {}  # {Port -> Device}

    def connect_device(self, device, port):
        """Connects an end device to a specific port."""
        self.ports[port] = device
        device.port = port
        print(f"Connected {device} to port {port}")

    def receive_frame(self, src_mac, dest_mac, data):
        """Processes incoming frames and forwards them intelligently."""
        print(f"\nFrame received from {src_mac} -> {dest_mac}: {data}")
    
        # Find the port where the source MAC is connected
        src_port = None
        for port, device in self.ports.items():
            if device.mac == src_mac:
                src_port = port
                break
            
        if src_port is None:
            print(f"Source MAC {src_mac} is unknown. Frame dropped.")
            return  # Drop the frame if source MAC is unknown
    
        # Learn the MAC address if it's not already in the table
        if src_mac not in self.mac_table:
            print(f"Learning MAC {src_mac} on port {src_port}")
            self.mac_table[src_mac] = src_port
    
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


def run_simulation():
    """Runs the network bridge simulation."""
    bridge = Bridge()

    # Creating devices
    device_A = Device("AA:BB:CC:DD:EE:01")
    device_B = Device("AA:BB:CC:DD:EE:02")
    device_C = Device("AA:BB:CC:DD:EE:03")

    # Connecting devices to the bridge
    bridge.connect_device(device_A, 1)
    bridge.connect_device(device_B, 2)
    bridge.connect_device(device_C, 3)

    # Sending frames (communication)
    bridge.receive_frame("AA:BB:CC:DD:EE:01", "AA:BB:CC:DD:EE:02", "Hello B!")
    bridge.receive_frame("AA:BB:CC:DD:EE:02", "AA:BB:CC:DD:EE:03", "Hello C!")
    bridge.receive_frame("AA:BB:CC:DD:EE:03", "AA:BB:CC:DD:EE:01", "Hello A!")

    # Displaying the learned MAC table
    bridge.display_mac_table()


#Will not run automatically
if __name__ == "__main__":
    run_simulation()
