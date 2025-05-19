from host import Host
from router import Router, run_rip_simulation
from switch import Switch
from serialLink import SerialLink

# ------------------ Switches ------------------
s1 = Switch("Switch1")
s2 = Switch("Switch2")

# ------------------ Router --------------------
r1 = Router("Router1", {
    "eth1": ("11.11.11.1", "AA:BB:CC:DD:EE:01", 24),
    "eth2": ("22.22.22.1", "AA:BB:CC:DD:EE:02", 24)
})

# Connect Router interfaces to Switches
r1.connect_interface("eth1", s1)
r1.connect_interface("eth2", s2)

# ------------------ Hosts ---------------------
h1 = Host("PC-A", "11.11.11.10", "AA:AA:AA:AA:AA:01", "11.11.11.1")  # PC-A in subnet 11.11.11.0/24
h2 = Host("PC-B", "22.22.22.40", "AA:AA:AA:AA:AA:02", "22.22.22.1")  # PC-B in subnet 22.22.22.0/24

# Connect Hosts to Switches
h1.connect(s1, 2)
s1.connect_device(r1, 3)

h2.connect(s2, 5)
s2.connect_device(r1, 4)

# ------------------ STATIC ROUTING ------------------
# Add manually known subnets to routing table
r1.rip.routing_table["11.11.11.0/24"] = (1, "eth1")
r1.rip.routing_table["22.22.22.0/24"] = (1, "eth2")

print("\n==== STATIC ROUTING: PC-A -> PC-B ====")
h1.send_data("22.22.22.40")

print("\n==== STATIC ROUTING: PC-B -> PC-A ====")
h2.send_data("11.11.11.10")

# ------------------ RIP ROUTING ------------------
# Clear static routes
r1.rip.routing_table.clear()

print("\n==== RUNNING RIP (No Neighbors) ====")
run_rip_simulation([r1])  # Won’t learn anything, but simulates RIP

print("\n==== RIP ROUTING: PC-A -> PC-B ====")
h1.send_data("22.22.22.40")

print("\n==== RIP ROUTING: PC-B -> PC-A ====")
h2.send_data("11.11.11.10")
