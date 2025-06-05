
class Device:
    def __init__(self, name):
        self.name = name
        self.interfaces = []

    def add_interface(self, ip, mac):
        raise NotImplementedError("Use subclass to implement interface logic")
