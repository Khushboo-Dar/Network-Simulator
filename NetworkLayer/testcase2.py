from host import Host
from router import Router
from switch import Switch
from serialLink import SerialLink

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

# ------------ RIP CONFIGURATION --------------
r1.add_rip_neighbor(r3, cost=1)
r2.add_rip_neighbor(r3, cost=1)
r3.add_rip_neighbor(r1, cost=1)
r3.add_rip_neighbor(r2, cost=1)

def run_rip_simulation(routers, max_iterations=5):
    for i in range(max_iterations):
        print(f"\n--- RIP ROUND {i+1} ---")
        updated = False
        for router in routers:
            for neighbor in router.rip_neighbors:
                updated |= router.exchange_routing_info(neighbor)
        if not updated:
            print("RIP tables converged.\n")
            break
    for router in routers:
        print(f"\nRouter {router.name} RIP Table:")
        router.print_rip_table()

# ------------ RUN SIMULATION -----------------
run_rip_simulation([r1, r2, r3])

print("\n---- Simulating PC0 -> PC1 ----")
pc0.send_data("20.0.0.2")

print("\n---- Simulating PC1 -> PC0 ----")
pc1.send_data("10.0.0.2")
