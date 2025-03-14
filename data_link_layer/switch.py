import logging

class Switch:
    def __init__(self, name):
        self.name = name
        self.mac_table = {}  # MAC address table
        self.ports = []
        logging.basicConfig(level=logging.INFO)

    def connect(self, device):
        """Connect a device to the switch"""
        self.ports.append(device)
        logging.info(f"Device connected: {device}")

    def receive_frame(self, frame, sender):
        """Process an incoming frame"""
        if frame.is_corrupt():
            logging.warning(f"Corrupted frame received from {sender}")
            return

        self.mac_table[frame.src_mac] = sender  # Learn source MAC
        logging.info(f"MAC table updated: {frame.src_mac} -> {sender}")

        if frame.dest_mac in self.mac_table:
            # Forward to specific device
            receiver = self.mac_table[frame.dest_mac]
            logging.info(f"Switch forwarding frame to {frame.dest_mac}")
            receiver.receive_frame(frame)
        else:
            # Broadcast to all except sender
            logging.info(f"Switch broadcasting frame as {frame.dest_mac} is unknown")
            for device in self.ports:
                if device != sender:
                    device.receive_frame(frame)