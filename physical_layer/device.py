#defines end devices and hub class
class EndDevice:
    def __init__(self,name):
        self.name =name
        self.connections=[]
        
    def connect(self,device):
        #connect this device to another device
        self.connectionns.append(device)
        device.connections.append(self) #bi-dir connec
        print("Devices connected")
        
    def send_data(self, data, destination):
        #send data to another device
        print(f"{self.name} sending data: '{data}'")
        for device in self.connections:
            device.receive_data(data, self, destination)
        
    def receive_data(self,data,sender,destination):
        #receive data and check if it is for this device
        if self==destination:
            print(f"{self.name} received data: '{data}' from {sender.name}")
        else:
            print(f"{self.name} received data but not for it. Ignoring...")
            
        
        
class Hub:
    def __init__(self,name):
        self.name=name
        self.connections=[]
    def connect(self,device):
        #conect a device to this hub
        self.connections.append(device)
        device.connections.append(self)
        print("Device connected to hub")

    def receive_data(self,data,sender,destination):
        #broadcast data to all devices connected to the hub except sender
        print(f"{self.name} received data from {sender.name}. Broadcasting...")
        for device in self.connections:
            if device!=sender:
                device.receive_data(data,self,destination)