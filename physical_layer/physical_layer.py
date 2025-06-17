import random

class EndDevice:
    """Simulates an End Device in the physical layer"""

    @staticmethod
    def generate_mac_address():
        mac_address = [f"{random.randint(0x00, 0xFF):02X}" for _ in range(5)]
        return "00:" + ":".join(mac_address)

    def __init__(self, ip, port, data, seq_no):
        self.ip = ip.strip()
        self.mac = EndDevice.generate_mac_address()
        self.port = port
        self.data = data
        self.seq_no = seq_no
        self.message = ""
        self.device_id = seq_no

    def display(self):
        print("IP Address    :", self.ip)
        print("MAC Address   :", self.mac)
        print("Port Value    :", self.port)

class Hub:
    def __init__(self):
        self.port1 = 0
        self.port2 = 0
        self.port3 = 0
        self.port4 = 0
        self.port5 = 0

    def hub_vacant(self):
        return self.port1 == 0 or self.port2 == 0 or self.port3 == 0 or self.port4 == 0 or self.port5 == 0

class Connection:
    def __init__(self, sender: EndDevice, receiver: EndDevice):
        self.sender = sender
        self.receiver = receiver
        self.connected = False

    def make_connection(self):
        if self.sender.port == 0 and self.receiver.port == 0:
            self.sender.port = 1
            self.receiver.port = 2
            self.connected = True
            print("Connection Made between two End Devices")
        else:
            print("No connection possible, one or both ports already occupied")

    def transmit_message(self, message: str):
        if not self.connected:
            print("Connection not established. Cannot transmit message.")
            return

        self.sender.data = message
        self.receiver.data = self.sender.data

        print(f"Message sent from {self.sender.device_id} to {self.receiver.device_id}: {message}")

        if self.receiver.data == self.sender.data:
            print(f"---TRANSMISSION SUCCESSFUL--- ACK RECEIVED from End Device {self.receiver.device_id}")
        else:
            print("---ACK LOST---")

# Devices pool
e1 = EndDevice("192.168.56.1", 0, "No data", 1)
e2 = EndDevice("192.168.56.2", 0, "No data", 2)
e3 = EndDevice("192.168.56.3", 0, "No data", 3)
e4 = EndDevice("192.168.56.4", 0, "No data", 4)
e5 = EndDevice("192.168.56.5", 0, "No data", 5)
e6 = EndDevice("192.168.56.6", 0, "No data", 6)
e7 = EndDevice("192.168.56.7", 0, "No data", 7)
e8 = EndDevice("192.168.56.8", 0, "No data", 8)
e9 = EndDevice("192.168.56.9", 0, "No data", 9)
e10 = EndDevice("192.168.56.10", 0, "No data", 10)

# Index 0 is dummy to support 1-based indexing
endDevices = [-1, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]

def get_end_device(device_id: int) -> EndDevice:
    return endDevices[device_id]

def end_device_vacant():
    return any(device.port == 0 for device in endDevices[1:])
