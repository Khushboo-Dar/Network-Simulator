class EndDevice:
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac

    def receive_frame(self, frame):
        print(f"{self.name} received frame: {frame}")