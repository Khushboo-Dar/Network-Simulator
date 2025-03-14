import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_link_layer.switch import Switch
from data_link_layer.frame import Frame
from data_link_layer.access_control import CSMA_CD
from data_link_layer.end_device import EndDevice

logging.basicConfig(level=logging.INFO)

class Hub:
    def __init__(self, name):
        self.name = name
        self.ports = []

    def connect(self, device):
        self.ports.append(device)

    def receive_frame(self, frame, sender):
        for device in self.ports:
            if device != sender:
                device.receive_frame(frame, sender)  # Pass the sender argument

def task1():
    # Task 1: Create a switch with five end devices
    print("Executing Task 1...")
    devices = [EndDevice(f"PC{i+1}", f"AA:BB:CC:DD:EE:0{i+1}") for i in range(5)]
    switch = Switch("Switch1")

    # Connect devices
    for device in devices:
        switch.connect(device)

    # Create and send frames
    csma_cd = CSMA_CD()
    for i in range(len(devices)):
        for j in range(len(devices)):
            if i != j:
                frame = Frame(devices[i].mac, devices[j].mac, f"Hello from PC{i+1} to PC{j+1}")
                csma_cd.send_frame(frame, devices[i], switch)

    # Report the number of broadcast and collision domains
    print("Total number of broadcast domains: 1")
    print("Total number of collision domains: 5")

def task2():
    # Task 2: Create two star topologies with hubs and connect them using a switch
    print("Executing Task 2...")
    devices1 = [EndDevice(f"PC{i+1}", f"AA:BB:CC:DD:EE:0{i+1}") for i in range(5)]
    devices2 = [EndDevice(f"PC{i+6}", f"AA:BB:CC:DD:EE:0{i+6}") for i in range(5)]

    # Create hubs
    hub1 = Hub("Hub1")
    hub2 = Hub("Hub2")

    # Connect devices to hubs
    for device in devices1:
        hub1.connect(device)
    for device in devices2:
        hub2.connect(device)

    # Create switch and connect hubs to switch
    switch = Switch("Switch1")
    switch.connect(hub1)
    switch.connect(hub2)

    # Create and send frames
    csma_cd = CSMA_CD()
    for i in range(len(devices1)):
        for j in range(len(devices2)):
            frame = Frame(devices1[i].mac, devices2[j].mac, f"Hello from PC{i+1} to PC{j+6}")
            csma_cd.send_frame(frame, devices1[i], switch)

    # Report the number of broadcast and collision domains
    print("Total number of broadcast domains: 1")
    print("Total number of collision domains: 10")

if __name__ == "__main__":
    task1()
    task2()