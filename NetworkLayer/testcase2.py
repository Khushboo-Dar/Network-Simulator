from host import Host
from router import Router
from switch import Switch
from serialLink import SerialLink


#---------- SIMULATION -------------

s1 = Switch("Switch1")
s2 = Switch("Switch2")
  
r1 = Router("Router1", {
    "eth0": ("10.0.0.1", "AA:BB:CC:DD:EE:11", 24),
    "Se1/0": ("192.168.1.1", "AA:BB:CC:DD:EE:12", 30)
})
r2 = Router("Router2", {
    "eth0": ("20.0.0.1", "AA:BB:CC:DD:EE:21", 24),
    "Se1/1": ("192.168.2.2", "AA:BB:CC:DD:EE:22", 30)
})
r3 = Router("Router3", {
    "Se1/0": ("192.168.1.2", "AA:BB:CC:DD:EE:31", 30),
    "Se1/1": ("192.168.2.1", "AA:BB:CC:DD:EE:32", 30)
})
 
pc0 = Host("PC0", "10.0.0.2", "AA:AA:AA:AA:AA:01", "10.0.0.1")
pc1 = Host("PC1", "20.0.0.2", "AA:AA:AA:AA:AA:02", "20.0.0.1")
 
# Connect PCs and routers to switches
pc0.connect(s1, 1)
s1.connect_device(r1, 2)
r1.connect_interface("eth0", s1)
 
pc1.connect(s2, 1)
s2.connect_device(r2, 2)
r2.connect_interface("eth0", s2)
 
# Serial connections
link1 = SerialLink(r1, "Se1/0", r3, "Se1/0")
link2 = SerialLink(r2, "Se1/1", r3, "Se1/1")
r1.connect_interface("Se1/0", link1, "Se1/0")
r2.connect_interface("Se1/1", link2, "Se1/1")
r3.connect_interface("Se1/0", link1, "Se1/0")
r3.connect_interface("Se1/1", link2, "Se1/1")

# Routing tables
r1.routing_table[("20.0.0.0", 24)] = "Se1/0"
r2.routing_table[("10.0.0.0", 24)] = "Se1/1"
r3.routing_table[("10.0.0.0", 24)] = "Se1/0"
r3.routing_table[("20.0.0.0", 24)] = "Se1/1"

# Simulate PC0 sending data to PC1
pc0.send_data("20.0.0.2")

  




