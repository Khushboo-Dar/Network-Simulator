from host import Host
from router import Router
from switch import Switch
from serialLink import SerialLink

def run_rip_simulation(routers):
    changed = True
    while changed:
        changed = False
        for r1 in routers:
            for r2 in routers:
                if r1 != r2:
                    changed |= r1.exchange_routing_info(r2)
    for router in routers:
        router.print_rip_table()

# ----- Network Topology -----
s1 = Switch("Switch1")
s2 = Switch("Switch2")

# Create Router and assign IPs to interfaces
r1 = Router("Router1", {
    "eth1": ("11.11.11.1", "AA:BB:CC:DD:EE:01", 24),
    "eth2": ("22.22.22.1", "AA:BB:CC:DD:EE:02", 24)
})

r2 = Router("Router2", {
    "eth1": ("33.33.33.1", "AA:BB:CC:DD:EE:03", 24)
})

r3 = Router("Router3", {
    "eth1": ("44.44.44.1", "AA:BB:CC:DD:EE:04", 24)
})

# Connect Router interfaces to Switches
r1.connect_interface("eth1", s1)
r1.connect_interface("eth2", s2)

# RIP Neighbor Setup
r1.add_rip_neighbor(r2, 1)
r2.add_rip_neighbor(r1, 1)
r2.add_rip_neighbor(r3, 2)
r3.add_rip_neighbor(r2, 2)

# Run RIP Distance Vector Routing Simulation
run_rip_simulation([r1, r2, r3])

# ----- Hosts -----
h1 = Host("PC-A", "11.11.11.10", "AA:AA:AA:AA:AA:01", "11.11.11.1")
h2 = Host("PC-B", "22.22.22.40", "AA:AA:AA:AA:AA:02", "22.22.22.1")

# Connect Hosts to Switches
h1.connect(s1, 2)  # PC-A on Switch1 port 2
s1.connect_device(r1, 3)  # Router eth1 on Switch1 port 3

h2.connect(s2, 5)  # PC-B on Switch2 port 5
s2.connect_device(r1, 4)  # Router eth2 on Switch2 port 4

# Trigger PC-A sending data to PC-B
h1.send_data("22.22.22.40")

# Now simulate PC-B replying to PC-A
h2.send_data("11.11.11.10")

