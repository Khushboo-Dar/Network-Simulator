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

# ----- Switches -----
sw1 = Switch("Switch1")
sw2 = Switch("Switch2")

# ----- Routers -----
r1 = Router("R1", {
    "eth0": ("10.0.0.1", "AA:BB:CC:DD:EE:11", 24),
    "se1/0": ("192.168.1.1", "AA:BB:CC:DD:EE:01", 30)
})

r2 = Router("R2", {
    "eth0": ("20.0.0.1", "AA:BB:CC:DD:EE:02", 24),
    "se1/1": ("192.168.2.2", "AA:BB:CC:DD:EE:03", 30)
})

r3 = Router("R3", {
    "se1/0": ("192.168.1.2", "AA:BB:CC:DD:EE:31", 30),
    "se1/1": ("192.168.2.1", "AA:BB:CC:DD:EE:32", 30)
})

# ----- Serial Links -----
link1 = SerialLink(r1, "se1/0", r3, "se1/0")
link2 = SerialLink(r2, "se1/1", r3, "se1/1")

# ----- Hosts -----
pc0 = Host("PC0", "10.0.0.2", "AA:AA:AA:AA:AA:01", "10.0.0.1")
pc1 = Host("PC1", "20.0.0.2", "AA:AA:AA:AA:AA:02", "20.0.0.1")

# ----- Connect Hosts to Switches -----
pc0.connect(sw1, 2)
sw1.connect_device(r1, 3)

r1.connect_interface("eth0", sw1)
r2.connect_interface("eth0", sw2)

pc1.connect(sw2, 2)
sw2.connect_device(r2, 3)

# ----- RIP Neighbor Setup -----
r1.add_rip_neighbor(r3, 1)
r2.add_rip_neighbor(r3, 1)
r3.add_rip_neighbor(r1, 1)
r3.add_rip_neighbor(r2, 1)

# ----- Run RIP Simulation -----
run_rip_simulation([r1, r2, r3])

# ----- Trigger Communication -----
pc0.send_data("20.0.0.2")
pc1.send_data("10.0.0.2")
