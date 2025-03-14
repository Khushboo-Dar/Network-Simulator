import logging

class Bridge:
    def __init__(self, name):
        self.name = name
        self.mac_table = {}  # MAC address table mapping MAC addresses to connected segments/devices
        self.ports = []      # List of connected segments or devices
        logging.basicConfig(level=logging.INFO)

    def connect(self, segment):
        """Connect a network segment or device to the bridge."""
        self.ports.append(segment)
        logging.info(f"Segment connected: {segment}")

    def receive_frame(self, frame, sender):
        """Process an incoming frame from a connected segment/device."""
        if frame.is_corrupt():
            logging.warning(f"Bridge: Corrupted frame received from {sender}")
            return

        # Learn the source MAC address and record which port (segment) it came from.
        self.mac_table[frame.src_mac] = sender
        logging.info(f"Bridge MAC table updated: {frame.src_mac} -> {sender}")

        if frame.dest_mac in self.mac_table:
            # Forward the frame to the specific segment/device associated with the destination MAC.
            receiver = self.mac_table[frame.dest_mac]
            logging.info(f"Bridge forwarding frame to {frame.dest_mac} via {receiver}")
            receiver.receive_frame(frame)
        else:
            # Broadcast the frame to all segments/devices except the sender if destination is unknown.
            logging.info(f"Bridge broadcasting frame: destination {frame.dest_mac} unknown")
            for segment in self.ports:
                if segment != sender:
                    segment.receive_frame(frame)
