class Switch:
    def __init__(self):
        """Initialize a switch with an empty MAC address table."""
        self.mac_table = {}

    def learn_mac(self, mac, port):
        """Learn and store MAC addresses in the switch's table."""
        self.mac_table[mac] = port
        print(f"\n[SWITCH] Learned MAC {mac} on port {port}\n")

    def forward_frame(self, frame, incoming_port):
        """Forward frames based on MAC address learning."""
        dest_mac = frame.dest_mac

        if dest_mac in self.mac_table:
            port = self.mac_table[dest_mac]
            print(f"\n[SWITCH] Forwarding frame to port {port} (Dest: {dest_mac})\n")
        else:
            print("\n[SWITCH] Destination unknown, broadcasting...\n")
            for port in range(1, 6):  # Assume switch has 5 ports
                if port != incoming_port:
                    print(f"  --> Broadcast on Port {port}")

    def display_mac_table(self):
        """Print the current MAC address table."""
        print("\n===========================")
        print("      SWITCH MAC TABLE    ")
        print("===========================")
        for mac, port in self.mac_table.items():
            print(f"MAC: {mac}  ->  Port: {port}")
        print("===========================\n")
