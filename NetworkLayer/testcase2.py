from host import Host
from router import Router, run_rip_simulation
from switch import Switch
from serialLink import SerialLink
import ipaddress

def get_network(ip, prefix):
    return str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False).network_address)

#---------- SIMULATION TOPOLOGY -------------

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

# Connect hosts to switches
pc0.connect(s1, 1)
s1.connect_device(r1, 2)
r1.connect_interface("eth0", s1)

pc1.connect(s2, 1)
s2.connect_device(r2, 2)
r2.connect_interface("eth0", s2)

# Connect routers via serial links
link1 = SerialLink(r1, "Se1/0", r3, "Se1/0")
link2 = SerialLink(r2, "Se1/1", r3, "Se1/1")

r1.connect_interface("Se1/0", link1, "Se1/0")
r2.connect_interface("Se1/1", link2, "Se1/1")
r3.connect_interface("Se1/0", link1, "Se1/0")
r3.connect_interface("Se1/1", link2, "Se1/1")

# --------- STATIC ROUTING PHASE --------------

# Add static routes manually to routing_table
r1.routing_table[(get_network("20.0.0.0", 24), 24)] = "Se1/0"  # via r3
r2.routing_table[(get_network("10.0.0.0", 24), 24)] = "Se1/1"  # via r3
r3.routing_table[(get_network("10.0.0.0", 24), 24)] = "Se1/0"  # to r1
r3.routing_table[(get_network("20.0.0.0", 24), 24)] = "Se1/1"  # to r2

# ------------ SEND DATA: STATIC ROUTING -----------------

print("\n==== [STATIC ROUTING] PC0 -> PC1 ====")
pc0.send_data("20.0.0.2")

print("\n==== [STATIC ROUTING] PC1 -> PC0 ====")
pc1.send_data("10.0.0.2")

# ----------- CLEAR STATIC ROUTES BEFORE RIP -------------

def reset_to_directly_connected(router):
    directly_connected = {}
    for iface, (ip, mac, prefix) in router.interfaces.items():
        network = get_network(ip, prefix)
        directly_connected[(network, prefix)] = iface
    router.routing_table = directly_connected

reset_to_directly_connected(r1)
reset_to_directly_connected(r2)
reset_to_directly_connected(r3)

# ------------ RIP CONFIGURATION -------------------------

r1.rip.add_neighbor(r3.name, cost=1)
r2.rip.add_neighbor(r3.name, cost=1)
r3.rip.add_neighbor(r1.name, cost=1)
r3.rip.add_neighbor(r2.name, cost=1)

# ------------ RUN RIP -------------------------
run_rip_simulation([r1, r2, r3])

# ------------ SEND DATA: RIP ROUTING -----------------

print("\n==== [RIP ROUTING] PC0 -> PC1 ====")
pc0.send_data("20.0.0.2")

print("\n==== [RIP ROUTING] PC1 -> PC0 ====")
pc1.send_data("10.0.0.2")
