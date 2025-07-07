import threading
from .sliding_window import go_back_n_send, go_back_n_receive  # Relative import

class TransportLayer:
    def __init__(self, channel):
        self.channel = channel
        self.port_table = {}
        self.lock = threading.Lock()
        self.next_ephemeral = 1024
        self.last_source_port = None

    def assign_port(self, process_name, port_no=None):
        with self.lock:
            if port_no is None:
                while self.next_ephemeral in self.port_table:
                    self.next_ephemeral += 1
                port = self.next_ephemeral
                self.port_table[port] = process_name
                return port
            else:
                self.port_table[port_no] = process_name
                return port_no

    def send(self, src_port, dst_port, data, channel=None):
        """Send data with channel fallback"""
        channel = channel or self.channel  # Use instance channel if none provided
        if not isinstance(data, str):
            data = str(data)
        print(f"[Transport] Sending {len(data)} bytes from {src_port} to {dst_port}")
        go_back_n_send(data, channel, src_port, dst_port)

    def receive(self, port, channel=None):
        """Receive data with channel fallback"""
        channel = channel or self.channel
        result = go_back_n_receive(channel, port)
        self.last_source_port = result["src_port"]
        return result["data"]