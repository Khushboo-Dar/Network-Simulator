class Bridge:
    def __init__(self):
        # MAC address table: { MAC address -> Port }
        self.mac_table = {}

    def learn_mac_address(self, mac, port):
        """Learns the MAC address and stores its corresponding port."""
        if mac not in self.mac_table:
            self.mac_table[mac] = port
            print(f"[Bridge] Learned MAC: {mac} on Port: {port}")

    def forward_frame(self, src_mac, dst_mac, src_port):
        """
        Forwards frames intelligently:
        - If the destination MAC is known, send to the correct port.
        - If unknown, broadcast to all except the source port.
        """
        self.learn_mac_address(src_mac, src_port)

        if dst_mac in self.mac_table:
            dst_port = self.mac_table[dst_mac]
            print(f"[Bridge] Forwarding frame from {src_mac} to {dst_mac} via Port {dst_port}")
        else:
            print("[Bridge] Destination unknown, broadcasting frame.")

    def display_mac_table(self):
        """Displays the MAC address table."""
        print("\n[Bridge] MAC Address Table:")
        for mac, port in self.mac_table.items():
            print(f"  {mac} -> Port {port}")
        print()
