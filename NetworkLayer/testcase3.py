from host import Host
from router import Router
from switch import Switch

# Create switches
s1 = Switch("Switch1")
s2 = Switch("Switch2")
s3 = Switch("Switch3")

# Create router with 3 interfaces
r1 = Router("Router1", {
    "eth0": ("10.0.0.1", "AA:BB:CC:DD:00:01", 24),
    "eth1": ("20.0.0.1", "AA:BB:CC:DD:00:02", 24),
    "eth2": ("20.0.1.1", "AA:BB:CC:DD:00:03", 25)  # /25 is longer than /24
})

# Connect router interfaces to switches
r1.connect_interface("eth0", s1)
r1.connect_interface("eth1", s2)
r1.connect_interface("eth2", s3)

# Create hosts
h1 = Host("PC-A", "10.0.0.10", "AA:AA:AA:AA:AA:01", "10.0.0.1")
h2 = Host("PC-B", "20.0.0.20", "AA:AA:AA:AA:AA:02", "20.0.0.1")
h3 = Host("PC-C", "20.0.1.30", "AA:AA:AA:AA:AA:03", "20.0.1.1")

# Connect hosts to switches
h1.connect(s1, 2)
s1.connect_device(r1, 3)

h2.connect(s2, 2)
s2.connect_device(r1, 4)

h3.connect(s3, 2)
s3.connect_device(r1, 5)

# Now simulate PC-A sending data to PC-C (20.0.1.30)
h1.send_data("20.0.1.30")
