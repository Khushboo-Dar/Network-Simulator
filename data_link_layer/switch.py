from data_link_layer.frame import Frame

class Switch:
    def __init__(self):
        """ Initialize switch with an empty MAC address table. """
        self.mac_table = {}  # Dictionary to store MAC-to-port mappings

    def learn_mac(self, mac_address, port):
        """ Store the MAC address in the switch table. """
        self.mac_table[mac_address] = port
        print("\n========================================")
        print(f"[SWITCH] Learned MAC {mac_address} on port {port}")
        print("========================================\n")

    def forward_frame(self, sender, receiver, data):
        """ Forward frame based on the MAC address table. """
        
        print("\n========================================")
        print(f"[SWITCH] Received Frame from {sender} to {receiver}")
        print("========================================\n")

        # Create a Frame object
        frame = Frame(sender, receiver, data)

        if frame.dest_mac in self.mac_table:
            port = self.mac_table[frame.dest_mac]
            print(f"\n[SWITCH] Forwarding frame to {frame.dest_mac} on port {port}\n")
        else:
            print("\n[SWITCH] Destination unknown, broadcasting...\n")
            for port in self.mac_table.values():
                print(f"  --> Broadcast on Port {port}")
            print("\n========================================\n")
